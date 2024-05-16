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
    
    def get_all_figures(self, color):
        figures = []
        for row in self.board:
            for figure in row:
                if figure != 0 and figure.color == color:
                    figures.append(figure)
        return figures

    
    def board_as_tuple(self):
        """
        Represents the board as a tuple.
        Black figures are represented by 1, empty cells by 0, and red figures by 2.
        """
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

    @classmethod
    def tuple_to_board(cls, tuple_board):
        """
        Reconstructs the board with figures from a tuple representation.
        """
        board = cls()
        for row, tuple_row in enumerate(tuple_board):
            for col, cell_value in enumerate(tuple_row):
                if cell_value == 1:
                    board.board[row][col] = Figure(row, col, utilities.black)
                elif cell_value == 2:
                    board.board[row][col] = Figure(row, col, utilities.red)
        return board
    
        

            