# -*- coding: utf-8 -*-
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt
import pygame

from core.game_state import GameState
from core.game_controller import GameController
from levels_config import get_level

from screens.menu_screen import MenuPage
from screens.instructions_screen import InstructionsPage
from screens.level_select_screen import LevelSelectPage
from screens.game_screen import GamePage


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Matrix Pyramid")
        self.setMinimumSize(1024, 640)
        
        # Estado y Controlador del juego
        self.state = GameState()
        self.controller = GameController(self.state)
        
        # Stack de páginas
        self.stack = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stack)
        
        # Crear páginas
        self.menu = MenuPage()
        self.instructions = InstructionsPage()
        self.levels = LevelSelectPage(self.controller)
        self.game = GamePage(self.controller)
        
        # Agregar al stack
        self.stack.addWidget(self.menu)          # 0
        self.stack.addWidget(self.levels)        # 1
        self.stack.addWidget(self.instructions)  # 2
        self.stack.addWidget(self.game)          # 3
        
        # Conectar señales de navegación
        self.menu.go_play.connect(self.go_to_level_select)
        self.menu.go_instructions.connect(lambda: self.stack.setCurrentIndex(2))
        self.menu.quit_app.connect(self.close)
        
        self.instructions.back_to_menu.connect(lambda: self.stack.setCurrentIndex(0))
        
        self.levels.level_chosen.connect(self.on_level_chosen)
        self.levels.back_to_menu.connect(lambda: self.stack.setCurrentIndex(0))
        
        self.game.back_to_levels.connect(self.go_to_level_select)
        self.game.next_level.connect(self.on_level_chosen)
        
        # Atajo ENTER en menú
        self.shortcut_enter = QtGui.QShortcut(QtGui.QKeySequence(Qt.Key.Key_Return), self)
        self.shortcut_enter.activated.connect(self.on_enter_pressed)
        
    def on_enter_pressed(self):
        """Maneja la tecla ENTER según la página actual"""
        current_idx = self.stack.currentIndex()
        if current_idx == 0:  # Menú
            self.go_to_level_select()
    
    def go_to_level_select(self):
        """Va a la pantalla de selección de niveles"""
        self.stack.setCurrentIndex(1)
    
    def on_level_chosen(self, lvl: int):
        """Se ejecuta cuando el jugador selecciona un nivel"""
        # Cargar el nivel
        self.game.load_level(lvl)
        
        # Ir a la pantalla de juego
        self.stack.setCurrentIndex(3)
    
    def closeEvent(self, event):
        """Limpieza al cerrar"""
        pygame.quit()
        event.accept()