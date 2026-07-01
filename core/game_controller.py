# -*- coding: utf-8 -*-
from typing import Tuple, Dict
from core.game_state import GameState
from core.grid_logic import try_move
from levels_config import get_level

class GameController:
    """
    Controlador del juego (MVC - Controller).
    Maneja la lógica de negocio del juego, coordina las mutaciones del modelo
    (GameState) y expone métodos de control limpios a la interfaz de usuario (View).
    """
    def __init__(self, state: GameState):
        self.state = state
        
    def load_level(self, level_num: int):
        """Carga la configuración de un nivel en el estado del juego"""
        config = get_level(level_num)
        self.state.load_level(config)
        
    def execute_move(self, scalars: Dict[str, int]) -> Tuple[bool, str]:
        """
        Intenta ejecutar un movimiento basado en la combinación lineal de vectores.
        Retorna (éxito, mensaje_de_estado).
        """
        return try_move(self.state, scalars)
        
    def reset_current_level(self) -> str:
        """Reinicia el nivel actual manteniendo el progreso general"""
        config = get_level(self.state.current_level)
        self.state.reset_level(config)
        return "Nivel reiniciado"
        
    def advance_to_next_level(self) -> bool:
        """
        Intenta avanzar al siguiente nivel.
        Retorna True si el nivel siguiente fue cargado con éxito, False de lo contrario.
        """
        if self.state.current_level < 6:
            next_lvl = self.state.current_level + 1
            self.load_level(next_lvl)
            return True
        return False
