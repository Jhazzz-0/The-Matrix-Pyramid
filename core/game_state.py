# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Tuple, List, Dict

@dataclass
class GameState:
    """Estado global del juego"""
    # Progreso del jugador
    unlocked_levels: int = 1
    current_level: int = 1
    completed_levels: List[int] = field(default_factory=list)
    
    # Estado del nivel actual
    grid_size: int = 2
    player: Tuple[int, int] = (0, 0)
    player_start: Tuple[int, int] = (0, 0)  # Para reiniciar al caer en trampa
    key_pos: Tuple[int, int] = (1, 1)
    exit_pos: Tuple[int, int] = (0, 1)
    walls: List[Tuple[int, int]] = field(default_factory=list)
    traps: List[Tuple[int, int]] = field(default_factory=list)  # NUEVO: Trampillas
    has_key: bool = False
    win: bool = False
    
    # Vectores disponibles del nivel actual
    vectors: Dict[str, Tuple[int, int]] = field(default_factory=dict)
    
    # Estadísticas
    moves_count: int = 0  # Contador de movimientos
    trap_falls: int = 0   # Veces que cayó en trampa
    
    def load_level(self, level_config):
        """Carga un nivel desde su configuración"""
        self.current_level = level_config.level_num
        self.grid_size = level_config.grid_size
        self.player = level_config.player_start
        self.player_start = level_config.player_start  # Guardar inicio
        self.key_pos = level_config.key_pos
        self.exit_pos = level_config.exit_pos
        self.walls = level_config.walls.copy()
        self.traps = level_config.traps.copy() if hasattr(level_config, 'traps') else []
        self.vectors = level_config.vectors.copy()
        self.has_key = False
        self.win = False
        self.moves_count = 0
        self.trap_falls = 0
    
    def complete_current_level(self):
        """Marca el nivel actual como completado y desbloquea el siguiente"""
        if self.current_level not in self.completed_levels:
            self.completed_levels.append(self.current_level)
        
        # Desbloquear el siguiente nivel
        if self.current_level < 6:  # 6 niveles totales
            self.unlocked_levels = max(self.unlocked_levels, self.current_level + 1)
    
    def is_wall(self, pos: Tuple[int, int]) -> bool:
        """Verifica si una posición es una pared"""
        return pos in self.walls
    
    def is_trap(self, pos: Tuple[int, int]) -> bool:
        """Verifica si una posición es una trampilla"""
        return pos in self.traps
    
    def reset_player_position(self):
        """Reinicia al jugador a la posición inicial (al caer en trampa)"""
        self.player = self.player_start
        self.has_key = False  # Pierde la llave si la tenía
        self.trap_falls += 1
    
    def reset_level(self, level_config):
        """Resetea el nivel actual sin cambiar el progreso"""
        self.load_level(level_config)