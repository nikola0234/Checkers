import pygame
from board import Board
from utilities import width, height, red, black, rows, cols, blue
from copy import deepcopy
from minimax import get_all_moves


class Game(object):
    def __init__(self, screen):
        self.screen = screen
        pygame.display.set_caption("Checkers")
        self.fps = 20
        self.board = Board()
        self.clock = pygame.time.Clock()
        self.run = True
        self.seletced_figure = None
        self.turn = red
        self.allowed_moves = {}
        self.turn_number = 0
        self.red_skipped = 0
        self.black_skipped = 0
        self.mode2 = False
    
    def get_selected_figure(self):
        return self.seletced_figure
    
    def get_board(self):
        return self.board
    
    def get_turn(self):
        return self.turn
    
    def update_display(self):
        if self.board is not None:    
            self.board.draw_board(self.screen)
            self.draw_options(self.allowed_moves)
            pygame.display.update()
        else:
            return None
    
    def select(self, row, col):
        if self.seletced_figure:
            result = self.move(row, col)
            if not result:
                self.seletced_figure = None
                self.allowed_moves = {}
                self.select(row, col)
        
        if self.board is not None:    
            figure = self.board.get_figure(row, col)

            if figure != 0 and figure.color == self.turn:    
                self.seletced_figure = figure
                self.allowed_moves = self.get_valid_moves(self.seletced_figure)
                if self.mode2 == True:

                    moves_copy = self.allowed_moves.copy()

                    for move in moves_copy:
                        if len(moves_copy[move]) > 0:
                            for move1 in moves_copy:
                                if len(moves_copy[move1]) == 0:
                                    self.allowed_moves.pop(move1) 

                if self.seletced_figure:
                    return True
                return False
            
    def move(self, row, col):
        figure = self.board.get_figure(row, col)
        
        if self.seletced_figure and figure == 0 and (row, col) in self.allowed_moves:
            self.board.move_figure(self.seletced_figure, row, col)
            skipped_figures = self.allowed_moves[(row, col)]
            if skipped_figures:    
                self.board.remove(skipped_figures)
                if self.turn == red:
                    self.black_skipped += 1
                else:
                    self.red_skipped += 1
            self.changing_turn()            
        else:
            return False

    def changing_turn(self):
        self.allowed_moves = {}
        if self.turn == red:
            self.turn = black
        elif self.turn == black:
            self.turn = red
        self.turn_number += 1


    def is_move_valid(self, figure, row, col):
        moves = self.get_valid_moves(figure)
        if row >= 0 and col >= 0 and (row, col) in moves:
            return True
        return False


    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == red or piece.dama:
            moves.update(self._traverse(row - 1, max(row - 3, -1), -1, piece.color, left, direction='left'))
            moves.update(self._traverse(row - 1, max(row - 3, -1), -1, piece.color, right, direction='right'))
        if piece.color == black or piece.dama:
            moves.update(self._traverse(row + 1, min(row + 3, rows), 1, piece.color, left, direction='left'))
            moves.update(self._traverse(row + 1, min(row + 3, rows), 1, piece.color, right, direction='right'))

        return moves

    def _traverse(self, start, stop, step, color, col, direction, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if col < 0 or col >= cols:
                break

            current = self.board.board[r][col]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, col)] = last + skipped
                else:
                    moves[(r, col)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, rows)
                    moves.update(self._traverse(r + step, row, step, color, col - 1, direction='left', skipped=last))
                    moves.update(self._traverse(r + step, row, step, color, col + 1, direction='right', skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            if direction == 'left':
                col -= 1
            elif direction == 'right':
                col += 1

        return moves


    def draw_options(self, moves):
        for move in moves:
            figure = self.seletced_figure
            if figure.color == self.turn:
                row, col = move
                pygame.draw.circle(self.screen, blue, (col * width // cols + width // cols // 2, row * height // rows + height // rows // 2), width // cols // 8)
    
    def is_game_over(self):
        return self.board.red_figures == 0 or self.board.black_figures == 0

    def get_winner(self):
        if self.red_skipped == 12:
            return black
        elif self.black_skipped == 12:
            return red
        return None
                
    def black_move(self, board):
        self.board = board
        self.changing_turn()
    
    def get_all_moves(self, color):
        moves = []
        if self.board != None:
            for row in range(rows):
                for col in range(cols):
                    figure = self.board.get_figure(row, col)
                    if figure != 0 and figure.color == color:
                        new_board = deepcopy(self.board)
                        new_fiugre = new_board.get_figure(row, col)
                        new_board1 = self.move(row, col)

                        moves.append(new_board1)
        return moves
    