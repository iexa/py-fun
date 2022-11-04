import pygame
from models import GameObj, Ship
from pygame.image import load
from pathlib import Path
import logging as log


log.basicConfig(level=log.DEBUG, format='%(levelname)s: %(message)s')


def load_sprite(name: str, with_alpha=True):
    file = Path(__file__).parent / f'assets/{name}.png'
    sprite = load(file.resolve()) # or file.resolve()
    if with_alpha:
        return sprite.convert_alpha()
    return sprite.convert()


class Asteroids:
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Asteroidzzz')
        self.scr = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.background = load_sprite('space', False)
        self.collision_count = 0

        self.ship = Ship((400, 300), load_sprite('spaceship'))
        sprite = load_sprite('asteroid')
        self.rock = GameObj((50, 300), sprite, (1,0))


    def main_loop(self):
        while 1:
            self._handle_input()
            self._game_logic()
            self._draw()


    def _handle_input(self):
        is_key_pressed = pygame.key.get_pressed()
        for evt in pygame.event.get(): # queue
            # log.info(evt)
            if evt.type == pygame.QUIT or is_key_pressed[pygame.K_ESCAPE]:
                quit()
        if is_key_pressed[pygame.K_RIGHT]:
             self.ship.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            self.ship.rotate(clockwise=False)


    def _game_logic(self):
        self.ship.move()
        self.rock.move()


    def _draw(self):
        # self.scr.fill((0,0,255))
        self.scr.blit(self.background, (0,0))
        self.ship.draw(self.scr)
        self.rock.draw(self.scr)
        pygame.display.flip()

        if self.ship.collides_with(self.rock):
            self.collision_count += 1
            log.info(f'{self.collision_count=}')

        self.clock.tick(30) # set framerate