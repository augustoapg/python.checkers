from copy import deepcopy
import pygame

RED = (255, 0, 0)
WHITE = (255, 255, 255)

# position: current board object. Where we are, what is our current position
# depth: how far will this tree go
# max_player: boolean that says if we're minimizing or maximizing the value
# game: game object
def minimax(position, depth, max_player, game):
    # if depth is 0 then it is time to make the evaluation
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position

    if max_player:
        maxEval = float('-inf')
        best_move = None

        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth-1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None

        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move

        return minEval, best_move

def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board

def get_all_moves(board, color, game):
    # 2d list, where each item is contains a new_board and a piece object, representing
    # what the board would look like if we move that piece
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)

        # move is the row and column, and skip is a list of pieces that were eaten
        for move, skip in valid_moves.items():
            # draw_moves(game, board, piece) #! uncomment to show AI considering its moves
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)

    return moves

def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)

    # draw a green circle to show possible moves
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    pygame.time.delay(100)
