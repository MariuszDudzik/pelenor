import pygame

class Screen(object):

    def __init__(self):
        info = pygame.display.Info()
        self._width = info.current_w
        self._height = info.current_h
        self._screen = pygame.display.set_mode((self._width, self._height), pygame.FULLSCREEN)

        pygame.display.set_caption("Bitwa na polach pelennoru")

    def get_width(self):
        return self._width
    
    def get_height(self):
        return self._height
    
    def get_screen(self):
        return self._screen