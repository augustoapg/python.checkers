import pygame
from .constants import BLACK, RED, ROWS, SQUARE_SIZE

class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            # it will only draw the red squares, and it will depend on which row it
            # currently is, making the alternating pattern
            for col in range(row % 2, ROWS, 2):
                # in pygame we start drawing from top left
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))