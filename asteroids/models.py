from pathlib import Path
from random import randrange, randint

from pygame.math import Vector2
from pygame.transform import rotozoom
from pygame import Surface
from pygame.image import load
from pygame.mixer import Sound


DIR_UP = Vector2(0, -1)


def load_sprite(name: str, with_alpha=True):
    file = Path(__file__).parent / f'assets/{name}.png'
    sprite = load(file.resolve())  # or file or file.resolve()
    return sprite.convert_alpha() if with_alpha else sprite.convert()


def load_sound(name: str) -> Sound:
    file = Path(__file__).parent / f'assets/{name}.ogg'
    return Sound(file)


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
        # TODO: https://stackoverflow.com/questions/57886086/pygame-sprite-transparency-collision
        distance = self.pos.distance_to(other.pos)
        return distance < self.radius + other.radius


class Ship(GameObj):
    """ ship also shoots bullets """
    ROTATION_SPEED = 3
    ACCELERATION = 0.3
    BULLET_SPEED = 5
    LIVES = 3

    def __init__(self, pos: Vector2, bullets, lives=LIVES):
        self.dir = Vector2(DIR_UP)
        self.bullets = bullets
        self.lives = lives
        self.snd_bullet = load_sound('laser')
        super().__init__(pos, load_sprite('spaceship2'), Vector2(0))

    @property
    def is_alive(self):
        return self.lives > 0

    def decrease_lives(self):
        self.lives = max(self.lives-1, 0)

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
        if not self.lives:  # no lives left, do not draw anything
            return
        velocity = self.dir * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.pos, velocity)
        self.bullets.append(bullet)
        self.snd_bullet.play()

    def draw(self, surface: Surface):
        if not self.lives:  # no lives left, do not draw anything
            return
        angle = self.dir.angle_to(DIR_UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())

        blit_pos = self.pos - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_pos)

    # def collides_with(self, other: 'GameObj'):
    #     if not self.lives:
    #         return
    #     collided = super().collides_with(other)
    #     return collided


class Rock(GameObj):
    MIN_START_GAP = 200
    MIN_SPEED = 1
    MAX_SPEED = 3
    rocks = []  # rocks container from main game, passed in from there upon init
    snd_boom = load_sound('boom')

    def __init__(self, pos: Vector2, size=3):
        _scale_map = {3: 1.0, 2: 0.5, 1: 0.25}
        self.size = size
        sprite = rotozoom(load_sprite('asteroid'), 0, _scale_map[size])
        speed = randint(self.MIN_SPEED, self.MAX_SPEED)
        angle = randint(0, 360)
        velocity = Vector2(speed, 0).rotate(angle)
        super().__init__(pos, sprite, velocity)

    @classmethod
    def create_random(cls, surface: Surface, ship_pos: Vector2):
        while True:  # do not be too close to ship
            pos = Vector2(randrange(surface.get_width()),
                          randrange(surface.get_height()))
            if pos.distance_to(ship_pos) > cls.MIN_START_GAP:
                break
        return Rock(pos)

    def play_boom_sound(self):
        self.snd_boom.play()

    def split(self):
        if self.size == 1:
            return
        # setting class attr, if using self then only instance changes
        type(self).rocks.append(Rock(self.pos, self.size-1))
        type(self).rocks.append(Rock(self.pos, self.size-1))


class Bullet(GameObj):
    def __init__(self, pos: Vector2, velocity):
        super().__init__(pos, load_sprite('bullet'), velocity, wraps=False)
