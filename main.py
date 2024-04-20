import pygame
import sys
import random
import math
import time

from draw_grid_functions import draw_custom_grid
from tower import Tower, tower_functionality
from enemy import Enemy, make_enemies_for_level, get_enemies_for_level, enemy_functionality
from maps import *
from menu import *
from images import *
from game_functions import * 

# Initialize Pygame
pygame.init()

# Initialize the font
pygame.font.init()
font = pygame.font.Font("fonts/Arial.ttf", 30)  # You can adjust the font size here
level_font = pygame.font.Font("fonts/Arial.ttf", 90)

clock = pygame.time.Clock()

shooting_clock = pygame.time.Clock()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750

GRID_ROWS = 15
GRID_COLUMNS = 15
CELL_SIZE = 50


grid = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 3],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 3],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 3],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 3],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 3],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 3],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 3],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 3],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 3],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 3],
    [1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 3],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
]

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

pygame.display.set_caption("Tower Defense Game")

# Importing images needed in main loop
path_image = pygame.image.load("images/path.png").convert()
grass_image = pygame.image.load("images/grass.png").convert()

side_menu_image = pygame.image.load("images/menu.png").convert()
pygame.transform.scale(side_menu_image, (375, 750))

side_menu_small_image = pygame.image.load("images/menu_small.png").convert()
pygame.transform.scale(side_menu_small_image, (50, 750))

main_menu_bg = pygame.image.load("images/main_menu_bg.png").convert()
pygame.transform.scale(main_menu_bg, (750,750))



# Variables to track progress

tower = None

all_enemies = []
all_towers = []
temp_towers = []

side_menu_open = False
main_menu_open = True

level = 1
level_start = False
game_start = False

spawn_timer = 0
enemy_spawn_interval = 1000

level_enemies = [0,0]
level_enemies_count = [0,0]

total_shooting_time = 0

picked_tower = None

money = 200

health = 100

