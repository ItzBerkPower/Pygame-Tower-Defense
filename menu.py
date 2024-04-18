import pygame, sys

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if self.checkForInput(position):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)


pygame.init()


pygame.display.set_caption("Menu")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)
    
def controls(screen, background):
    controls = True
    while controls:
        CONTROLS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("black")

        CONTROLS_TITLE = get_font(40).render("Controls", True, "#b68f40")
        CONTROLS_TITLE_RECT = CONTROLS_TITLE.get_rect(center=(375, 100))
        screen.blit(CONTROLS_TITLE, CONTROLS_TITLE_RECT)

        GAME_AIM_TEXT = get_font(10).render("Aim of the game is to make sure the enemy doesn't reach the end!", True, "White")
        GAME_AIM_RECT = GAME_AIM_TEXT.get_rect(center = (375, 200))
        screen.blit(GAME_AIM_TEXT, GAME_AIM_RECT)

        CONTROLS_TEXT = get_font(10).render("Controls are simple, just drag and drop towers!", True, "White")
        CONTROLS_TEXT_RECT = CONTROLS_TEXT.get_rect(center = (375, 300))
        screen.blit(CONTROLS_TEXT, CONTROLS_TEXT_RECT)

        BEFORE_ROUND_TEXT = get_font(10).render("Also, before each round you have time to place towers", True, "White")
        BEFORE_ROUND_RECT = BEFORE_ROUND_TEXT.get_rect(center = (375, 350))
        screen.blit(BEFORE_ROUND_TEXT, BEFORE_ROUND_RECT)

        SPACE_TO_START_TEXT = get_font(10).render("Press space to start every round!", True, "White") 
        SPACE_TO_START_RECT = SPACE_TO_START_TEXT.get_rect(center = (375, 400))
        screen.blit(SPACE_TO_START_TEXT, SPACE_TO_START_RECT)

        CONTROLS_BACK = Button(image=None, pos=(375, 450), 
                            text_input="BACK", font=get_font(20), base_color="White", hovering_color="Green")

        CONTROLS_BACK.changeColor(CONTROLS_MOUSE_POS)
        CONTROLS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CONTROLS_BACK.checkForInput(CONTROLS_MOUSE_POS):
                    main_menu(screen, background)
                    controls = False

        pygame.display.update()

def main_menu(screen, background):
    menu = True
    while menu:
        screen.blit(background, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(60).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center = (375, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos = (375, 210), 
                            text_input="PLAY", font = get_font(70), base_color = "#d7fcd4", hovering_color = "White")
        
        CONTROLS_BUTTON = Button(image=pygame.image.load("assets/Controls Rect.png"), pos = (375, 375), 
                            text_input="CONTROLS", font = get_font(70), base_color = "#d7fcd4", hovering_color = "White")
        
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos = (375, 540), 
                            text_input="QUIT", font = get_font(70), base_color = "#d7fcd4", hovering_color = "White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, CONTROLS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    menu = False
                if CONTROLS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    controls(screen, background)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

    return


