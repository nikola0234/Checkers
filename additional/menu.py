import pygame, sys
from utilities import *

background = pygame.image.load('./images/Background.png', 'Background')
background = pygame.transform.scale(background, (1200, 800))
pygame.init()

def get_font(size): 
    return pygame.font.Font("./images/font.ttf", size)

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
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)
			

def main_menu(screen, play, game):
    while True:
        screen.blit(background, (0,0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(40).render("WELCOME TO CHECKERS", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        MODE1_TEXT = get_font(20).render("MODE 1: Skipping is optional ", True, "#b68f40")
        MODE1_RECT = MODE1_TEXT.get_rect(center=(400, 250))

        MODE2_TEXT = get_font(20).render("MODE 2: Skipping is mandatory", True, "#b68f40")
        MODE2_RECT = MODE2_TEXT.get_rect(center=(400, 450))

        PLAY_BUTTON = Button(image=pygame.image.load("./images/Play Rect.png"), pos=(400, 350), 
                            text_input="MODE 1", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
		
        PLAY_BUTTON2 = Button(image=pygame.image.load("./images/Play Rect.png"), pos=(400, 550),
                            text_input="MODE 2", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        
        QUIT_BUTTON = Button(image=pygame.image.load("./images/Quit Rect.png"), pos=(400, 750), 
                            text_input="QUIT", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(MODE1_TEXT, MODE1_RECT)
        screen.blit(MODE2_TEXT, MODE2_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON, PLAY_BUTTON2]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
				
                if PLAY_BUTTON2.checkForInput(MENU_MOUSE_POS):
				    
                    game.mode2 = True
					
                    play()
                
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.update()

def open_victory_screen(screen):
    screen.fill("#b68f40")
    VICTORY_TEXT = get_font(40).render("VICTORY", True, "White")
    VICTORY_RECT = VICTORY_TEXT.get_rect(center=(400, 200))
    screen.blit(VICTORY_TEXT, VICTORY_RECT)
    pygame.display.update()
    pygame.time.wait(3000)

def open_loose_screen(screen):
    red = (255, 10, 10)
    screen.fill(red)
    LOOSE_TEXT = get_font(40).render("LOOSE", True, "White")
    LOOSE_RECT = LOOSE_TEXT.get_rect(center=(400, 200))
    screen.blit(LOOSE_TEXT, LOOSE_RECT)
    pygame.display.update()
    pygame.time.wait(3000)