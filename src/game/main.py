import random
import sys
from typing import TYPE_CHECKING, Literal

import pygame
from pygame.locals import QUIT
from pygame.math import Vector2
from pygame.sprite import Sprite

from game.config import BOUNCE, COLORS, HEIGHT, PLAYER_SIZE, WHITE, WIDTH
from game.objects import Other, Player

if TYPE_CHECKING:
    from pygame.surface import Surface


FPS = 60


pygame.init()


FRAME_PER_SEC = pygame.time.Clock()

DISPLAY_SURFACE = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")



sprites = pygame.sprite.Group()

# Initialize player
p_1 = Player(size=PLAYER_SIZE)
sprites.add(p_1)


# Initialize object
o_list = []
for o in range(0, 1):
    color_idx = random.randint(0, len(COLORS) - 1)
    color = COLORS[color_idx]
    o = Other(
        vel=(random.randint(0, 10), random.randint(0, 10)), friction=0, color=color
    )
    o_list.append(o)
    sprites.add(o)

# Event loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # elif event.type == COLLID

    DISPLAY_SURFACE.fill(WHITE)
    for sprite in sprites:
        sprite.move()
        sprite.draw(DISPLAY_SURFACE)

    p_1.move()
    # p_1.draw(DISPLAY_SURFACE)

    for o_idx, o in enumerate(o_list):
        collide = p_1.rect.colliderect(o.rect)
        if collide:
            # o_list.pop(idx)
            # o.move()
            # o.draw(DISPLAY_SURFACE)

            o.vel.x = -o.vel.x
            o.vel.y = -o.vel.y
            o.change_color()
            # o.draw(DISPLAY_SURFACE)

            for obj_idx in range(0, 1):
                _o = Other(
                    pos=(p_1.pos.x + PLAYER_SIZE, p_1.pos.y + PLAYER_SIZE),
                    vel=(-p_1.vel.x, p_1.vel.y),
                    friction=0,
                )
                # _o.draw(DISPLAY_SURFACE)
                o_list.append(_o)
                sprites.add(_o)

            # o.vel.x = 0
            # o.vel.y = 0

            p_1.change_color()
            # p_1.draw(DISPLAY_SURFACE)
            p_1.vel.x = -p_1.vel.x * BOUNCE
            p_1.vel.y = -p_1.vel.y * BOUNCE

    pygame.display.update()
    FRAME_PER_SEC.tick(FPS)
