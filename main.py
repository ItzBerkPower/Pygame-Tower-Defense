import pygame
import sys
import random
import math
import time

from draw_grid_functions import draw_custom_grid, fadein, fadeout
from tower import Tower
from enemy import Enemy
from maps import *
from menu import *
from images import *

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
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 2],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 2],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 2],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 2],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 2],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 2],
    [1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
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

side_menu_open = False
main_menu_open = True

level = 0 
level_start = False
game_start = False

spawn_timer = 0
enemy_spawn_interval = 1000
enemies = 5

total_shooting_time = 0

picked_tower = None

money = 200

# Main game loop
def main():
    global tower, all_enemies, side_menu_open, main_menu_open
    global enemy_spawn_interval, enemies, spawn_timer, total_shooting_time
    global money, level, level_start, game_start
    global picked_tower, all_towers

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not main_menu_open:
                        x,y = event.pos

                        grid_x = x // CELL_SIZE
                        grid_y = y // CELL_SIZE

                        print(x,y)

                        if side_menu_open and x > 430 and x < 615:
                            if y > 125 and y < 180 and money >= 100:
                                picked_tower = "turret1"
                                money -= 100
                            
                            elif y > 275 and y < 330 and money >= 200:
                                picked_tower = "turret2"
                                money -= 200

                            elif y > 430 and y < 480 and money >= 400:
                                picked_tower = "turret3"
                                money -= 400
                        
                        if side_menu_open == False and picked_tower != None:
                            if grid[grid_y][grid_x] == 0:
                                tower = Tower((grid_x, grid_y), CELL_SIZE, picked_tower, 1)
                                all_towers.append(tower)
                                picked_tower = None


            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not main_menu_open and not level_start:
                        level_start = True


        if main_menu_open:
            main_menu(screen, main_menu_bg)
            main_menu_open = False


        if not main_menu_open:

            if not game_start:
                screen.fill((0,0,0))

                level_text = level_font.render(f"Level: {level}", True, (255,0,0))

                screen.blit(level_text, (150,375))
                pygame.display.flip()
                pygame.time.delay(2000)

                screen.fill((0,0,0))
                pygame.time.delay(500)

                game_start = True
                

            #fadeout(screen)
            if game_start:
                draw_custom_grid(screen, grid, CELL_SIZE, path_image, grass_image)
                
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if tower in all_towers:
                    for tower in all_towers:

                        try:
                            tower.update_angle((all_enemies[0].previous_position[0], all_enemies[0].previous_position[1]))
                        except:
                            continue
                        tower.draw(screen)


                        if tower.can_shoot():
                            tower.shoot()
                            shooting_clock.tick(60)
                            total_shooting_time += shooting_clock.get_time()
                            enemy.be_shot()

                            money += 2  
                            all_enemies.remove(enemy)

                            if total_shooting_time > 2000:
                                tower.revert_image()
                                total_shooting_time = 0
                                print("e")


                if side_menu_open:
                    side_menu_rect = side_menu_image.get_rect()
                    side_menu_rect.topleft = (300, 0)
                    screen.blit(side_menu_image, side_menu_rect)

                    if mouse_x < 370:
                        side_menu_open = False

                if not side_menu_open:
                    menu_rect = side_menu_small_image.get_rect()
                    menu_rect.topleft = (700, 0)
                    screen.blit(side_menu_small_image, menu_rect)

                    if mouse_x > 700:
                        side_menu_open = True
                    

                if level_start:


                    # Enemy
                    current_time = pygame.time.get_ticks()
                    if current_time - spawn_timer > enemy_spawn_interval and len(all_enemies) < enemies:
                        enemy = Enemy(2, CELL_SIZE)
                        all_enemies.append(enemy)
                        spawn_timer = current_time



                    for enemy in all_enemies:
                        prev_states = {}
                        #enemy.current_position = dfs(screen, CELL_SIZE, grid, enemy.current_position, enemy.visited_set, prev_states, enemy.colour, enemy.speed, enemy.enemy1_image)
                        enemy.current_position = enemy.dfs(screen, grid, prev_states)
                        
                        if enemy.current_position == enemy.previous_position:
                            enemy.visited_set.clear()
                            enemy.current_position = None
                            all_enemies.remove(enemy)
                        
                        else:
                            enemy.previous_position = enemy.current_position
                    

                    for enemy in all_enemies:
                        enemy.draw(screen, grid, prev_states)
                    pygame.time.delay(200)



                money_text = font.render(f"Money: {money}", True, (255,255,255))
                money_rect = money_text.get_rect(center = (90,20))
                screen.blit(money_text, money_rect)
        
        # Clear the screen
        pygame.display.flip()
        clock.tick(60)
    

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
