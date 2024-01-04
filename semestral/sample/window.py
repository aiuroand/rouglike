import pygame

class Window:
    screen = ...
    name = ...
    menu_width = ...
    menu_height = ...
    game_width = ...
    game_height = ...
    def __init__(self, path):
        with open(path, 'r') as f:
            self.name = next(f)[:-1]
            self.menu_width, self.menu_height = [int(x) for x in next(f).split()]
            self.game_width, self.game_height = [int(x) for x in next(f).split()]

        pygame.init()
        pygame.display.set_caption(self.name)
        self.screen = pygame.display.set_mode((self.menu_width, self.menu_height))
    
    
    def __del__(self):
        pygame.quit()
    
    
    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
        
    
    def change_size(self):
        self.screen = pygame.display.set_mode((1000, 1000))