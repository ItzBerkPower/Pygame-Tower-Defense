import pygame
import sys
from collections import deque

# Intialise screen width and screen height
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750

def draw_custom_grid(screen, grid, CELL_SIZE, path_image, grass_image):
    """
    Draws the map to the screen based on the 2-D grid
    """

    # Loop through all the rows and columns for each individual cell
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            # If cell is 1, draw a path block
            if value == 1:
                image_rect = path_image.get_rect()
                image_rect.topleft = (col_idx * CELL_SIZE, row_idx * CELL_SIZE)
                screen.blit(path_image, image_rect)
            
            # If cell is 0, draw a grass block
            elif value == 0:
                image_rect = grass_image.get_rect()
                image_rect.topleft = (col_idx * CELL_SIZE, row_idx * CELL_SIZE)
                screen.blit(grass_image, image_rect)
