import pygame
import utilities
from figures import Figure


class Board:
    def __init__(self):
        self.board = []
        self.red_figures = 12
        self.black_figures = 12
        self.red_dame = 0
        self.black_dame = 0
        self.draw_figure()
        self.state = self.board
        
    
    def create_board(self, screen):
        screen.fill(utilities.green)
        for row in range(utilities.rows):
            for col in range(utilities.cols):
                if row % 2 == col % 2:
                    pygame.draw.rect(screen, utilities.white, (row * utilities.square_size, col * utilities.square_size, utilities.square_size, utilities.square_size))
                else:
                    pygame.draw.rect(screen, utilities.green, (row * utilities.square_size, col * utilities.square_size, utilities.square_size, utilities.square_size))        

    def draw_figure(self):
        for row in range(utilities.rows):
            self.board.append([])
            for col in range(utilities.cols):
                figure = 0
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        figure = Figure(row, col, utilities.black)
                    elif row > 4:
                        figure = Figure(row, col, utilities.red)
                self.board[row].append(figure)
        print(self.board_as_tuple())

    def get_all_figures(self, color):
        figures = []
        for row in self.board:
            for figure in row:
                if figure != 0 and figure.color == color:
                    figures.append(figure)
        return figures

    
    def draw_board(self, screen):
        self.create_board(screen)
        for row in range(utilities.rows):
            for col in range(utilities.cols):
                figure = self.board[row][col]
                if figure != 0:
                    figure.draw(screen)

    
    def remove(self, figures):
        for figure in figures:
            self.board[figure.row][figure.col] = 0
            if figure.color == utilities.red:
                self.red_figures -= 1
            else:
                self.black_figures -= 1
    
    def move_figure(self, figure, row, col):
        if figure != 0:
            self.board[figure.row][figure.col], self.board[row][col] = self.board[row][col], self.board[figure.row][figure.col]
            figure.moved(row, col)
            if row == utilities.rows - 1 or row == 0:
                figure.make_dama()
                if figure.color == utilities.red:
                    self.red_dame += 1
                else:
                    self.black_dame += 1

    def get_figure(self, row, col):
        return self.board[row][col]
    
    def board_as_tuple(self):

        tuple_board = []
        for row in range(utilities.rows):
            tuple_row = []
            for col in range(utilities.cols):
                figure = self.board[row][col]
                if figure == 0:
                    tuple_row.append(0)
                elif figure.color == utilities.black and not figure.is_dama():
                    tuple_row.append(1)
                elif figure.color == utilities.red and not figure.is_dama():
                    tuple_row.append(2)
                elif figure.color == utilities.black and figure.is_dama():
                    tuple_row.append(3)
                elif figure.color == utilities.red and figure.is_dama():
                    tuple_row.append(4)
            tuple_board.append(tuple(tuple_row))
        return tuple(tuple_board)
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == utilities.red or piece.dama:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == utilities.black or piece.dama:
            moves.update(self._traverse_left(row +1, min(row+3, utilities.rows), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, utilities.rows), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, utilities.rows)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= utilities.cols:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, utilities.rows)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves


    @classmethod
    def tuple_to_board(cls, tuple_board):
        board = cls()
        for row, tuple_row in enumerate(tuple_board):
            for col, cell_value in enumerate(tuple_row):
                if cell_value == 1:
                    board.board[row][col] = Figure(row, col, utilities.black)
                elif cell_value == 2:
                    board.board[row][col] = Figure(row, col, utilities.red)
        return board
    
        

            