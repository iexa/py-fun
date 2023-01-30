from pathlib import Path
from random import randrange, randint

from pygame.math import Vector2
from pygame.transform import rotozoom
from pygame import Surface
from pygame.image import load


DIR_UP = Vector2(0, -1)


def load_sprite(name: str, with_alpha=True):
    file = Path(__file__).parent / f'assets/{name}.png'
    sprite = load(file.resolve())  # or file or file.resolve()
    return sprite.convert_alpha() if with_alpha else sprite.convert()


class GameObj:
    """ base game objects for all sprites """
    def __init__(self, pos: Vector2, sprite: Surface, velocity, wraps=True):
        self.pos = Vector2(pos)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)
        self.wraps = wraps

    def draw(self, surface: Surface):
        pos = self.pos - Vector2(self.radius)  # convert from center to top-left based coord
        surface.blit(self.sprite, pos)

    def _wrap_pos(self, surface: Surface):
        x, y = self.pos
        w, h = surface.get_size()
        return Vector2(x % w, y % h)  # simple modulo

    def move(self, surface: Surface):
        # surface is on which we move, to be able to wrap around
        self.pos = self.pos + self.velocity
        if self.wraps:
            self.pos = self._wrap_pos(surface)

    def collides_with(self, other: 'GameObj'):
        distance = self.pos.distance_to(other.pos)
        return distance < self.radius + other.radius


class Ship(GameObj):
    """ ships also shoot bullets """
    ROTATION_SPEED = 3
    ACCELERATION = 0.3
    BULLET_SPEED = 5

    def __init__(self, pos: Vector2, bullets):
        self.dir = Vector2(DIR_UP)
        self.bullets = bullets
        super().__init__(pos, load_sprite('spaceship'), Vector2(0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.ROTATION_SPEED * sign
        self.dir.rotate_ip(angle)  # _ip = in_place

    def accelerate(self):
        self.velocity += self.dir * self.ACCELERATION

    def decelerate(self):
        # TODO: check so it cannot go in reverse, so stop at 0 vel.
        self.velocity -= self.dir * self.ACCELERATION

    def shoot(self):
        velocity = self.dir * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.pos, velocity)
        self.bullets.append(bullet)

    def draw(self, surface: Surface):
        angle = self.dir.angle_to(DIR_UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())

        blit_pos = self.pos - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_pos)


class Rock(GameObj):
    MIN_START_GAP = 200
    MIN_SPEED = 1
    MAX_SPEED = 3

    def __init__(self, surface: Surface, ship_pos: Vector2):
        while True:  # do not be too close to ship
            pos = Vector2(randrange(surface.get_width()),
                          randrange(surface.get_height()))
            if pos.distance_to(ship_pos) > self.MIN_START_GAP:
                break

        speed = randint(self.MIN_SPEED, self.MAX_SPEED)
        angle = randint(0, 360)
        velocity = Vector2(speed, 0).rotate(angle)
        super().__init__(pos, load_sprite('asteroid'), velocity)


class Bullet(GameObj):
    def __init__(self, pos: Vector2, velocity):
        super().__init__(pos, load_sprite('bullet'), velocity, wraps=False)
