import pygame
import utilities

screen = pygame.display.set_mode((utilities.width, utilities.height))

pygame.display.set_caption("Checkers")

def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(utilities.fps)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
if __name__ == "__main__":
    main()