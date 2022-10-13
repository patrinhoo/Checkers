import pygame
from settings import SIZE, CELL_SIZE, OFFSET, COORDINATES_WIDTH


class Player:
    def __init__(self, name: str, first_player: bool):
        self.name = name
        self.first_player = first_player
        self.pawns = []

        if first_player:
            for i in range(SIZE):
                for j in range(int(SIZE/2) - 1):
                    if (i+j) % 2 == 1:
                        self.pawns.append(
                            Pawn((i, j), self.first_player))
        else:
            for i in range(SIZE):
                for j in range(int(SIZE/2) + 1, SIZE):
                    if (i+j) % 2 == 1:
                        self.pawns.append(
                            Pawn((i, j), self.first_player))

    def draw_pawns(self, win, images):
        for pawn in self.pawns:
            pawn.draw_pawn(win, images)


class Pawn:
    def __init__(self, pos: tuple, first_player: bool):
        self.pos = pos
        self.first_player = first_player
        self.clicked = False
        self.lady = False

    def draw_pawn(self, win, images):
        pawn_rect = pygame.Rect(
            self.pos[0] * CELL_SIZE + COORDINATES_WIDTH + 5, self.pos[1] * CELL_SIZE + OFFSET + COORDINATES_WIDTH + 5, CELL_SIZE-10, CELL_SIZE-10)
        if self.first_player and not self.lady and not self.clicked:
            win.blit(images[0], pawn_rect)
        elif not self.first_player and not self.lady and not self.clicked:
            win.blit(images[1], pawn_rect)
        elif self.first_player and self.lady and not self.clicked:
            win.blit(images[2], pawn_rect)
        elif not self.first_player and self.lady and not self.clicked:
            win.blit(images[3], pawn_rect)
        elif self.first_player and not self.lady and self.clicked:
            win.blit(images[4], pawn_rect)
        elif not self.first_player and not self.lady and self.clicked:
            win.blit(images[5], pawn_rect)
        elif self.first_player and self.lady and self.clicked:
            win.blit(images[6], pawn_rect)
        elif not self.first_player and self.lady and self.clicked:
            win.blit(images[7], pawn_rect)

    def check_lady(self):
        if self.first_player:
            if self.pos[1] == (SIZE-1):
                self.lady = True
        else:
            if self.pos[1] == 0:
                self.lady = True
