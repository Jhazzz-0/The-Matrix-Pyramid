# -*- coding: utf-8 -*-
"""
Configuración de los 6 niveles del juego The Matrix Pyramid.
Estructura de pirámide: 
  Nivel 6 (cima)
  Niveles 4-5 (medio)
  Niveles 1-2-3 (base)
"""
from typing import List, Tuple, Dict, Any

# Tipo para definir paredes: lista de posiciones (x, y) que son bloqueadas
Walls = List[Tuple[int, int]]

class LevelConfig:
    """Configuración de un nivel individual"""
    def __init__(
        self,
        level_num: int,
        title: str,
        grid_size: int,
        player_start: Tuple[int, int],
        key_pos: Tuple[int, int],
        exit_pos: Tuple[int, int],
        vectors: Dict[str, Tuple[int, int]],
        walls: Walls = None,
        traps: Walls = None,  # NUEVO: Trampillas
        description: str = ""
    ):
        self.level_num = level_num
        self.title = title
        self.grid_size = grid_size
        self.player_start = player_start
        self.key_pos = key_pos
        self.exit_pos = exit_pos
        self.vectors = vectors
        self.walls = walls if walls else []
        self.traps = traps if traps else []  # NUEVO
        self.description = description

# ============================================================================
# DEFINICIÓN DE LOS 6 NIVELES
# ============================================================================

LEVELS = [
    # NIVEL 1: Tutorial básico 2x2
    LevelConfig(
        level_num=1,
        title="THE FIRST STEP",
        grid_size=2,
        player_start=(0, 0),
        key_pos=(1, 1),
        exit_pos=(0, 1),
        vectors={
            "U": (1, 0),   # Derecha →
            "V": (0, 1),   # Abajo ↓
        },
        walls=[],
        description="Aprende el movimiento básico"
    ),
    
    # NIVEL 2: Introducción a obstáculos 3x3
    LevelConfig(
        level_num=2,
        title="THE BARRIER",
        grid_size=3,
        player_start=(0, 0),
        key_pos=(2, 2),
        exit_pos=(0, 2),
        vectors={
            "U": (1, 0),   # Derecha →
            "V": (0, 1),   # Abajo ↓
        },
        walls=[
            (1, 0),  # Pared en medio-arriba
            (1, 1),  # Pared en centro
        ],
        description="Esquiva las paredes"
    ),
    
    # NIVEL 3: Laberinto simple 4x4 con TRAMPAS
    LevelConfig(
        level_num=3,
        title="THE MAZE",
        grid_size=4,
        player_start=(0, 0),
        key_pos=(3, 3),
        exit_pos=(3, 0),
        vectors={
            "U": (1, 0),   # Derecha →
            "V": (0, 1),   # Abajo ↓
            "W": (-1, 0),  # Izquierda ←
        },
        walls=[
            (1, 1),  # Pequeño obstáculo en el centro
            (2, 2),
        ],
        traps=[
            (2, 0),  # Trampa en camino directo
            (0, 2),  # Trampa lateral
        ],
        description="¡Cuidado con las trampillas! 💀"
    ),
    
    # NIVEL 4: Cuatro direcciones 4x4 con TRAMPAS
    LevelConfig(
        level_num=4,
        title="THE FOUR PATHS",
        grid_size=4,
        player_start=(0, 0),
        key_pos=(3, 3),
        exit_pos=(0, 3),
        vectors={
            "U": (1, 0),   # Derecha →
            "V": (0, 1),   # Abajo ↓
            "W": (-1, 0),  # Izquierda ←
            "X": (0, -1),  # Arriba ↑
        },
        walls=[
            (1, 1), (2, 1),  # Pared horizontal arriba
            (1, 2),          # Una celda bloqueada
        ],
        traps=[
            (3, 1),  # Trampa esquina
            (2, 3),  # Trampa cerca de salida
            (1, 0),  # Trampa en ruta
        ],
        description="Más trampas, más peligro 💀"
    ),
    
    # NIVEL 5: Laberinto 5x5 con TRAMPAS - Diseño en forma de cruz
    LevelConfig(
        level_num=5,
        title="THE LABYRINTH",
        grid_size=5,
        player_start=(0, 0),
        key_pos=(4, 4),
        exit_pos=(2, 2),  # En el centro
        vectors={
            "U": (1, 0),   # Derecha →
            "V": (0, 1),   # Abajo ↓
            "W": (-1, 0),  # Izquierda ←
            "X": (0, -1),  # Arriba ↑
        },
        walls=[
            # Patrón en cruz - Paredes en las esquinas del centro
            (1, 1), (3, 1),  # Arriba izq y der
            (1, 3), (3, 3),  # Abajo izq y der
            (2, 0),          # Una extra arriba
            (0, 2),          # Una extra izquierda
        ],
        traps=[
            (4, 0),  # Trampa esquina superior derecha
            (0, 4),  # Trampa esquina inferior izquierda
            (2, 1),  # Trampa en el pasillo
            (1, 2),  # Trampa lateral
            (3, 2),  # Trampa lateral derecha
        ],
        description="Laberinto con muchas trampas 💀"
    ),
    
    # NIVEL 6: Desafío final 6x6 - Laberinto en U con TRAMPAS
    LevelConfig(
        level_num=6,
        title="THE APEX",
        grid_size=6,
        player_start=(0, 0),
        key_pos=(5, 5),
        exit_pos=(5, 0),  # Esquina opuesta
        vectors={
            "U": (2, 0),    # Salto doble derecha ⇒
            "V": (0, 2),    # Salto doble abajo ⇓
            "W": (-1, 0),   # Izquierda ←
            "X": (0, -1),   # Arriba ↑
        },
        walls=[
            # Patrón en U - Fuerza a usar los saltos dobles
            (2, 1), (2, 2), (2, 3),  # Pared vertical central
            (3, 1), (3, 2), (3, 3),  # Pared vertical central
            (1, 4), (2, 4), (3, 4), (4, 4),  # Pared horizontal abajo
        ],
        traps=[
            (1, 0),  # Trampa en ruta superior
            (4, 1),  # Trampa lateral
            (0, 3),  # Trampa izquierda
            (5, 2),  # Trampa derecha
            (1, 5),  # Trampa inferior
            (4, 5),  # Trampa inferior derecha
            (5, 3),  # Trampa en camino a llave
        ],
        description="Desafío final: Paredes + Trampas 💀"
    ),
]

def get_level(level_num: int) -> LevelConfig:
    """Obtiene la configuración de un nivel específico"""
    if 1 <= level_num <= len(LEVELS):
        return LEVELS[level_num - 1]
    return LEVELS[0]  # Fallback al nivel 1

def get_total_levels() -> int:
    """Retorna el número total de niveles"""
    return len(LEVELS)