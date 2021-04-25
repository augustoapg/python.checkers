import pygame
from .board import Board
from .constants import RED, SQUARE_SIZE, VALID_MOVE_COLOR, VALID_MOVE_RADIUS, WHITE, BLUE


class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def reset(self):
        self._init()

    # either move or select a piece
    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            
            # reset selection if move is not valid
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)

        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)

        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]

            if skipped:
                self.board.remove(skipped)

            self.change_turn()
        else:
            return False
        
        return True

    def change_turn(self):
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED
        
        self.valid_moves = {}

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            x = col * SQUARE_SIZE + SQUARE_SIZE//2
            y = row * SQUARE_SIZE + SQUARE_SIZE//2
            pygame.draw.circle(self.win, VALID_MOVE_COLOR, (x, y), VALID_MOVE_RADIUS)

    def winner(self):
        return self.board.winner()

    def get_board(self):
        return self.board

    # returns new board
    def ai_move(self, board):
        self.board = board
        self.change_turn()
