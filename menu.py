import pygame, sys

# Button class
class Button():
    # Initialise all the bits needed for class (Variable names self-explanatory)
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos, self.y_pos = pos
	
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
          
        self.text_input = text_input
          
        self.text = self.font.render(self.text_input, True, self.base_color)
          
        if self.image is None:
            self.image = self.text
               
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    
    def update(self, screen):
        """
        Draw button to screen, parameters: Screen to draw on
        """
        # If the button has a backdrop, draw the backdrop
        if self.image is not None:
            screen.blit(self.image, self.rect)
        # Draw the actual button text as well
        screen.blit(self.text, self.text_rect)


    def changeColor(self, position):
        """
        Change colour of button when input, parameters: Position of mouse for input
        """

        # If player hovers over, change colour of button
        if self.checkForInput(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        
        # If not, keep base colour
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
            

    def checkForInput(self, position):
        """
        Check for player hovering, parameters: Position of mouse
        """

        # If player hovers over button, return True, otherwise, return False
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False



pygame.init()
pygame.display.set_caption("Menu")


def get_font(size):
    """
    Get the font size of the blocky font, parameters: Size of font
    """

    # Return the font with specified size, exiting the functionfil
    return pygame.font.Font("fonts/blocky_font.ttf", size)


    
def controls(screen, background):
    """
    Controls screen on main menu, parameters: Screen to draw on, background picture of main menu
    """
    # Infinite loop
    controls = True
    while controls:
        # Get mouse positions
        CONTROLS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("black") # Reset the screen

        # Create a title for the page called "Controls"
        CONTROLS_TITLE = get_font(40).render("Controls", True, "#b68f40")
        CONTROLS_TITLE_RECT = CONTROLS_TITLE.get_rect(center=(375, 100))
        screen.blit(CONTROLS_TITLE, CONTROLS_TITLE_RECT)

        # Aim of game text
        GAME_AIM_TEXT = get_font(10).render("Aim of the game is to make sure the enemy doesn't reach the end!", True, "White")
        GAME_AIM_RECT = GAME_AIM_TEXT.get_rect(center = (375, 200))
        screen.blit(GAME_AIM_TEXT, GAME_AIM_RECT)

        # Controls of game text
        CONTROLS_TEXT = get_font(10).render("Controls are simple, just drag and drop towers!", True, "White")
        CONTROLS_TEXT_RECT = CONTROLS_TEXT.get_rect(center = (375, 300))
        screen.blit(CONTROLS_TEXT, CONTROLS_TEXT_RECT)

        # Before each round text
        BEFORE_ROUND_TEXT = get_font(10).render("Also, before each round you have time to place towers", True, "White")
        BEFORE_ROUND_RECT = BEFORE_ROUND_TEXT.get_rect(center = (375, 350))
        screen.blit(BEFORE_ROUND_TEXT, BEFORE_ROUND_RECT)

        # How to start each round text
        SPACE_TO_START_TEXT = get_font(10).render("Press space to start every round!", True, "White") 
        SPACE_TO_START_RECT = SPACE_TO_START_TEXT.get_rect(center = (375, 400))
        screen.blit(SPACE_TO_START_TEXT, SPACE_TO_START_RECT)

        # Create a back button
        CONTROLS_BACK = Button(image=None, pos=(375, 450), 
                            text_input="BACK", font=get_font(20), base_color="White", hovering_color="Green")

        CONTROLS_BACK.changeColor(CONTROLS_MOUSE_POS)
        CONTROLS_BACK.update(screen)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If user clicks the X in top right, quit the game
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if CONTROLS_BACK.checkForInput(CONTROLS_MOUSE_POS): # If user clicks on "BACK" button, go back to the main menu and terminate infinite loop
                    main_menu(screen, background)
                    controls = False

        pygame.display.update()


def main_menu(screen, background):
    """
    Main menu screen, parameters: Screen to draw on, background picture of main menu
    """

    # Infinite loop
    menu = True
    while menu:
        screen.blit(background, (0, 0)) # Put the background picture up

        # Get the mouse coordinates of menu
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Main menu title at the top
        MENU_TEXT = get_font(60).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center = (375, 100))
        screen.blit(MENU_TEXT, MENU_RECT)


        # Make a play button
        PLAY_BUTTON = Button(image=pygame.image.load("fonts/font_backgrounds/Play Rect.png"), pos = (375, 210), 
                            text_input="PLAY", font = get_font(70), base_color = "#d7fcd4", hovering_color = "White")
        
        # Make a controls button
        CONTROLS_BUTTON = Button(image=pygame.image.load("fonts/font_backgrounds/Controls Rect.png"), pos = (375, 375), 
                            text_input="CONTROLS", font = get_font(70), base_color = "#d7fcd4", hovering_color = "White")
        
        # Make a quit button
        QUIT_BUTTON = Button(image=pygame.image.load("fonts/font_backgrounds/Quit Rect.png"), pos = (375, 540), 
                            text_input="QUIT", font = get_font(70), base_color = "#d7fcd4", hovering_color = "White")

        
        # Loop through all the buttons, printing them to screen
        for button in [PLAY_BUTTON, CONTROLS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If user clicks the X in top right, quit the game
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS): # If the user clicks the play button, terminate the while loop and exit the function
                    menu = False
                if CONTROLS_BUTTON.checkForInput(MENU_MOUSE_POS): # If the user clicks the controls button, go to the controls screen
                    controls(screen, background)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS): # If the user clicks the quit button, quit the game
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

    return



