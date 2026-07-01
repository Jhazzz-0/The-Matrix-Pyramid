# -*- coding: utf-8 -*-
"""Utilidades para dibujar pixel art egipcio mediante pygame."""
from typing import Tuple
import pygame
from core.constants import (
    RES_W, RES_H, SUNSET1, SUNSET2, SUNSET3, NIGHT1, NIGHT2,
    STONE, STONE_DARK, STONE_LIGHT, AMBER, GOLD, DOOR_CYAN, CYAN, WHITE
)


def draw_sunset_desert(surface: pygame.Surface):
    """Dibuja el fondo del desierto al atardecer para el menú"""
    w, h = surface.get_size()
    
    # Cielo en bandas degradadas
    for i, c in enumerate([SUNSET3, SUNSET2, SUNSET1]):
        pygame.draw.rect(surface, c, (0, int(h * i / 3), w, int(h / 3)))
    
    # Sol grande
    sun_r = min(w, h) // 4
    sun_center = (w // 2, h // 2)
    
    # Halo del sol
    for r in range(sun_r + 30, sun_r, -6):
        alpha_color = tuple(min(255, c + (sun_r + 30 - r) * 2) for c in AMBER)
        pygame.draw.circle(surface, alpha_color, sun_center, r, 3)
    
    pygame.draw.circle(surface, AMBER, sun_center, sun_r)
    pygame.draw.circle(surface, (255, 200, 100), sun_center, sun_r, 4)
    
    # Dunas de arena con más detalle
    dune_colors = [(220, 170, 90), (210, 160, 80), (200, 150, 70), (190, 140, 60), (180, 130, 50)]
    for i, color in enumerate(dune_colors):
        y = int(h * 0.55 + i * 18)
        points = [
            (0, y),
            (w * 0.2, y - 10),
            (w * 0.5, y + 5),
            (w * 0.8, y - 8),
            (w, y),
            (w, h),
            (0, h)
        ]
        pygame.draw.polygon(surface, color, points)
    
    # Pirámides principales
    def pyramid(cx, cy, size, base_color):
        left = (cx - size, cy + size // 2)
        top = (cx, cy - size // 2)
        right = (cx + size, cy + size // 2)
        bottom = (cx, cy + size // 2)
        
        # Lado izquierdo (más claro)
        pygame.draw.polygon(surface, base_color, [left, top, bottom])
        
        # Lado derecho (más oscuro)
        c2 = tuple(max(0, v - 50) for v in base_color)
        pygame.draw.polygon(surface, c2, [right, top, bottom])
        
        # Línea central (detalle)
        pygame.draw.line(surface, (255, 220, 140), top, bottom, 2)
        
        # Bloques de piedra
        for i in range(0, size // 2, 20):
            y_line = bottom[1] - i
            x_start = cx - (size - i * 2)
            x_end = cx + (size - i * 2)
            pygame.draw.line(surface, tuple(max(0, v - 20) for v in base_color), 
                           (x_start, y_line), (x_end, y_line), 1)
    
    # Tres pirámides
    pyramid(int(w * 0.25), int(h * 0.50), 120, (210, 160, 90))
    pyramid(int(w * 0.55), int(h * 0.45), 180, (205, 150, 80))
    pyramid(int(w * 0.75), int(h * 0.52), 100, (200, 155, 85))
    
    # Palmeras mejoradas
    def palm(x, y, scale=1.0):
        trunk_w = int(6 * scale)
        trunk_h = int(40 * scale)
        
        # Tronco con textura
        trunk = pygame.Rect(x, y, trunk_w, trunk_h)
        pygame.draw.rect(surface, (90, 60, 30), trunk)
        
        # Líneas de textura del tronco
        for i in range(0, trunk_h, 8):
            pygame.draw.line(surface, (70, 50, 25), 
                           (x, y + i), (x + trunk_w, y + i), 1)
        
        # Hojas (palmas)
        leaf_color = (20, 120, 60)
        leaf_dark = (15, 90, 45)
        leaves = [
            (-22, -12), (-10, -18), (0, -20), (10, -18), (22, -12),
            (-18, -6), (-8, -12), (8, -12), (18, -6)
        ]
        
        for dx, dy in leaves:
            # Hoja con sombra
            start = (x + trunk_w // 2, y)
            end = (x + trunk_w // 2 + int(dx * scale), y + int(dy * scale))
            pygame.draw.line(surface, leaf_dark, 
                           (start[0] + 1, start[1] + 1), 
                           (end[0] + 1, end[1] + 1), int(4 * scale))
            pygame.draw.line(surface, leaf_color, start, end, int(4 * scale))
    
    # Palmeras en diferentes posiciones
    palm(int(w * 0.12), int(h * 0.58), 1.2)
    palm(int(w * 0.88), int(h * 0.60), 1.0)
    palm(int(w * 0.05), int(h * 0.65), 0.8)


def draw_night_pyramid(surface: pygame.Surface):
    """Dibuja la pirámide nocturna para selección de niveles"""
    w, h = surface.get_size()
    
    # Degradado nocturno mejorado
    for i in range(h):
        t = i / h
        c = (
            int(NIGHT2[0] * (1-t) + NIGHT1[0] * t),
            int(NIGHT2[1] * (1-t) + NIGHT1[1] * t),
            int(NIGHT2[2] * (1-t) + NIGHT1[2] * t),
        )
        pygame.draw.line(surface, c, (0, i), (w, i))
    
    # Estrellas con diferentes tamaños
    import random
    random.seed(42)  # Mismas estrellas siempre
    
    for i in range(150):
        x = random.randint(0, w)
        y = random.randint(0, h // 2)
        brightness = random.randint(150, 255)
        
        if random.random() < 0.1:  # Estrellas grandes
            pygame.draw.circle(surface, (brightness, brightness, brightness), (x, y), 2)
        elif random.random() < 0.3:  # Estrellas medianas
            pygame.draw.rect(surface, (brightness, brightness, 255), (x, y, 2, 2))
        else:  # Estrellas pequeñas
            surface.set_at((x, y), (brightness, brightness, 255))
    
    # Luna
    moon_x, moon_y = int(w * 0.15), int(h * 0.15)
    moon_r = 35
    pygame.draw.circle(surface, (240, 240, 255), (moon_x, moon_y), moon_r)
    pygame.draw.circle(surface, (220, 220, 240), (moon_x + 8, moon_y - 6), moon_r - 5)
    
    # Pirámide central grande
    cx, cy = w // 2, int(h * 0.62)
    size = 280
    left = (cx - size, cy + size // 2)
    top = (cx, cy - size // 2)
    right = (cx + size, cy + size // 2)
    
    # Sombra de la pirámide
    shadow_offset = 8
    pygame.draw.polygon(surface, (15, 15, 25), 
                       [(p[0] + shadow_offset, p[1] + shadow_offset) for p in [left, top, right]])
    
    # Cuerpo de la pirámide
    pygame.draw.polygon(surface, STONE, [left, top, right])
    pygame.draw.polygon(surface, STONE_DARK, [left, top, right], 3)
    
    # Bloques y jeroglíficos (sin líneas horizontales)
    for row in range(12):
        y = int(cy - size * 0.45 + row * (size / 12))
        
        # Símbolos pseudo-jeroglíficos
        for col in range(10):
            if random.random() < 0.2:  # Reducido para menos símbolos
                bx = cx - size + 30 + col * 50 + (row % 2) * 15
                by = y + 8
                
                # Diferentes símbolos
                symbol_type = (row + col) % 4
                if symbol_type == 0:  # Rectángulo
                    pygame.draw.rect(surface, STONE_DARK, (bx, by, 4, 6))
                elif symbol_type == 1:  # Línea
                    pygame.draw.line(surface, STONE_DARK, (bx, by), (bx + 4, by + 6), 1)
                elif symbol_type == 2:  # Punto
                    pygame.draw.circle(surface, STONE_DARK, (bx + 2, by + 3), 2)
                else:  # Cruz
                    pygame.draw.line(surface, STONE_DARK, (bx, by), (bx + 4, by + 4), 1)
                    pygame.draw.line(surface, STONE_DARK, (bx + 4, by), (bx, by + 4), 1)
    
    # Entrada de la pirámide
    entrance_w = 60
    entrance_h = 80
    entrance_x = cx - entrance_w // 2
    entrance_y = cy + size // 2 - entrance_h
    
    pygame.draw.rect(surface, (10, 10, 15), 
                    (entrance_x, entrance_y, entrance_w, entrance_h))
    pygame.draw.rect(surface, (40, 35, 30), 
                    (entrance_x, entrance_y, entrance_w, entrance_h), 3)
    
    # Suelo desértico
    ground_y = int(h * 0.80)
    pygame.draw.rect(surface, (35, 30, 40), (0, ground_y, w, h - ground_y))
    
    # Dunas en el suelo
    for i in range(5):
        dune_y = ground_y + i * 12
        dune_color = (30 + i * 3, 28 + i * 2, 38 + i * 2)
        points = [(0, dune_y), (w * 0.3, dune_y - 6), (w * 0.7, dune_y + 4), (w, dune_y), (w, h), (0, h)]
        pygame.draw.polygon(surface, dune_color, points)


def draw_tomb_interior(surface: pygame.Surface):
    """Dibuja el interior de la tumba para el juego"""
    w, h = surface.get_size()
    surface.fill((30, 20, 16))
    
    # Pared con bloques de piedra detallados
    block_size = 32
    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            # Bloque base
            block_color = (
                STONE[0] + ((x + y) % 20 - 10),
                STONE[1] + ((x + y) % 15 - 7),
                STONE[2] + ((x + y) % 10 - 5)
            )
            pygame.draw.rect(surface, block_color, (x, y, block_size, block_size))
            
            # Bordes del bloque
            pygame.draw.rect(surface, STONE_DARK, (x, y, block_size, block_size), 1)
            
            # Grietas y detalles
            if ((x // block_size + y // block_size) % 3) == 0:
                crack_x = x + block_size // 3
                crack_y = y + block_size // 4
                pygame.draw.line(surface, STONE_DARK, 
                               (crack_x, crack_y), 
                               (crack_x + block_size // 3, crack_y + block_size // 2), 1)
            
            # Símbolo jeroglífico ocasional
            if ((x // block_size + y // block_size) % 7) == 0:
                symbol_x = x + block_size // 2 - 2
                symbol_y = y + block_size // 2 - 2
                pygame.draw.rect(surface, STONE_LIGHT, (symbol_x, symbol_y, 4, 4))
    
    # Antorchas decorativas
    # Calculamos el flicker basado en el tiempo (sin import adicional)
    import time
    flicker = int((time.time() * 4) % 4)  # Cambia cada 0.25 segundos
    
    torch_positions = [(30, 30), (w - 50, 30)]
    
    for torch_x, torch_y in torch_positions:
        # Soporte de la antorcha
        pygame.draw.rect(surface, (80, 40, 20), (torch_x + 2, torch_y, 6, 32))
        
        # Llama
        flame_center = (torch_x + 5, torch_y - 10)
        
        # Llama con efecto parpadeante (ya calculado arriba)
        # Llama exterior (naranja)
        flame_points = [
            (flame_center[0], flame_center[1] - 15 - flicker),
            (flame_center[0] - 8, flame_center[1]),
            (flame_center[0] + 8, flame_center[1])
        ]
        pygame.draw.polygon(surface, (255, 140, 0), flame_points)
        
        # Llama interior (amarilla)
        inner_flame = [
            (flame_center[0], flame_center[1] - 10 - flicker),
            (flame_center[0] - 4, flame_center[1]),
            (flame_center[0] + 4, flame_center[1])
        ]
        pygame.draw.polygon(surface, (255, 220, 80), inner_flame)
        
        # Resplandor
        for r in range(15, 5, -3):
            alpha_color = (255, 200 - r * 8, 80 - r * 4)
            pygame.draw.circle(surface, alpha_color, flame_center, r, 1)


def draw_pixel_text(surface: pygame.Surface, text: str, pos: Tuple[int, int], 
                    color=WHITE, scale: int = 2):
    """Dibuja texto pixel art"""
    pygame.font.init()
    f = pygame.font.Font(None, 16)
    img = f.render(text, False, color)
    
    if scale != 1:
        new_w = img.get_width() * scale
        new_h = img.get_height() * scale
        img = pygame.transform.scale(img, (new_w, new_h))
    
    surface.blit(img, pos)


def make_stone_button_surface(text: str, w: int, h: int, state: str="normal", 
                              scale: int=2) -> pygame.Surface:
    """
    Crea un Surface (RGB) con un botón tipo piedra estilo pixel.
    state: "normal" | "hover" | "pressed"
    """
    surf = pygame.Surface((w, h))
    surf.fill((0, 0, 0))

    # Paleta según estado
    if state == "pressed":
        base = (95, 88, 80)
        top = (75, 68, 60)
        shine = (140, 132, 122)
        shadow = (55, 48, 42)
        text_col = GOLD
    elif state == "hover":
        base = (125, 116, 106)
        top = (105, 96, 88)
        shine = (170, 160, 150)
        shadow = (65, 56, 48)
        text_col = GOLD
    else:
        base = (112, 104, 95)
        top = (92, 84, 76)
        shine = (155, 145, 135)
        shadow = (60, 52, 45)
        text_col = AMBER

    # Fondo del botón
    r = pygame.Rect(0, 0, w, h)
    pygame.draw.rect(surf, base, r)

    # Bisel 3D
    border = 6
    pygame.draw.rect(surf, shadow, (0, 0, w, h), 0)
    pygame.draw.rect(surf, base, (border, border, w-2*border, h-2*border))
    
    # Luces y sombras
    pygame.draw.line(surf, shine, (border, border), (w-border, border), 3)
    pygame.draw.line(surf, shine, (border, border), (border, h-border), 3)
    pygame.draw.line(surf, top, (border, h-border), (w-border, h-border), 3)
    pygame.draw.line(surf, top, (w-border, border), (w-border, h-border), 3)

    # Grietas decorativas
    crack = shadow
    for x in range(border+15, w-border-15, 45):
        pygame.draw.line(surf, crack, (x, border+12), (x+10, border+22), 2)
    
    if w > 100:
        pygame.draw.line(surf, crack, (w//3, h//2), (w//3+20, h//2+12), 2)
        pygame.draw.line(surf, crack, (2*w//3, h//2+10), (2*w//3-12, h//2+24), 2)

    # Marco exterior
    pygame.draw.rect(surf, (40, 32, 28), r, 4)

    # Texto centrado
    text_w = len(text) * 6 * scale
    x = max(10, (w - text_w) // 2)
    y = (h // 2) - (8 * scale) // 2
    
    # Sombra del texto
    draw_pixel_text(surf, text, (x + 2, y + 2), (30, 22, 18), scale=scale)
    # Texto principal
    draw_pixel_text(surf, text, (x, y), text_col, scale=scale)

    return surf