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
        vel: tuple[float, float] = [0.0, 0.0],
        friction: float = FRIC,
        color: tuple[int, int, int] | None = None,
        size: int = OBJ_SIZE,
    ):
        super().__init__()
        self.size = size
        self.surf = pygame.Surface((size, size))
        if color is None:
            color = random.choice(COLORS)
        self.surf.fill(color)
        self.rect = self.surf.get_rect()

        if pos is None:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            self.pos = Vector2((x, y))
        else:
            self.pos = Vector2(pos[0], pos[1])

        self.vel = Vector2(vel[0], vel[1])
        self.acc = Vector2(0, 0)

        self.friction = friction

    def change_color(self):
        color_idx = random.randint(0, len(COLORS) - 1)
        self.color = COLORS[color_idx]
        self.surf.fill(self.color)

    def draw(self, surface: "Surface"):
        surface.blit(self.surf, self.rect)

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
