""" File that contains game window representation. """


import pygame


class Window:
    """Class, that represents user-made wrapper for pygame.display.

    Arguments:
        my_screen (pygame.display): pygame window.
        name (str): window name.
        width (int): window's width in pixels.
        height (int): window's height in pixels.
    """
    screen: pygame.display
    name: str
    width: int
    height: int

    def __init__(self, path: str):
        """Constructor

        Args:
            path (str): file that contains window's configuration.
        """
        with open(path, 'r') as f:
            self.name = next(f)[:-1]
            self.width, self.height = [int(x) for x in next(f).split()]

        pygame.init()
        pygame.display.set_caption(self.name)
        self.screen = pygame.display.set_mode((self.width, self.height))

    def __del__(self):
        """Destructor
        """
        pygame.quit()

    def draw_text(self, text: str, font: pygame.font, color: tuple, x: int, y: int) -> None:
        """User-made functiont that draws given text on given cooridnates.

        Args:
            text (str): text to be printed.
            font (pygame.font): font size and type.
            color (tuple): text color in RGB format.
            x (int): x coordinate of text's center in pixels.
            y (int): y coordinate of text's center in pixels.
        """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)


assert (__name__ != "__main__")
