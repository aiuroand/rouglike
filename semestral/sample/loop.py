""" Represnting loop, that connects menu, game, rules, maps """


import sys

from menu import Menu
from window import Window
from game import Game
from rules import Rules
from levelselecting import Levelselecting
from enumerator import Status
from exceptions import MapAmount


class Loop:
    """Main loop, that connects all game parts.

    Arguments:
        status (Status): enumerator that represents current program status.
        my_screen (Window): user-made wrapper for pygame.display.
        settings (list): list that contains paths to configurtation files.
        menu (Menu): object, that represents main game menu.
        level (Levelselecting): object, that represents level selecting menu.
        rules (Rules): object, that represents rules.
        chosen_map (str): path, that is choosen in level selecting phase.
    """
    status: Status
    my_screen: Window
    settings: list
    menu: Menu
    level: Levelselecting
    rules: Rules
    chosen_map: str

    def __init__(self, settings_path: str) -> None:
        """Constuctor

        Args:
            settings_path (str): path to main configuration files.
        """
        with open(settings_path, 'r') as f:
            self.settings = [line.rsplit() for line in f]
        self.status = Status.MENU
        self.my_screen = Window(self.settings[0][0])
        self.menu = Menu(self.my_screen)
        self.rules = Rules(self.my_screen)
        try:
            self.level = Levelselecting(self.my_screen, self.settings[1][0])
        except MapAmount as e:
            print(e)
            sys.exit()
        self.chosen_map = None

    def loop(self) -> None:
        """Main loop that connects all game parts together.
        """
        while True:
            if self.status == Status.MENU:
                self.status = self.menu.menu_loop()
            elif self.status == Status.LEVEL:
                self.status, self.chosen_map = self.level.level_loop()
            elif self.status == Status.GAME:
                try:
                    game = Game(self.settings[2][0], self.my_screen, self.chosen_map)
                    self.status = game.game_loop()
                    game = None
                    print(self.status)
                except AssertionError as e:
                    print(e.args[0])
                    self.status = Status.MENU
            elif self.status == Status.RULES:
                self.status = self.rules.rules_loop()
            elif self.status == Status.EXIT:
                sys.exit()


assert (__name__ != "__main__")
