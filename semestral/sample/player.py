from entity import Entity
from enumerator import Colors
import pygame

class Player(Entity):
    def __init__(self, pos, speed, color):
        Entity.__init__(self, pos, speed, color)


    def move(self, map, key_array):
        difference = (0, 0)
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_w] & keys[pygame.K_d]:
        #     new_pos = (self.pos[0] - self.speed, self.pos[1] + self.speed)
        # elif keys[pygame.K_w] & keys[pygame.K_a]:
        #     new_pos = (self.pos[0] - self.speed, self.pos[1] - self.speed)
        # elif keys[pygame.K_s] & keys[pygame.K_d]:
        #     new_pos = (self.pos[0] + self.speed, self.pos[1] + self.speed)
        # elif keys[pygame.K_s] & keys[pygame.K_a]:
        #     new_pos = (self.pos[0] + self.speed, self.pos[1] - self.speed)
        if keys[pygame.K_w]:
            new_pos = (self.pos[0] - self.speed, self.pos[1])
        elif keys[pygame.K_s]:
            new_pos = (self.pos[0] + self.speed, self.pos[1])
        elif keys[pygame.K_a]:
            new_pos = (self.pos[0], self.pos[1] - self.speed)
        elif keys[pygame.K_d]:
            new_pos = (self.pos[0], self.pos[1] + self.speed)
        else:
            return (0, 0)

        difference = (self.pos[0] - new_pos[0], self.pos[1] - new_pos[1])
        
        if map[new_pos[0]][new_pos[1]] == ' ':
            self.pos = new_pos
            return difference
        else:
            for Color, color, key_pos in  [('P', 'p', 0),
                                           ('B', 'b', 1),
                                           ('Y', 'y', 2)]:
                if map[new_pos[0]][new_pos[1]] == Color and key_array[key_pos] == True:
                   self.pos = new_pos
                   return difference
                elif map[new_pos[0]][new_pos[1]] == color:
                   key_array[key_pos] = True
                   map[new_pos[0]][new_pos[1]] = ' '
                   self.pos = new_pos
                   return difference
        return (0, 0)



    
    def draw(self, screen, rect_size, camera):
        pygame.draw.circle(screen.screen, Colors.GREEN.value, (500 + rect_size // 2, 400 + rect_size // 2), rect_size // 3)
