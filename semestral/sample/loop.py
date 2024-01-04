from menu import Menu
from window import Window
from enumerator import Status
import sys

class Loop:
    status = ...
    setting_path = ...
    my_screen = ...
    settings = ...
    menu = ...
    
    def __init__(self, settings_path):
        with open(settings_path, 'r') as f:
            self.settings = [line.rsplit() for line in f]
        self.status = Status.MENU 
        self.setting_path = settings_path
        self.my_screen = Window(self.settings[0][0])
        self.menu = Menu(self.my_screen)

    
    def loop(self):
        while True:
            if self.status == Status.MENU:
                self.status = self.menu.menu_loop()
            elif self.status == Status.GAME:
                self.my_screen = self.my_screen.change_size()
                self.status = Status.MENU
            elif self.status == Status.RULES:
                sys.exit()
            elif self.status == Status.EXIT:
                sys.exit()
                
            