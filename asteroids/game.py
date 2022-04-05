import pygame
import logging as log

log.basicConfig(level=log.DEBUG, format='%(levelname)s: %(message)s')



class Asteroids:
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Asteroidzzz')
        self.scr = pygame.display.set_mode((800, 600))


    def main_loop(self):
        while 1:
            self._handle_input()
            self._game_logic()
            self._draw()


    def _handle_input(self):
        for evt in pygame.event.get(): # queue
            # log.info(evt)
            if evt.type == pygame.QUIT or \
            (evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE):
                quit()


    def _game_logic(self):
        pass


    def _draw(self):
        self.scr.fill((0,0,255))
        pygame.display.flip()
