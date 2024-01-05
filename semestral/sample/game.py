import pygame
import sys
import math

from enumerator import Colors
from player import Player

class Game:
    my_screen = ...
    width = ...
    height = ...
    clock = ...
    view_distance = ...
    size = ...
    keys = [False, False, False]
    game_map = []
    entities = []    
    
    def __init__(self, settings_path, screen, map_path):
        self.my_screen = screen
        self.clock = pygame.time.Clock()
        with open(map_path, 'r') as f:
            for l in f.readlines():
                line = [i for i in l][:-1]
                self.game_map.append(line)
        
        with open(settings_path, 'r') as f:
            self.size = int(next(f))
            self.view_distance = int(next(f))
        
        self.height = len(self.game_map)
        self.width = len(self.game_map[0])
        for i in range(self.height):
            for j in range(self.width):
                if self.game_map[i][j] == 'P':
                    self.entities.append(Player((i, j), 1, Colors.GREEN.value))
            

    def draw_map(self):
        for i in range(self.height):
            for j in range(self.width):
                symb = self.game_map[i][j]
                distance = math.sqrt((self.entities[0].pos[0] - i) ** 2 + (self.entities[0].pos[1] - j) ** 2)
                if distance <= self.view_distance:
                    
                    rect = pygame.Rect(j * self.size, i * self.size, self.size, self.size)
                    
                    if symb == '#':
                        pygame.draw.rect(self.my_screen.screen, Colors.WHITE.value, rect)
                    elif symb == 'R':
                        pygame.draw.rect(self.my_screen.screen, Colors.RED.value, rect)
                    elif symb == 'r':
                        pygame.draw.polygon(self.my_screen.screen, Colors.RED.value, [((j+0.2)*self.size, (i+0.4)*self.size),
                                                                                      ((j+0.7)*self.size, (i+0.4)*self.size),
                                                                                      ((j+0.7)*self.size, (i+0.5)*self.size),
                                                                                      ((j+0.4)*self.size, (i+0.5)*self.size),
                                                                                      ((j+0.4)*self.size, (i+0.6)*self.size),
                                                                                      ((j+0.2)*self.size, (i+0.6)*self.size),
                                                                                     ])


    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.my_screen.screen.fill(Colors.BLACK.value)
            self.draw_map()

            for entity in self.entities:
                entity.move(self.game_map, self.keys)
                entity.draw(self.my_screen, self.size)
                
            pygame.display.flip()
            self.clock.tick(20)