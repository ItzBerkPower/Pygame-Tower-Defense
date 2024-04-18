import pygame
import sys
from collections import deque


SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750

# Draw grid based on 0s and 1s in the grid
def draw_custom_grid(screen, grid, CELL_SIZE, path_image, grass_image):
    # Draw cells based on the values in the 2D array
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value == 1:
                '''
                rect = pygame.Rect(col_idx * CELL_SIZE, row_idx * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, (255,255,255), rect, 1)
                '''
                image_rect = path_image.get_rect()
                image_rect.topleft = (col_idx * CELL_SIZE, row_idx * CELL_SIZE)
                screen.blit(path_image, image_rect)
            
            elif value == 0:
                image_rect = grass_image.get_rect()
                image_rect.topleft = (col_idx * CELL_SIZE, row_idx * CELL_SIZE)
                screen.blit(grass_image, image_rect)


def fadeout(screen):
    fadeout = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
    fadeout.fill((0,0,0))
    for i in range(255):
        fadeout.set_alpha(i)
        screen.blit(fadeout, (0, 0))
        pygame.display.update()


def fadein(screen):
    fadein = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
    fadein.fill((0,0,0))
    for i in range(255):
        fadein.set_alpha(255-i)
        screen.blit(fadein, (0, 0))
        pygame.display.flip()

'''

# Depth-First Search (DFS) to find the path
def dfs(screen, CELL_SIZE, grid, current_pos, visited, prev_states, colour, speed, enemy_image):
    if current_pos == None:
        return
    
    x, y = current_pos
    visited.add(current_pos)

    if grid[y][x] == 1:
        prev_states[(x * CELL_SIZE, y * CELL_SIZE)] = screen.copy().subsurface((x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        #pygame.draw.rect(screen, colour, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        screen.blit(enemy_image, (x * CELL_SIZE, y * CELL_SIZE))
        pygame.display.flip()
        pygame.time.delay(200)


    # Define adjacent positions
    #adjacent_positions = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]
    adjacent_positions = [(x+speed, y), (x, y+speed), (x-speed, y), (x, y-speed), (x+1, y), (x, y+1), (x-1, y), (x, y-1)]

    # Explore adjacent cells one by one
    for next_pos in adjacent_positions:
        if 0 <= next_pos[0] < len(grid[0]) and 0 <= next_pos[1] < len(grid) and next_pos not in visited:
            # Check if the next position is along the path
            if grid[next_pos[1]][next_pos[0]] == 1:

                # Restore previous state of the cell before moving on
                if (x * CELL_SIZE, y * CELL_SIZE) in prev_states:
                    prev_state = prev_states[(x * CELL_SIZE, y * CELL_SIZE)]
                    screen.blit(prev_state, (x * CELL_SIZE, y * CELL_SIZE))

                if adjacent_positions not in [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]:
                    if not if_jumping_over_grass_block(grid, current_pos, next_pos):   
                        add_blocks_jumped_over(current_pos, next_pos, visited, speed)
                        return next_pos
                    
                
                if if_jumping_over_grass_block(grid, current_pos, next_pos):
                    short_adjacent_positions = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]

                    for i in short_adjacent_positions:
                        try:
                            if i not in visited and grid[i[1]][i[0]] == 1:
                                return i

                        except:
                            continue    
                
                # Handle turns
                if (x, y) != (next_pos[0], y) and (x, y) != (x, next_pos[1]):
                    # Check if the next position is reachable
                    next_x, next_y = next_pos
                    if grid[y][next_x] == 1:
                        return next_pos
                    elif grid[next_y][x] == 1:
                        return next_pos

    # If no valid adjacent position is found, remove the green square
    if (x * CELL_SIZE, y * CELL_SIZE) in prev_states:
        screen.fill((0, 0, 0), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        del prev_states[(x * CELL_SIZE, y * CELL_SIZE)]
            
    return current_pos
    

# Check if jumping over grass block or not
def if_jumping_over_grass_block(grid, current_pos, next_pos):
    x, y = current_pos
    next_x, next_y = next_pos

    # Check if horizontal movement
    if y == next_y:
        # Check if grass block between movement
        for i in range(min(x, next_x), max(x, next_x) + 1):
            if grid[y][i] == 0:
                print("E")
                return True

    # Check if vertical movement
    elif x == next_x:
        # Check if grass block between movement
        for i in range(min(y, next_y), max(y, next_y) + 1):
            if grid[i][x] == 0:
                print("E")
                return True
    
    return False 


def add_blocks_jumped_over(current_pos, next_pos, visited, speed):
    x, y = current_pos
    next_x, next_y = next_pos

    dx, dy = next_x - x, next_y - y

    num_blocks = speed 

    # If travelled distance was horizontal
    if dx != 0:
        if dx < 0:
            for i in range(speed):
                visited.add((x - i, y))  
        
        else:
            for i in range(speed):
                visited.add((x + i, y))

    # If travelled distance was vertical
    elif dy != 0:
        if dy < 0:
            for i in range(speed):
                visited.add((x, y - i))
        
        else:
            for i in range(speed):
                visited.add((x, y + i))
    
    print(visited)

'''

