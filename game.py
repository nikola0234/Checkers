import pygame
from board import Board
from utilities import width, height, red, black, rows, cols, blue


class Game(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Checkers")
        self.fps = 60
        self.board = Board()
        self.clock = pygame.time.Clock()
        self.run = True
        self.seletced_figure = None
        self.turn = red
        self.allowed_moves = {}
    
    def get_selected_figure(self):
        return self.seletced_figure
    
    def get_board(self):
        return self.board
    
    def get_turn(self):
        return self.turn
    
    def update_display(self):
        self.board.draw_board(self.screen)
        self.draw_options(self.allowed_moves)
        pygame.display.update()
    
    def reset(self):
        self.board = Board()
        self.seletced_figure = None
        self.turn = red
        self.allowed_moves = {}

    def select(self, row, col):
        if self.seletced_figure:
            self.move(row, col)
            
        self.seletced_figure = self.board.get_figure(row, col)
        self.allowed_moves = self.get_allowed_moves(self.seletced_figure)
        print(self.allowed_moves)
        self.draw_options(self.allowed_moves)
        return True if self.seletced_figure else False
    
    def move(self, row, col):
        figure = self.board.get_figure(row, col)
        if self.seletced_figure and figure == 0 and (row, col) in self.allowed_moves:
            self.board.move_figure(self.seletced_figure, row, col)
            skipped_figures = self.allowed_moves[(row, col)]
            if skipped_figures:
                self.board.remove(skipped_figures)
            self.changing_turn()    
        else:
            return False
        return True

    def changing_turn(self):
        if self.turn == red:
            self.turn = black
        elif self.turn == black:
            self.turn = red

    
    def get_allowed_moves(self, figure):
        allowed_moves = {}

        if figure == 0 or figure.color != self.turn:
            return {}
        
        row = figure.row
        col = figure.col

        if not figure.is_dama():
            if figure.color == red:    
                directions = [(-1, -1), (-1, 1)]
            else:
                directions = [(1, -1), (1, 1)]
        if figure.is_dama():
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dir, dic in directions:
            new_row = row + dir
            new_col = col + dic
            if 0 <= new_row < rows and 0 <= new_col < cols and self.board.get_figure(new_row, new_col) == 0:
                allowed_moves[(new_row, new_col)] = []
            elif 0 <= new_row < rows and 0 <= new_col < cols and self.board.get_figure(new_row, new_col) != 0 and self.board.get_figure(new_row, new_col).color != figure.color:
                skipped_figure = self.board.get_figure(new_row, new_col)
                new_row += dir
                new_col += dic
                if 0 <= new_row < rows and 0 <= new_col < cols and self.board.get_figure(new_row, new_col) == 0:
                    allowed_moves[(new_row, new_col)] = [skipped_figure]
        return allowed_moves
        
    def draw_options(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.screen, blue, (col * width // cols + width // cols // 2, row * height // rows + height // rows // 2), width // cols // 8)