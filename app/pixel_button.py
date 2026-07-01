# -*- coding: utf-8 -*-
"""
Botón estilo pixel-art generado en tiempo real (sin assets).
Se apoya en pygame para dibujar el botón y luego lo convierte a QPixmap.
"""
from __future__ import annotations

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QSize
import pygame

from core.egypt_pixel import make_stone_button_surface


def _surface_to_qpixmap(surface: pygame.Surface) -> QtGui.QPixmap:
    """Convierte un Surface (RGB) a QPixmap."""
    w, h = surface.get_size()
    raw = pygame.image.tostring(surface, "RGB")
    img = QtGui.QImage(raw, w, h, QtGui.QImage.Format.Format_RGB888)
    return QtGui.QPixmap.fromImage(img)


class PixelButton(QtWidgets.QPushButton):
    """
    QPushButton que se ve como botón pixel-art.
    Usa íconos para dibujar el fondo del botón (normal/hover/pressed).
    """
    def __init__(self, text: str, w: int = 360, h: int = 90, scale: int = 2, parent=None):
        super().__init__("", parent)  # texto lo dibujamos nosotros en el surface
        self._label = text
        self._w = w
        self._h = h
        self._scale = scale
        self.setFixedSize(w, h)
        self.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFlat(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Generar pixmaps para estados
        self._pm_normal = _surface_to_qpixmap(make_stone_button_surface(text, w, h, state="normal", scale=scale))
        self._pm_hover  = _surface_to_qpixmap(make_stone_button_surface(text, w, h, state="hover",  scale=scale))
        self._pm_press  = _surface_to_qpixmap(make_stone_button_surface(text, w, h, state="pressed",scale=scale))

        self._set_pm(self._pm_normal)

        # QSS: sin bordes para que se vea el icono
        self.setStyleSheet("""
            QPushButton { border: none; padding: 0px; background: transparent; }
        """)
        # Importante: icono ocupa todo el botón
        self.setIconSize(QSize(w, h))

    def _set_pm(self, pm: QtGui.QPixmap):
        self.setIcon(QtGui.QIcon(pm))

    def enterEvent(self, event):
        self._set_pm(self._pm_hover)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._set_pm(self._pm_normal)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._set_pm(self._pm_press)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        # volver a hover si el mouse sigue encima
        if self.underMouse():
            self._set_pm(self._pm_hover)
        else:
            self._set_pm(self._pm_normal)
        super().mouseReleaseEvent(event)