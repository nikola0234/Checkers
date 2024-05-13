import utilities
from tree import Node
from copy import deepcopy

def minimax(board, depth, max_player, game, alpha, beta):
    if depth == 0 or game.get_winner() is not None:
        return evaluate_current_board(board), None

    if max_player:
        max_eval = float("-inf")
        best_move = None
        for move in get_all_moves(board, utilities.black, game):
            evaluation, _ = minimax(move, depth - 1, False, game, alpha, beta)
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break  
        return max_eval, best_move
    else:
        min_eval = float("inf")
        best_move = None
        for move in get_all_moves(board, utilities.red, game):
            evaluation, _ = minimax(move, depth - 1, True, game, alpha, beta)
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break  
        return min_eval, best_move

def evaluate_current_board(board):
    return board.black_figures - board.red_figures + (board.black_dame * 0.5 - board.red_dame * 0.5) 

# def minimax_alpha_beta(node, depth, alfa, beta, maxPlayer, game):
#     if depth == 0 or game.get_winner != 0:
#         return game.evaluete_current_board(), None
    
#     possible_moves = get_all_moves(game.board )
    


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

def move_new(figure, move, skipped, board):
    board.move_figure(figure, move[0], move[1])
    if skipped:
        board.remove(skipped)
    return board

def build_boards_tree(board, color, game, node, depth):
    if depth == 0 or game.get_winner() != None:
        return
    
    node.children = get_all_moves(board, color, game)
    if color == utilities.black:
        for child in node.children:
            build_boards_tree(child, utilities.red, game, node, depth - 1)
    else:
        for child in node.children:
            build_boards_tree(child, utilities.black, game, node, depth - 1)