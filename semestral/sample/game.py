import pygame
import sys
import math

from enumerator import Colors
from player import Player
from exceptions import WrongPlayersAmount

class Game:
    my_screen = ...
    width = ...
    height = ...
    clock = ...
    view_distance = ...
    size = ...
    camera = ...
    FPS = ...
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
            self.FPS = int(next(f))
        
        self.height = len(self.game_map)
        self.width = len(self.game_map[0])
        player = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.game_map[i][j] == '@':
                    player += 1
                    self.game_map[i][j] = ' '
                    self.entities.append(Player((i,j), 1, Colors.GREEN.value))
                    self.camera = ((self.my_screen.screen.get_size()[1] // 2 - i * self.size),
                                   (self.my_screen.screen.get_size()[0] // 2 - j * self.size))
        if player != 1:
            raise WrongPlayersAmount(f'Wrong amount of players on the map. Check if file {map_path} is not damaged.')
  

    def drawKey(self, i, j, color):
        pygame.draw.polygon(self.my_screen.screen, color, [((j+0.2)*self.size + self.camera[1], (i+0.4)*self.size + self.camera[0]),
                                                           ((j+0.7)*self.size + self.camera[1], (i+0.4)*self.size + self.camera[0]),
                                                           ((j+0.7)*self.size + self.camera[1], (i+0.5)*self.size + self.camera[0]),
                                                           ((j+0.4)*self.size + self.camera[1], (i+0.5)*self.size + self.camera[0]),
                                                           ((j+0.4)*self.size + self.camera[1], (i+0.6)*self.size + self.camera[0]),
                                                           ((j+0.2)*self.size + self.camera[1], (i+0.6)*self.size + self.camera[0]),
                                                          ])          


    def camera_update(self, difference):
        self.camera = (self.camera[0] + difference[0] * self.size,
                       self.camera[1] + difference[1] * self.size)
        
    def draw_map(self):
        for i in range(self.height):
            for j in range(self.width):
                symb = self.game_map[i][j]
                distance = math.sqrt((self.entities[0].pos[0] - i) ** 2 + (self.entities[0].pos[1] - j) ** 2)
                if distance <= self.view_distance:
                    
                    rect = pygame.Rect(j * self.size + self.camera[1],
                                       i * self.size + self.camera[0], self.size, self.size)
                    
                    if symb == '#':
                        pygame.draw.rect(self.my_screen.screen, Colors.WHITE.value, rect)
                    elif symb in ['B', 'P', 'Y', 'y', 'b', 'p']:
                        for Color, color, color_enum in  [('P', 'p', Colors.PURPLE.value),
                                                          ('B', 'b', Colors.BLUE.value),
                                                          ('Y', 'y', Colors.YELLOW.value)]:
                            if symb == Color:
                                pygame.draw.rect(self.my_screen.screen, color_enum, rect)
                            elif symb == color:
                                self.drawKey(i, j, color_enum)



    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.my_screen.screen.fill(Colors.BLACK.value)
            self.draw_map()

            for entity in self.entities:
                difference = entity.move(self.game_map, self.keys)
                self.camera_update(difference)
                entity.draw(self.my_screen, self.size, self.camera)
            
            pygame.display.flip()
            self.clock.tick(self.FPS)