from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QFont, QMovie, QPainterPath, QRegion, QPainter, QColor, QPen
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QLabel, \
    QGraphicsDropShadowEffect, QHBoxLayout, QPushButton, QWidget
from util import RoundedWidget


class StatPanel(QGroupBox):
    # statSignal = pyqtSignal(object)

    def __init__(self, runTetrisParent) -> None:
        super(StatPanel, self).__init__(runTetrisParent)
        self.runParent = runTetrisParent
        self.width, self.height = self.runParent.width, self.runParent.height
        self.setContentsMargins(25, 25, 25, 25)
        self.setFixedSize(self.width - 200, self.height + 100)

        self.small = self.runParent.smallFont
        self.medium = self.runParent.mediumFont
        self.large = self.runParent.largeFont

        # self.statInit()

    def statInit(self):
        vbox = QVBoxLayout()
        ctrlBox = self.addRoundedWidget(300, 800)
        print(ctrlBox)
        vbox.addWidget(ctrlBox)
        vbox.addStretch()
        self.setLayout(vbox)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        self.drawStatBox(painter)
        self.drawPieces(painter)

    def drawStatBox(self, painter):
        origin = QPointF(25, 25)
        self.runParent.board.drawBackground(painter, width=300, height=850, start=origin)
        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(self.medium)
        painter.drawText(50, 100, "STATISTICS")
        painter.setFont(QFont('Arcade', 25))
        self.drawPieces(painter)

    def drawPieces(self, painter):
        pieces: list[object] = self.runParent.board.fallingPieceStrux
        for piece in pieces:
            # i.e. {'hue': '#EF233C', 'tint': '#f13950', 'shade': '#d72036'}
            currentColors: dict = self.runParent.board.getCurrentPieceColors(piece)
            # or piece.getCellColors() --> tuple(hue, tint, shade)
            blist: list[list[bool]] = piece.getPiece()
            pieceType: str = piece.getPieceType()
            for i in range(len(blist)):
                for j in range(len(blist[0])):
                    if blist[i][j]:
                        hue = currentColors['hue']
                        self.runParent.board.drawCell(painter, i, j, hue, piece=pieceType)
                        self.runParent.board.drawPiecePart(painter, i, j, hue, piece=pieceType)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mouseReleaseEvent(event)

    @staticmethod
    def addRoundedWidget(width, height):
        box = QWidget()
        box.setAutoFillBackground(True)
        box.setFixedSize(width, height)
        path = QPainterPath()
        radius = 20.0
        path.addRoundedRect(QRectF(box.rect()), radius, radius)
        mask = QRegion(path.toFillPolygon().toPolygon())
        box.setMask(mask)
        box.setObjectName("outer-box")
        box.setStyleSheet(open('styles.qss').read())
        return box
