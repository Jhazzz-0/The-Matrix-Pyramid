# -*- coding: utf-8 -*-
from PyQt6 import QtWidgets
from app.pixel_button import PixelButton
from PyQt6.QtCore import Qt, pyqtSignal

class InstructionsPage(QtWidgets.QWidget):
    back_to_menu = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)

        title = QtWidgets.QLabel("Instrucciones")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:22px; font-weight:800; color:#f8c552;")

        txt = QtWidgets.QLabel(
            (
                "Objetivo: Recoge la llave (Ankh) y llega a la puerta EXIT.\n"
                "Mecánica del Nivel 1: Movimiento por combinación lineal\n"
                "  Ca·U + Cb·V con U=(1,0), V=(0,1).\n"
                "Ingresa enteros para Ca y Cb y ejecuta el movimiento.\n"
                "Si sales de la grilla 4×4, el movimiento se cancela."
            )
        )
        txt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        txt.setStyleSheet("color:#ddd;")

        btn = PixelButton("Volver", w=260, h=84, scale=3)
        btn.clicked.connect(self.back_to_menu.emit)
        

        layout.addSpacing(20)
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(txt)
        layout.addSpacing(20)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)