""" File that contains abstract class for entities and enemies. """


import pygame
import math

from window import Window
from abc import abstractmethod


class Entity:
    """Parent class for Player and Enemies.

    Attributes:
        pos (tuple): coordinates of entity in the maze.
        color (tuple): color of entity in RGB format.
    """
    pos: tuple
    color: tuple

    def __init__(self, pos: tuple, color: tuple):
        """Constructor

        Args:
            pos (tuple): coordinates of entity in the maze.
            color (tuple): color of entity in RGB format.
        """
        self.pos = pos
        self.color = color


class Enemy(Entity):
    """Parent class for Enemies that inherits from Entity.
    """
    def __init__(self, pos: tuple, color: tuple):
        """Constructor that firstly creates parent class Entity
        """
        Entity.__init__(self, pos, color)

    @abstractmethod
    def move(self, game_map: list, player_coords: tuple) -> None:
        """Abstract method that will implement enemies movement.

        Args:
            game_map (list): 2D array that represents game map.
            player_coords (tuple): player coorinates to detect collisions.
        """
        pass

    def draw(self, screen: Window, rect_size: int, vector: tuple, player_coords: tuple, view_distance: int) -> None:
        """Drawe enemy on the screen using it's relative posotion to player.

        Args:
            screen (Window): user-made class that represents decorator for pygame window.
            rect_size (int): reference size of one cell.
            vector (tuple): translation vector to draw relative to the window center.
            player_coords (tuple): coordinates of a player to detect if enemy is in player's view distance.
            view_distance (int): player's view distance.
        """
        distance = math.sqrt((player_coords[0] - self.pos[0]) ** 2 + (player_coords[1] - self.pos[1]) ** 2)
        if distance <= view_distance:
            pygame.draw.circle(screen.screen,
                               self.color,
                               (self.pos[1] * rect_size + rect_size // 2 + vector[1],
                                self.pos[0] * rect_size + rect_size // 2 + vector[0]),
                               rect_size // 3)


assert (__name__ != "__main__")
