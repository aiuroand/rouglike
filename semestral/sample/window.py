import pygame

class Window:
    screen = ...
    name = ...
    width = ...
    height = ...
    def __init__(self, path):
        with open(path, 'r') as f:
            self.name = next(f)[:-1]
            self.width, self.height = [int(x) for x in next(f).split()]

        pygame.init()
        pygame.display.set_caption(self.name)
        self.screen = pygame.display.set_mode((self.width, self.height))
    
    
    def __del__(self):
        pygame.quit()
    
    
    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)