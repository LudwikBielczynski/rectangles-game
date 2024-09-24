import random
import sys
from time import time
from typing import TYPE_CHECKING, Literal

import pygame
from pygame.locals import QUIT
from pygame.math import Vector2
from pygame.sprite import Sprite

from game.config import (BLACK, BOUNCE, COLORS, HEIGHT, PLAYER_SIZE, WHITE,
                         WIDTH)
from game.objects import BasicObject, Player

if TYPE_CHECKING:
    from pygame.surface import Surface

CREATION_LAG = 2
FPS = 60


class App:
    def __init__(self):
        self._running = False
        self._display_surf = None
        self.size = self.width, self.height = WIDTH, HEIGHT
        self.sprites = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.player = None

        self.last_object_created = time()

    def on_game_init(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self._display_surf = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Game")

        self.player = Player(size=PLAYER_SIZE)
        self.sprites.add(self.player)

        # Initialize BasicObject objects
        o_list = []
        for o in range(0, 1):
            o = BasicObject(
                vel=(random.randint(0, 10), random.randint(0, 10)),
                friction=0,
            )
            self.objects.add(o)
            self.sprites.add(o)

        self._running = True

    def on_execute(self):
        if self._running == False:
            self.on_game_init()

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

        self.on_cleanup()

    def on_loop(self):
        self._display_surf.fill(BLACK)

        for o_idx, o in enumerate(self.objects):
            collide = self.player.rect.colliderect(o.rect)
            if collide:
                if self.player.color == o.color:
                    o.kill()
                    self.player.increase_size(10)

                else:
                    o.vel.x = -o.vel.x
                    o.vel.y = -o.vel.y
                    o.change_color()

                    if time() > self.last_object_created + CREATION_LAG:
                        for obj_idx in range(0, 4):
                            _o = BasicObject(
                                pos=(
                                    self.player.pos.x + PLAYER_SIZE,
                                    self.player.pos.y + PLAYER_SIZE,
                                ),
                                vel=(
                                    -self.player.vel.x + random.randint(0, 5),
                                    self.player.vel.y + random.randint(0, 5),
                                ),
                                friction=0,
                            )
                            self.objects.add(_o)
                            self.sprites.add(_o)

                            self.last_object_created = time()

                    self.player.next_color()
                    self.player.vel.x = -self.player.vel.x * BOUNCE
                    self.player.vel.y = -self.player.vel.y * BOUNCE

    def on_render(self):
        for sprite in self.sprites:
            sprite.move()
        self.sprites.draw(self._display_surf)

        pygame.display.update()
        self.clock.tick(FPS)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            _o = BasicObject(
                pos=pos,
                vel=(random.randint(0, 10), random.randint(0, 10)),
                friction=0,
            )
            self.objects.add(_o)
            self.sprites.add(_o)

    def on_cleanup(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = App()
    app.on_execute()
