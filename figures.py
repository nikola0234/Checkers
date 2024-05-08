import pygame
import utilities


class Figure(object):
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.dama = False
        self.x = 0
        self.y = 0
        self.position()
    
    def position(self):
        self.x = self.col * utilities.square_size + utilities.square_size // 2
        self.y = self.row * utilities.square_size + utilities.square_size // 2
    
    def make_dama(self):
        self.dama = True
    
    def draw(self, screen):
        pygame.draw.circle(screen, utilities.grey, (self.x, self.y), utilities.square_size // 3 + 5)
        pygame.draw.circle(screen, self.color, (self.x, self.y), utilities.square_size // 3)

        if self.dama:
            screen.blit(utilities.dame_crown, (self.x - utilities.square_size // 3 - 10, self.y - utilities.square_size // 3 + 5))

    def is_dama(self):
        return self.dama
    
    def moved(self, row, col):
        self.row = row
        self.col = col
        self.position()
