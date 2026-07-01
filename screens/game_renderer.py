# -*- coding: utf-8 -*-
from typing import Tuple, Dict
# pyrefly: ignore [missing-import]
import pygame
from core.constants import (
    GAME_CANVAS_W, GAME_CANVAS_H, GOLD, DOOR_CYAN, CYAN, WHITE, BLACK, STONE, STONE_DARK
)
from core.egypt_pixel import draw_tomb_interior, draw_pixel_text
from core.grid_logic import grid_to_px
from core.game_state import GameState

# ============================================================================
# BITMAPS PIXEL ART (Sprites definidos por código sin recursos externos)
# ============================================================================

# Arqueólogo (Indiana Jones style) en 16x16 píxeles
PLAYER_SPRITE = [
    "....HHHHHH......",
    "...HHHHHHHH.....",
    "...HBBBBBBH.....",
    "H HHHHHHHHHHHH..",
    "....SSSSS.......",
    "....SESES.......",
    "....SSSSS.......",
    "...JJJJJJJ......",
    "..JJCJCJCJJ.....",
    "..JJJJJJJJJ.....",
    "..JJWJJWJJJ.....",
    "...JJJJJJJ......",
    "....PP.PP.......",
    "....PP.PP.......",
    "....KK.KK.......",
    "...KKK.KKK......"
]

PLAYER_COLORS = {
    'H': (139, 90, 43),    # Sombrero marrón
    'B': (60, 45, 30),     # Banda oscura del sombrero
    'S': (244, 164, 96),   # Piel / Cabeza
    'E': (0, 0, 0),        # Ojos negros
    'J': (160, 110, 60),   # Chaqueta
    'C': (240, 240, 220),  # Camisa clara
    'W': (90, 50, 20),     # Correa de cuero
    'P': (50, 80, 120),    # Pantalón azul
    'K': (40, 30, 20),     # Botas de cuero oscuras
}

# Llave Ankh (Dorada con brillo) en 8x12 píxeles
ANKH_SPRITE = [
    "..DDD...",
    ".DGWGD..",
    ".DG.GD..",
    ".DGWGD..",
    "..DDD...",
    ".DDDDD..",
    "DGGGGGD.",
    ".DDDDD..",
    "..GD....",
    "..GD....",
    "..GD....",
    "..DD...."
]

ANKH_COLORS = {
    'G': (255, 215, 0),    # Oro brillante
    'D': (180, 130, 20),   # Oro sombreado / bordes
    'W': (255, 255, 200)   # Brillo blanco
}

# Puerta de Salida EXIT (Portal mágico) en 12x16 píxeles
EXIT_DOOR_SPRITE = [
    "..SSSSSSSS..",
    ".SBBBBBBBBS.",
    "SBPPPPPPPPSB",
    "SPGGPPPPGGPS",
    "SPPPPPPPPPPS",
    "SPPPPPPPPPPS",
    "SPPGGGGGPBPS",
    "SPPPPPPPPPPS",
    "SPPPPPPPPPPS",
    "SPGGPPPPGGPS",
    "SPPPPPPPPPPS",
    "SPPPPPPPPPPS",
    "SPPGGGGGPBPS",
    "SPPPPPPPPPPS",
    "SPPPPPPPPPPS",
    "SBBBBBBBBBBS"
]

EXIT_DOOR_COLORS = {
    'S': (80, 70, 60),     # Bloques de piedra
    'P': (0, 200, 200),    # Portal cyan
    'G': (150, 255, 255),  # Glifo luminoso
    'B': (0, 100, 100)     # Aura/Borde del portal
}

# Paredes de Ladrillos de Arena en 16x16 píxeles
WALL_SPRITE = [
    "LLLLLLLLLLDLLLLL",
    "LSSSSSSSSDMLSSSS",
    "LSSSSSSSSDMLSSSS",
    "DDDDDDDDDDDDDDDD",
    "LLLLLLDLLLLLLLLL",
    "LSSSSSDMLSSSSSSS",
    "LSSSSSDMLSSSSSSS",
    "DDDDDDDDDDDDDDDD",
    "LLLLLLLLLLDLLLLL",
    "LSSSSSSSSDMLSSSS",
    "LSSSSSSSSDMLSSSS",
    "DDDDDDDDDDDDDDDD",
    "LLLLLLDLLLLLLLLL",
    "LSSSSSDMLSSSSSSS",
    "LSSSSSDMLSSSSSSS",
    "DDDDDDDDDDDDDDDD"
]

