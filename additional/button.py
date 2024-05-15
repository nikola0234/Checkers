import pygame


class Button(object):
    def __init__(self, position, image, hovering_color, width, height, color, text=None):
        self.x = position[0]
        self.y = position[1]
        self.image = image
        self.color = color
        self.hovering_color = hovering_color
        self.width = width
        self.height = height
        self.text = text
        self.font = pygame.font.SysFont("comicsans", 40)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.text_rect = self.text.get_rect(center=(self.x, self.y))
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        if self.text:
            text = self.font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (self.x + self.width // 2 - text.get_width() // 2, self.y + self.height // 2 - text.get_height() // 2))
    
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def clicked(self, pos):
        x, y = pos
        
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            return True
        return False
    
    def hover(self, pos):
        x, y = pos
        
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            self.text = self.font.render(self.text, True, self.hovering_color)
        
        else: 
            self.text = self.font.render(self.text, True, self.color)