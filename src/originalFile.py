import sys

import pygame

from src.gameboard.Board import Board
from src.gameboard.Hexagon import Hexagon

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_board = Board()

pygame.display.set_caption('Catan Clone')

pygame.init()

# make background black
game_window.fill((0, 0, 0))
pygame.display.init()

# hexagon radius
hex_size = 50

# colors for tiles
color_dictionary = {
    'Black': (0, 0, 0),
    'Ocean': (0, 105, 181),
    'Purple': (51, 0, 77),
    'Brick': (102, 0, 0),
    'Ore': (96, 96, 96),
    'Sheep': (76, 153, 0),
    'Wood': (0, 102, 0),
    'Wheat': (204, 204, 0),
    'Desert': (255, 164, 104)
}

base_hexagon = Hexagon(hex_size, False)
base_hexagon_integer = []
for point in base_hexagon.points:
    base_hexagon_integer.append((int(point[0]) + 400, int(point[1]) + 300))

ocean_hexagon = []
for point in Hexagon(int(hex_size * 6), True).points:
    ocean_hexagon.append((int(point[0] + center[0]), int(point[1] + center[1])))

resource_hexes = game_board.land_list
ocean_hexes = game_board.ocean_list

running = True
ran_once = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # hexes
    for tile in resource_hexes:
        pygame.draw.polygon(game_window,
                            color_dictionary.get(tile.resource),
                            base_hexagon.offset_pointy(tile.location, center),
                            0)
    # outlines
    for tile in resource_hexes:
        pygame.draw.polygon(game_window,
                            color_dictionary.get('Black'),
                            base_hexagon.offset_pointy(tile.location, center),
                            2)
    # circles
    for tile in resource_hexes:
        for points in base_hexagon.offset_pointy(tile.location, center):
            radius = 5

            pygame.draw.circle(game_window, (0, 0, 0),
                               (int(points[0]), int(points[1])), radius)

    pygame.display.update()
    ran_once = True

pygame.quit()
sys.exit()
