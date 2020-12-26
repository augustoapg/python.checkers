from .constants import WHITE, RED, SQUARE_SIZE, GREY, CROWN
import pygame

class Piece:
    PADDING = 18
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.radius = SQUARE_SIZE//2 - self.PADDING
        self.color = color
        self.king = False

        if self.color == RED:
            self.direction = -1
        else:
            self.direction = 1

        self.x = 0
        self.y = 0
        self.calc_pos()

    # calculate x/y position (of circle center) based on row/col
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, win):
        pygame.draw.circle(win, GREY, (self.x, self.y), self.radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

        if self.king:
            # blit is put image directly into the screen
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)
