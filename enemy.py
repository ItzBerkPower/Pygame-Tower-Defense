import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed, CELL_SIZE):
        super().__init__()

        self.speed = speed
        self.CELL_SIZE = CELL_SIZE

        self.angle = 0

        self.current_position = (0,0)
        self.previous_position = None
        self.visited_set = set()

        self.enemy1_image = pygame.image.load('images/enemy/enemy1.png').convert_alpha()
        pygame.transform.scale(self.enemy1_image, (50, 50))

        self.enemy2_image = pygame.image.load('images/enemy/enemy2.png').convert_alpha()
        pygame.transform.scale(self.enemy2_image, (50, 50))

        self.enemy3_image = pygame.image.load('images/enemy/enemy3.png').convert_alpha()
        pygame.transform.scale(self.enemy3_image, (50, 50))


    def update_angle(self, next_pos):
        # Calculate angle based on the difference in coordinates between current and next positions
        dx = next_pos[0] - self.current_position[0]
        dy = next_pos[1] - self.current_position[1]
        
        if dx >= 1 and dy == 0:
            # Moving right
            self.angle = -90
        elif dx <= -1 and dy == 0:
            # Moving left
            self.angle = 90
        elif dy >= 1 and dx == 0:
            # Moving down
            self.angle = 180
        elif dy <= -1 and dx == 0:
            # Moving up
            self.angle = 0

    # Depth-First Search (DFS) to find the path
    def dfs(self, screen, grid, prev_states):
        if self.current_position == None:
            return
                
        x, y = self.current_position
        self.visited_set.add(self.current_position)

        if grid[y][x] == 1:
            prev_states[(x * self.CELL_SIZE, y * self.CELL_SIZE)] = screen.copy().subsurface((x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))
            '''
            #pygame.draw.rect(screen, colour, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            #screen.blit(self.enemy1_image, (x * self.CELL_SIZE, y * self.CELL_SIZE))
            self.rect = pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
            rotated_surface = pygame.transform.rotate(self.enemy1_image, self.angle)
            rotated_rect = rotated_surface.get_rect(center=self.rect.center)
            screen.blit(rotated_surface, rotated_rect.topleft)
            pygame.display.flip()
            pygame.time.delay(200)
            '''


        # Define adjacent positions
        #adjacent_positions = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]
        adjacent_positions = [(x+self.speed, y), (x, y+self.speed), (x-self.speed, y), (x, y-self.speed), (x+1, y), (x, y+1), (x-1, y), (x, y-1)]

        # Explore adjacent cells one by one
        for next_pos in adjacent_positions:
            if 0 <= next_pos[0] < len(grid[0]) and 0 <= next_pos[1] < len(grid) and next_pos not in self.visited_set:
                # Check if the next position is along the path
                if grid[next_pos[1]][next_pos[0]] == 1:
                        
                    # Restore previous state of the cell before moving on
                    if (x * self.CELL_SIZE, y * self.CELL_SIZE) in prev_states:
                        prev_state = prev_states[(x * self.CELL_SIZE, y * self.CELL_SIZE)]
                        screen.blit(prev_state, (x * self.CELL_SIZE, y * self.CELL_SIZE))
                    
                    if adjacent_positions not in [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]:
                        if not self.if_jumping_over_grass_block(grid, next_pos):   
                            self.add_blocks_jumped_over(next_pos)
                            self.update_angle(next_pos)
                            return next_pos
                        
                    '''
                    if if_jumping_over_grass_block(grid, current_pos, next_pos):
                        short_adjacent_positions = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]

                        for i in short_adjacent_positions:
                            try:
                                if i not in visited and grid[i[1]][i[0]] == 1:
                                    return i

                            except:
                                continue    
                    '''
                    # Handle turns
                    if (x, y) != (next_pos[0], y) and (x, y) != (x, next_pos[1]):
                        # Check if the next position is reachable
                        next_x, next_y = next_pos
                        if grid[y][next_x] == 1:
                            self.update_angle(next_pos)
                            return next_pos
                        elif grid[next_y][x] == 1:
                            self.update_angle(next_pos)
                            return next_pos

          
        # If no valid adjacent position is found, remove the green square
        if (x * self.CELL_SIZE, y * self.CELL_SIZE) in prev_states:
            screen.fill((0, 0, 0), (x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))
            del prev_states[(x * self.CELL_SIZE, y * self.CELL_SIZE)]
        
        
                
        return self.current_position
        
    def draw(self, screen, grid, prev_states):
        x,y = self.current_position
        if grid[y][x] == 1:
            #pygame.draw.rect(screen, colour, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            #screen.blit(self.enemy1_image, (x * self.CELL_SIZE, y * self.CELL_SIZE))
            self.rect = pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
            rotated_surface = pygame.transform.rotate(self.enemy1_image, self.angle)
            rotated_rect = rotated_surface.get_rect(center=self.rect.center)
            screen.blit(rotated_surface, rotated_rect.topleft)
            pygame.display.flip()

        



    # Check if jumping over grass block or not
    def if_jumping_over_grass_block(self, grid, next_pos):
        x, y = self.current_position
        next_x, next_y = next_pos

        # Check if horizontal movement
        if y == next_y:
            # Check if grass block between movement
            for i in range(min(x, next_x), max(x, next_x) + 1):
                if grid[y][i] == 0:
                    return True

        # Check if vertical movement
        elif x == next_x:
            # Check if grass block between movement
            for i in range(min(y, next_y), max(y, next_y) + 1):
                if grid[i][x] == 0:
                    return True
        
        return False 


    def add_blocks_jumped_over(self, next_pos):
        x, y = self.current_position
        next_x, next_y = next_pos

        dx, dy = next_x - x, next_y - y

        # If travelled distance was horizontal
        if dx != 0:
            if dx < 0:
                for i in range(self.speed):
                    self.visited_set.add((x - i, y))  
            
            else:
                for i in range(self.speed):
                    self.visited_set.add((x + i, y))

        # If travelled distance was vertical
        elif dy != 0:
            if dy < 0:
                for i in range(self.speed):
                    self.visited_set.add((x, y - i))
            
            else:
                for i in range(self.speed):
                    self.visited_set.add((x, y + i))
        
    def be_shot(self):
        self.current_position = None
        return True