""" File that provides enumerators for the game. """


from enum import Enum


class Status(Enum):
    """Enumerator for menu status.
    """
    MENU = 1
    LEVEL = 2
    GAME = 3
    RULES = 4
    EXIT = 0


class Colors(Enum):
    """Enumerator for all avialable colors.
    """
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    PURPLE = (102, 23, 204)
    YELLOW = (247, 249, 60)
    BROWN = (139, 69, 19)


class GameStatus(Enum):
    """Enumerator for current game status.
    """
    PROCESSING = 1
    WIN = 2
    LOSE = 3
    EXIT = 0


assert (__name__ != "__main__")
