from PyQt6.QtCore import QPoint, QRect, QSizeF, QPointF, pyqtSignal
from PyQt6.QtGui import QPalette, QColor, QPolygon, QRegion, QPaintEvent
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget

# I use PySide6, but whatever library should work.
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPainter, QPainterPath, QBrush, QPen
from PyQt6.QtCore import Qt, QRectF


class BoardBkgd(QWidget):
   # paint_event_bkgd = pyqtSignal(QPaintEvent)

    def __init__(self, boardParent, width, height):
        super(BoardBkgd, self).__init__()
        self.board = boardParent
        self.width = width
        self.height = height
        self.px = 5
        self.radius = 20
        self.outlineColor = "#333333"
        self.drawBackground()

    def drawBackground(self):
        self.setAutoFillBackground(True)
        self.setFixedSize(self.width, self.height)
        path = QPainterPath()
        size = QSizeF(self.width, self.height)
        rect = QRectF(QPointF(0, 0), size)
        path.addRoundedRect(rect, self.radius, self.radius)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)
        self.setObjectName("bkgd-box")
        self.setStyleSheet('''
                    QWidget#bkgd-box {
                        border-radius: 20px;
                        background: rgba(151, 217, 0, 0.15);
                        border: 5px solid #333333;
                    }''')
        return self


'''
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        # Set painter colors to given values.
        pen = QPen(self.outlineColor, self.px)
        painter.setPen(pen)
        brush = QBrush(self.fillColor)
        painter.setBrush(brush)
        size = QSizeF(self.width, self.height)
        rect = QRectF(QPointF(0, 0), size)
        rect.adjust(self.px/2, self.px/2, -self.px/2, -self.px/2)

        path.addRoundedRect(rect, self.radius, self.radius)
        painter.setClipPath(path)

        # Fill shape, draw the border and center the text.
        painter.fillPath(path, painter.brush())
        painter.strokePath(path, painter.pen())
        painter.drawText(rect, Qt.AlignCenter, self.text())
'''


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
