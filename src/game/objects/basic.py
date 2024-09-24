import random
import sys
from typing import TYPE_CHECKING, Literal

import pygame
from pygame.math import Vector2
from pygame.sprite import Sprite

from game.config import (BLACK, COLORS, FRIC, HEIGHT, OBJ_SIZE, TOP_MARGIN,
                         WIDTH)

if TYPE_CHECKING:
    from pygame.surface import Surface


class BasicObject(Sprite):
    color: tuple[int, int, int] = BLACK

    def __init__(
        self,
        pos: tuple[float, float] | None = None,
        vel: tuple[float, float] | None = None,
        friction: float = FRIC,
        color: tuple[int, int, int] | None = None,
        size: int = OBJ_SIZE,
    ):
        super().__init__()
        self.size = size
        self.size_max = size * 3

        self.image = pygame.Surface((size, size))
        self.color_idx = 0
        self.change_color(color)

        self.rect = self.image.get_rect()

        if pos is None:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            self.pos = Vector2((x, y))
        else:
            self.pos = Vector2(pos[0], pos[1])

        if vel is None:
            vel = (random.randint(0, 10), random.randint(0, 10))
        self.vel = Vector2(vel[0], vel[1])
        self.acc = Vector2(0, 0)

        self.friction = friction

    def change_size(self, size: int):
        self.size = size
        self.image = pygame.transform.scale(self.image, (size, size))
        # self.rect = self.image.get_rect()

    def increase_size(self, size_increase: int):
        self.rect = self.rect.inflate(size_increase, size_increase)

        size = self.size + size_increase
        if size > self.size_max:
            size = self.size_max
        self.change_size(size)

    def change_color(self, color: tuple[int, int, int] | None = None):
        if color is None:
            self.color = random.choice(COLORS)
        else:
            self.color = color
        self.image.fill(self.color)

    def next_color(self):
        self.color_idx += 1
        if self.color_idx >= len(COLORS):
            self.color_idx = 0

        color = COLORS[self.color_idx]
        self.change_color(color)

    def draw(self, surface: "Surface"):
        surface.blit(self.image, self.rect)

    def move(self):
        self.acc = Vector2(0, 0)

        self.acc += self.vel * self.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        bounce_x = False
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
            bounce_x = True

        elif self.pos.x < 0:
            self.pos.x = 0
            bounce_x = True

        bounce_y = False
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT
            bounce_y = True

        elif self.pos.y < TOP_MARGIN:
            self.pos.y = TOP_MARGIN
            bounce_y = True

        if bounce_x:
            self._bounce("x")
        elif bounce_y:
            self._bounce("y")

        self.rect.midbottom = self.pos

    def _bounce(self, axis_name: Literal["x", "y"]):
        self.acc.__setattr__(axis_name, 0)
        vel = self.vel.__getattribute__(axis_name)
        self.vel.__setattr__(axis_name, -vel)
