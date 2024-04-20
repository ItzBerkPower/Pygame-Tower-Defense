import pygame
import math

# Tower class
class Tower(pygame.sprite.Sprite):
    
    # Initialise all the bits needed for class (Variable names self-explanatory)
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

        self.shooting_image = None

        self.firing_rate = self.get_firing_rate()
        self.last_shot_time = pygame.time.get_ticks()
    

    def load_images(self):
        """
        Load the images for the tower, parameters: None
        """

        # Dictionary with the image paths for every upgrade file
        image_paths = {
            'turret1': ['1_1.png', '1_2.png', '1_3.png', '1_4.png'],
            'turret2': ['2_1.png', '2_2.png', '2_3.png', '2_4.png'],
            'turret3': ['3_1.png', '3_2.png', '3_3.png']
        }

        # Load image based on turret type and upgrade level
        self.image_path = f"images/tower/unshot/{image_paths[self.turret_type][self.upgrade_level - 1]}"
        self.shooting_image_path = f"images/tower/shot/{image_paths[self.turret_type][self.upgrade_level - 1].replace('.png', '_shot.png')}"

        # Update the self.image for when drawing the actual tower
        self.image = pygame.image.load(self.image_path)
        pygame.transform.scale(self.image, (50,50))

        # Create the rect for the tower
        self.rect = self.image.get_rect(center=(self.position[0] * self.CELL_SIZE + self.CELL_SIZE / 2,
                                                 self.position[1] * self.CELL_SIZE + self.CELL_SIZE / 2))
        
    
    def get_firing_rate(self):
        """
        Get the firing rate per tower, parameters: None
        """

        if self.turret_type == "turret1": # If turret 1, firing rate = Once per 2000ms
            return 2000

        elif self.turret_type == "turret2": # If turret 2, firing rate = Once per 1750ms
            return 1750

        elif self.turret_type == "turret3": # If turret 3, firing rate = Once per 1500ms
            return 1500


    def update_angle(self, target_position):
        """
        Update the angle of the tower, parameters: Position of enemy
        """

        # Calculate the angle between the tower and the target position
        dx = target_position[0] - self.position[0] # Done by finding the angle using a right angle triangle and tangent
        dy = target_position[1] - self.position[1]
        angle_rad = math.atan2(dy, dx)
        self.angle = -math.degrees(angle_rad) # Convert angle to degrees

    def default_angle(self):
        """
        Set the angle to what it was before if no enemies are alive, parameters: None
        """

        self.angle = self.angle


    def draw(self, screen):
        """
        Draw the enemies to the screen, parameters: Screen to draw on
        """

        self.load_images() # Load the image for the tower
        rotated_surface = pygame.transform.rotate(self.image, self.angle) # Rotate tower based on angle, and draw to screen
        rotated_rect = rotated_surface.get_rect(center=self.rect.center)
        screen.blit(rotated_surface, rotated_rect.topleft)


    def can_shoot(self, time_after_enemy_spawn):
        """
        Check if the tower can shoot or not, parameters: Time after the enemy has spawned
        """

        current_time = pygame.time.get_ticks() # Get the current time, to get the time elapsed after last shot
        elapsed_time = current_time - self.last_shot_time

        # Return a boolean, checks if enough time elapsed, and 1 second has passed since enemy spawned
        return (elapsed_time >= self.firing_rate) and (time_after_enemy_spawn > 1000)


    def shoot(self):
        """
        Change the picture of the tower to shooting picture, and update last shot time, parameters: None
        """

        self.image = pygame.image.load(self.shooting_image_path).convert_alpha()
        self.last_shot_time = pygame.time.get_ticks()  # Update last shot time after shooting
        
    
    def revert_image(self):
        """
        Revert the image back to normal after shooting, parameters: None
        """

        self.image = pygame.image.load(self.image_path)


    def can_upgrade(self, money):
        """
        Check if the tower is able to be upgraded, parameters: Player money
        """

        upgrade_prices = { # Dictionary with all the upgrade prices per tower level
            'turret1': [0, 100, 125, 150],
            'turret2': [0, 200, 250, 300],
            'turret3': [0, 400, 500]
        }

        # If the price is an integer, and player has enough money, return True (Can be upgraded)
        if type(upgrade_prices[self.turret_type][self.upgrade_level]) is int and money >= upgrade_prices[self.turret_type][self.upgrade_level]:
            return True
        
        # Otherwise return False (Can't be upgraded)
        else:
            return False
        
        
    def upgrade_tower(self, money):
        """
        Upgrade the actual tower, parameters: Player money
        """

        upgrade_prices = { # Dictionary with all the upgrade prices per tower level
            'turret1': [0, 100, 125, 150],
            'turret2': [0, 200, 250, 300],
            'turret3': [0, 400, 500]
        }

        self.firing_rate -= 100 # Lower the firing rate
        self.upgrade_level += 1 # Increase the level

        money -= upgrade_prices[self.turret_type][self.upgrade_level - 1] # Subtract the money from the user

        # Return the changed money variable
        return money





def tower_functionality(screen, tower, all_towers, all_enemies, shooting_clock, total_shooting_time, money):
    """
    The actual tower functionality, parameters: Screen to draw on, tower, list of all towers, list of all enemies, shooting clock, the total shooting time, player money
    """

    # If there is a tower in all towers, loop through all the towers
    if tower in all_towers:
        for tower in all_towers:
            # Try setting a tower target that corresponds to the index of the tower in the all_towers list
            try:
                tower_target = all_enemies[all_towers.index(tower)]
            # If not, make it aim at the oldest enemy on the screen
            except:
                if len(all_enemies) > 0:
                    tower_target = all_enemies[0]

            # Try to update the angle based on the target enemy, but if there isn't any enemies, then keep the angle how it was
            try:
                tower.update_angle((tower_target.previous_position[0], tower_target.previous_position[1]))
            except:
                tower.default_angle()

            tower.draw(screen) # Draw the tower to the screen

            # If there is an enemy on screen, check if the tower is able to shoot
            if len(all_enemies) > 0:
                if tower.can_shoot(tower_target.time_after_spawn):
                    tower.shoot() # Shoot the enemy (Explained in actual function)
                    money += 2 # Increase money

                    tower_target.be_shot(all_enemies) # Remove the enemy (Explained in actual function)
                    shooting_clock.tick(60) # Update the shooting clock and update the total shooting time
                    total_shooting_time += shooting_clock.get_time()

                    # If the total shooting time has passed 2 seconds, change the image back and re-declare the total_shooting_time variable
                    if total_shooting_time > 2000:
                        tower.revert_image()
                        total_shooting_time = 0
    
    # Return the changed variables, which are the total shooting time and players money
    return total_shooting_time, money

