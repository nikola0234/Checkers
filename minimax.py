import utilities
from copy import deepcopy
from board import Board
from figures import Figure


def minimax(board, depth, max_player, game, alpha, beta):
    
    if depth == 0 or game.get_winner() != None:
        return evaluate_current_board(board), board

    if max_player:
        max_eval = float("-inf")
        best_move = None
        for move in get_all_moves(board, utilities.black, game):
            if move.board_as_tuple() == ((0, 1, 0, 1, 0, 1, 0, 1), (1, 0, 1, 0, 1, 0, 1, 0), (0, 1, 0, 1, 0, 1, 0, 1), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (2, 0, 2, 0, 2, 0, 2, 0), (0, 2, 0, 2, 0, 2, 0, 2), (2, 0, 2, 0, 2, 0, 2, 0)):
                continue    
            evaluation = minimax(move, depth - 1, False, game, alpha, beta)[0]
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        print(max_eval)  
        return max_eval, best_move
    else:
        min_eval = float("inf")
        best_move = None
        for move in get_all_moves(board, utilities.red, game):
            if move.board_as_tuple() == ((0, 1, 0, 1, 0, 1, 0, 1), (1, 0, 1, 0, 1, 0, 1, 0), (0, 1, 0, 1, 0, 1, 0, 1), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (2, 0, 2, 0, 2, 0, 2, 0), (0, 2, 0, 2, 0, 2, 0, 2), (2, 0, 2, 0, 2, 0, 2, 0)):
                continue
            evaluation = minimax(move, depth - 1, True, game, alpha, beta)[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        print(min_eval)  
        return min_eval, best_move


def minimax1(position, depth, max_player, game, alfa, beta):
    if depth == 0:
        return evaluate_current_board(position), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves1(position, utilities.black, game):
            if move.board_as_tuple() == ((0, 1, 0, 1, 0, 1, 0, 1), (1, 0, 1, 0, 1, 0, 1, 0), (0, 1, 0, 1, 0, 1, 0, 1), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (2, 0, 2, 0, 2, 0, 2, 0), (0, 2, 0, 2, 0, 2, 0, 2), (2, 0, 2, 0, 2, 0, 2, 0)):
                continue
            evaluation = minimax1(move, depth-1, False, game, alfa, beta)[0]
            maxEval = max(maxEval, evaluation)
            alfa = max(alfa, evaluation)
            if beta <= alfa * 0.5:
                break
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves1(position, utilities.red, game):
            if move.board_as_tuple() == ((0, 1, 0, 1, 0, 1, 0, 1), (1, 0, 1, 0, 1, 0, 1, 0), (0, 1, 0, 1, 0, 1, 0, 1), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (2, 0, 2, 0, 2, 0, 2, 0), (0, 2, 0, 2, 0, 2, 0, 2), (2, 0, 2, 0, 2, 0, 2, 0)):
                continue
            evaluation = minimax1(move, depth-1, True, game, alfa, beta)[0]
            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alfa * 0.5:
                break
            if minEval == evaluation:
                best_move = move
        return minEval, best_move


# Heuristika, na osnovu koje se racuna vrednost trenutne table. Na osnovu probe, smatram ove vrednosti optimalnim.

def evaluate_current_board1(board):
    return board.black_figures - board.red_figures + 0.5*(board.black_dame - board.red_dame)

def evaluate_current_board(board):
  
    regular_figure_weight = 5
    dama_weight = 7.75
    figure_in_back_row_weight = 4
    figure_in_middle_box_weight = 2.5
    figure_in_middle_two_rows_weight = 0.5
    protected_figure_weight = 3
    figure_in_corner_weight = 3
    vulnerable_figure_weight = -3

    player_figures = 0
    computer_figures = 0
    player_dama = 0
    computer_dama = 0
    player_figures_in_back_row = 0
    computer_figures_in_back_row = 0
    player_figures_in_middle_box = 0
    computer_figures_in_middle_box = 0
    player_figures_in_middle_two_rows = 0
    computer_figures_in_middle_two_rows = 0
    player_protected_figures = 0
    computer_protected_figures = 0
    player_figures_in_corner = 0
    computer_figures_in_corner = 0
    player_vulnerable_figures = 0
    computer_vulnerable_figures = 0

    for row in range(8):
        for col in range(8):
            figure = board.get_figure(row, col)
            if figure is not None and figure != 0:
                if figure.color == utilities.red:
                    player_figures += 1
                    if figure.is_dama():
                        player_dama += 1
                    else:
                        if row == 7:
                            player_figures_in_back_row += 1
                        if 2 <= row <= 5 and 2 <= col <= 5:
                            player_figures_in_middle_box += 1
                        if 3 <= row <= 4:
                            player_figures_in_middle_two_rows += 1
                        if is_protected(board, figure):
                            player_protected_figures += 1
                        if is_figure_in_corner(figure):
                            player_figures_in_corner += 1
                        if is_figure_vulnerable(board, figure):
                            player_vulnerable_figures += 1
                elif figure.color == utilities.black:
                    computer_figures += 1
                    if figure.is_dama():
                        computer_dama += 1
                    else:
                        if row == 0:
                            computer_figures_in_back_row += 1
                        if 2 <= row <= 5 and 2 <= col <= 5:
                            computer_figures_in_middle_box += 1
                        if 3 <= row <= 4:
                            computer_figures_in_middle_two_rows += 1
                        if is_protected(board, figure):
                            computer_protected_figures += 1
                        if is_figure_in_corner(figure):
                            computer_figures_in_corner += 1
                        if is_figure_vulnerable(board, figure):
                            computer_vulnerable_figures += 1
    
    player_score = (regular_figure_weight * player_figures +
                    dama_weight * player_dama +
                    figure_in_back_row_weight * player_figures_in_back_row +
                    figure_in_middle_box_weight * player_figures_in_middle_box +
                    figure_in_middle_two_rows_weight * player_figures_in_middle_two_rows + 
                    protected_figure_weight * player_protected_figures + 
                    figure_in_corner_weight * player_figures_in_corner +
                    vulnerable_figure_weight * player_vulnerable_figures)

    computer_score = (regular_figure_weight * computer_figures +
                      dama_weight * computer_dama +
                      figure_in_back_row_weight * computer_figures_in_back_row +
                      figure_in_middle_box_weight * computer_figures_in_middle_box +
                      figure_in_middle_two_rows_weight * computer_figures_in_middle_two_rows + 
                      protected_figure_weight * computer_protected_figures + 
                      figure_in_corner_weight * computer_figures_in_corner +
                      vulnerable_figure_weight * computer_vulnerable_figures)

    return computer_score - player_score


# Funckija koja proverava da li je figura zasticena.
def is_protected(board, figure):
        row = figure.row
        col = figure.col
        if row < 7 and col < 7:
            right_corner = board.get_figure(row + 1, col + 1)
            left_corner = board.get_figure(row + 1, col - 1)
        else:
            return False
        if right_corner != 0 and right_corner.color == figure.color:
            return True
        if left_corner != 0 and left_corner.color == figure.color:
            return True
        return False


def is_figure_in_corner(figure):
    if (figure.row == 0 and figure.col == 0) or (figure.row == 0 and figure.col == 7) or (figure.row == 7 and figure.col == 0) or (figure.row == 7 and figure.col == 7):
        return True
    return False

def is_figure_vulnerable(board, figure):
    row = figure.row
    col = figure.col
    
    if figure.color == utilities.red:
        if row < 7 and col < 7 and row > 0 and col > 0:
            right_corner = board.get_figure(row + 1, col + 1)
            left_corner = board.get_figure(row + 1, col - 1)
        else:
            return False
        if right_corner == 0 or(right_corner.color == utilities.black):
            return True
        if left_corner == 0 or(left_corner.color == utilities.black):
            return True
    elif figure.color == utilities.black:
        if row > 0 and col > 0 and row < 7 and col < 7:
            right_corner = board.get_figure(row - 1, col + 1)
            left_corner = board.get_figure(row - 1, col - 1)
        else:
            return False
        if right_corner == 0 or(right_corner.color == utilities.red):
            return True
        if left_corner == 0 or(left_corner.color == utilities.red):
            return True
    return False

# Funkcija koja vraca sve moguce poteze za odredjenu boju.
def get_all_moves(board, color, game):
    moves = []
    if board != None:
        for row in range(utilities.rows):
            for col in range(utilities.cols):
                figure = board.get_figure(row, col)
                if figure != 0 and figure.color == color:
                    valid_moves = game.get_valid_moves(figure)

                    for move, skipped in valid_moves.items():
                        new_board = deepcopy(board)
                        new_figure = new_board.get_figure(row, col)
                        new_board1 = move_new(new_figure, move, skipped, new_board)
                    
                        moves.append(new_board1)
    return moves

def get_all_moves1(board, color, game):
    moves = []

    for piece in board.get_all_figures(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_figure(piece.row, piece.col)
            new_board = move_new(temp_piece, move, skip, temp_board)
            moves.append(new_board)
   
    return moves



# Funkcija koja doprema sledece stanje(tablu nakog odigranog poteza).
def move_new(figure, move, skipped, board):
    board.move_figure(figure, move[0], move[1])
    if skipped:
        board.remove(skipped)
    return board

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
    


def evaluate_depth(game):
    depth = 4

    if game.turn == utilities.black:
        if game.board.black_figures < 3:
            depth  = 6
        if game.board.black_figures < 4:
            depth = 5
        if len(get_all_moves(game.board, utilities.black, game)) < 5:
            depth = 6

    return depth