# Main game loop
def main():
    global tower, all_towers, temp_towers, picked_tower
    global all_enemies, enemy_spawn_interval, spawn_timer, total_shooting_time, level_enemies, level_enemies_count
    global money, health
    global level, level_start, game_start
    global side_menu_open, main_menu_open

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                grid_x = x // CELL_SIZE
                grid_y = y // CELL_SIZE

                if event.button == 1:
                    if not main_menu_open:
                        
                        # Pick tower (Explained in function)
                        money, picked_tower = pick_tower(side_menu_open, x, y, money, picked_tower)

                        # Actually place the tower (Well put it in list)
                        # Check if side menu isn't open, and a tower is picked
                        if side_menu_open == False and picked_tower != None:
                            # If the grid_x and grid_y are integers, and a grass block clicked
                            if type(grid_y) is int and type(grid_x) is int and grid[grid_y][grid_x] == 0:
                                colliding_with_another_tower = False # Initialise colliding variable

                                # Loop through all towers (For all_towers if level started)
                                for tower in all_towers:
                                    if (grid_x == tower.position[0]) and (grid_y == tower.position[1]): # If a tower already there, it's colliding
                                        colliding_with_another_tower = True

                                # Loop through all towers (For all_towers if level hasn't started)
                                for tower in temp_towers:
                                    if (grid_x == tower.position[0]) and (grid_y == tower.position[1]): # If a tower already there, it's colliding
                                        colliding_with_another_tower = True

                                # If the level has started and isn't colliding with another tower
                                if level_start and not colliding_with_another_tower:
                                    # Make a tower, and update the picked_tower variable
                                    tower = Tower((grid_x, grid_y), CELL_SIZE, picked_tower, 1)
                                    all_towers.append(tower)
                                    picked_tower = None


                                elif not level_start and not colliding_with_another_tower:
                                    # Make a tower, and update the picked_tower variable                                    
                                    tower = Tower((grid_x, grid_y), CELL_SIZE, picked_tower, 1)
                                    temp_towers.append(tower)
                                    picked_tower = None      
                        
                        

                        
                # Upgrading towers
                if event.button == 3:
                    if not main_menu_open:
                        # If level started, change all_towers list
                        if level_start:
                            for tower in all_towers: # Loop through all towers
                                # If the place clicked matches with tower, and have enough money, upgrade tower
                                if (grid_x == tower.position[0]) and (grid_y == tower.position[1]) and (tower.can_upgrade(money)):
                                    money = tower.upgrade_tower(money)
                        
                        # If level not started, change temp_towers list
                        else:
                            for tower in temp_towers: # Loop through all towers
                                # If the place clicked matches with tower, and have enough money, upgrade tower
                                if (grid_x == tower.position[0]) and (grid_y == tower.position[1]) and (tower.can_upgrade(money)):
                                    money = tower.upgrade_tower(money)


            # Starting the level, check if space bar pressed and start level
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not main_menu_open and not level_start:
                        level_start = True

        # If the main menu should be open, open the main menu
        if main_menu_open:
            main_menu(screen, main_menu_bg)
            main_menu_open = False

        # If the main menu shouldn't be open
        if not main_menu_open:
            
            # If game hasn't started, show the level screen
            if not game_start:
                # Fill screen with black, show level, and then start game
                screen.fill((0,0,0))

                level_text(screen, level)

                pygame.display.flip()
                pygame.time.delay(2000)

                screen.fill((0,0,0))
                pygame.time.delay(500)

                game_start = True
                

            # If the game has started
            if game_start:
                # Draw the grid (Explained in actual function)
                draw_custom_grid(screen, grid, CELL_SIZE, path_image, grass_image)
                
                mouse_x, mouse_y = pygame.mouse.get_pos() # Get mouse positions

                # Draw all the towers before the round starts
                if tower in temp_towers:
                    for tower in temp_towers:
                        tower.draw(screen)

                # Side menu functionality (Explained in actual function)
                side_menu_open = side_menu(screen, side_menu_open, side_menu_image, side_menu_small_image, mouse_x)

                # If the level has started and player hasn't died yet
                if level_start and health > 0:
                    # Get the amount of enemies for the level (Explained in actual function)
                    get_enemies_for_level(level, level_enemies)

                    # Loop through all the temp_towers and transfer to proper list (all_towers)
                    for i in range(len(temp_towers)):
                        all_towers.append(temp_towers[i])
                    temp_towers.clear()


                    current_time = pygame.time.get_ticks() # Get the current time (How many ticks have passed)
                    # Make the enemies for the level (Explained in actual function)
                    all_enemies, level_enemies_count, spawn_timer = make_enemies_for_level(spawn_timer, all_enemies, level, CELL_SIZE, level_enemies, level_enemies_count, current_time)

                    # Tower & Enemy functionalities (Explained in actual functions)
                    total_shooting_time, money = tower_functionality(screen, tower, all_towers, all_enemies, shooting_clock, total_shooting_time, money)
                    health, all_enemies = enemy_functionality(screen, all_enemies, health, grid)


                    # Level beaten if all enemies spawn and no enemies left
                    if level_enemies == level_enemies_count and len(all_enemies) == 0:
                        level += 1 # Increase the level by 1

                        game_start = False # Make sure the code that runs if the game or level has started is not being run
                        level_start = False

                        level_enemies_count[0] = 0 # Reset level 1 & level 2 enemies count
                        level_enemies_count[1] = 0 

                        spawn_timer = 0 # Reset the spawn timer to 0

                        money = refund_money(money, all_towers) # Refund the money (Explained in actual function)

                # If the health is below 0 (Player died)
                if health <= 0:
                    screen.fill((0,0,0)) # Fill screen with black

                    game_start = False # Make sure the code that runs if the game or level has started is not being run
                    level_start = False

                    pygame.time.delay(2000) # Pause for 2 seconds to remind the player they died
                    
                    # Open the game over screen (Explained in actual function)
                    main_menu_open = True
                    game_over(screen, main_menu_bg, level)

                # Print money and health texts (Explained in actual function)
                money_text(screen, money)
                health_text(screen, health)
        
        # Clear the screen
        pygame.display.flip()
        clock.tick(60)
    
    # Quit the game if user quits
    pygame.quit()
    sys.exit()

# If main file being run, run main
if __name__ == "__main__":
    main()
