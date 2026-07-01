# -*- coding: utf-8 -*-
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt, pyqtSignal
import pygame

class PygameCanvas(QtWidgets.QLabel):
    """QLabel que muestra un Surface de pygame y emite clicks."""
    clicked = pyqtSignal(int, int)

    def __init__(self, width: int, height: int, parent=None):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.setScaledContents(True)
        self.setMouseTracking(True)

    def set_frame(self, surface: pygame.Surface):
        w, h = surface.get_size()
        raw = pygame.image.tostring(surface, "RGB")
        img = QtGui.QImage(raw, w, h, QtGui.QImage.Format.Format_RGB888)
        self.setPixmap(QtGui.QPixmap.fromImage(img))

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            x = int(event.position().x())
            y = int(event.position().y())
            self.clicked.emit(x, y)
        return super().mousePressEvent(event)
