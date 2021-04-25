import pygame
from .constants import BLACK, RED, WHITE, ROWS, COLS, SQUARE_SIZE
from .piece import Piece

class Board:
    def __init__(self):
        # 2d array, where each position is a row and each row has either a 0 when nothing is there
        # or it has a Piece object
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    # create internal representation of board with pieces
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
    
    def draw(self, win):
        self.draw_squares(win)
        
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                
                if piece != 0:
                    piece.draw(win)

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            # it will only draw the red squares, and it will depend on which row it
            # currently is, making the alternating pattern
            for col in range(row % 2, ROWS, 2):
                # in pygame we start drawing from top left
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        
        return pieces

    # update the internal list and calls move method in piece
    def move(self, piece, row, col):
        # swap positions
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()

            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1    

    

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0

            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1
    
    def winner(self):
        if self.red_left <= 0:
            return RED
        elif self.white_left <= 0:
            return WHITE
        
        return None

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))

        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
        
        return moves
    
    # start: row where we start checking (either -1 if moving up the board or +1 if moving down)
    # stop: row where we stop checking (either 2 rows away from start or board limit)
    # step: for loop step
    # color: piece color
    # left: where is the column to the left of this piece
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []

        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]

            # if empty square
            if current == 0:
                # if we skipped over something, we found a blank square
                # and we don't have anything we can skip again, we can't move there
                if skipped and not last:
                    break

                # double jump
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)

                    # do recursive call to see if we can move again
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped = last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped = last))
                
                break

            # if not empty and same color
            elif current.color == color:
                break

            # if not empty and different color
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []

        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]

            # if empty square
            if current == 0:
                # if we skipped over something, we found a blank square
                # and we don't have anything we can skip again, we can't move there
                if skipped and not last:
                    break

                # double jump
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)

                    # do recursive call to see if we can move again
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped = last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped = last))
                    
                break

            # if not empty and same color
            elif current.color == color:
                break

            # if not empty and different color
            else:
                last = [current]

            right += 1

        return moves
