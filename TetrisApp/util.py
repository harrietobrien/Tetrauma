from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QRegion, QFont
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPainterPath
from PyQt6.QtCore import QRectF


class BKGDCell(QWidget):

    def __init__(self, color, cellSize):
        super().__init__()
        self.cs = cellSize
        self.setFixedWidth(self.cs)
        self.setFixedHeight(self.cs)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
        self.setContentsMargins(0, 0, 0, 0)


class RoundedWidget(QWidget):

    def __init__(self, width, height, label=""):
        super().__init__()
        self.width = width
        self.height = height
        self.label = label
        self.font2 = QFont('Helvetica', 20, QFont.Weight.Medium)
        self.setAutoFillBackground(True)
        self.setFixedSize(self.width, self.height)
        path = QPainterPath()
        radius = 20.0
        path.addRoundedRect(QRectF(self.rect()), radius, radius)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)
        self.setObjectName("outer-box")
        self.setStyleSheet(open('styles.qss').read())

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


if '__name__' == '__main__':
    pass