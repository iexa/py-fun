""" simple asteroids game - good ideas with pygame """
import logging as log
import pygame

from models import Ship, Rock, load_sprite


log.basicConfig(level=log.DEBUG, format='%(levelname)s: %(message)s')


# TODO: implement an opening screen
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
        self.rocks = [Rock.create_random(self.scr, self.ship.pos) for _ in range(7)]
        Rock.rocks = self.rocks  # pass rocks container into Rock class

    def main_loop(self):
        while 1:
            self._handle_input()
            self._game_logic()
            self._draw()

    @property
    def game_objects(self):
        all = [*self.rocks, *self.bullets]
        if self.ship.is_alive:
            all.append(self.ship)
        return all


    def _handle_input(self):
        is_key_pressed = pygame.key.get_pressed()
        # log.info(f"{is_key_pressed=}")
        for evt in pygame.event.get():  # queue
            if evt.type == pygame.QUIT or is_key_pressed[pygame.K_ESCAPE]:
                pygame.quit()
            # if using is_key_pressed that means shooting until key is pressed not once only
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

        # remove bullets outside screen
        rect = self.scr.get_rect()
        for bullet in self.bullets[:]:  # cant remove items while iterating over
            if not rect.collidepoint(bullet.pos):
                self.bullets.remove(bullet)

        # bullet meets rock? (remove both first)
        for bullet in self.bullets[:]:
            for rock in self.rocks[:]:
                if rock.collides_with(bullet):
                    self.rocks.remove(rock)
                    rock.play_boom_sound()
                    rock.split()
                    self.bullets.remove(bullet)
                    break  # if 2+ rocks overlap remove only one, not all...

        # ship hit by rock?
        # TODO: multiple lifes + show lives left
        if self.ship.is_alive:
            for rock in self.rocks:
                if rock.collides_with(self.ship):
                    rock.play_boom_sound()
                    self.rocks.remove(rock)
                    self.ship.decrease_lives()
                    log.info(f'{self.ship.lives=}')
                    # log.info(f'{self.ship.is_alive=}')
                    # TODO: mark that life decreased and be invincible for a second
                    break

    def _draw(self):
        # self.scr.fill((0,0,255))
        self.scr.blit(self.background, (0, 0))
        for obj in self.game_objects:
            obj.draw(self.scr)
        pygame.display.flip()

        self.clock.tick(30)  # set framerate
