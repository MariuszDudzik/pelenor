import pygame

class Screen(object):

    def __init__(self):
        info = pygame.display.Info()
        self._width = info.current_w
        self._height = info.current_h
        self._screen = pygame.display.set_mode((self._width, self._height), pygame.FULLSCREEN)
        self.background = pygame.Surface(self._screen.get_size())
        self.background.fill((0, 0, 0))

        pygame.display.set_caption("Bitwa na polach pelennoru")

    def get_width(self):
        return self._width
    
    def get_height(self):
        return self._height
    
    def get_screen(self):
        return self._screen
    
    def get_background(self):
        return self.background

    def fill_background(self, color=(0, 0, 0)):
        self.background.fill(color)
    
    