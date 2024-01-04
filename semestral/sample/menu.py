from enumerator import Status
from enumerator import Colors
import pygame

class Menu:
    my_screen = ...
    
    def __init__(self, my_screen):
        self.my_screen = my_screen
    
    
    def menu_loop(self):
        while True:            
            font = pygame.font.Font(None, 30)
            
            self.my_screen.screen.fill(Colors.BLACK.value)
            self.my_screen.draw_text("Main menu", font, Colors.WHITE.value, self.my_screen.menu_width // 2, self.my_screen.menu_height // 4)
            self.my_screen.draw_text("1. Start Game", font, Colors.WHITE.value, self.my_screen.menu_width // 2, self.my_screen.menu_height // 2)
            self.my_screen.draw_text("2. Rules", font, Colors.WHITE.value, self.my_screen.menu_width // 2, self.my_screen.menu_height // 2 + 50)
            self.my_screen.draw_text("3. Quit", font, Colors.WHITE.value, self.my_screen.menu_width // 2, self.my_screen.menu_height // 2 + 100)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return Status.EXIT
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return Status.GAME
                    elif event.key == pygame.K_2:
                        return Status.RULES
                    elif event.key == pygame.K_3:
                        return Status.EXIT