WALL_COLORS = {
    'S': (160, 130, 95),   # Piedra arenisca
    'L': (200, 175, 140),  # Brillo de luz superior
    'D': (120, 95, 65),    # Sombra del bloque
    'M': (80, 60, 45)      # Mortero / División vertical
}

# Trampas de Pinchos de Hierro en 16x16 píxeles
TRAP_SPRITE = [
    "TTTTTTTTTTTTTTTT",
    "TppppppppppppppT",
    "Tp.R.pp.R.pp.R.pT",
    "TpRSRppRSRppRSRpT",
    "Tp.S.pp.S.pp.S.pT",
    "TppppppppppppppT",
    "T.R.pp.R.pp.R.p.T",
    "TRSRppRSRppRSRp.T",
    "T.S.pp.S.pp.S.p.T",
    "TppppppppppppppT",
    "Tp.R.pp.R.pp.R.pT",
    "TpRSRppRSRppRSRpT",
    "Tp.S.pp.S.pp.S.pT",
    "TppppppppppppppT",
    "TppppppppppppppT",
    "TTTTTTTTTTTTTTTT"
]

TRAP_COLORS = {
    'T': (110, 75, 50),    # Madera del marco
    'p': (35, 22, 17),     # Oscuridad de la fosa
    'R': (200, 40, 40),    # Sangre/Óxido en pinchos
    'S': (210, 210, 210),  # Metal afilado
    '.': (35, 22, 17)
}


