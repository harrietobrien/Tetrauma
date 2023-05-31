from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QRegion, QFont
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPainterPath
from PyQt6.QtCore import QRectF


class RoundedWidget(QWidget):

    def __init__(self, statPanel, width, height):
        super(RoundedWidget, self).__init__(statPanel)
        self.parent = statPanel
        self.width = width
        self.height = height
        self.addRoundedWidget()

    def addRoundedWidget(self):
        self.setAutoFillBackground(True)
        self.setFixedSize(self.width, self.height)
        path = QPainterPath()
        radius = 20.0
        path.addRoundedRect(QRectF(self.rect()), radius, radius)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)
        self.setObjectName("outer-box")
        self.setStyleSheet(open('styles.qss').read())
        return self
