from entity import Entity
from enumerator import Colors
import pygame

class Player(Entity):
    def __init__(self, pos, speed, color):
        Entity.__init__(self, pos, speed, color)


    def move(self, map, key_array):
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
            return

        if map[new_pos[0]][new_pos[1]] == ' ':
            self.pos = new_pos
        elif map[new_pos[0]][new_pos[1]] == 'R' and key_array[0] == True:
            self.pos = new_pos
        elif map[new_pos[0]][new_pos[1]] == 'r':
            key_array[0] = True
            map[new_pos[0]][new_pos[1]] = ' '

    
    def draw(self, screen, rect_size):
        pygame.draw.circle(screen.screen, Colors.GREEN.value, (int(self.pos[1] * rect_size + rect_size // 2),
                                                               int(self.pos[0] * rect_size + rect_size // 2)), rect_size // 3)
