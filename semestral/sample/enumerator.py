from enum import Enum

class Status(Enum):
    MENU = 1
    GAME = 2
    RULES = 3
    EXIT = 0

class Colors(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)