class GameRenderer:
    """
    Renderizador del Juego (MVC - View Renderer Component).
    Se encarga exclusivamente del dibujado pixel art del escenario del juego sobre
    una superficie de pygame, implementando el Single Responsibility Principle (SRP).
    """
    def __init__(self):
        self.cell = 0
        self.grid_origin = (0, 0)
        
    def draw_sprite(self, surface: pygame.Surface, x_start: int, y_start: int, 
                    size: int, sprite: list, colors: dict, padding: int = 4):
        """Dibuja un sprite de caracteres escalando los píxeles a la grilla"""
        rows = len(sprite)
        cols = len(sprite[0])
        
        # Calcular el tamaño de cada pixel del sprite
        usable_size = size - padding * 2
        pixel_size = max(1, usable_size // max(rows, cols))
        
        # Centrar el sprite dentro de la celda
        ox = x_start + (size - cols * pixel_size) // 2
        oy = y_start + (size - rows * pixel_size) // 2
        
        for r in range(rows):
            for c in range(cols):
                char = sprite[r][c]
                if char in colors:
                    pygame.draw.rect(
                        surface,
                        colors[char],
                        (ox + c * pixel_size, oy + r * pixel_size, pixel_size, pixel_size)
                    )

    def render(self, s: pygame.Surface, state: GameState):
        """Dibuja el mundo del juego sobre la superficie provista"""
        # Dibujar el fondo del interior de la tumba
        draw_tomb_interior(s)
        
        # Calcular dimensiones de la grilla
        margin = 30
        usable_w = GAME_CANVAS_W - margin * 2
        usable_h = GAME_CANVAS_H - margin * 2
        
        grid_n = state.grid_size
        self.cell = min(usable_w // grid_n, usable_h // grid_n)
        
        # Ajustar tamaño máximo de celda para niveles pequeños
        if grid_n <= 3:
            self.cell = min(self.cell, 120)
        
        grid_px_w = self.cell * grid_n
        grid_px_h = self.cell * grid_n
        
        ox = (GAME_CANVAS_W - grid_px_w) // 2
        oy = (GAME_CANVAS_H - grid_px_h) // 2
        self.grid_origin = (ox, oy)
        
        # 1. Dibujar piso de arena con textura de granos pixelados
        for gy in range(grid_n):
            for gx in range(grid_n):
                x, y = grid_to_px((gx, gy), self.grid_origin, self.cell)
                sand_color = (170, 140, 90)
                
                # Variación de color tipo damero
                if (gx + gy) % 2 == 0:
                    sand_color = (165, 135, 85)
                
                pygame.draw.rect(s, sand_color, (x+1, y+1, self.cell-2, self.cell-2))
                
                # Añadir granos de arena pixelados para dar textura
                grain_color = (180, 150, 100) if (gx + gy) % 2 == 0 else (155, 125, 75)
                pixel_unit = max(1, self.cell // 16)
                
                # Dibujar unos granos esparcidos
                s.set_at((x + 3 * pixel_unit, y + 4 * pixel_unit), grain_color)
                s.set_at((x + 12 * pixel_unit, y + 3 * pixel_unit), grain_color)
                s.set_at((x + 6 * pixel_unit, y + 10 * pixel_unit), grain_color)
                s.set_at((x + 11 * pixel_unit, y + 11 * pixel_unit), grain_color)
        
        # 2. Dibujar trampillas (casillas peligrosas)
        for trap_pos in state.traps:
            tx, ty = grid_to_px(trap_pos, self.grid_origin, self.cell)
            self.draw_sprite(s, tx, ty, self.cell, TRAP_SPRITE, TRAP_COLORS, padding=2)
        
        # 3. Dibujar paredes de ladrillo pixeladas
        for wall_pos in state.walls:
            wx, wy = grid_to_px(wall_pos, self.grid_origin, self.cell)
            self.draw_sprite(s, wx, wy, self.cell, WALL_SPRITE, WALL_COLORS, padding=1)
        
        # 4. Líneas de grilla (más oscuras y sutiles para que resalte el arte)
        grid_line_color = (15, 100, 100) # Cyan oscuro transparente
        for i in range(grid_n + 1):
            lx = ox + i * self.cell
            ly = oy + i * self.cell
            pygame.draw.line(s, grid_line_color, (lx, oy), (lx, oy + grid_px_h), 2)
            pygame.draw.line(s, grid_line_color, (ox, ly), (ox + grid_px_w, ly), 2)
        
        # 5. Llave Ankh (si no ha sido recogida)
        if not state.has_key:
            kx, ky = grid_to_px(state.key_pos, self.grid_origin, self.cell)
            
            # Efecto de levitación animada usando ticks
            levitation = int(pygame.time.get_ticks() / 250) % 4
            self.draw_sprite(s, kx, ky - levitation, self.cell, ANKH_SPRITE, ANKH_COLORS, padding=8)
            
            # Brillo de luz de la llave (partículas sutiles)
            cx, cy = kx + self.cell // 2, ky + self.cell // 2 - levitation
            pulse = int(abs(pygame.time.get_ticks() / 200 % 6 - 3))
            pygame.draw.circle(s, (255, 255, 150), (cx, cy), pulse + 10, 1)
        
        # 6. Puerta EXIT
        ex, ey = grid_to_px(state.exit_pos, self.grid_origin, self.cell)
        self.draw_sprite(s, ex, ey, self.cell, EXIT_DOOR_SPRITE, EXIT_DOOR_COLORS, padding=2)
        
        # Texto EXIT arriba de la puerta
        exit_scale = 1 if self.cell < 60 else 2
        draw_pixel_text(s, "EXIT", (ex + (self.cell - 20 * exit_scale) // 2, ey - 22), DOOR_CYAN, scale=exit_scale)
        
        # 7. Arqueólogo (Jugador en 16x16 pixel-art)
        px, py = grid_to_px(state.player, self.grid_origin, self.cell)
        self.draw_sprite(s, px, py, self.cell, PLAYER_SPRITE, PLAYER_COLORS, padding=4)
        
        # 8. Mensaje inferior
        bottom_msg = f"Grid: {grid_n}×{grid_n} | Pos: {state.player}"
        draw_pixel_text(s, bottom_msg, (10, GAME_CANVAS_H - 22), WHITE, scale=1)
