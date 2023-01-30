import logging as log
import pygame

from models import Ship, Rock, load_sprite


log.basicConfig(level=log.DEBUG, format='%(levelname)s: %(message)s')


class Asteroids:
    """ Main Game """
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Asteroidzzz')
        self.scr = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.background = load_sprite('space', False)
        self.collision_count = 0

        self.bullets = []
        self.ship = Ship((400, 300), self.bullets)
        self.rocks = [Rock(self.scr, self.ship.pos) for _ in range(7)]

    def main_loop(self):
        while 1:
            self._handle_input()
            self._game_logic()
            self._draw()

    @property
    def game_objects(self):
        return [*self.rocks, *self.bullets, self.ship]

    def _handle_input(self):
        is_key_pressed = pygame.key.get_pressed()
        # log.info(f"{is_key_pressed=}")
        for evt in pygame.event.get():  # queue
            if evt.type == pygame.QUIT or is_key_pressed[pygame.K_ESCAPE]:
                quit()
            if evt.type == pygame.KEYDOWN and evt.key == pygame.K_SPACE:
                self.ship.shoot()
        if is_key_pressed[pygame.K_RIGHT]:
            self.ship.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            self.ship.rotate(clockwise=False)
        elif is_key_pressed[pygame.K_UP]:
            self.ship.accelerate()
        elif is_key_pressed[pygame.K_DOWN]:
            self.ship.decelerate()
            

    def _game_logic(self):
        for obj in self.game_objects:
            obj.move(self.scr)

        # remove bullets outside scr
        rect = self.scr.get_rect()
        for bullet in self.bullets[:]:  # cant remove items while iterating over
            if not rect.collidepoint(bullet.pos):
                self.bullets.remove(bullet)

    def _draw(self):
        # self.scr.fill((0,0,255))
        self.scr.blit(self.background, (0, 0))
        for obj in self.game_objects:
            obj.draw(self.scr)
        pygame.display.flip()

        for rock in self.rocks:
            if self.ship.collides_with(rock):
                self.collision_count += 1
                log.info(f'{self.collision_count=}')

        self.clock.tick(30)  # set framerate
