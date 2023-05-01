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
        self.vbox = None
        self.font2 = QFont('Helvetica', 20, QFont.Weight.Medium)
        self.hcenter = Qt.AlignmentFlag.AlignHCenter
        self.vcenter = Qt.AlignmentFlag.AlignVCenter
        self.top = Qt.AlignmentFlag.AlignTop
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
        self.setStyleSheet(open('styles.css').read())
        self.vbox = QVBoxLayout()
        text = QLabel(self.label, self, alignment=self.hcenter | self.top)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        text.setGraphicsEffect(shadow)
        text.setFont(self.font2)
        text.setObjectName("text")
        text.setStyleSheet(open('styles.css').read())
        self.vbox.addWidget(text, alignment=self.hcenter | self.top)
        self.vbox.setAlignment(self.hcenter)
        self.setLayout(self.vbox)
        return self


if '__name__' == '__main__':
    pass