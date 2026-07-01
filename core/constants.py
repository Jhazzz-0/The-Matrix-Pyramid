# -*- coding: utf-8 -*-
from typing import Tuple

# Resolución base para los canvas de pygame
RES_W, RES_H = 960, 540
FPS = 60

# Juego
GRID_N = 4
GAME_CANVAS_W = 640
GAME_CANVAS_H = 480

# Colores RGB
COL = lambda r, g, b: (r, g, b)
WHEAT = COL(245, 222, 179)
SAND = COL(230, 200, 132)
SUNSET1 = COL(255, 132, 68)
SUNSET2 = COL(206, 73, 61)
SUNSET3 = COL(124, 68, 90)
NIGHT1 = COL(18, 18, 38)
NIGHT2 = COL(36, 36, 66)
STONE_DARK = COL(60, 44, 36)
STONE = COL(94, 76, 66)
STONE_LIGHT = COL(140, 120, 100)
CYAN = COL(0, 200, 255)
GOLD = COL(255, 208, 0)
DOOR_CYAN = COL(0, 190, 170)
BLACK = COL(0, 0, 0)
WHITE = COL(255, 255, 255)
AMBER = COL(255, 170, 40)

# Vectores del nivel 1
U = (1, 0)
V = (0, 1)
