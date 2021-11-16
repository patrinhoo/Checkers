import pygame
from items.board import Board
from items.player import Player
from items.settings import SIZE, CELL_SIZE, OFFSET, COORDINATES_WIDTH
pygame.font.init()


class Game:
    def __init__(self):
        self.win_width = SIZE * CELL_SIZE + 2 * COORDINATES_WIDTH
        self.win_height = self.win_width + 2 * OFFSET

        self.player1_turn = True
        self.selected = False
        self.selected_pawn = None
        self.images = []
        self.multiple_beats = False

        # colors of our board (to change: color1, color2, color_map)
        self.board_color1 = (253, 228, 86)
        self.board_color2 = (0, 100, 255)
        self.color_map = (134, 184, 200)
        self.player1_color = (255, 255, 255)
        self.player2_color = (0, 0, 0)

        self.my_board = Board(self.board_color1, self.board_color2)

        self.player1 = Player('White', True)
        self.player2 = Player('Black', False)

# DRAWING
    def draw_items(self, win):
        win.fill(self.color_map)
        self.my_board.draw_board(win)
        self.player1.draw_pawns(win, self.images)
        self.player2.draw_pawns(win, self.images)
        self.show_names(win)
        self.draw_player_turn(win)
        if self.multiple_beats:
            self.draw_possible_beats(win)
        else:
            self.draw_possible_moves(win)

    def show_names(self, win):
        fnt = pygame.font.SysFont('comicsans', 40)
        name1 = fnt.render(self.player1.name, True, self.player1_color)
        win.blit(name1, (self.win_width/2 - 60, OFFSET/2 - 25))

        name2 = fnt.render(self.player2.name, True, self.player2_color)
        win.blit(name2, (self.win_width/2 - 60,
                 self.win_height - OFFSET/2 - 25))

    def draw_2_middle(self, win, message_1, message_2, color):
        fnt = pygame.font.SysFont('comicsans', CELL_SIZE)

        label_1 = fnt.render(message_1, True, color)
        win.blit(label_1, ((self.win_width - label_1.get_width()) /
                 2, (self.win_height - label_1.get_height())/2-100))

        label_2 = fnt.render(message_2, True, color)
        win.blit(label_2, ((self.win_width - label_2.get_width())/2,
                 (self.win_height - label_2.get_height())/2 + 100))

        pygame.display.update()
        pygame.time.delay(1500)

    def draw_starting_view(self, win):
        color = (255, 255, 255)
        message_1 = "Let's play"
        message_2 = "CHECKERS!"
        win.fill(self.color_map)
        self.draw_2_middle(win, message_1, message_2, color)
        message_3 = (self.player1.name).upper()
        message_4 = "starts"
        win.fill(self.color_map)
        self.draw_2_middle(win, message_3, message_4, color)

    def draw_ending_view(self, win):
        color = (0, 0, 0)
        self.draw_items(win)
        pygame.display.update()
        pygame.time.delay(1000)
        message_1 = "The winner is"
        if self.player1_turn:
            message_2 = self.player2.name
            color = (0, 0, 0)
        else:
            message_2 = self.player1.name
            color = (255, 255, 255)

        self.draw_2_middle(win, message_1, message_2, color)

    def draw_player_turn(self, win):
        radius = 10
        if self.player1_turn:
            draw_pos = ((SIZE//2 + 1) * CELL_SIZE + COORDINATES_WIDTH,
                        OFFSET // 2 + 5)
            pygame.draw.circle(win, self.player1_color, draw_pos, radius)
        elif not self.player1_turn:
            draw_pos = ((SIZE//2 + 1) * CELL_SIZE + COORDINATES_WIDTH,
                        self.win_height - OFFSET//2 + 5)
            pygame.draw.circle(win, self.player2_color, draw_pos, radius)

    def draw_possible_moves(self, win):
        if self.selected:
            moves = []
            beats = []
            color = (255, 0, 0)
            radius = 10

            opponent_pawns_pos = [pawn.pos for pawn in self.opponent_pawns()]

            moves.extend(self.move_positions(self.selected_pawn.pos))
            for move in moves[:2]:
                if self.check_board_pos(move) and self.check_empty(move) and (self.player1_turn or self.selected_pawn.lady):
                    draw_pos = (COORDINATES_WIDTH + move[0] * CELL_SIZE + CELL_SIZE//2,
                                OFFSET + COORDINATES_WIDTH + move[1] * CELL_SIZE + CELL_SIZE//2)
                    pygame.draw.circle(win, color, draw_pos, radius)

            for move in moves[2:]:
                if self.check_board_pos(move) and self.check_empty(move) and (not self.player1_turn or self.selected_pawn.lady):
                    draw_pos = (COORDINATES_WIDTH + move[0] * CELL_SIZE + CELL_SIZE//2,
                                OFFSET + COORDINATES_WIDTH + move[1] * CELL_SIZE + CELL_SIZE//2)
                    pygame.draw.circle(win, color, draw_pos, radius)

            beats.extend(self.beat_positions(self.selected_pawn.pos))
            for nr, beat in enumerate(beats[:2]):
                if self.check_board_pos(beat) and self.check_empty(beat) and (moves[nr] in opponent_pawns_pos) and (self.player1_turn or self.selected_pawn.lady) and not self.multiple_beats:
                    draw_pos = (COORDINATES_WIDTH + beat[0] * CELL_SIZE + CELL_SIZE//2,
                                OFFSET + COORDINATES_WIDTH + beat[1] * CELL_SIZE + CELL_SIZE//2)
                    pygame.draw.circle(win, color, draw_pos, radius)

            for nr, beat in enumerate(beats[2:], 2):
                if self.check_board_pos(beat) and self.check_empty(beat) and (moves[nr] in opponent_pawns_pos) and (not self.player1_turn or self.selected_pawn.lady) and not self.multiple_beats:
                    draw_pos = (COORDINATES_WIDTH + beat[0] * CELL_SIZE + CELL_SIZE//2,
                                OFFSET + COORDINATES_WIDTH + beat[1] * CELL_SIZE + CELL_SIZE//2)
                    pygame.draw.circle(win, color, draw_pos, radius)

    def draw_possible_beats(self, win):
        if self.selected:
            moves = []
            beats = []
            color = (255, 0, 0)
            radius = 10

            opponent_pawns_pos = [pawn.pos for pawn in self.opponent_pawns()]
            moves.extend(self.move_positions(self.selected_pawn.pos))
            beats.extend(self.beat_positions(self.selected_pawn.pos))

            for nr, beat in enumerate(beats[:2]):
                if self.check_board_pos(beat) and self.check_empty(beat) and (moves[nr] in opponent_pawns_pos) and (self.player1_turn or self.selected_pawn.lady):
                    draw_pos = (COORDINATES_WIDTH + beat[0] * CELL_SIZE + CELL_SIZE//2,
                                OFFSET + COORDINATES_WIDTH + beat[1] * CELL_SIZE + CELL_SIZE//2)
                    pygame.draw.circle(win, color, draw_pos, radius)

            for nr, beat in enumerate(beats[2:], 2):
                if self.check_board_pos(beat) and self.check_empty(beat) and (moves[nr] in opponent_pawns_pos) and (not self.player1_turn or self.selected_pawn.lady):
                    draw_pos = (COORDINATES_WIDTH + beat[0] * CELL_SIZE + CELL_SIZE//2,
                                OFFSET + COORDINATES_WIDTH + beat[1] * CELL_SIZE + CELL_SIZE//2)
                    pygame.draw.circle(win, color, draw_pos, radius)


# MOVES

    def check_board_pos(self, pos: tuple):
        x, y = pos
        if 0 <= x < SIZE and 0 <= y < SIZE:
            return True
        return False

    def convert_to_board_pos(self, pos: tuple):
        x = (pos[0] - COORDINATES_WIDTH) // CELL_SIZE
        y = (pos[1] - OFFSET - COORDINATES_WIDTH) // CELL_SIZE

        return (x, y)

    def check_empty(self, next_pos):
        for pawn in (self.player1.pawns + self.player2.pawns):
            if pawn.pos == next_pos:
                return False
        return True

    def move_right_down(self, pawn):
        pawn.pos = (pawn.pos[0] + 1, pawn.pos[1] + 1)
        self.after_move(pawn)

    def move_right_up(self, pawn):
        pawn.pos = (pawn.pos[0] + 1, pawn.pos[1] - 1)
        self.after_move(pawn)

    def move_left_down(self, pawn):
        pawn.pos = (pawn.pos[0] - 1, pawn.pos[1] + 1)
        self.after_move(pawn)

    def move_left_up(self, pawn):
        pawn.pos = (pawn.pos[0] - 1, pawn.pos[1] - 1)
        self.after_move(pawn)

    def select_pawn(self, pawn):
        if pawn.clicked:
            pawn.clicked = False
            self.selected_pawn = None
            self.selected = False
            if self.multiple_beats:
                self.multiple_beats = False
                self.player1_turn = not self.player1_turn
        else:
            pawn.clicked = True
            self.selected_pawn = pawn
            self.selected = True

    def after_move(self, pawn):
        pawn.check_lady()
        self.select_pawn(pawn)
        self.player1_turn = not self.player1_turn

    def after_beat(self, pawn):
        self.selected_pawn = pawn
        if not self.check_next_beat(pawn):
            self.multiple_beats = False
            self.after_move(pawn)

    def check_next_beat(self, pawn):
        right_down_pos, left_down_pos, right_up_pos, left_up_pos = self.move_positions(
            pawn.pos)
        right_down_beat, left_down_beat, right_up_beat, left_up_beat = self.beat_positions(
            pawn.pos)

        for beated_pawn in self.opponent_pawns():
            if pawn.first_player or pawn.lady:
                if self.check_empty((right_down_beat)) and self.check_board_pos((right_down_beat)) and ((right_down_pos) == beated_pawn.pos):
                    self.multiple_beats = True
                    return True
                if self.check_empty((left_down_beat)) and self.check_board_pos((left_down_beat)) and ((left_down_pos) == beated_pawn.pos):
                    self.multiple_beats = True
                    return True
            if not pawn.first_player or pawn.lady:
                if self.check_empty((right_up_beat)) and self.check_board_pos((right_up_beat)) and ((right_up_pos) == beated_pawn.pos):
                    self.multiple_beats = True
                    return True
                if self.check_empty((left_up_beat)) and self.check_board_pos((left_up_beat)) and ((left_up_pos) == beated_pawn.pos):
                    self.multiple_beats = True
                    return True

        return False

    def beat_right_down(self, pawn, beated_pawn):
        self.pop_pawn(pawn, beated_pawn)
        pawn.pos = (pawn.pos[0] + 2, pawn.pos[1] + 2)
        self.after_beat(pawn)

    def beat_right_up(self, pawn, beated_pawn):
        self.pop_pawn(pawn, beated_pawn)
        pawn.pos = (pawn.pos[0] + 2, pawn.pos[1] - 2)
        self.after_beat(pawn)

    def beat_left_down(self, pawn, beated_pawn):
        self.pop_pawn(pawn, beated_pawn)
        pawn.pos = (pawn.pos[0] - 2, pawn.pos[1] + 2)
        self.after_beat(pawn)

    def beat_left_up(self, pawn, beated_pawn):
        self.pop_pawn(pawn, beated_pawn)
        pawn.pos = (pawn.pos[0] - 2, pawn.pos[1] - 2)
        self.after_beat(pawn)

    def pop_pawn(self, pawn, beated_pawn):
        if pawn.first_player:
            self.player2.pawns.remove(beated_pawn)
        else:
            self.player1.pawns.remove(beated_pawn)

    def move_positions(self, pos):
        right_down_pos = (pos[0] + 1, pos[1] + 1)
        left_down_pos = (pos[0] - 1, pos[1] + 1)
        right_up_pos = (pos[0] + 1, pos[1] - 1)
        left_up_pos = (pos[0] - 1, pos[1] - 1)

        return right_down_pos, left_down_pos, right_up_pos, left_up_pos

    def beat_positions(self, pos):
        right_down_beat = (pos[0] + 2, pos[1] + 2)
        left_down_beat = (pos[0] - 2, pos[1] + 2)
        right_up_beat = (pos[0] + 2, pos[1] - 2)
        left_up_beat = (pos[0] - 2, pos[1] - 2)

        return right_down_beat, left_down_beat, right_up_beat, left_up_beat

# END GAME
    def check_end_game(self):
        if self.player1_turn:
            pawns = self.player1.pawns
        else:
            pawns = self.player2.pawns

        for pawn in pawns:
            # Define move and beat positions
            right_down_pos, left_down_pos, right_up_pos, left_up_pos = self.move_positions(
                pawn.pos)
            right_down_beat, left_down_beat, right_up_beat, left_up_beat = self.beat_positions(
                pawn.pos)

            # False if found any move
            if pawn.first_player or pawn.lady:
                if self.check_empty((right_down_pos)) and self.check_board_pos((right_down_pos)):
                    return False
                if self.check_empty((left_down_pos)) and self.check_board_pos((left_down_pos)):
                    return False
            if not pawn.first_player or pawn.lady:
                if self.check_empty((right_up_pos)) and self.check_board_pos((right_up_pos)):
                    return False
                if self.check_empty((left_up_pos)) and self.check_board_pos((left_up_pos)):
                    return False
            # False if found any beat
            for beated_pawn in self.opponent_pawns():
                if pawn.first_player or pawn.lady:
                    if self.check_empty((right_down_beat)) and self.check_board_pos((right_down_beat)) and ((right_down_pos) == beated_pawn.pos):
                        return False
                    if self.check_empty((left_down_beat)) and self.check_board_pos((left_down_beat)) and ((left_down_pos) == beated_pawn.pos):
                        return False
                if not pawn.first_player or pawn.lady:
                    if self.check_empty((right_up_beat)) and self.check_board_pos((right_up_beat)) and ((right_up_pos) == beated_pawn.pos):
                        return False
                    if self.check_empty((left_up_beat)) and self.check_board_pos((left_up_beat)) and ((left_up_pos) == beated_pawn.pos):
                        return False
        # Otherwise True
        return True

    def opponent_pawns(self):
        if self.player1_turn:
            return self.player2.pawns
        else:
            return self.player1.pawns

# GAME
    def play(self):
        win = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption('Checkers')
        run = True
        self.draw_starting_view(win)

        pawn1 = pygame.image.load('png/pawn1.png').convert_alpha()
        pawn2 = pygame.image.load('png/pawn2.png').convert_alpha()
        lady1 = pygame.image.load('png/lady1.png').convert_alpha()
        lady2 = pygame.image.load('png/lady2.png').convert_alpha()

        pawn1_selected = pygame.image.load(
            'png/pawn1_selected.png').convert_alpha()
        pawn2_selected = pygame.image.load(
            'png/pawn2_selected.png').convert_alpha()
        lady1_selected = pygame.image.load(
            'png/lady1_selected.png').convert_alpha()
        lady2_selected = pygame.image.load(
            'png/lady2_selected.png').convert_alpha()

        self.images.extend([pawn1, pawn2, lady1, lady2, pawn1_selected,
                           pawn2_selected, lady1_selected, lady2_selected])

        # MAIN GAME LOOP
        while run:
            self.draw_items(win)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    clicked_pos = self.convert_to_board_pos(pos)
                    if self.check_board_pos(clicked_pos):
                        for pawn in (self.player1.pawns + self.player2.pawns):
                            # Define check and uncheck
                            if pawn.pos == clicked_pos and pawn.first_player == self.player1_turn:
                                if not self.selected:
                                    self.select_pawn(pawn)
                                elif self.selected_pawn.pos == clicked_pos and pawn.first_player == self.player1_turn:
                                    self.select_pawn(pawn)

                            # Define moves
                            if self.selected and pawn.pos == self.selected_pawn.pos:

                                # Define next positions
                                right_down_pos, left_down_pos, right_up_pos, left_up_pos = self.move_positions(
                                    self.selected_pawn.pos)
                                # Define beating positions
                                right_down_beat, left_down_beat, right_up_beat, left_up_beat = self.beat_positions(
                                    self.selected_pawn.pos)

                                # Define move
                                if self.check_empty(right_down_pos) and right_down_pos == clicked_pos and (
                                        pawn.first_player or pawn.lady) and not self.multiple_beats:
                                    self.move_right_down(pawn)

                                elif self.check_empty(left_down_pos) and left_down_pos == clicked_pos and (
                                        pawn.first_player or pawn.lady) and not self.multiple_beats:
                                    self.move_left_down(pawn)

                                elif self.check_empty(right_up_pos) and right_up_pos == clicked_pos and (
                                        not pawn.first_player or pawn.lady) and not self.multiple_beats:
                                    self.move_right_up(pawn)

                                elif self.check_empty(left_up_pos) and left_up_pos == clicked_pos and (
                                        not pawn.first_player or pawn.lady) and not self.multiple_beats:
                                    self.move_left_up(pawn)

                                # Define beat
                                for beated_pawn in self.opponent_pawns():
                                    if (right_down_pos == beated_pawn.pos) and (self.check_empty(right_down_beat)) and (
                                            right_down_beat == clicked_pos) and (pawn.first_player or pawn.lady):
                                        self.beat_right_down(pawn, beated_pawn)

                                    elif (left_down_pos == beated_pawn.pos) and (self.check_empty(left_down_beat)) and (
                                            left_down_beat == clicked_pos) and (pawn.first_player or pawn.lady):
                                        self.beat_left_down(pawn, beated_pawn)

                                    elif (right_up_pos == beated_pawn.pos) and (self.check_empty(right_up_beat)) and (
                                            right_up_beat == clicked_pos) and (not pawn.first_player or pawn.lady):
                                        self.beat_right_up(pawn, beated_pawn)

                                    elif (left_up_pos == beated_pawn.pos) and (self.check_empty(left_up_beat)) and (
                                            left_up_beat == clicked_pos) and (not pawn.first_player or pawn.lady):
                                        self.beat_left_up(pawn, beated_pawn)

            pygame.display.update()
            if self.check_end_game():
                run = False
                self.draw_ending_view(win)

        pygame.display.quit()
        pygame.quit()


if __name__ == '__main__':
    my_game = Game()
    my_game.play()
