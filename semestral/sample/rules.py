""" File that contains rules window representation. """


from enumerator import Status
from enumerator import Colors
import pygame


class Rules:
    my_screen = ...

    def __init__(self, my_screen):
        self.my_screen = my_screen

    def rules_loop(self):
        while True:
            font = pygame.font.Font(None, 30)

            # 0.
            self.my_screen.screen.fill(Colors.BLACK.value)
            self.my_screen.draw_text("Welcome to my maze game",
                                     font, Colors.WHITE.value,
                                     self.my_screen.width // 2, self.my_screen.height // 4)
            
            # 1.
            self.my_screen.draw_text("1. This is you     ", 
                                     font, Colors.WHITE.value,
                                     self.my_screen.width // 2, self.my_screen.height // 2 - 70)
            pygame.draw.circle(self.my_screen.screen,
                               Colors.GREEN.value,
                               (self.my_screen.width // 2 + 70, self.my_screen.height // 2 - 70),
                                30 // 3)
            
            # 2.
            for i, letter in [(self.my_screen.width // 2, 'A'),
                              (self.my_screen.width // 2 + 26, 'S'),
                              (self.my_screen.width // 2 + 52, 'D')]:
                rect = pygame.Rect(i + 26,
                                   self.my_screen.height // 2 - 13,
                                   24, 24)
                rect1 = pygame.Rect(i + 27,
                                    self.my_screen.height // 2 - 12,
                                    22, 22)
                pygame.draw.rect(self.my_screen.screen, Colors.WHITE.value, rect)
                pygame.draw.rect(self.my_screen.screen, Colors.BLACK.value, rect1)
                self.my_screen.draw_text(letter, font, Colors.WHITE.value, i + 38, self.my_screen.height // 2 - 1)
            rect = pygame.Rect(self.my_screen.width // 2 + 26 + 26,
                               self.my_screen.height // 2 - 40,
                               24, 24)
            rect1 = pygame.Rect(self.my_screen.width // 2 + 26 + 27,
                                self.my_screen.height // 2 - 39,
                                22, 22)
            pygame.draw.rect(self.my_screen.screen, Colors.WHITE.value, rect)
            pygame.draw.rect(self.my_screen.screen, Colors.BLACK.value, rect1)
            self.my_screen.draw_text('W', font, Colors.WHITE.value, self.my_screen.width // 2 + 26 + 38, self.my_screen.height // 2 - 24)
            self.my_screen.draw_text("2. You can move using                buttons.", font, Colors.WHITE.value, self.my_screen.width // 2, self.my_screen.height // 2)
            
            # 3.
            self.my_screen.draw_text("3. You can collect keys               ", 
                                     font, Colors.WHITE.value,
                                     self.my_screen.width // 2, self.my_screen.height // 2 + 70)
            for j, color in [(self.my_screen.width // 2 + 80, Colors.BLUE.value),
                             (self.my_screen.width // 2 + 105, Colors.YELLOW.value),
                             (self.my_screen.width // 2 + 130, Colors.PURPLE.value)]:
                pygame.draw.polygon(self.my_screen.screen, color, [((j + 0.2 * 30), (self.my_screen.height // 2 + 55 + 0.4 * 30)),
                                                                   ((j + 0.7 * 30), (self.my_screen.height // 2 + 55 + 0.4 * 30)),
                                                                   ((j + 0.7 * 30), (self.my_screen.height // 2 + 55 + 0.5 * 30)),
                                                                   ((j + 0.4 * 30), (self.my_screen.height // 2 + 55 + 0.5 * 30)),
                                                                   ((j + 0.4 * 30), (self.my_screen.height // 2 + 55 + 0.6 * 30)),
                                                                   ((j + 0.2 * 30), (self.my_screen.height // 2 + 55 + 0.6 * 30))]
                                    )
            self.my_screen.draw_text("to open doors               ", 
                                     font, Colors.WHITE.value,
                                     self.my_screen.width // 2, self.my_screen.height // 2 + 100)
            for j, color in [(self.my_screen.width // 2 + 63, Colors.BLUE.value),
                             (self.my_screen.width // 2 + 103, Colors.YELLOW.value),
                             (self.my_screen.width // 2 + 143, Colors.PURPLE.value)]:
                rect = pygame.Rect(j,
                                   self.my_screen.height // 2 + 85,
                                   30, 30)
                rect1 = pygame.Rect(j + 20,
                                    self.my_screen.height // 2 + 100,
                                    5, 5)
                pygame.draw.rect(self.my_screen.screen, color, rect)
                pygame.draw.rect(self.my_screen.screen, Colors.BLACK.value, rect1)

            # 5.
            self.my_screen.draw_text("5. Avoid enemies       . Some of them may be very smart and dangerous.",
                                     font, Colors.WHITE.value,
                                     self.my_screen.width // 2, self.my_screen.height // 2 + 170)
            pygame.draw.circle(self.my_screen.screen,
                               Colors.RED.value,
                               (self.my_screen.width // 2 + 70 - 230, self.my_screen.height // 2 + 170),
                                30 // 3)
            # 6.
            self.my_screen.draw_text("I wish you Good Luck! :)",
                                     font, Colors.WHITE.value,
                                     self.my_screen.width // 2, self.my_screen.height // 2 + 240)
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return Status.MENU


assert (__name__ != "__main__")
