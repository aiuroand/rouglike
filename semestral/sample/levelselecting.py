""" Level selecting menu implementation. """


import pygame
import os
from enumerator import Colors
from enumerator import Status
from exceptions import MapAmount


class Levelselecting:
    my_screen = ...
    maps_dir = ...
    maps = ...

    def __init__(self, screen, path):
        self.my_screen = screen
        self.maps_dir = path
        self.maps = os.listdir(path)
        if len(self.maps) > 10:
            raise MapAmount('Wrong amount of maps, check if maps amount is < 10.')

    def level_loop(self):
        while True:
            font = pygame.font.Font(None, 30)

            self.my_screen.screen.fill(Colors.BLACK.value)
            self.my_screen.draw_text("Select map", font, Colors.WHITE.value, self.my_screen.width // 2, self.my_screen.height // 4)

            i = 1
            for name in self.maps:
                self.my_screen.draw_text(f'{i}: {name}',
                                         font,
                                         Colors.WHITE.value,
                                         self.my_screen.width // 2,
                                         self.my_screen.height // 2 - 200 + i * 50)
                i += 1

            pygame.display.flip()

            d = {}
            key_list = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0][0:i - 1]
            for j in range(i - 1):
                d[key_list[j]] = self.maps_dir + self.maps[j]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return (Status.EXIT, None)
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_list:
                        return (Status.GAME, d[event.key])


assert (__name__ != "__main__")
