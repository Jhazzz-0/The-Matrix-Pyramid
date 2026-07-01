# -*- coding: utf-8 -*-
import sys
from PyQt6 import QtWidgets
import pygame
from app.window import MainWindow


def main():
    pygame.display.init()
    pygame.font.init()
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
