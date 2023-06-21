from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QFont, QMovie, QPainterPath, QRegion, QPainter, QColor, QPen
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QLabel, \
    QGraphicsDropShadowEffect, QHBoxLayout, QPushButton, QWidget
from util import RoundedWidget


class StatPanel(QGroupBox):

    def __init__(self, runTetrisParent) -> None:
        super(StatPanel, self).__init__(runTetrisParent)
        self.runParent = runTetrisParent
        self.pieceCounts = dict(zip(list('IJLOSTZ'), [0] * 7))
        self.width, self.height = self.runParent.width, self.runParent.height
        self.setContentsMargins(25, 25, 25, 25)
        self.setFixedSize(self.width - 200, self.height + 100)
        self.runParent.board.pieceCountSignal[object].connect(self.setPieceCounts)
        self.runParent.board.gameStatusSignal[bool].connect(self.getGameStatus)
        self.small = self.runParent.smallFont
        self.medium = self.runParent.mediumFont
        self.large = self.runParent.largeFont

    def setPieceCounts(self, pieceCounts: dict):
        self.pieceCounts = pieceCounts
        self.update()

    def getGameStatus(self, gameOver: bool):
        if gameOver:
            self.pieceCounts = dict(zip(list('IJLOSTZ'), [0] * 7))
            self.update()

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
        # self.drawPieces(painter)
        self.drawPieceCounts(painter)

    def drawPieceCounts(self, painter):
        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(QFont('Arcade', 25))
        x, y = 250, 150
        for i in self.pieceCounts:
            painter.drawText(x, y, str(self.pieceCounts[i]))
            if i == "I":
                y += 90
            else:
                y += 115

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

