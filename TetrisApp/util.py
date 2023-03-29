from PyQt6.QtCore import QPoint, QRect
from PyQt6.QtGui import QPalette, QColor, QPolygon
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget


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


class PieceCell(QWidget):

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

    @staticmethod
    def roundHalfUp(d):
        import decimal
        # Round to nearest with ties going away from zero.
        rounding = decimal.ROUND_HALF_UP
        # See other rounding options here:
        return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

    def getInnerCellOffset(self):
        x = (8 * self.cs) / 9
        # print('x\t', x)
        return self.roundHalfUp(x)

    def drawPiecePart(self, painter):
        # Bitmap Graphics ? Rounded rectangle ?
        # PART 1 - 9 x 9 - 2 triangles (polygons)
        blCell, brCell = QPoint(0, 0), QPoint(self.cs, 0)
        tlCell, trCell = QPoint(0, self.cs), QPoint(self.cs, self.cs)
        tintTriangle = QPolygon()
        tintTriangle << blCell << brCell << trCell
        shadeTriangle = QPolygon()
        shadeTriangle << blCell << tlCell << trCell
        painter.drawPolygon(tintTriangle)
        painter.drawPolygon(shadeTriangle)
        # PART 2 - 8 x 8
        offset = self.getInnerCellOffset()
        blRect = blCell + QPoint(offset, offset)
        trRect = trCell + QPoint(-offset, -offset)
        # innerCell = QRect(blRect, trRect)
        painter.drawRect(QRect(blRect, trRect))
        # painter.setRenderHint()


class ButtonBox(QWidget):
    def __init__(self, boardParent) -> None:
        super(ButtonBox, self).__init__()
        self.parent = boardParent
        hbox = QHBoxLayout()
        # start button
        startButton = QPushButton('START', self)
        startButton.pressed.connect(self.parent.startGame)
        hbox.addWidget(startButton)
        # pause button
        pauseButton = QPushButton("PAUSE", self)
        pauseButton.clicked.connect(self.parent.pauseGame)
        hbox.addWidget(pauseButton)

        self.setLayout(hbox)


if '__name__' == '__main__':
    buttons = ButtonBox()
    print(buttons)
