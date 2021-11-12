# from items.pawn import Pawn
import pygame
from items.board import Board
from items.player import Player
from settings import SIZE, CELL_SIZE, OFFSET, COORDINATES_WIDTH
pygame.font.init()


class Game:
    def __init__(self):
        # size of our game (to change: game_size, pawn_size, offset)
        self.game_size = SIZE
        self.cell_size = CELL_SIZE
        self.offset = OFFSET
        self.coordinates_width = COORDINATES_WIDTH

        self.win_width = self.game_size * self.cell_size + 2 * self.coordinates_width
        self.win_height = self.win_width + 2 * self.offset

        self.player1_turn = True
        self.selected = False
        self.selected_pos = None
        self.images = []

        # colors of our board (to change: color1, color2, color_map)
        self.board_color1 = (253, 228, 86)
        self.board_color2 = (0, 100, 255)
        self.color_map = (134, 184, 200)
        self.pawn_color1 = (255, 255, 255)
        self.pawn_color2 = (0, 0, 0)

        self.my_board = Board(self.game_size, self.cell_size, self.offset, self.coordinates_width,
                              self.board_color1, self.board_color2)

        self.player1 = Player('White', self.cell_size,
                              self.game_size, self.offset, self.coordinates_width, True)
        self.player2 = Player('Black', self.cell_size,
                              self.game_size, self.offset, self.coordinates_width, False)

    def show_names(self, win):
        fnt = pygame.font.SysFont('comicsans', 40)
        name1 = fnt.render(self.player1.name, True, self.pawn_color1)
        win.blit(name1, (self.win_width/2 - 60, self.offset/2 - 25))

        name2 = fnt.render(self.player2.name, True, self.pawn_color2)
        win.blit(name2, (self.win_width/2 - 60,
                 self.win_height - self.offset/2 - 25))

    def draw_2_middle(self, win, message_1, message_2):
        fnt = pygame.font.SysFont('comicsans', self.cell_size)
        win.fill(self.color_map)

        label_1 = fnt.render(message_1, True, self.pawn_color1)
        win.blit(label_1, ((self.win_width - label_1.get_width()) /
                 2, (self.win_height - label_1.get_height())/2-100))

        label_2 = fnt.render(message_2, True, self.pawn_color1)
        win.blit(label_2, ((self.win_width - label_2.get_width())/2,
                 (self.win_height - label_2.get_height())/2 + 100))

        pygame.display.update()
        pygame.time.delay(1500)

    def draw_starting_view(self, win):
        message_1 = "Let's play"
        message_2 = "CHECKERS!"
        self.draw_2_middle(win, message_1, message_2)

    def draw_ending_view(self, win):
        message_1 = "The winner is"
        if self.player1_turn:
            message_2 = self.player2.name
        else:
            message_2 = self.player1.name

        self.draw_2_middle(win, message_1, message_2)

    def draw_items(self, win):
        win.fill(self.color_map)
        self.my_board.draw_board(win)
        self.player1.draw_pawns(win, self.images)
        self.player2.draw_pawns(win, self.images)
        self.show_names(win)
        self.draw_player_turn(win)

    def draw_player_turn(self, win):
        radius = 10
        if self.player1_turn:
            draw_pos = ((self.game_size//2 + 1) * self.cell_size + self.coordinates_width,
                        self.offset // 2 + 5)
            pygame.draw.circle(win, self.pawn_color1, draw_pos, radius)
        elif not self.player1_turn:
            draw_pos = ((self.game_size//2 + 1) * self.cell_size + self.coordinates_width,
                        self.win_height - self.offset//2 + 5)
            pygame.draw.circle(win, self.pawn_color2, draw_pos, radius)

    def check_board_pos(self, pos: tuple):
        x, y = self.convert_to_board_pos(pos)

        if 0 <= x <= self.game_size-1 and 0 <= y <= self.game_size-1:
            return True
        return False

    def convert_to_board_pos(self, pos: tuple):
        x = (pos[0] - self.coordinates_width) // self.cell_size
        y = (pos[1] - self.offset - self.coordinates_width) // self.cell_size

        return (x, y)

    def check_collision(self, next_pos):
        """Checking collision between given position and any other pawn

        Args:
            next_pos (tuple): Given position to check collision

        Returns:
            bool: False if there is collision, otherwise True
        """
        for pawn in (self.player1.pawns + self.player2.pawns):
            if pawn.pos == next_pos:
                return False
        return True

    def pop_pawn(self, pawn, beated_pawn):
        if pawn.first_player:
            self.player2.pawns.remove(beated_pawn)
        else:
            self.player1.pawns.remove(beated_pawn)

    def after_move(self):
        self.selected_pos = None
        self.selected = False
        self.player1_turn = not self.player1_turn

    def after_beat(self, pawn):
        pawn.check_lady(self.game_size)
        pawn.selected()
        self.selected_pos = None
        self.selected = False
        self.player1_turn = not self.player1_turn

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

    def opponent_pawns(self, pawn):
        if pawn.first_player:
            return self.player2.pawns
        else:
            return self.player1.pawns

    def end_game(self):
        if self.player1_turn:
            pawns = self.player1.pawns
        else:
            pawns = self.player2.pawns

        for pawn in pawns:
            if pawn.first_player or pawn.lady:
                if self.check_collision((pawn.pos[0] + 1, pawn.pos[1] + 1)) and (pawn.pos[0] + 1 <= self.game_size-1) and (pawn.pos[1] + 1 < self.game_size):
                    return False
                if self.check_collision((pawn.pos[0] - 1, pawn.pos[1] + 1)) and (pawn.pos[0] - 1 >= 0) and (pawn.pos[1] + 1 < self.game_size):
                    return False
            if not pawn.first_player or pawn.lady:
                if self.check_collision((pawn.pos[0] + 1, pawn.pos[1] - 1)) and (pawn.pos[0] + 1 < self.game_size) and (pawn.pos[1] - 1 >= 0):
                    return False
                if self.check_collision((pawn.pos[0] - 1, pawn.pos[1] - 1)) and (pawn.pos[0] - 1 >= 0) and (pawn.pos[1] - 1 >= 0):
                    return False

        return True

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
                    if self.check_board_pos(pos):
                        for pawn in (self.player1.pawns + self.player2.pawns):
                            # Define check and uncheck
                            if pawn.pos == self.convert_to_board_pos(pos) and pawn.first_player == self.player1_turn:
                                if not self.selected:
                                    pawn.selected()
                                    self.selected_pos = pawn.pos
                                    self.selected = True
                                elif self.selected_pos == self.convert_to_board_pos(pos) and pawn.first_player == self.player1_turn:
                                    pawn.selected()
                                    self.selected_pos = None
                                    self.selected = False

                            if self.selected:
                                # Define next positions
                                right_down_pos = (
                                    self.selected_pos[0] + 1, self.selected_pos[1] + 1)
                                left_down_pos = (
                                    self.selected_pos[0] - 1, self.selected_pos[1] + 1)
                                right_up_pos = (
                                    self.selected_pos[0] + 1, self.selected_pos[1] - 1)
                                left_up_pos = (
                                    self.selected_pos[0] - 1, self.selected_pos[1] - 1)

                                # Define beating positions
                                right_down_beat = (
                                    self.selected_pos[0] + 2, self.selected_pos[1] + 2)
                                left_down_beat = (
                                    self.selected_pos[0] - 2, self.selected_pos[1] + 2)
                                right_up_beat = (
                                    self.selected_pos[0] + 2, self.selected_pos[1] - 2)
                                left_up_beat = (
                                    self.selected_pos[0] - 2, self.selected_pos[1] - 2)

                            # Define move
                            if self.selected and pawn.pos == self.selected_pos:
                                if self.check_collision(right_down_pos) and right_down_pos == self.convert_to_board_pos(pos) and (
                                        pawn.first_player or pawn.lady):
                                    pawn.move_right_down()
                                    self.after_move()
                                elif self.check_collision(left_down_pos) and left_down_pos == self.convert_to_board_pos(pos) and (
                                        pawn.first_player or pawn.lady):
                                    pawn.move_left_down()
                                    self.after_move()
                                elif self.check_collision(right_up_pos) and right_up_pos == self.convert_to_board_pos(pos) and (
                                        not pawn.first_player or pawn.lady):
                                    pawn.move_right_up()
                                    self.after_move()
                                elif self.check_collision(left_up_pos) and left_up_pos == self.convert_to_board_pos(pos) and (
                                        not pawn.first_player or pawn.lady):
                                    pawn.move_left_up()
                                    self.after_move()

                                # Define beat
                                for beated_pawn in self.opponent_pawns(pawn):
                                    if (right_down_pos == beated_pawn.pos) and (self.check_collision(right_down_beat)) and (
                                            right_down_beat == self.convert_to_board_pos(pos)) and (pawn.first_player or pawn.lady):
                                        self.beat_right_down(pawn, beated_pawn)
                                    elif (left_down_pos == beated_pawn.pos) and (self.check_collision(left_down_beat)) and (
                                            left_down_beat == self.convert_to_board_pos(pos)) and (pawn.first_player or pawn.lady):
                                        self.beat_left_down(pawn, beated_pawn)
                                    elif (right_up_pos == beated_pawn.pos) and (self.check_collision(right_up_beat)) and (
                                            right_up_beat == self.convert_to_board_pos(pos)) and (not pawn.first_player or pawn.lady):
                                        self.beat_right_up(pawn, beated_pawn)
                                    elif (left_up_pos == beated_pawn.pos) and (self.check_collision(left_up_beat)) and (
                                            left_up_beat == self.convert_to_board_pos(pos)) and (not pawn.first_player or pawn.lady):
                                        self.beat_left_up(pawn, beated_pawn)

            pygame.display.update()
            if self.end_game():
                self.draw_items(win)
                pygame.display.update()
                pygame.time.delay(1000)
                run = False
                self.draw_ending_view(win)

        pygame.display.quit()


if __name__ == '__main__':
    my_game = Game()
    my_game.play()
    pygame.quit()
