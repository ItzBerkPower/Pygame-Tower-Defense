import pygame
import math


class Tower(pygame.sprite.Sprite):

    def __init__(self, position, CELL_SIZE, turret_type, upgrade_level):
        super().__init__()

        self.rect = pygame.Rect(position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        self.position = position
        self.CELL_SIZE = CELL_SIZE
        self.angle = 0

        self.turret_type = turret_type
        self.upgrade_level = upgrade_level

        self.image = None
        self.rect = None
        self.load_images()

        self.shooting_image = None


        # Firing rate in milliseconds (e.g., 1000 milliseconds = 1 second)
        self.firing_rate = 1500
        self.last_shot_time = pygame.time.get_ticks()
    
    def load_images(self):
        image_paths = {
            'turret1': ['1_1.png', '1_2.png', '1_3.png', '1_4.png'],
            'turret2': ['2_1.png', '2_2.png', '2_3.png', '2_4.png'],
            'turret3': ['3_1.png', '3_2.png', '3_3.png']
        }

        # Load image based on turret type and upgrade level
        self.image_path = f"images/tower/unshot/{image_paths[self.turret_type][self.upgrade_level - 1]}"
        self.shooting_image_path = f"images/tower/shot/{image_paths[self.turret_type][self.upgrade_level - 1].replace('.png', '_shot.png')}"

        self.image = pygame.image.load(self.image_path)
        pygame.transform.scale(self.image, (50,50))

        self.rect = self.image.get_rect(center=(self.position[0] * self.CELL_SIZE + self.CELL_SIZE / 2,
                                                 self.position[1] * self.CELL_SIZE + self.CELL_SIZE / 2))
        



    def update_angle(self, target_position):
        # Calculate the angle between the tower and the target position
        dx = target_position[0] - self.position[0]
        dy = target_position[1] - self.position[1]
        angle_rad = math.atan2(dy, dx)
        self.angle = -math.degrees(angle_rad)

    def default_angle(self):
        self.angle = self.angle



    def draw(self, screen):
        rotated_surface = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_surface.get_rect(center=self.rect.center)
        screen.blit(rotated_surface, rotated_rect.topleft)


    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_shot_time
        return elapsed_time >= self.firing_rate

    def shoot(self):
        # Perform shooting action here
        self.image = pygame.image.load(self.shooting_image_path).convert_alpha()
        self.last_shot_time = pygame.time.get_ticks()  # Update last shot time after shooting

    
    def revert_image(self):
        self.image = pygame.image.load(self.image_path)


































    # Old draw function for when tower was red rectangle
    '''
    def draw(self, screen):
        #pygame.draw.rect(screen, (255,0,0), self.rect)
        rotated_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        rotated_surface.fill((0, 0, 0, 0))  # Transparent background
        rotated_rect = self.rect.copy()
        rotated_rect.center = rotated_surface.get_rect().center
        pygame.draw.rect(rotated_surface, (255,0,0), rotated_rect)

        # Rotate the surface
        rotated_surface = pygame.transform.rotate(rotated_surface, self.angle)
        
        # Get the rotated rectangle from the rotated surface
        rotated_rect = rotated_surface.get_rect(center=self.rect.center)

        # Draw the rotated rectangle on the screen
        screen.blit(rotated_surface, rotated_rect.topleft)
    '''

