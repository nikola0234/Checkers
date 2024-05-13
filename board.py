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
        self.board[figure.row][figure.col], self.board[row][col] = self.board[row][col], self.board[figure.row][figure.col]
        figure.moved(row, col)
        if row == utilities.rows - 1 or row == 0 and figure.dama == False:
            figure.make_dama()
            if figure.color == utilities.red:
                self.red_dame += 1
            else:
                self.black_dame += 1
    
    def get_figure(self, row, col):
        return self.board[row][col]

            