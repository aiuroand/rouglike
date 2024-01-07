""" File that represets implementation of game itself. """


import pygame
import sys
import math
import time

from enumerator import Colors, GameStatus, Status
from player import Player
from enemies import Vertical, Horizontal, Follower
from check_map import check_map
from window import Window


class Game:
    """Class that represents game itself.

    Arguments:
        my_screen (Window): user-made wrapper for pygame.display.
        width (int): width of the map in cells.
        height (int): height of the ma in cells.
        clock (pygame.time.Clock): helping arguments that represents clocks for cicle.
        view_distance (int): view distance of player in cells.
        FPS (int): frequency of gain game loop updated.
        size (int): reference size of one wall in pixels.
        vector (tuple): translation vector to draw map relative to the window center.
        player_freq (int): frequency for player speed. Final speed is calculated as FPS / player_freq.
        monster_freq (int): frequency for enemies speed. Final speed is calculated as FPS / monster_freq.
        game_status (Status): current game status that controls game loop and represents if player won or lost.
        keys (list): list of onformation about 3 keys.
        game_map (list): game par represented as 2D array.
        player (Player): player.
        entities (list): monsters and other entities.
    """
    my_screen: Window
    width: int
    height: int
    clock: pygame.time.Clock
    view_distance: int
    FPS: int
    size: int
    vector: tuple
    player_freq: int
    monster_freq: int
    game_status: Status
    keys: list
    game_map: list
    player: Player
    entities: list

    def __init__(self, settings_path: str, screen: Window, map_path: str):
        """Game constructor

        Args:
            settings_path (str): file that contains game configuration.
            screen (Window): user-made Window.
            map_path (str): file that contains map folder.
        """
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

        check_map(self.game_map, map_path)

        with open(settings_path, 'r') as f:
            self.size = int(next(f))
            self.view_distance = int(next(f))
            self.FPS = int(next(f))
            self.player_freq = self.FPS // int(next(f))
            self.monster_freq = self.FPS // int(next(f))

        self.height = len(self.game_map)
        self.width = len(self.game_map[0])
        for i in range(self.height):
            for j in range(self.width):
                if self.game_map[i][j] == '@':
                    self.game_map[i][j] = ' '
                    self.player = Player((i, j), Colors.GREEN.value)
                    self.vector = ((self.my_screen.screen.get_size()[1] // 2 - i * self.size),
                                   (self.my_screen.screen.get_size()[0] // 2 - j * self.size))
                elif self.game_map[i][j] == 'V':
                    self.game_map[i][j] = ' '
                    self.entities.append(Vertical((i, j), Colors.RED.value))
                elif self.game_map[i][j] == 'H':
                    self.game_map[i][j] = ' '
                    self.entities.append(Horizontal((i, j), Colors.RED.value))
                elif self.game_map[i][j] == 'R':
                    self.game_map[i][j] = ' '
                    self.entities.append(Follower((i, j), Colors.RED.value))

    def draw_key(self, i: int, j: int, color: tuple, coords: bool = False) -> None:
        """Draws key of given color on given position.

        Args:
            i (int): height position.
            j (int): width position.
            color (tuple): color in RGB format.
            coords (bool, optional): checks if position is given in cell coord or in pixel coords. Defaults to False.
        """
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

    def draw_door(self, i: int, j: int, color: tuple) -> None:
        """Draws door on given position.

        Args:
            i (int): height in grid coords.
            j (int): width in grid coords.
            color (tuple): color in RBG format.
        """
        rect = pygame.Rect(j * self.size + self.vector[1],
                           i * self.size + self.vector[0],
                           self.size, self.size)
        rect1 = pygame.Rect((j + 0.7) * self.size + self.vector[1],
                            (i + 0.4) * self.size + self.vector[0],
                            self.size // 5, self.size // 5)
        pygame.draw.rect(self.my_screen.screen, color, rect)
        pygame.draw.rect(self.my_screen.screen, Colors.BLACK.value, rect1)

    def vector_update(self, difference: tuple) -> None:
        """Updates translation vector to actual player position.

        Args:
            difference (tuple): (int, int) that represents last player's move.
        """
        self.vector = (self.vector[0] + difference[0] * self.size,
                       self.vector[1] + difference[1] * self.size)

    def draw_map(self) -> None:
        """Draws all map elemets within player's view/
        """
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

    def draw_inventory(self) -> None:
        """Draws 3 cells of inventory and keys on fixed positions.
        """
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

            if self.keys[k]:
                self.draw_key(self.my_screen.screen.get_size()[1] - self.size * 2 - self.size // 2 + 3 + 15,
                              i + 15,
                              color,
                              True)
            k += 1

    def end_game(self) -> None:
        """Checks how the game ended and prints related message.
        """
        if self.game_status == GameStatus.EXIT:
            pass
        elif self.game_status == GameStatus.WIN:
            self.my_screen.screen.fill(Colors.BLACK.value)
            self.my_screen.draw_text("You won! Congratulations", pygame.font.Font(None, 60), Colors.WHITE.value, self.my_screen.width // 2, self.my_screen.height // 2)
            pygame.display.flip()
            time.sleep(3)
        elif self.game_status == GameStatus.LOSE:
            time.sleep(2)
            self.my_screen.screen.fill(Colors.BLACK.value)
            self.my_screen.draw_text("You lost :( Better luck next time!", pygame.font.Font(None, 60), Colors.WHITE.value, self.my_screen.width // 2, self.my_screen.height // 2)
            pygame.display.flip()
            time.sleep(3)

    def game_loop(self) -> Status:
        """Main game loop that represents gameplay.

        Returns:
            Status: Status.MENU at the end of the game.
        """
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
        self.end_game()
        return Status.MENU


assert (__name__ != "__main__")
