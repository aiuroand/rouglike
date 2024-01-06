""" File that contains classes, that represent enemies. """


from entity import Enemy
from enumerator import GameStatus
import pygame


class Vertical(Enemy):
    up = ...

    def __init__(self, pos, speed, color):
        Enemy.__init__(self, pos, speed, color)
        self.up = True

    def move(self, map, player_coords):
        if self.up:
            new_pos = (self.pos[0] - self.speed, self.pos[1])
        else:
            new_pos = (self.pos[0] + self.speed, self.pos[1])

        if new_pos == player_coords:
            self.pos = new_pos
            return GameStatus.LOSE
        elif map[new_pos[0]][new_pos[1]] == ' ':
            self.pos = new_pos
            return GameStatus.PROCESSING
        else:
            self.up = not self.up

        return GameStatus.PROCESSING

    def draw(self, screen, rect_size, vector):
        pygame.draw.circle(screen.screen,
                           self.color,
                           (self.pos[1] * rect_size + rect_size // 2 + vector[1],
                            self.pos[0] * rect_size + rect_size // 2 + vector[0]),
                           rect_size // 3)


class Horizontal(Enemy):
    left = ...

    def __init__(self, pos, speed, color):
        Enemy.__init__(self, pos, speed, color)
        self.left = True

    def move(self, map, player_coords):
        if self.left:
            new_pos = (self.pos[0], self.pos[1] - self.speed)
        else:
            new_pos = (self.pos[0], self.pos[1] + self.speed)

        if new_pos == player_coords:
            self.pos = new_pos
            return GameStatus.LOSE
        elif map[new_pos[0]][new_pos[1]] == ' ':
            self.pos = new_pos
            return GameStatus.PROCESSING
        else:
            self.left = not self.left

        return GameStatus.PROCESSING

    def draw(self, screen, rect_size, vector):
        pygame.draw.circle(screen.screen,
                           self.color,
                           (self.pos[1] * rect_size + rect_size // 2 + vector[1],
                            self.pos[0] * rect_size + rect_size // 2 + vector[0]),
                           rect_size // 3)
