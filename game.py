import random
from typing import Literal

from constant import *
from tile import Tile

pygame.init()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")


def draw_grid(window: pygame.Surface):
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)


def draw(window: pygame.Surface, tiles: dict[str, Tile], status: Literal["continue", "lose"] = "continue"):
    window.fill(BACKGROUND_COLOR)

    for tile in tiles.values():
        tile.draw(window)
        draw_grid(window)

    if status == "lose":
        lose_text = FONT.render("YOU LOSE", 1, "red")
        restart_text = FONT.render("PRESS R TO PLAY AGAIN", 1, "red")
        window.blit(
            lose_text,
            (
                (WIDTH / 2 - lose_text.get_width() / 2),
                (HEIGHT / 2 - lose_text.get_height() / 2) - 50
            )
        )
        window.blit(
            restart_text,
            (
                (WIDTH / 2 - restart_text.get_width() / 2),
                (HEIGHT / 2 - restart_text.get_height() / 2) + 50
            )
        )

    pygame.display.update()


def get_random_pos(tiles: dict[str, Tile]) -> tuple[int, int]:
    row = None
    col = None
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)

        if f"{row}{col}" not in tiles:
            break
    return row, col


def move_tiles(
        window: pygame.Surface,
        tiles: dict[str, Tile],
        clock,
        direction: Literal['left', 'right', 'up', 'down']
) -> Literal["continue", "lost"]:
    updated = True
    blocks = set()

    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL
        move_check = lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
        ceil = True

    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check = lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        ceil = False

    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check = lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        ceil = True

    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, MOVE_VEL)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check = lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y
        ceil = False

    else:
        raise ValueError(f"Unknown direction {direction}")

    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue
            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif (
                    tile.value == next_tile.value
                    and tile not in blocks
                    and tile not in blocks
            ):
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *= 2
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue

            tile.set_pos(ceil)
            updated = True

        update_tiles(window, tiles, sorted_tiles)

    return end_move(tiles)


def end_move(tiles: dict[str, Tile]) -> Literal["continue", "lost"]:
    if len(tiles) == 16:
        return "lost"

    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"


def update_tiles(
        window: pygame.Surface,
        tiles: dict[str, Tile],
        sorted_tiles: list[Tile]
) -> None:
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

    draw(window, tiles)


def generate_tiles() -> dict[str, Tile]:
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)
    return tiles


def main(window: pygame.Surface):
    clock = pygame.time.Clock()
    run = True

    tiles = generate_tiles()
    status = "continue"

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    tiles = generate_tiles()
                if event.key == pygame.K_LEFT:
                    status = move_tiles(window, tiles, clock, "left")
                if event.key == pygame.K_RIGHT:
                    status = move_tiles(window, tiles, clock, "right")
                if event.key == pygame.K_UP:
                    status = move_tiles(window, tiles, clock, "up")
                if event.key == pygame.K_DOWN:
                    status = move_tiles(window, tiles, clock, "down")

        draw(window, tiles, status)

    pygame.quit()


if __name__ == "__main__":
    main(WINDOW)
