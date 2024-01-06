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
    def __init__ (self, pos, speed, color):
        Entity.__init__(self, pos, speed, color)


    @abstractmethod
    def move(self, map, player_coords):
        pass


    @abstractmethod
    def draw(self, screen, rect_size, vector):
        pass
