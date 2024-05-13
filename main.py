import pygame
import utilities
from board import Board
from game import Game
from minimax import get_all_moves, minimax, build_boards_tree
from tree import Node


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

        if game.turn == utilities.black:
            value, new_board = minimax(game.board, 3, utilities.black, game,  float("-inf"), float("inf"))
            possible_moves = get_all_moves(new_board, utilities.black, game)
            game.black_move(new_board)
            print(new_board.black_dame)

        if game.get_winner() != None:
            print(game.get_winner())
            run = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                row, col = utilities.mouse_coordinates(position)
        
                game.select(row, col)

            game.update_display()
    pygame.quit()
if __name__ == "__main__":
    main()