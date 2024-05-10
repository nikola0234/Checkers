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
        self.draw_options(self.allowed_moves)
        return True if self.seletced_figure else False
    
    def move(self, row, col):
        figure = self.board.get_figure(row, col)
        if self.seletced_figure and figure == 0 and (row, col) in self.allowed_moves:
            self.board.move_figure(self.seletced_figure, row, col)
            skipped_figures = []
            for row1, col1 in self.allowed_moves:  
                if row1 >= 0 and col1 >= 0:  
                    skipped_figures.append(self.allowed_moves[(row1, col1)])
            for skipped_figure in skipped_figures:
                self.board.remove(skipped_figure)
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

        def check_options(allowed_moves, new_row, new_col, directions, dir, dic):
            if 0 <= new_row < rows and 0 <= new_col < cols and new_row >= 0 and new_col >= 0 and self.board.get_figure(new_row, new_col) == 0 and (new_row, new_col) not in allowed_moves:
                allowed_moves[(new_row, new_col)] = []
                print(allowed_moves)
            elif 0 <= new_row < rows and 0 <= new_col < cols and new_row >= 0 and new_col >= 0 and self.board.get_figure(new_row, new_col) != 0 and self.board.get_figure(new_row, new_col).color == figure.color and (new_row, new_col) not in allowed_moves:
                return allowed_moves
            elif 0 <= new_row < rows and 0 <= new_col < cols and new_row >= 0 and new_col >= 0 and self.board.get_figure(new_row, new_col) != 0 and self.board.get_figure(new_row, new_col).color != figure.color and (new_row, new_col) not in allowed_moves:
                after_row = new_row + dir
                after_col = new_col + dic
                skipped_figure = self.board.get_figure(new_row, new_col)
                allowed_moves[(after_row, after_col)] = [skipped_figure]
                if 0 <= after_row < rows and 0 <= after_col < cols and self.board.get_figure(after_row, after_col) != 0:
                    allowed_moves.pop((after_row, after_col))
                elif 0 <= after_row < rows and 0 <= after_col < cols and self.board.get_figure(after_row, after_col) == 0:
                    for dir1, dic1 in directions:
                        if 0 <= after_row + dir1 < rows and 0 <= after_col + dic1 < cols and after_row + dir1 >= 0 and after_col + dic1 >= 0:
                            print(allowed_moves)
                            check_options(allowed_moves, after_row + dir1, after_col + dic1, directions, dir, dic)
                            print(allowed_moves)
            
        for dir, dic in directions:
            new_row = row + dir
            new_col = col + dic 
            check_options(allowed_moves, new_row, new_col, directions, dir, dic)
        
        return allowed_moves

    def draw_options(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.screen, blue, (col * width // cols + width // cols // 2, row * height // rows + height // rows // 2), width // cols // 8)
    
    def is_game_over(self):
        return self.board.red_figures == 0 or self.board.black_figures == 0