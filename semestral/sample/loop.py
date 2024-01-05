from menu import Menu
from window import Window
from game import Game
from levelselecting import Levelselecting
from enumerator import Status
import sys

class Loop:
    status = ...
    my_screen = ...
    settings = ...
    menu = ...
    level = ...
    map = ...
    
    def __init__(self, settings_path):
        with open(settings_path, 'r') as f:
            self.settings = [line.rsplit() for line in f]
        self.status = Status.MENU 
        self.my_screen = Window(self.settings[0][0])
        self.menu = Menu(self.my_screen)
        try:
            self.level = Levelselecting(self.my_screen, self.settings[1][0])
        except Exception as e:
            print(e)
            sys.exit()
        self.map = None

    
    def loop(self):
        while True:
            if self.status == Status.MENU:
                self.status = self.menu.menu_loop()
            elif self.status == Status.LEVEL:
                self.status, self.map = self.level.level_loop()
            elif self.status == Status.GAME:
                game = Game(self.settings[2][0], self.my_screen, self.map)
                self.status = game.game_loop()
            elif self.status == Status.RULES:
                sys.exit()
            elif self.status == Status.EXIT:
                sys.exit()
                
            