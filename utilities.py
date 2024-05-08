import pygame

width = 800
height = 800

rows = 8
cols = 8

square_size = width // cols

red = (204, 0, 0)
green = (0, 102, 51)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
grey = (128, 128, 128)

dame_crown = pygame.transform.scale(pygame.image.load("dame-kruna.png"), (88, 50))

def mouse_coordinates(pos):
    x, y = pos
    row = y // square_size
    col = x // square_size
    return row, col

def draw_options(row, col, screen):
    while not pygame.MOUSEBUTTONDOWN:    
        pygame.draw.circle(screen, blue, (col * square_size + square_size // 2, row * square_size + square_size // 2), square_size // 8)
        pygame.display.update()