import pygame
import utilities
from game import Game
from minimax import get_all_moves, minimax, tuple_to_board, evaluate_depth
import csv
from additional.menu import main_menu

screen = pygame.display.set_mode((utilities.width, utilities.height))
memoization = {}

pygame.display.set_caption("Checkers")

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

        screen.fill('black')

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
            depth = evaluate_depth(game)
            print(depth)
            board_key = game.board.board_as_tuple()
            if board_key in memoization:
                new_board = tuple_to_board(memoization[board_key])
                game.black_move(new_board)
                continue
            value, new_board = minimax(game.board, depth, utilities.black, game,  float("-inf"), float("inf"))
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
                print(len(get_all_moves(game.board, utilities.red, game)))
                

            game.update_display()
    pygame.quit()
if __name__ == "__main__":
    main_menu(screen, main)