import pygame


class Player:
    def __init__(self, name: str, cell_size: int, board_size: int, offset: int, coordinates_width: int,
                 first_player: bool):
        self.name = name
        # Size of one cell
        self.cell_size = cell_size
        # Size of single pawn
        self.pawn_size = cell_size - 10
        # Board size (e.g. 8x8 for board_size=8)
        self.board_size = board_size
        # Offset of board from top and bottom of the window
        self.offset = offset
        # Coordinates width
        self.coordinates_width = coordinates_width

        self.first_player = first_player
        self.pawns = []

        if first_player:
            for i in range(self.board_size):
                for j in range(int(self.board_size/2) - 1):
                    if (i+j) % 2 == 1:
                        self.pawns.append(
                            Pawn(self.pawn_size, self.cell_size, self.offset, self.coordinates_width, (i, j), self.first_player, self.board_size))
        else:
            for i in range(self.board_size):
                for j in range(int(self.board_size/2) + 1, self.board_size):
                    if (i+j) % 2 == 1:
                        self.pawns.append(
                            Pawn(self.pawn_size, self.cell_size, self.offset, self.coordinates_width, (i, j), self.first_player, self.board_size))

    def draw_pawns(self, win, images):

        for pawn in self.pawns:
            pawn.draw_pawn(win, images)


class Pawn:
    def __init__(self, size: int, cell_size: int, offset: int, coordinates_width: int, pos: tuple, first_player: bool, board_size: int):
        self.radius = size/2
        self.pos = pos
        self.cell_size = cell_size
        self.offset = offset
        self.first_player = first_player
        self.clicked = False
        self.lady = False
        self.board_size = board_size
        self.coordinates_width = coordinates_width

    def draw_pawn(self, win, images):
        pawn_rect = pygame.Rect(
            self.pos[0] * self.cell_size + self.coordinates_width + 5, self.pos[1] * self.cell_size + self.offset + self.coordinates_width + 5, self.cell_size-10, self.cell_size-10)
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

    def move_right_down(self):
        self.pos = (self.pos[0] + 1, self.pos[1] + 1)
        self.check_lady(self.board_size)
        self.selected()

    def move_right_up(self):
        self.pos = (self.pos[0] + 1, self.pos[1] - 1)
        self.check_lady(self.board_size)
        self.selected()

    def move_left_down(self):
        self.pos = (self.pos[0] - 1, self.pos[1] + 1)
        self.check_lady(self.board_size)
        self.selected()

    def move_left_up(self):
        self.pos = (self.pos[0] - 1, self.pos[1] - 1)
        self.check_lady(self.board_size)
        self.selected()

    def selected(self):
        if self.clicked:
            self.clicked = False
        else:
            self.clicked = True

    def check_lady(self, board_size):
        if self.first_player:
            if self.pos[1] == (board_size-1):
                self.lady = True
        else:
            if self.pos[1] == 0:
                self.lady = True
