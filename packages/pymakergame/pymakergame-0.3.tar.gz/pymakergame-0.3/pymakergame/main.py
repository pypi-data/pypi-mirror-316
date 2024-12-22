from sys import exit
import pygame

class Game():
    """Create a game window with a 
    title (str -> "Hello")
    size (tuple -> (0, 0))
    color (tuple -> (0, 0, 0) [RGB])
    icon (str -> "assets/icon.png")
    """
    def __init__(self, name: str = "PyMakerGame", size: tuple = (500, 500), icon: str = "icon.png", color: tuple = (255, 255, 255)):
        self.name = name
        self.width, self.height = size
        self.icon = icon
        self.bg_color = color
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.name)
        if icon != None: pygame.display.set_icon(pygame.image.load(self.icon))

        #Running Time
        self.running = True
        self.clock = pygame.time.Clock()
        while self.running:
            self.clock.tick(60)
            self.screen.fill(self.bg_color)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
        pygame.quit()
        exit()