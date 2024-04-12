import math

import pygame

from constant import RECT_WIDTH, RECT_HEIGHT, FONT, TEXT_COLOR


class Tile:
    COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]

    def __init__(self, value: int, row: int, col: int):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT

    @property
    def color(self) -> tuple[int, int, int]:
        color_index = int(math.log2(self.value)) - 1
        color = self.COLORS[color_index]
        return color

    def draw(self, window: pygame.Surface):
        pygame.draw.rect(
            window,
            self.color,
            (self.x, self.y, RECT_WIDTH, RECT_HEIGHT)
        )
        text = FONT.render(str(self.value), 1, TEXT_COLOR)
        window.blit(
            text,
            (
                self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2)
            )
        )

    def move(self, delta: list[int, int] | tuple[int, int]):
        self.x += delta[0]
        self.y += delta[1]

    def set_pos(self, ceil: bool = False):
        if ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)
