import pygame, sys
import utilities
from game import Game
from minimax import get_all_moves, minimax, tuple_to_board, evaluate_depth, minimax2
import csv
from additional.menu import main_menu, open_victory_screen, open_loose_screen

screen = pygame.display.set_mode((utilities.width, utilities.height))
memoization = {}

pygame.display.set_caption("Checkers")
pygame.init()
game = Game(screen)

def main():
    run = True
    clock = game.clock
    fps = game.fps
    
    
    if game.mode2 == False:
        with open('moves.csv', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                key, value = eval(row[0]), eval(row[1])
                memoization[key] = value
    if game.mode2 == True:
        with open('moves2.csv', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                key, value = eval(row[0]), eval(row[1])
                memoization[key] = value

    while run:
        clock.tick(fps)

        screen.fill('black')

        if game.get_winner() != None:
            if game.mode2 == False:
                with open('moves.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    for key, value in memoization.items():
                        writer.writerow([key, value])
            elif game.mode2 == True:
                with open('moves2.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    for key, value in memoization.items():
                        writer.writerow([key, value])
            if game.get_winner() == utilities.red:
                open_victory_screen(screen)
            elif game.get_winner() == utilities.black:
                open_loose_screen(screen)
            run = False
        
        
        if get_all_moves(game.board, utilities.red) == []:
            print("Black wins")
            if game.mode2 == False:
                with open('moves.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    for key, value in memoization.items():
                        writer.writerow([key, value])
            elif game.mode2 == True:
                with open('moves2.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    for key, value in memoization.items():
                        writer.writerow([key, value])
            open_loose_screen(screen)
            run = False
        
        elif get_all_moves(game.board, utilities.black) == []: 
            print("Red wins")
            if game.mode2 == False:    
                with open('moves.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    for key, value in memoization.items():
                        writer.writerow([key, value])
            elif game.mode2 == True:
                with open('moves2.csv', 'w', 'newline') as csvfile:
                    writer = csv.writer(csvfile)
                    for key, value in memoization.items():
                        writer.writerow([key, value])
            open_victory_screen(screen)
            run = False
        
        if game.turn == utilities.black and game.board.red_figures > 2:
            
            depth = evaluate_depth(game)
            board_key = game.board.board_as_tuple()
            if board_key in memoization:
                new_board = tuple_to_board(memoization[board_key])
                game.black_move(new_board)
                continue
            value, new_board = minimax(game.board, depth, True, game, float('-inf'), float('inf'))
            if new_board is not None and board_key not in memoization:    
                memoization[board_key] = new_board.board_as_tuple()
            game.black_move(new_board)
        
        elif game.turn == utilities.black and (game.board.red_figures <= 2 or game.board.black_figures <= 2):
            depth = 4
            board_key = game.board.board_as_tuple()
            if board_key in memoization:
                new_board = tuple_to_board(memoization[board_key])
                game.black_move(new_board)
                continue
            value, new_board = minimax2(game.board, depth, True, game)
            if new_board is not None and board_key not in memoization:
                memoization[board_key] = new_board.board_as_tuple()
            game.black_move(new_board)

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                row, col = utilities.mouse_coordinates(position)
        
                game.select(row, col)

            game.update_display()
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main_menu(screen, main, game)