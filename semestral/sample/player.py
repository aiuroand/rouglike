""" File that contains information about human player. """


import pygame

from window import Window
from entity import Entity
from enumerator import GameStatus


class Player(Entity):
    """Class that represents player. Inherits from Entity class.
    """
    def __init__(self, pos: tuple, color: tuple):
        """Constructor

        Args:
            pos (tuple): player starting postion.
            color (tuple): player color.
        """
        Entity.__init__(self, pos, color)

    def move(self, game_map: list, key_array: list) -> (GameStatus, tuple):
        """Makes 1 step in choose by user direction.

        Args:
            game_map (list): 2D array, that represents game map.
            key_array (list): 1D array, that represents collected keys.

        Returns:
            (GameStatus, tuple): (GameStatus.WIN, (0, 0)) if player fount the exit.
                                 (GameStatus.PROCESSING, (int, int)) if player successfuly made a move in chosen direction.
                                 (GameStatus.PROCESSING, (0, 0)) if player's move was not correct or if no keyboard input recieved.
                                 (GameStatus.EXIT, (0, 0)) if player pressed 'escape' button
        """
        difference = (0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            new_pos = (self.pos[0] - 1, self.pos[1])
        elif keys[pygame.K_s]:
            new_pos = (self.pos[0] + 1, self.pos[1])
        elif keys[pygame.K_a]:
            new_pos = (self.pos[0], self.pos[1] - 1)
        elif keys[pygame.K_d]:
            new_pos = (self.pos[0], self.pos[1] + 1)
        elif keys[pygame.K_ESCAPE]:
            return (GameStatus.EXIT, (0, 0))
        else:
            return (GameStatus.PROCESSING, (0, 0))

        difference = (self.pos[0] - new_pos[0], self.pos[1] - new_pos[1])

        if game_map[new_pos[0]][new_pos[1]] == ' ':
            self.pos = new_pos
            return (GameStatus.PROCESSING, difference)
        elif game_map[new_pos[0]][new_pos[1]] == 'E':
            return (GameStatus.WIN, difference)
        else:
            for Color, color, key_pos in [('P', 'p', 0),
                                          ('B', 'b', 1),
                                          ('Y', 'y', 2)]:
                if game_map[new_pos[0]][new_pos[1]] == Color and key_array[key_pos]:
                    self.pos = new_pos
                    game_map[new_pos[0]][new_pos[1]] = ' '
                    return (GameStatus.PROCESSING, difference)
                elif game_map[new_pos[0]][new_pos[1]] == color:
                    key_array[key_pos] = True
                    game_map[new_pos[0]][new_pos[1]] = ' '
                    self.pos = new_pos
                    return (GameStatus.PROCESSING, difference)
        return (GameStatus.PROCESSING, (0, 0))

    def draw(self, screen: Window, rect_size: int, win_size: tuple) -> None:
        """Draws player of given coordinates.

        Args:
            screen (Window): user-made wrapper for pygame.display.
            rect_size (int): reference size of 1 cell.
            win_size (tuple): window game size in pixels.
        """

        pygame.draw.circle(screen.screen,
                           self.color,
                           (win_size[0] // 2 + rect_size // 2,
                            win_size[1] // 2 + rect_size // 2),
                           rect_size // 3)


assert (__name__ != "__main__")
