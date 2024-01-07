""" File that contains abstract class for entities and enemies. """


import pygame
import math

from abc import abstractmethod


class Entity:
    pos = ...
    speed = ...
    color = ...

    def __init__(self, pos, speed, color):
        self.pos = pos
        self.speed = speed
        self.color = color


class Enemy(Entity):
    def __init__(self, pos, speed, color):
        Entity.__init__(self, pos, speed, color)

    @abstractmethod
    def move(self, map, player_coords):
        pass

    def draw(self, screen, rect_size, vector, player_coords, view_distance):
        distance = math.sqrt((player_coords[0] - self.pos[0]) ** 2 + (player_coords[1] - self.pos[1]) ** 2)
        if distance <= view_distance:
            pygame.draw.circle(screen.screen,
                               self.color,
                               (self.pos[1] * rect_size + rect_size // 2 + vector[1],
                                self.pos[0] * rect_size + rect_size // 2 + vector[0]),
                               rect_size // 3)


assert (__name__ != "__main__")
