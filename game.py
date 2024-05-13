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
            result = self.move(row, col)
            if not result:
                self.seletced_figure = None
                self.allowed_moves = {}
                self.select(row, col)
        
        figure = self.board.get_figure(row, col)

        if figure != 0 and figure.color == self.turn:    
            self.seletced_figure = figure
            self.allowed_moves = self.get_valid_moves(self.seletced_figure)
            if self.seletced_figure:
                return True
            return False
        
    def move(self, row, col):
        figure = self.board.get_figure(row, col)
        
        if self.seletced_figure and figure == 0 and (row, col) in self.allowed_moves:
            self.board.move_figure(self.seletced_figure, row, col)
            skipped_figures = []
            for row1, col1 in self.allowed_moves:  
                if row1 >= 0 and col1 >= 0 and row == row1 and col == col1:  
                    skipped_figures.append(self.allowed_moves[(row1, col1)])
            for skipped_figure in skipped_figures:
                self.board.remove(skipped_figure)  
        else:
            return False
        self.changing_turn()  

    def changing_turn(self):
        self.allowed_moves = {}
        if self.turn == red:
            self.turn = black
        elif self.turn == black:
            self.turn = red


    def is_move_valid(self, figure, row, col):
        moves = self.get_valid_moves(figure)
        if row >= 0 and col >= 0 and (row, col) in moves:
            return True
        return False


    def get_valid_moves(self, figure):
        moves = {}
        skipped = []
        left = figure.col - 1
        right = figure.col + 1
        row = figure.row

        if figure.color == red or figure.dama:
            moves.update(self._traverse_direction(row - 1, max(row - 3, -1), -1, figure.color, left, -1, skipped))
            moves.update(self._traverse_direction(row - 1, max(row - 3, -1), -1, figure.color, right, 1, skipped ))
        if figure.color == black or figure.dama:
            moves.update(self._traverse_direction(row + 1, min(row + 3, rows), 1, figure.color, left, -1, skipped))
            moves.update(self._traverse_direction(row + 1, min(row + 3, rows), 1, figure.color, right, 1, skipped))

        return moves

    def _traverse_direction(self, start, stop, step, color, col, direction, skipped):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if direction == -1 and col < 0:
                break
            if direction == 1 and col >= cols:
                break

            current = self.board.get_figure(r, col)
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
                    moves.update(self._traverse_direction(r + step, row, step, color, col - 1, -1, skipped=last))
                    moves.update(self._traverse_direction(r + step, row, step, color, col + 1, 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            col += direction

        return moves
    

    def get_allowed_moves(self, figure):
        allowed_moves = {}

        if figure == 0 or figure.color != self.turn:
            return allowed_moves
        
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
            
            elif 0 <= new_row < rows and 0 <= new_col < cols and new_row >= 0 and new_col >= 0 and self.board.get_figure(new_row, new_col) != 0 and self.board.get_figure(new_row, new_col).color == figure.color and (new_row, new_col) not in allowed_moves:
                return
                
            elif 0 <= new_row < rows and 0 <= new_col < cols and self.board.get_figure(new_row, new_col) != 0 and self.board.get_figure(new_row, new_col).color != figure.color and (new_row, new_col) not in allowed_moves:
                after_row = new_row + dir
                after_col = new_col + dic
                skipped_figure = self.board.get_figure(new_row, new_col)
                allowed_moves[(after_row, after_col)] = [skipped_figure]

                if 0 <= after_row < rows and 0 <= after_col < cols and self.board.get_figure(after_row, after_col) == 0:
                    
                    if 0 <= after_row + dir < rows and 0 <= after_col + dic < cols and after_row + dir >= 0 and after_col + dic >= 0 and self.board.get_figure(after_row + dir, after_col + dic) != 0 and self.board.get_figure(after_row + dir, after_col + dic).color != figure.color:
                        check_options(allowed_moves, after_row + dir, after_col + dic, directions, dir, dic)
                
                elif 0 <= after_row < rows and 0 <= after_col < cols and self.board.get_figure(after_row, after_col) != 0:
                    allowed_moves.pop((after_row, after_col))

        for dir, dic in directions:
            new_row = row + dir
            new_col = col + dic 
            check_options(allowed_moves, new_row, new_col, directions, dir, dic)
        
        return allowed_moves

    def draw_options(self, moves):
        for move in moves:
            figure = self.seletced_figure
            if figure.color == self.turn:
                row, col = move
                pygame.draw.circle(self.screen, blue, (col * width // cols + width // cols // 2, row * height // rows + height // rows // 2), width // cols // 8)
    
    def is_game_over(self):
        return self.board.red_figures == 0 or self.board.black_figures == 0

    def get_winner(self):
        if self.board.red_figures == 0:
            return black
        elif self.board.black_figures == 0:
            return red
        return None
                
    def black_move(self, board):
        self.board = board
        self.changing_turn()