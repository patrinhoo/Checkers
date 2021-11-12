import pygame
from pygame import draw


class Board:
    def __init__(self, size: int, pawn_size: int, offset: int, coordinates_width,
                 color1, color2):
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.pawn_size = pawn_size
        self.offset = offset
        self.coordinates_width = coordinates_width
        self.coordinates_color1 = color1
        self.coordinates_color2 = color2
        self.letters = ['A', 'B', 'C', 'D', 'E',
                        'F', 'G', 'H', 'I', 'J', 'K', 'L']
        self.numbers = ['1', '2', '3', '4', '5',
                        '6', '7', '8', '9', '10', '11', '12']

    def draw_board(self, win):
        fnt = pygame.font.SysFont('comicsans', int(self.pawn_size/2))
        self.draw_cells(win, fnt)
        self.draw_coordinates(win, fnt)

    def draw_cells(self, win, fnt):
        # Draw board
        for i in range(self.size):
            for j in range(self.size):
                if (i+j) % 2 == 0:
                    pygame.draw.rect(win, self.color1, (j*self.pawn_size + self.coordinates_width, i *
                                     self.pawn_size + self.offset + self.coordinates_width, self.pawn_size, self.pawn_size))
                if (i+j) % 2 == 1:
                    pygame.draw.rect(win, self.color2, (j*self.pawn_size + self.coordinates_width, i *
                                     self.pawn_size + self.offset + self.coordinates_width, self.pawn_size, self.pawn_size))

    def draw_coordinates(self, win, fnt):
        # Draw coordinates
        for i in range(self.size):
            if i % 2 == 0:
                # Vertical coordinates
                pygame.draw.rect(win, self.coordinates_color2, (0, i*self.pawn_size +
                                 self.coordinates_width + self.offset, self.coordinates_width, self.pawn_size))
                pygame.draw.rect(win, self.coordinates_color1, (self.size * self.pawn_size + self.coordinates_width,
                                 i*self.pawn_size + self.coordinates_width + self.offset, self.coordinates_width, self.pawn_size))

                # Horizontal coordinates
                pygame.draw.rect(win, self.coordinates_color2, (self.coordinates_width +
                                 i*self.pawn_size, self.offset, self.pawn_size, self.coordinates_width))
                pygame.draw.rect(win, self.coordinates_color1, (self.coordinates_width + i*self.pawn_size, self.offset +
                                 self.size * self.pawn_size + self.coordinates_width, self.pawn_size, self.coordinates_width))

                # Numbers
                number = fnt.render(self.numbers[i], True,
                                    self.coordinates_color1)
                win.blit(number, (5, self.offset +
                         self.coordinates_width + i*self.pawn_size + 10))
                number = fnt.render(self.numbers[i], True,
                                    self.coordinates_color2)
                win.blit(number, (self.coordinates_width + self.size * self.pawn_size + 10, self.offset +
                         self.coordinates_width + i*self.pawn_size + 10))

                # Letters
                letter = fnt.render(self.letters[i], True,
                                    self.coordinates_color1)
                win.blit(letter, (self.coordinates_width +
                         i*self.pawn_size + int(self.pawn_size/3), self.offset - int(self.coordinates_width/4)))
                letter = fnt.render(self.letters[i], True,
                                    self.coordinates_color2)
                win.blit(letter, (self.coordinates_width +
                         i*self.pawn_size + int(self.pawn_size/3), self.offset + self.coordinates_width + self.size*self.pawn_size - int(self.coordinates_width/4)))

            else:
                # Vertical coordinates
                pygame.draw.rect(win, self.coordinates_color1, (0, i*self.pawn_size +
                                 self.coordinates_width + self.offset, self.coordinates_width, self.pawn_size))
                pygame.draw.rect(win, self.coordinates_color2, (self.size * self.pawn_size + self.coordinates_width,
                                 i*self.pawn_size + self.coordinates_width + self.offset, self.coordinates_width, self.pawn_size))

                # Horizontal coordinates
                pygame.draw.rect(win, self.coordinates_color1, (self.coordinates_width +
                                 i*self.pawn_size, self.offset, self.pawn_size, self.coordinates_width))
                pygame.draw.rect(win, self.coordinates_color2, (self.coordinates_width + i*self.pawn_size, self.offset +
                                 self.size * self.pawn_size + self.coordinates_width, self.pawn_size, self.coordinates_width))

                # Numbers
                number = fnt.render(self.numbers[i], True,
                                    self.coordinates_color2)
                win.blit(number, (5, self.offset +
                         self.coordinates_width + i*self.pawn_size + 10))
                number = fnt.render(self.numbers[i], True,
                                    self.coordinates_color1)
                win.blit(number, (self.coordinates_width + self.size * self.pawn_size + 10, self.offset +
                         self.coordinates_width + i*self.pawn_size + 10))

                # Letters
                letter = fnt.render(self.letters[i], True,
                                    self.coordinates_color2)
                win.blit(letter, (self.coordinates_width +
                         i*self.pawn_size + int(self.pawn_size/3), self.offset - int(self.coordinates_width/4)))
                letter = fnt.render(self.letters[i], True,
                                    self.coordinates_color1)
                win.blit(letter, (self.coordinates_width +
                         i*self.pawn_size + int(self.pawn_size/3), self.offset + self.coordinates_width + self.size*self.pawn_size - int(self.coordinates_width/4)))
