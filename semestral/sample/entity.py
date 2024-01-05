from abc import abstractmethod
class Entity:
    pos = ...
    speed = ...
    color = ...
    def __init__(self, pos, speed, color):
        self.pos = pos
        self.speed = speed
        self.color = color

    @abstractmethod
    def move(self):
        pass
    
    @abstractmethod
    def draw(self, screen, rect_size, key_array, camera):
        pass
