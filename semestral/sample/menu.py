""" File that contains main menu representation. """


import pygame

from window import Window
from enumerator import Status
from enumerator import Colors


class Menu:
    """Class that represents main menu.

    Arguments:
        my_screen (Window): user-created wrapper for pygame.display.
    """
    my_screen: Window

    def __init__(self, my_screen: Window):
        """Constructor

        Args:
            my_screen (Window): user-created wrapper for pygame.display.
        """
        self.my_screen = my_screen

    def menu_loop(self) -> Status:
        """Main menu loop.

        Returns:
            Status: Status.LEVEL if user selects Start Game.
                    Status.RULES if user selects Rules.
                    Status.QUIT if user selects Quit ot closes the window.
        """
        while True:
            font = pygame.font.Font(None, 30)

            self.my_screen.screen.fill(Colors.BLACK.value)
            self.my_screen.draw_text("Main menu",     font, Colors.WHITE.value, self.my_screen.width // 2, self.my_screen.height // 4)
            self.my_screen.draw_text("1. Start Game", font, Colors.WHITE.value, self.my_screen.width // 2, self.my_screen.height // 2)
            self.my_screen.draw_text("2. Rules",      font, Colors.WHITE.value, self.my_screen.width // 2, self.my_screen.height // 2 + 50)
            self.my_screen.draw_text("3. Quit",       font, Colors.WHITE.value, self.my_screen.width // 2, self.my_screen.height // 2 + 100)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return Status.EXIT
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return Status.LEVEL
                    elif event.key == pygame.K_2:
                        return Status.RULES
                    elif event.key == pygame.K_3:
                        return Status.EXIT


assert (__name__ != "__main__")
