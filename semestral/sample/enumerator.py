from enum import Enum

class Status(Enum):
    MENU = 1
    LEVEL = 2
    GAME = 3
    RULES = 4
    EXIT = 0

class Colors(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED   = (255, 0, 0)
    BLUE  = (0, 0, 255)
    PURPLE  = (102, 23, 204)
    YELLOW  = (247, 249, 60)