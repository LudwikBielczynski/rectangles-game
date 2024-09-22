from typing import Literal

import pygame
from pygame.locals import K_DOWN, K_LEFT, K_RIGHT, K_UP
from pygame.math import Vector2

from game.config import ACC, BLUE, FRIC, HEIGHT, OBJ_SIZE, WIDTH
from game.objects import BasicObject


class Player(BasicObject):
    color = BLUE

    def __init__(
        self,
        pos: tuple[float, float] | None = None,
        vel: tuple[float, float] | None = None,
        friction: float = FRIC,
        color: tuple[int, int, int] | None = None,
        size: int = OBJ_SIZE,
    ):
        super().__init__(
            pos=pos, vel=(0, 0), friction=friction, color=self.color, size=size
        )

    def move(self):
        self.acc = Vector2(0, 0)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        if pressed_keys[K_UP]:
            self.acc.y = -ACC
        if pressed_keys[K_DOWN]:
            self.acc.y = ACC

        self.acc += self.vel * FRIC
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

        elif self.pos.y < self.size:
            self.pos.y = self.size
            bounce_y = True

        if bounce_x:
            self._bounce("x")
            self.change_color()
        elif bounce_y:
            self._bounce("y")
            self.change_color()

        self.rect.midbottom = self.pos

    def _bounce(self, axis_name: Literal["x", "y"]):
        self.acc.__setattr__(axis_name, 0)
        vel = self.vel.__getattribute__(axis_name)
        self.vel.__setattr__(axis_name, -vel)
