""" File that contains classes, that represent enemies. """


from entity import Enemy
from enumerator import GameStatus, Colors
from a_star import a_star


class Vertical(Enemy):
    """ Class that inherits from abstract class Enemy.

    Represents up-down wakling enemy.

    Attributes:
        up (bool): current direction of mevement.
    """
    up: bool = True

    def __init__(self, pos: tuple, color: tuple):
        """ Constructor that firstly creates parren class Enemy.

        Args:
            pos (tuple): Enemy position.
            color (Colors): Enemy color in RGB format.
        """
        Enemy.__init__(self, pos, color)

    def move(self, game_map: list, player_coords: tuple) -> GameStatus:
        """ Enemy makes 1 step above or 1 step below.

        Args:
            game_map (list): 2D array that represents game map.
            player_coords (tuple): Current coordinates of a player to detect possible collision.

        Returns:
            GameStatus: Enumerator, that show is emeny killed player or not.
        """
        if self.up:
            new_pos = (self.pos[0] - 1, self.pos[1])
        else:
            new_pos = (self.pos[0] + 1, self.pos[1])

        if new_pos == player_coords:
            self.pos = new_pos
            return GameStatus.LOSE
        elif game_map[new_pos[0]][new_pos[1]] == ' ':
            self.pos = new_pos
            return GameStatus.PROCESSING
        else:
            self.up = not self.up

        return GameStatus.PROCESSING


class Horizontal(Enemy):
    """ Class that inherits from abstract class Enemy.

    Represents left-right wakling enemy.

    Attributes:
        left (bool): current direction of mevement.
    """
    left: bool = True

    def __init__(self, pos: tuple, color: tuple):
        """ Constructor that firstly creates parren class Enemy.

        Args:
            pos (tuple): Enemy position.
            color (Colors): Enemy color in RGB format.
        """
        Enemy.__init__(self, pos, color)

    def move(self, game_map: list, player_coords: tuple) -> GameStatus:
        """ Enemy makes 1 step to the left or 1 step to the right.

        Args:
            game_map (list): 2D array that represents game map.
            player_coords (tuple): Current coordinates of a player to detect possible collision.

        Returns:
            GameStatus: Enumerator, that show is emeny killed player or not.
        """
        if self.left:
            new_pos = (self.pos[0], self.pos[1] - 1)
        else:
            new_pos = (self.pos[0], self.pos[1] + 1)

        if new_pos == player_coords:
            self.pos = new_pos
            return GameStatus.LOSE
        elif game_map[new_pos[0]][new_pos[1]] == ' ':
            self.pos = new_pos
            return GameStatus.PROCESSING
        else:
            self.left = not self.left

        return GameStatus.PROCESSING


class Follower(Enemy):
    """Class that inherits from abstract class Enemy.

    Represents enemy, that follows player using A* algorithm.
    """
    def __init__(self, pos: tuple, color: tuple):
        """ Constructor that firstly creates parren class Enemy.

        Args:
            pos (tuple): Enemy position.
            color (Colors): Enemy color in RGB format.
        """
        Enemy.__init__(self, pos, color)

    def move(self, game_map: list, player_coords: tuple) -> None:
        """ Enemy finds the best route using A* algorithm and makes 1 stem in that direction.

        Args:
            game_map (list): 2D array that represents game map.
            player_coords (tuple): Current coordinates of a player to detect possible collision.

        Returns:
            GameStatus: Enumerator, that show is emeny killed player or not.
        """
        way = a_star(game_map, self.pos, player_coords)
        if len(way) == 0:
            return GameStatus.PROCESSING
        self.pos = way[1]
        if self.pos == player_coords:
            return GameStatus.LOSE
        else:
            return GameStatus.PROCESSING


assert (__name__ != "__main__")
