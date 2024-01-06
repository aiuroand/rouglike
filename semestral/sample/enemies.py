""" File that contains classes, that represent enemies. """


import pygame

from entity import Enemy
from enumerator import GameStatus
from a_star import a_star

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


class Follower(Enemy):

    def __init__(self, pos, speed, color):
        Enemy.__init__(self, pos, speed, color)

    def move(self, map, player_coords):
        way = a_star(map, self.pos, player_coords)
        if len(way) == 0:
            return GameStatus.PROCESSING
        self.pos = way[1]
        if self.pos == player_coords:
            return GameStatus.LOSE
        else:
            return GameStatus.PROCESSING

        # if new_pos == player_coords:
        #     self.pos = new_pos
        #     return GameStatus.LOSE
        # elif map[new_pos[0]][new_pos[1]] == ' ':
        #     self.pos = new_pos
            # return GameStatus.PROCESSING
        # else:
            # self.left = not self.left

        return GameStatus.PROCESSING


assert (__name__ != "__main__")
