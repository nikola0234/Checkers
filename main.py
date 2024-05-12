import pygame
import utilities
from board import Board
from game import Game


screen = pygame.display.set_mode((utilities.width, utilities.height))

pygame.display.set_caption("Checkers")

def main():
    run = True
    game = Game()
    clock = game.clock
    board = game.board
    fps = game.fps

    while run:
        clock.tick(fps)

        if game.get_winner() != None:
            print(game.get_winner())
            run = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                row, col = utilities.mouse_coordinates(position)
                figure_to_move = board.get_figure(row, col)  

                game.select(row, col)  

            board.draw_board(screen)
            pygame.display.update()

            game.update_display()
    pygame.quit()
if __name__ == "__main__":
    main()