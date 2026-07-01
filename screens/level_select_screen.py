# -*- coding: utf-8 -*-
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import pyqtSignal
import pygame
from app.pygame_canvas import PygameCanvas
from app.pixel_button import PixelButton
from core.constants import RES_W, RES_H, FPS, GOLD, WHITE
from core.egypt_pixel import draw_night_pyramid, draw_pixel_text

class LevelSelectPage(QtWidgets.QWidget):
    level_chosen = pyqtSignal(int)
    back_to_menu = pyqtSignal()

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.state = controller.state
        self.canvas = PygameCanvas(RES_W, RES_H)
        self.canvas.clicked.connect(self.on_click_canvas)
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.on_tick)
        self.timer.start(int(1000/FPS))
        
        # Layout principal
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addWidget(self.canvas)
        
        # Botón de volver (overlay)
        self.btn_back = PixelButton("Volver al Menú", w=260, h=70, scale=2)
        self.btn_back.clicked.connect(self.back_to_menu.emit)
        
        # Posicionar el botón en la esquina inferior
        btn_container = QtWidgets.QWidget()
        btn_container.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        btn_layout = QtWidgets.QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(20, 20, 20, 20)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_back)
        btn_layout.addStretch()
        
        main_layout.addWidget(btn_container)
        
        self.surf = pygame.Surface((RES_W, RES_H))
        
        # Posiciones de bloques de nivel en forma de pirámide
        # Nivel 6 (cima)
        # Niveles 4-5 (medio)
        # Niveles 1-2-3 (base)
        
        cx, cy = RES_W // 2, int(RES_H * 0.55)
        block_size = 70
        spacing = 10
        
        self.level_rects = {
            # Fila inferior (base): niveles 1, 2, 3
            1: pygame.Rect(cx - block_size * 1.5 - spacing, cy + block_size * 1.2, block_size, block_size),
            2: pygame.Rect(cx - block_size // 2, cy + block_size * 1.2, block_size, block_size),
            3: pygame.Rect(cx + block_size // 2 + spacing, cy + block_size * 1.2, block_size, block_size),
            
            # Fila media: niveles 4, 5
            4: pygame.Rect(cx - block_size - spacing // 2, cy + block_size * 0.4, block_size, block_size),
            5: pygame.Rect(cx + spacing // 2, cy + block_size * 0.4, block_size, block_size),
            
            # Fila superior (cima): nivel 6
            6: pygame.Rect(cx - block_size // 2, cy - block_size * 0.5, block_size, block_size),
        }
        
        self.hover_level = None

    def on_tick(self):
        self.draw()
        self.canvas.set_frame(self.surf)

    def draw(self):
        s = self.surf
        draw_night_pyramid(s)
        
        # Título
        draw_pixel_text(s, "Selecciona un Nivel", (RES_W//2 - 140, int(RES_H*0.90)), GOLD, scale=2)
        
        # Dibujar bloques de niveles
        for lvl in range(1, 7):
            rect = self.level_rects[lvl]
            unlocked = lvl <= self.state.unlocked_levels
            completed = lvl in self.state.completed_levels
            is_current = lvl == self.state.current_level
            is_hover = lvl == self.hover_level
            
            # Color base del bloque
            if not unlocked:
                base_color = (60, 50, 45)  # Bloqueado
                border_color = (40, 35, 30)
            elif completed:
                base_color = (100, 140, 100)  # Verde para completado
                border_color = (60, 100, 60)
            elif is_current:
                base_color = (140, 120, 80)  # Dorado para nivel actual
                border_color = GOLD
            else:
                base_color = (90, 80, 70)  # Normal
                border_color = (130, 120, 110)
            
            # Efecto hover
            if is_hover and unlocked:
                base_color = tuple(min(255, c + 20) for c in base_color)
            
            # Dibujar bloque con efecto 3D
            shadow_offset = 4
            pygame.draw.rect(s, (30, 25, 20), rect.move(shadow_offset, shadow_offset))
            pygame.draw.rect(s, base_color, rect)
            pygame.draw.rect(s, border_color, rect, 4)
            
            # Highlight si está seleccionado
            if is_current and unlocked:
                pygame.draw.rect(s, GOLD, rect.inflate(8, 8), 3)
            
            # Texto del nivel
            if unlocked:
                # Número del nivel
                text_color = WHITE if not completed else (200, 255, 200)
                num_text = str(lvl)
                text_x = rect.x + rect.w // 2 - 8
                text_y = rect.y + rect.h // 2 - 14
                draw_pixel_text(s, num_text, (text_x, text_y), text_color, scale=3)
                
                # Marca de completado
                if completed:
                    check_x = rect.x + rect.w - 16
                    check_y = rect.y + 4
                    draw_pixel_text(s, "✓", (check_x, check_y), (100, 255, 100), scale=2)
            else:
                # Candado para niveles bloqueados
                lock_x = rect.x + rect.w // 2 - 10
                lock_y = rect.y + rect.h // 2 - 12
                
                # Dibujar candado pixel art
                lock_color = (80, 70, 60)
                # Arco del candado
                pygame.draw.rect(s, lock_color, (lock_x + 4, lock_y, 12, 6), 2)
                # Cuerpo del candado
                pygame.draw.rect(s, lock_color, (lock_x, lock_y + 6, 20, 14))
                # Ojo de cerradura
                pygame.draw.circle(s, (40, 35, 30), (lock_x + 10, lock_y + 13), 3)
        
        # Sprite del arqueólogo
        player_y = int(RES_H * 0.82)
        player_x = RES_W // 2 - 8
        
        # Cuerpo
        pygame.draw.rect(s, (130, 95, 70), (player_x, player_y, 16, 20))
        # Sombrero
        pygame.draw.rect(s, (110, 85, 60), (player_x, player_y - 8, 16, 8))
        # Borde del sombrero
        pygame.draw.line(s, (90, 70, 50), (player_x - 2, player_y), (player_x + 18, player_y), 2)
        
        # Instrucción
        instruction = "Haz clic en un nivel para jugar"
        draw_pixel_text(s, instruction, (RES_W//2 - 150, RES_H - 30), WHITE, scale=1)

    def on_click_canvas(self, x: int, y: int):
        """Maneja clicks en el canvas"""
        for lvl, rect in self.level_rects.items():
            if rect.collidepoint(x, y) and lvl <= self.state.unlocked_levels:
                self.level_chosen.emit(lvl)
                break
    
    def mouseMoveEvent(self, event):
        """Detecta hover sobre niveles"""
        x = int(event.position().x())
        y = int(event.position().y())
        
        self.hover_level = None
        for lvl, rect in self.level_rects.items():
            if rect.collidepoint(x, y) and lvl <= self.state.unlocked_levels:
                self.hover_level = lvl
                break
        
        super().mouseMoveEvent(event)