def game_over(screen, background, level):
    '''
    # Get mouse position
    #GAME_OVER_MOUSE_POS = pygame.mouse.get_pos()
    '''

    # Infinite loop
    game_over = True
    while game_over:
        screen.fill((0,0,0)) # Reset screen

        # Game over text
        GAME_OVER_TEXT = get_font(60).render("GAME OVER", True, "#b68f40")
        GAME_OVER_RECT = GAME_OVER_TEXT.get_rect(center = (375, 100))
        screen.blit(GAME_OVER_TEXT, GAME_OVER_RECT)

        # Level text
        FINAL_LEVEL_TEXT = get_font(20).render(f"Final Level: {level}", True, "White")
        FINAL_LEVEL_RECT = FINAL_LEVEL_TEXT.get_rect(center = (375, 200))
        screen.blit(FINAL_LEVEL_TEXT, FINAL_LEVEL_RECT)

        # Bye bye text
        BYE_BYE_TEXT = get_font(20).render("Bye bye!", True, "White")
        BYE_BYE_RECT = BYE_BYE_TEXT.get_rect(center = (375, 450))
        screen.blit(BYE_BYE_TEXT, BYE_BYE_RECT)
        
        # STUB: Adding back button on ending screen
        '''
        GAME_OVER_BACK = Button(image=None, pos=(375, 450), text_input="BACK", font=get_font(20), base_color="White", hovering_color="Green")

        GAME_OVER_BACK.changeColor(GAME_OVER_MOUSE_POS)
        GAME_OVER_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if GAME_OVER_BACK.checkForInput(GAME_OVER_MOUSE_POS):
                    main_menu(screen, background)
                    game_over = False
        '''

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If user clicks the X in top right, quit the game
                pygame.quit()
                sys.exit()

        pygame.display.update()



def level_text(screen, level):
    """
    Text that shows player level before every level, parameters: Screen to draw on, current player level
    """
    # Level text
    LEVEL_TEXT = get_font(40).render(f"Level: {level}", True, "#b68f40")
    LEVEL_RECT = LEVEL_TEXT.get_rect(center = (375, 375))
    screen.blit(LEVEL_TEXT, LEVEL_RECT)

def money_text(screen, money):
    """
    Text that shows the money the player has in the top right corner, parameters: Screen to draw on, current player money
    """
    # Money text
    MONEY_TEXT = get_font(15).render(f"Money: {money}", True, "White")
    MONEY_RECT = MONEY_TEXT.get_rect(center = (90, 20))
    screen.blit(MONEY_TEXT, MONEY_RECT)

def health_text(screen, health):
    """
    Text that shows the health the player has in the top left corner, parameters: Screen to draw on, current player health
    """
    # Health text
    HEALTH_TEXT = get_font(15).render(f"Health: {health}", True, "White")
    HEALTH_RECT = HEALTH_TEXT.get_rect(center = (640, 20))
    screen.blit(HEALTH_TEXT, HEALTH_RECT)