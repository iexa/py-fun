from pygame.math import Vector2
from pygame.transform import rotozoom
from pygame import Surface

DIR_UP = Vector2(0, -1)


class GameObj:
    def __init__(self, pos, sprite: Surface, velocity):
        self.pos = Vector2(pos)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    
    def draw(self, surface: Surface):
        pos = self.pos - Vector2(self.radius) # convert from center to top-left based coord
        surface.blit(self.sprite, pos)

    
    def move(self):
        self.pos = self.pos + self.velocity


    def collides_with(self, other: 'GameObj'):
        distance = self.pos.distance_to(other.pos)
        return distance < self.radius + other.radius



class Ship(GameObj):
    ROTATION_SPEED = 3

    def __init__(self, pos, sprite: Surface):
        self.dir = Vector2(DIR_UP)
        super().__init__(pos, sprite, (0,0))

    
    def rotate(self, clockwise = True):
        sign = 1 if clockwise else -1
        angle = self.ROTATION_SPEED * sign
        self.dir.rotate_ip(angle) # _ip = in_place


    def draw(self, surface: Surface):
        angle = self.dir.angle_to(DIR_UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())

        blit_pos = self.pos - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_pos)


