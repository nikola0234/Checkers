import pygame
import utilities
from board import Board
from game import Game
from minimax import get_all_moves, minimax
from figures import Figure
import csv

screen = pygame.display.set_mode((utilities.width, utilities.height))
memoization = {}

pygame.display.set_caption("Checkers")

def tuple_to_board(tuple_board):
        board = Board()
        for row, tuple_row in enumerate(tuple_board):
            for col, cell_value in enumerate(tuple_row):
                if cell_value == 1:
                    board.board[row][col] = Figure(row, col, utilities.black)
                elif cell_value == 2:
                    board.board[row][col] = Figure(row, col, utilities.red)
                elif cell_value == 3:
                    board.board[row][col] = Figure(row, col, utilities.black)
                    board.board[row][col].make_dama()
                elif cell_value == 4:
                    board.board[row][col] = Figure(row, col, utilities.red)
                    board.board[row][col].make_dama()
                elif cell_value == 0:
                    board.board[row][col] = 0
        return board
    

def main():
    run = True
    game = Game()
    clock = game.clock
    fps = game.fps
    
    with open('moves.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            key, value = eval(row[0]), eval(row[1])
            memoization[key] = value

    while run:
        clock.tick(fps)

        if game.get_winner() != None:
            print('over')
            with open('moves.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for key, value in memoization.items():
                    writer.writerow([key, value])
            run = False
        
        
        if get_all_moves(game.board, utilities.red, game) == []:
            print("Black wins")
            with open('moves.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for key, value in memoization.items():
                    writer.writerow([key, value])
            run = False
        
        if get_all_moves(game.board, utilities.black, game) == []: 
            print("Red wins")
            with open('moves.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for key, value in memoization.items():
                    writer.writerow([key, value])
            run = False
        

        if game.turn == utilities.black:
            board_key = game.board.board_as_tuple()
            if board_key in memoization:
                new_board = tuple_to_board(memoization[board_key])
                game.black_move(new_board)
                continue
            value, new_board = minimax(game.board, 4, utilities.black, game,  float("-inf"), float("inf"))
            if new_board is not None and board_key not in memoization:    
                memoization[board_key] = new_board.board_as_tuple()
            game.black_move(new_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('moves.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    for key, value in memoization.items():
                        writer.writerow([key, value])
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                row, col = utilities.mouse_coordinates(position)
        
                game.select(row, col)
                

            game.update_display()
    pygame.quit()
if __name__ == "__main__":
    main()