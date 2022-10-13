import pygame
from settings import SIZE, CELL_SIZE, OFFSET, COORDINATES_WIDTH


class Board:
    def __init__(self, color1, color2):
        self.color1 = color1
        self.color2 = color2
        self.coordinates_color1 = color1
        self.coordinates_color2 = color2
        self.letters = ['A', 'B', 'C', 'D', 'E',
                        'F', 'G', 'H', 'I', 'J', 'K', 'L']
        self.numbers = ['1', '2', '3', '4', '5',
                        '6', '7', '8', '9', '10', '11', '12']

    def draw_board(self, win):
        fnt = pygame.font.SysFont('comicsans', int(CELL_SIZE/2))
        self.draw_cells(win, fnt)
        self.draw_coordinates(win, fnt)

    def draw_cells(self, win, fnt):
        # Draw board
        for i in range(SIZE):
            for j in range(SIZE):
                if (i+j) % 2 == 0:
                    pygame.draw.rect(win, self.color1, (j*CELL_SIZE + COORDINATES_WIDTH, i *
                                     CELL_SIZE + OFFSET + COORDINATES_WIDTH, CELL_SIZE, CELL_SIZE))
                if (i+j) % 2 == 1:
                    pygame.draw.rect(win, self.color2, (j*CELL_SIZE + COORDINATES_WIDTH, i *
                                     CELL_SIZE + OFFSET + COORDINATES_WIDTH, CELL_SIZE, CELL_SIZE))

    def draw_coordinates(self, win, fnt):
        # Draw coordinates
        for i in range(SIZE):
            if i % 2 == 0:
                # Vertical coordinates
                pygame.draw.rect(win, self.coordinates_color2, (0, i*CELL_SIZE +
                                 COORDINATES_WIDTH + OFFSET, COORDINATES_WIDTH, CELL_SIZE))
                pygame.draw.rect(win, self.coordinates_color1, (SIZE * CELL_SIZE + COORDINATES_WIDTH,
                                 i*CELL_SIZE + COORDINATES_WIDTH + OFFSET, COORDINATES_WIDTH, CELL_SIZE))

                # Horizontal coordinates
                pygame.draw.rect(win, self.coordinates_color2, (COORDINATES_WIDTH +
                                 i*CELL_SIZE, OFFSET, CELL_SIZE, COORDINATES_WIDTH))
                pygame.draw.rect(win, self.coordinates_color1, (COORDINATES_WIDTH + i*CELL_SIZE, OFFSET +
                                 SIZE * CELL_SIZE + COORDINATES_WIDTH, CELL_SIZE, COORDINATES_WIDTH))

                # Numbers
                number = fnt.render(
                    self.numbers[i], True, self.coordinates_color1)
                win.blit(
                    number, (5, OFFSET + COORDINATES_WIDTH + i*CELL_SIZE + 10))
                number = fnt.render(
                    self.numbers[i], True, self.coordinates_color2)
                win.blit(number, (COORDINATES_WIDTH + SIZE * CELL_SIZE +
                         10, OFFSET + COORDINATES_WIDTH + i*CELL_SIZE + 10))

                # Letters
                letter = fnt.render(
                    self.letters[i], True, self.coordinates_color1)
                win.blit(letter, (COORDINATES_WIDTH + i*CELL_SIZE +
                         int(CELL_SIZE/3), OFFSET - int(COORDINATES_WIDTH/4)))
                letter = fnt.render(
                    self.letters[i], True, self.coordinates_color2)
                win.blit(letter, (COORDINATES_WIDTH + i*CELL_SIZE + int(CELL_SIZE/3),
                         OFFSET + COORDINATES_WIDTH + SIZE*CELL_SIZE - int(COORDINATES_WIDTH/4)))

            else:
                # Vertical coordinates
                pygame.draw.rect(win, self.coordinates_color1, (0, i*CELL_SIZE +
                                 COORDINATES_WIDTH + OFFSET, COORDINATES_WIDTH, CELL_SIZE))
                pygame.draw.rect(win, self.coordinates_color2, (SIZE * CELL_SIZE + COORDINATES_WIDTH,
                                 i*CELL_SIZE + COORDINATES_WIDTH + OFFSET, COORDINATES_WIDTH, CELL_SIZE))

                # Horizontal coordinates
                pygame.draw.rect(win, self.coordinates_color1, (COORDINATES_WIDTH +
                                 i*CELL_SIZE, OFFSET, CELL_SIZE, COORDINATES_WIDTH))
                pygame.draw.rect(win, self.coordinates_color2, (COORDINATES_WIDTH + i*CELL_SIZE, OFFSET +
                                 SIZE * CELL_SIZE + COORDINATES_WIDTH, CELL_SIZE, COORDINATES_WIDTH))

                # Numbers
                number = fnt.render(
                    self.numbers[i], True, self.coordinates_color2)
                win.blit(
                    number, (5, OFFSET + COORDINATES_WIDTH + i*CELL_SIZE + 10))
                number = fnt.render(
                    self.numbers[i], True, self.coordinates_color1)
                win.blit(number, (COORDINATES_WIDTH + SIZE * CELL_SIZE +
                         10, OFFSET + COORDINATES_WIDTH + i*CELL_SIZE + 10))

                # Letters
                letter = fnt.render(
                    self.letters[i], True, self.coordinates_color2)
                win.blit(letter, (COORDINATES_WIDTH + i*CELL_SIZE +
                         int(CELL_SIZE/3), OFFSET - int(COORDINATES_WIDTH/4)))
                letter = fnt.render(
                    self.letters[i], True, self.coordinates_color1)
                win.blit(letter, (COORDINATES_WIDTH + i*CELL_SIZE + int(CELL_SIZE/3),
                         OFFSET + COORDINATES_WIDTH + SIZE*CELL_SIZE - int(COORDINATES_WIDTH/4)))
