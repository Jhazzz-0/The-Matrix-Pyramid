# -*- coding: utf-8 -*-
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal
import pygame
from app.pygame_canvas import PygameCanvas
from app.pixel_button import PixelButton
from core.constants import RES_W, RES_H, FPS, GOLD
from core.egypt_pixel import draw_sunset_desert, draw_pixel_text

class MenuPage(QtWidgets.QWidget):
    go_play = pyqtSignal()
    go_instructions = pyqtSignal()
    quit_app = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.canvas = PygameCanvas(RES_W, RES_H)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.on_tick)
        self.timer.start(int(1000/FPS))

        # Botones (pixel art)
        self.btn_play = PixelButton("Jugar", w=420, h=96, scale=3)
        self.btn_instr = PixelButton("Instrucciones", w=420, h=96, scale=3)
        self.btn_quit = PixelButton("Salir", w=420, h=96, scale=3)

        self.btn_play.clicked.connect(self.go_play.emit)
        self.btn_instr.clicked.connect(self.go_instructions.emit)
        self.btn_quit.clicked.connect(self.quit_app.emit)

        layout = QtWidgets.QGridLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.canvas, 0, 0)

        overlay = QtWidgets.QVBoxLayout()
        overlay.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        overlay.addWidget(self.btn_play)
        overlay.addSpacing(10)
        overlay.addWidget(self.btn_instr)
        overlay.addSpacing(10)
        overlay.addWidget(self.btn_quit)

        panel = QtWidgets.QWidget()
        panel.setLayout(overlay)
        layout.addWidget(panel, 0, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.surf = pygame.Surface((RES_W, RES_H))

    def on_tick(self):
        self.draw()
        self.canvas.set_frame(self.surf)

    def draw(self):
        s = self.surf
        draw_sunset_desert(s)
        draw_pixel_text(s, "THE MATRIX PYRAMID", (RES_W//2 - 158, 44), (30,22,18), scale=3)
        draw_pixel_text(s, "THE MATRIX PYRAMID", (RES_W//2 - 160, 40), GOLD, scale=3)
        draw_pixel_text(s, "Presiona ENTER para continuar", (RES_W//2 - 150, RES_H - 40), (255,255,255), scale=2)
