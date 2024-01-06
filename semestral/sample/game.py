""" File that represets implementation of game itself. """


import pygame
import sys
import math
import time

from enumerator import Colors, GameStatus, Status
from player import Player
from enemies import Vertical, Horizontal, Follower
from exceptions import WrongPlayersAmount


class Game:
    my_screen = ...
    width = ...
    height = ...
    clock = ...
    view_distance = ...
    size = ...
    vector = ...
    FPS = ...
    player_freq = ...
    monster_freq = ...
    player = ...
    exit = ...
    game_status = ...
    keys = ...
    game_map = ...
    entities = ...

    def __init__(self, settings_path, screen, map_path):
        self.game_map = []
        self.entities = []
        self.keys = [False, False, False]
        self.my_screen = screen
        self.game_status = GameStatus.PROCESSING
        self.clock = pygame.time.Clock()
        with open(map_path, 'r') as f:
            for line in f.readlines():
                row = [i for i in line][:-1]
                self.game_map.append(row)

        with open(settings_path, 'r') as f:
            self.size = int(next(f))
            self.view_distance = int(next(f))
            self.FPS = int(next(f))
            self.player_freq = self.FPS // int(next(f))
            self.monster_freq = self.FPS // int(next(f))

        self.height = len(self.game_map)
        self.width = len(self.game_map[0])
        player = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.game_map[i][j] == '@':
                    player += 1
                    self.game_map[i][j] = ' '
                    self.player = Player((i, j), 1, Colors.GREEN.value)
                    self.vector = ((self.my_screen.screen.get_size()[1] // 2 - i * self.size),
                                   (self.my_screen.screen.get_size()[0] // 2 - j * self.size))
                elif self.game_map[i][j] == 'V':
                    self.game_map[i][j] = ' '
                    self.entities.append(Vertical((i, j), 1, Colors.RED.value))
                elif self.game_map[i][j] == 'H':
                    self.game_map[i][j] = ' '
                    self.entities.append(Horizontal((i, j), 1, Colors.RED.value))
                elif self.game_map[i][j] == 'R':
                    self.game_map[i][j] = ' '
                    self.entities.append(Follower((i, j), 1, Colors.RED.value))
        if player != 1:
            raise WrongPlayersAmount(f'Wrong amount of players on the map. Check if file {map_path} is not damaged.')

    def draw_key(self, i, j, color, coords=False):
        if not coords:
            pygame.draw.polygon(self.my_screen.screen, color, [((j + 0.2) * self.size + self.vector[1], (i + 0.4) * self.size + self.vector[0]),
                                                               ((j + 0.7) * self.size + self.vector[1], (i + 0.4) * self.size + self.vector[0]),
                                                               ((j + 0.7) * self.size + self.vector[1], (i + 0.5) * self.size + self.vector[0]),
                                                               ((j + 0.4) * self.size + self.vector[1], (i + 0.5) * self.size + self.vector[0]),
                                                               ((j + 0.4) * self.size + self.vector[1], (i + 0.6) * self.size + self.vector[0]),
                                                               ((j + 0.2) * self.size + self.vector[1], (i + 0.6) * self.size + self.vector[0])]
                                )
        else:
            pygame.draw.polygon(self.my_screen.screen, color, [((j + 0.2 * self.size), (i + 0.4 * self.size)),
                                                               ((j + 0.7 * self.size), (i + 0.4 * self.size)),
                                                               ((j + 0.7 * self.size), (i + 0.5 * self.size)),
                                                               ((j + 0.4 * self.size), (i + 0.5 * self.size)),
                                                               ((j + 0.4 * self.size), (i + 0.6 * self.size)),
                                                               ((j + 0.2 * self.size), (i + 0.6 * self.size))]
                                )

    def draw_door(self, i, j, color):
        rect = pygame.Rect(j * self.size + self.vector[1],
                           i * self.size + self.vector[0], self.size, self.size)
        rect1 = pygame.Rect((j + 0.7) * self.size + self.vector[1],
                            (i + 0.4) * self.size + self.vector[0], self.size // 5, self.size // 5)
        pygame.draw.rect(self.my_screen.screen, color, rect)
        pygame.draw.rect(self.my_screen.screen, Colors.BLACK.value, rect1)

    def vector_update(self, difference):
        self.vector = (self.vector[0] + difference[0] * self.size,
                       self.vector[1] + difference[1] * self.size)

    def draw_map(self):
        for i in range(self.height):
            for j in range(self.width):
                symb = self.game_map[i][j]
                distance = math.sqrt((self.player.pos[0] - i) ** 2 + (self.player.pos[1] - j) ** 2)
                if distance <= self.view_distance:

                    rect = pygame.Rect(j * self.size + self.vector[1],
                                       i * self.size + self.vector[0], self.size, self.size)

                    if symb == '#':
                        pygame.draw.rect(self.my_screen.screen, Colors.WHITE.value, rect)
                    elif symb == 'E':
                        self.draw_door(i, j, Colors.BROWN.value)
                    elif symb in ['B', 'P', 'Y', 'y', 'b', 'p']:
                        for Color, color, color_enum in [('P', 'p', Colors.PURPLE.value),
                                                         ('B', 'b', Colors.BLUE.value),
                                                         ('Y', 'y', Colors.YELLOW.value)]:
                            if symb == Color:
                                self.draw_door(i, j, color_enum)
                            elif symb == color:
                                self.draw_key(i, j, color_enum)

    def draw_inventory(self):
        k = 0
        for i, color in [(1 * (self.size // 2), Colors.PURPLE.value),
                         (6 * (self.size // 2), Colors.BLUE.value),
                         (11 * (self.size // 2), Colors.YELLOW.value)]:
            rect = pygame.Rect(i,
                               self.my_screen.screen.get_size()[1] - self.size * 2 - self.size // 2,
                               self.size * 2, self.size * 2)
            rect1 = pygame.Rect(i + 3,
                                self.my_screen.screen.get_size()[1] - self.size * 2 - self.size // 2 + 3,
                                self.size * 2 - 6, self.size * 2 - 6)
            pygame.draw.rect(self.my_screen.screen, Colors.WHITE.value, rect)
            pygame.draw.rect(self.my_screen.screen, Colors.BLACK.value, rect1)
            
            if self.keys[k] == True:
                self.draw_key(self.my_screen.screen.get_size()[1] - self.size * 2 - self.size // 2 + 3 + 15,
                              i + 15,
                              color,
                              True)
            k += 1

    def end_game(self):
        if self.game_status == GameStatus.EXIT:
            return Status.MENU
        elif self.game_status == GameStatus.WIN:
            self.my_screen.screen.fill(Colors.BLACK.value)
            self.my_screen.draw_text("You won! Congratulations", pygame.font.Font(None, 60), Colors.WHITE.value, self.my_screen.width // 2, self.my_screen.height // 2)
            pygame.display.flip()
            time.sleep(3)
            return Status.MENU
        elif self.game_status == GameStatus.LOSE:
            time.sleep(2)
            self.my_screen.screen.fill(Colors.BLACK.value)
            self.my_screen.draw_text("You lost :( Better luck next time!", pygame.font.Font(None, 60), Colors.WHITE.value, self.my_screen.width // 2, self.my_screen.height // 2)
            pygame.display.flip()
            time.sleep(3)
            return Status.MENU

    def game_loop(self):
        counter = 0
        while self.game_status == GameStatus.PROCESSING:
            counter = (counter + 1) % self.FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.my_screen.screen.fill(Colors.BLACK.value)
            self.draw_map()
            self.draw_inventory()

            if counter % self.player_freq == 1:
                self.game_status, difference = self.player.move(self.game_map, self.keys)
                self.vector_update(difference)
                for enemy in self.entities:
                    if self.player.pos == enemy.pos:
                        self.game_status = GameStatus.LOSE
                        break

            if self.game_status == GameStatus.PROCESSING and counter % self.monster_freq == 1:
                for entity in self.entities:
                    game_status = entity.move(self.game_map, self.player.pos)
                    if game_status == GameStatus.LOSE:
                        self.game_status = GameStatus.LOSE
                        break

            self.player.draw(self.my_screen, self.size, self.my_screen.screen.get_size())
            for entity in self.entities:
                entity.draw(self.my_screen, self.size, self.vector, self.player.pos, self.view_distance)

            pygame.display.flip()
            self.clock.tick(self.FPS)

        self.my_screen.screen.fill(Colors.BLACK.value)
        self.draw_map()
        self.player.draw(self.my_screen, self.size, self.my_screen.screen.get_size())
        for entity in self.entities:
            entity.draw(self.my_screen, self.size, self.vector, self.player.pos, self.view_distance)
        pygame.display.flip()
        self.clock.tick(self.FPS)
        return self.end_game()


assert (__name__ != "__main__")
