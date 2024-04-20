import pygame
import random

# Enemy class
class Enemy(pygame.sprite.Sprite):
    # Initialise all the bits needed for class (Variable names self-explanatory)
    def __init__(self, speed, CELL_SIZE):
        super().__init__()

        self.speed = speed
        self.CELL_SIZE = CELL_SIZE

        self.angle = 0

        self.current_position = (0,0)
        self.previous_position = None
        self.visited_set = set()

        self.time_after_spawn = pygame.time.get_ticks()

        self.enemy1_image = pygame.image.load('images/enemy/enemy1.png').convert_alpha()
        pygame.transform.scale(self.enemy1_image, (50, 50))

        self.enemy2_image = pygame.image.load('images/enemy/enemy2.png').convert_alpha()
        pygame.transform.scale(self.enemy2_image, (50, 50))

        self.enemy3_image = pygame.image.load('images/enemy/enemy3.png').convert_alpha()
        pygame.transform.scale(self.enemy3_image, (50, 50))


    def update_angle(self, next_pos):
        """
        Update the angle of the enemy based on what direction it is moving, parameters: The next position travelling to
        """

        # Calculate angle based on the difference in coordinates between current and next positions
        dx = next_pos[0] - self.current_position[0]
        dy = next_pos[1] - self.current_position[1]
        
        # If moving right, set angle to -90
        if dx >= 1 and dy == 0:
            self.angle = -90

        # If moving left, set angle to 90
        elif dx <= -1 and dy == 0:
            self.angle = 90

        # If moving down, set angle to 180
        elif dy >= 1 and dx == 0:
            self.angle = 180
        
        # If moving up, set angle to 0
        elif dy <= -1 and dx == 0:
            # Moving up
            self.angle = 0
    


    # Depth-First Search (DFS) to find the path
    def dfs(self, screen, grid, prev_states):
        """
        Algorithm to find the next square that the enemy travels to, parameters: Screen to draw on, Grid of game, Previous state of cell
        """

        # If no current position, return, killing the enemy as it means he reached the end
        if self.current_position == None:
            return
                
        # Get the current position of cell, and add it to visited as it has been visited now
        x, y = self.current_position
        self.visited_set.add(self.current_position)

        # If current position is path block, save the current state of it
        if grid[y][x] == 1:
            prev_states[(x * self.CELL_SIZE, y * self.CELL_SIZE)] = screen.copy().subsurface((x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

        # Define adjacent positions, which is up down left right in respect to current cell
        adjacent_positions = [(x+self.speed, y), (x, y+self.speed), (x-self.speed, y), (x, y-self.speed), (x+1, y), (x, y+1), (x-1, y), (x, y-1)]

        # Loop through every adjacent position, 
        for next_pos in adjacent_positions:
            # If the next position x & y in grid, and the next position isn't visited
            if 0 <= next_pos[0] < len(grid[0]) and 0 <= next_pos[1] < len(grid) and next_pos not in self.visited_set:
                # Check if the next position is on path
                if grid[next_pos[1]][next_pos[0]] == 1:
                        
                    # Restore previous state of the cell before moving on
                    if (x * self.CELL_SIZE, y * self.CELL_SIZE) in prev_states:
                        prev_state = prev_states[(x * self.CELL_SIZE, y * self.CELL_SIZE)]
                        screen.blit(prev_state, (x * self.CELL_SIZE, y * self.CELL_SIZE))
                    
                    # If the adjacent positions not moving in direction by 1 block, and if not jumping over a grass block (Explained in actual function)
                    if adjacent_positions not in [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]:
                        if not self.if_jumping_over_grass_block(grid, next_pos):   
                            # Add the blocks jumped over if a level 2 enemy (Explained in actual function), and update the angle for the next position (Explained in actual function)
                            self.add_blocks_jumped_over(next_pos)
                            self.update_angle(next_pos)
                            return next_pos # Return the next position, exiting the function

                    # If x and y coordinates don't equal the next position, 
                    if (x, y) != (next_pos[0], y) and (x, y) != (x, next_pos[1]):
                        # Check if the next position is reachable
                        next_x, next_y = next_pos
                        # If the same y-value but the next x-value is path block, then update the angle (Explained in actual function) and return the next position, exiting function
                        if grid[y][next_x] == 1:
                            self.update_angle(next_pos)
                            return next_pos
                        
                        # If the same x-value but the next y-value is path block, then update the angle (Explained in actual function) and return the next position, exiting function
                        elif grid[next_y][x] == 1:
                            self.update_angle(next_pos)
                            return next_pos

          
        # If no valid adjacent position is found, remove the green square
        if (x * self.CELL_SIZE, y * self.CELL_SIZE) in prev_states:
            screen.fill((0, 0, 0), (x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))
            del prev_states[(x * self.CELL_SIZE, y * self.CELL_SIZE)]
        
        
        # If next position wasn't found, just return the current position, exiting function
        return self.current_position
        

    def draw(self, screen, grid, prev_states):
        """
        Draw the enemy to the screen, parameters: Screen to draw on, grid of game, previous state of cell
        """
        # Get current position
        x,y = self.current_position
        
        # If current position is path block, get the spawn time and create the rect for enemy
        if grid[y][x] == 1:
            self.time_after_spawn = pygame.time.get_ticks()
            self.rect = pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
            
            # If level 1 enemy, use level 1 enemy image
            if self.speed == 1:
                rotated_surface = pygame.transform.rotate(self.enemy1_image, self.angle)
            # If level 2 enemy, use level 2 enemy image
            elif self.speed == 2:
                rotated_surface = pygame.transform.rotate(self.enemy2_image, self.angle)
            
            # Make final rect and draw to screen
            rotated_rect = rotated_surface.get_rect(center=self.rect.center)
            screen.blit(rotated_surface, rotated_rect.topleft)
            pygame.display.flip()

        



    # Check if jumping over grass block or not
    def if_jumping_over_grass_block(self, grid, next_pos):
        """
        Check if enemy is jumping over a grass block when moving multiple cells at a time, parameters: Grid of game, Next position coordinates
        """

        # Initialise separate variables for coordinates
        x, y = self.current_position
        next_x, next_y = next_pos

        # Check if horizontal movement
        if y == next_y:
            # Check if grass block between movement
            for i in range(min(x, next_x), max(x, next_x) + 1):
                # If grass block, return True (Jumping over grass block)
                if grid[y][i] == 0:
                    return True

        # Check if vertical movement
        elif x == next_x:
            # Check if grass block between movement
            for i in range(min(y, next_y), max(y, next_y) + 1):
                # If grass block, return True (Jumping over grass block)
                if grid[i][x] == 0:
                    return True
        
        # If not jumping over grass block, return False
        return False 


    def add_blocks_jumped_over(self, next_pos):
        """
        Add the blocks to visited set that enemy jumped over when moving multiple cells at a time, parameters: Next position coordinates
        """

        # Initialise separate variablers for coordinates
        x, y = self.current_position
        next_x, next_y = next_pos

        # Find the differences in x and y coordinates
        dx, dy = next_x - x, next_y - y

        # If travelled distance was horizontal
        if dx != 0:
            # If travelled towards the left, add all the blocks before it to visited set
            if dx < 0:
                for i in range(self.speed):
                    self.visited_set.add((x - i, y))  
            
            # If travelled towards the right, add all the blocks before it to visited set
            else:
                for i in range(self.speed):
                    self.visited_set.add((x + i, y))

        # If travelled distance was vertical
        elif dy != 0:
            # If travelled down, add all the blocks above it to visited set
            if dy < 0:
                for i in range(self.speed):
                    self.visited_set.add((x, y - i))
            
            # If travelled up, add all the blocks below it to visited set
            else:
                for i in range(self.speed):
                    self.visited_set.add((x, y + i))
        

    def be_shot(self, all_enemies):
        """
        Make the enemy be shot, by removing the enemy from the game, parameters: List of all the enemies
        """

        self.current_position = None # Update current position to nothing, and remove enemy from list
        all_enemies.remove(self)

        return True


def get_enemies_for_level(level, level_enemies):
    """
    Get the amount of enemies and what enemies for that specific level, parameters: Current level, the list that holds the enemies for that level
    """

    # Get the amount of enemies of each type for the level
    level_enemies[0] = level * 2
    level_enemies[1] = level * 1

    # Though if the level is 1, there shouldn't be any level 2 enemies
    if level == 1:
        level_enemies[1] = 0

    return True
 
    

def make_enemies_for_level(spawn_timer, all_enemies, level, CELL_SIZE, level_enemies, level_enemies_count, current_time):
    """
    Make the enemeis for the level, parameters: The spawn timer, list holding all the enemies, the current level, the cell size, the amount of enemies for that level, the list that holds how many enemies of each type has spawned, and the current time (In ms)
    """

    # Initialise enemy spawn intervals based on level
    enemy_spawn_interval = (level * 500) * 1.25 

    if level == 1:
        enemy_spawn_interval = 1000

    # If enough time has passed for next enemy to spawn, update spawn timer
    if (current_time - spawn_timer) > enemy_spawn_interval:
        spawn_timer = current_time

                        
        enemy_chooser = random.randint(1,3) # Choose number from 1 to 3
        print("chooser", enemy_chooser)
        # If number is 1 or 3, an enough level 1 enemies haven't spawned yet, add a level 1 enemy
        if (enemy_chooser == 1 or enemy_chooser == 3) and (level_enemies_count[0] < level_enemies[0]):
            enemy = Enemy(1, CELL_SIZE)
            all_enemies.append(enemy)
            level_enemies_count[0] += 1

        # If number is 2, an enough level 2 enemies haven't spawned yet, add a level 2 enemy
        elif (enemy_chooser == 2) and (level_enemies_count[1] < level_enemies[1]):
            enemy = Enemy(2, CELL_SIZE)
            all_enemies.append(enemy)
            level_enemies_count[1] += 1


    # Return the updated variables, exiting the function
    return all_enemies, level_enemies_count, spawn_timer



def enemy_functionality(screen, all_enemies, health, grid):
    """
    The actual functionality of the enemy, parameters: Screen to draw on, list that holds all the enemies, health of player, grid of game
    """

    # If enemy is on the map, loop through all the enemies
    if len(all_enemies) > 0:
        for enemy in all_enemies:
            prev_states = {} # Initialise the previous states set
            enemy.current_position = enemy.dfs(screen, grid, prev_states) # Get the next position to go to using the dfs algorithm
                            
            # If the current position is the same as previous position, it means the enemy has reached the end, so remove it from the game
            if enemy.current_position == enemy.previous_position:           
                enemy.visited_set.clear()
                enemy.current_position = None
                all_enemies.remove(enemy)

                # If enemy is level 1, remove 20 health
                if enemy.speed == 1:
                    health -= 50

                # If enemy is level 2, remove 40 health  
                elif enemy.speed == 2:
                    health -= 40

            # If enemy isn't dead, update the previous position to the current position 
            else:
                enemy.previous_position = enemy.current_position

        # Draw all the enemies to the screen, and delay for 200 m/s so game doesn't go to fast
        for enemy in all_enemies:
            enemy.draw(screen, grid, prev_states)
        pygame.time.delay(200)

    # Return the updated variables, exiting the function
    return health, all_enemies

