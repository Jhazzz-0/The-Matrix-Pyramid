# -*- coding: utf-8 -*-
"""
Lógica de movimiento en la grilla con soporte para:
- Múltiples vectores
- Paredes/obstáculos
- Validación de movimientos
"""
from typing import Tuple

def grid_to_px(grid_pos: Tuple[int, int], origin: Tuple[int, int], cell_size: int) -> Tuple[int, int]:
    """Convierte posición de grilla a píxeles en pantalla"""
    gx, gy = grid_pos
    ox, oy = origin
    return ox + gx * cell_size, oy + gy * cell_size

def is_inside(gx: int, gy: int, n: int) -> bool:
    """Verifica si la posición está dentro de la grilla NxN"""
    return 0 <= gx < n and 0 <= gy < n

def try_move(state, scalars: dict) -> Tuple[bool, str]:
    """
    Intenta mover al jugador usando combinación lineal de vectores.
    
    Args:
        state: GameState con la información del nivel
        scalars: dict con los valores escalares para cada vector
                 ej: {"Ca": 2, "Cb": 1, "Cc": 0}
    
    Returns:
        Tuple[bool, str]: (éxito, mensaje)
    """
    if state.win:
        return False, "Ya ganaste este nivel"
    
    # Calcular desplazamiento total: suma de Ca*U + Cb*V + Cc*W + ...
    dx = 0
    dy = 0
    
    # Mapeo de nombres de escalares a nombres de vectores
    scalar_to_vector = {
        "Ca": "U",
        "Cb": "V", 
        "Cc": "W",
        "Cd": "X"
    }
    
    for scalar_name, vector_name in scalar_to_vector.items():
        if vector_name in state.vectors and scalar_name in scalars:
            vector = state.vectors[vector_name]
            scalar = scalars[scalar_name]
            dx += scalar * vector[0]
            dy += scalar * vector[1]
    
    # Nueva posición
    nx = state.player[0] + dx
    ny = state.player[1] + dy
    new_pos = (nx, ny)
    
    # Validar movimiento
    if not is_inside(nx, ny, state.grid_size):
        return False, "Movimiento fuera de la grilla"
    
    if state.is_wall(new_pos):
        return False, "¡Hay una pared! No puedes pasar"
    
    # Ejecutar movimiento
    state.player = new_pos
    state.moves_count += 1
    
    # NUEVO: Verificar si cayó en una trampilla
    if state.is_trap(new_pos):
        state.reset_player_position()
        return True, f"💀 ¡TRAMPA! Vuelves al inicio. Caídas: {state.trap_falls}"
    
    # Verificar si recogió la llave
    if not state.has_key and state.player == state.key_pos:
        state.has_key = True
        return True, "✨ ¡Llave obtenida! Dirígete a la puerta"
    
    # Verificar victoria
    if state.player == state.exit_pos and state.has_key:
        state.win = True
        state.complete_current_level()
        return True, f"🎉 ¡VICTORIA! Completado en {state.moves_count} movimientos"
    
    # Movimiento normal
    if state.has_key:
        return True, "Busca la puerta EXIT 🚪"
    else:
        return True, f"Sigue buscando la llave 🔑 (Movimientos: {state.moves_count})"

def get_available_vector_names(state) -> list:
    """Retorna la lista de nombres de vectores disponibles en el nivel actual"""
    return sorted(state.vectors.keys())