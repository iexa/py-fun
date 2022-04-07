from pygame.math import Vector2
from pygame import Surface


class GameObj:
    def __init__(self, pos, sprite: Surface, velocity):
        self.pos = Vector2(pos)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    
    def draw(self, surface: Surface):
        pos = self.pos - Vector2(self.radius)
        surface.blit(self.sprite, pos)

    
    def move(self):
        self.pos = self.pos + self.velocity


    def collides_with(self, other: 'GameObj'):
        distance = self.pos.distance_to(other.pos)
        return distance < self.radius + other.radius

