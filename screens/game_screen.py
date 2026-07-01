# -*- coding: utf-8 -*-
# pyrefly: ignore [missing-import]
from PyQt6 import QtCore, QtWidgets, QtGui
# pyrefly: ignore [missing-import]
from PyQt6.QtCore import Qt, pyqtSignal
# pyrefly: ignore [missing-import]
import pygame
from app.pygame_canvas import PygameCanvas
from core.constants import GAME_CANVAS_W, GAME_CANVAS_H, FPS
from core.game_state import GameState
from core.game_controller import GameController
from screens.game_renderer import GameRenderer
from levels_config import get_level

class GamePage(QtWidgets.QWidget):
    back_to_levels = pyqtSignal()
    next_level = pyqtSignal(int)  # Nueva señal para avanzar al siguiente nivel

    def __init__(self, controller: GameController):
        super().__init__()
        self.controller = controller
        self.state = controller.state
        self.renderer = GameRenderer()
        
        wrapper = QtWidgets.QHBoxLayout(self)
        wrapper.setContentsMargins(10,10,10,10)
        
        # ========== HUD (Panel lateral) ==========
        hud = QtWidgets.QVBoxLayout()
        
        # Título del nivel
        self.lbl_title = QtWidgets.QLabel("LEVEL 1: THE FIRST STEP")
        self.lbl_title.setStyleSheet(
            "font-size:15px; font-weight:800; color:#f8c552; "
            "padding:8px; background:#2a1f1a; border:2px solid #4a3f3a;"
        )
        self.lbl_title.setWordWrap(True)
        hud.addWidget(self.lbl_title)
        
        hud.addSpacing(10)
        
        # Vectores disponibles
        lbl_vec = QtWidgets.QLabel("Vectores disponibles:")
        lbl_vec.setStyleSheet("color:#f8c552; font-weight:600; font-size:13px;")
        hud.addWidget(lbl_vec)
        
        # Contenedor dinámico para labels de vectores
        self.vector_labels_layout = QtWidgets.QVBoxLayout()
        hud.addLayout(self.vector_labels_layout)
        
        hud.addSpacing(10)
        
        # Inputs de escalares (dinámicos según vectores)
        form = QtWidgets.QFormLayout()
        self.scalar_inputs = {}  # Diccionario para guardar referencias a los spinboxes
        
        # Crear inputs para hasta 4 vectores posibles (U, V, W, X)
        for i, (scalar_name, vector_name) in enumerate([("Ca", "U"), ("Cb", "V"), ("Cc", "W"), ("Cd", "X")]):
            spin = QtWidgets.QSpinBox()
            spin.setRange(-10, 10)
            spin.setValue(0)
            spin.setStyleSheet("background:#3a2f29; color:white; border:2px solid #5a4f49;")
            
            label = QtWidgets.QLabel(f"Scalar {scalar_name[-1]} ({scalar_name}):")
            label.setStyleSheet("color:#ddd;")
            
            self.scalar_inputs[scalar_name] = {
                'spin': spin,
                'label': label,
                'row': form.rowCount()
            }
            form.addRow(label, spin)
        
        self.form_layout = form
        hud.addLayout(form)
        
        hud.addSpacing(10)
        
        # Botón ejecutar
        self.btn_exec = QtWidgets.QPushButton("Ejecutar Movimiento")
        self.btn_exec.setStyleSheet(
            "padding:10px; background:#6b5b53; color:#f8c552; "
            "border:3px solid #463a33; font-weight:700; font-size:14px;"
        )
        self.btn_exec.clicked.connect(self.on_execute_move)
        hud.addWidget(self.btn_exec)
        
        # Status message
        self.lbl_status = QtWidgets.QLabel("Find the key: Ca(U) + Cb(V)")
        self.lbl_status.setStyleSheet(
            "color:#fff; padding:8px; background:#2a1f1a; "
            "border:2px solid #4a3f3a; font-size:12px;"
        )
        self.lbl_status.setWordWrap(True)
        hud.addWidget(self.lbl_status)
        
        hud.addSpacing(10)
        
        # Estadísticas del nivel
        stats_container = QtWidgets.QWidget()
        stats_layout = QtWidgets.QVBoxLayout(stats_container)
        stats_layout.setContentsMargins(8, 8, 8, 8)
        stats_container.setStyleSheet("background:#1a1410; border:2px solid #3a2a22;")
        
        self.lbl_moves = QtWidgets.QLabel("Movimientos: 0")
        self.lbl_moves.setStyleSheet("color:#ddd; font-size:11px;")
        stats_layout.addWidget(self.lbl_moves)
        
        self.lbl_traps = QtWidgets.QLabel("Caídas en trampa: 0")
        self.lbl_traps.setStyleSheet("color:#ff6666; font-size:11px;")
        stats_layout.addWidget(self.lbl_traps)
        
        hud.addWidget(stats_container)
        
        hud.addSpacing(10)
        
        # Botón de reiniciar nivel
        self.btn_reset = QtWidgets.QPushButton("Reiniciar Nivel")
        self.btn_reset.setStyleSheet(
            "padding:6px; background:#5a4a42; color:#ddd; "
            "border:2px solid #3a2a22; font-size:12px;"
        )
        self.btn_reset.clicked.connect(self.on_reset_level)
        hud.addWidget(self.btn_reset)
        
        hud.addStretch(1)
        
        # Botón siguiente nivel (oculto hasta ganar)
        self.btn_next = QtWidgets.QPushButton("Siguiente Nivel →")
        self.btn_next.setStyleSheet(
            "padding:10px; background:#4a7a4a; color:white; "
            "border:3px solid #2a5a2a; font-weight:700; font-size:14px;"
        )
        self.btn_next.clicked.connect(self.on_next_level)
        self.btn_next.setVisible(False)
        hud.addWidget(self.btn_next)
        
        # Botón volver
        self.btn_back = QtWidgets.QPushButton("Volver a Selección")
        self.btn_back.clicked.connect(self.back_to_levels.emit)
        self.btn_back.setStyleSheet("padding:6px; background:#444; color:white;")
        hud.addWidget(self.btn_back)
        
        hud_widget = QtWidgets.QWidget()
        hud_widget.setLayout(hud)
        hud_widget.setFixedWidth(300)
        hud_widget.setStyleSheet("background:#3a2f29; border:3px solid #2b221c;")
        
        # ========== Canvas de Pygame ==========
        self.canvas = PygameCanvas(GAME_CANVAS_W, GAME_CANVAS_H)
        self.surf = pygame.Surface((GAME_CANVAS_W, GAME_CANVAS_H))
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.on_tick)
        self.timer.start(int(1000/FPS))
        
        wrapper.addWidget(hud_widget)
        wrapper.addSpacing(8)
        wrapper.addWidget(self.canvas, stretch=1)

    def load_level(self, level_num: int):
        """Carga un nivel específico"""
        self.controller.load_level(level_num)
        config = get_level(level_num)
        self.update_ui_for_level(config)
    
    def update_ui_for_level(self, config):
        """Actualiza la UI según la configuración del nivel"""
        # Actualizar título
        self.lbl_title.setText(f"LEVEL {config.level_num}: {config.title}")
        
        # Limpiar labels de vectores anteriores
        while self.vector_labels_layout.count():
            item = self.vector_labels_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Crear labels para vectores disponibles
        vector_symbols = {
            "U": "→",   # Derecha
            "V": "↓",   # Abajo
            "W": "←",   # Izquierda
            "X": "↑"    # Arriba
        }
        for vec_name in sorted(self.state.vectors.keys()):
            vec = self.state.vectors[vec_name]
            symbol = vector_symbols.get(vec_name, "•")
            
            # Determinar dirección en texto
            if vec == (1, 0):
                direction = "Derecha"
            elif vec == (0, 1):
                direction = "Abajo"
            elif vec == (-1, 0):
                direction = "Izquierda"
            elif vec == (0, -1):
                direction = "Arriba"
            elif vec == (2, 0):
                direction = "2× Derecha"
            elif vec == (0, 2):
                direction = "2× Abajo"
            else:
                direction = str(vec)
            
            lbl = QtWidgets.QLabel(f"{vec_name} = {symbol} {direction}")
            lbl.setStyleSheet("color:#ddd; font-family:monospace; padding:2px; font-size:12px;")
            self.vector_labels_layout.addWidget(lbl)
        
        # Mostrar/ocultar inputs de escalares según vectores disponibles
        scalar_to_vector = {"Ca": "U", "Cb": "V", "Cc": "W", "Cd": "X"}
        
        for scalar_name, info in self.scalar_inputs.items():
            vector_name = scalar_to_vector[scalar_name]
            is_needed = vector_name in self.state.vectors
            
            info['label'].setVisible(is_needed)
            info['spin'].setVisible(is_needed)
            info['spin'].setValue(0)  # Reset valor
        
        # Actualizar mensaje de status
        vec_formula = " + ".join([f"C{chr(97+i)}({v})" for i, v in enumerate(sorted(self.state.vectors.keys()))])
        self.lbl_status.setText(f"Find the key: {vec_formula}")
        
        # Ocultar botón de siguiente nivel
        self.btn_next.setVisible(False)

    def on_tick(self):
        self.renderer.render(self.surf, self.state)
        self.canvas.set_frame(self.surf)
        
        # Actualizar estadísticas
        self.lbl_moves.setText(f"Movimientos: {self.state.moves_count}")
        self.lbl_traps.setText(f"Caídas en trampa: {self.state.trap_falls}")

    def on_execute_move(self):
        """Ejecuta el movimiento con los escalares ingresados"""
        # Recopilar valores de escalares
        scalars = {}
        for name, info in self.scalar_inputs.items():
            if info['label'].isVisible():  # Solo si el input está visible
                scalars[name] = info['spin'].value()
        
        # Intentar movimiento
        success, message = self.controller.execute_move(scalars)
        self.lbl_status.setText(message)
        
        # Si ganó, mostrar botón de siguiente nivel
        if self.state.win:
            self.lbl_status.setStyleSheet(
                "color:#90ff90; padding:8px; background:#1a3a1a; "
                "border:2px solid #4aaa4a; font-size:12px; font-weight:700;"
            )
            
            # Mostrar botón siguiente solo si no es el último nivel
            if self.state.current_level < 6:
                self.btn_next.setVisible(True)

    def on_reset_level(self):
        """Reinicia el nivel actual"""
        message = self.controller.reset_current_level()
        self.lbl_status.setText(message)
        self.lbl_status.setStyleSheet(
            "color:#fff; padding:8px; background:#2a1f1a; "
            "border:2px solid #4a3f3a; font-size:12px;"
        )
        self.btn_next.setVisible(False)
    
    def on_next_level(self):
        """Avanza al siguiente nivel"""
        if self.controller.advance_to_next_level():
            config = get_level(self.state.current_level)
            self.update_ui_for_level(config)