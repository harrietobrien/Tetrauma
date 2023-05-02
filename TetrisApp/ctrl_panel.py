from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QFont, QMovie, QPainterPath, QRegion, QPainter, QColor
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QLabel, \
    QGraphicsDropShadowEffect, QHBoxLayout, QPushButton, QWidget
from util import RoundedWidget


class CtrlPanel(QGroupBox):
    def __init__(self, runTetrisParent) -> None:
        super(CtrlPanel, self).__init__(runTetrisParent)
        self.rows, self.score = 0, 0
        self.runParent = runTetrisParent
        self.runParent.userSignal[str].connect(self.getUser)
        self.runParent.board.gameStatusSignal[object].connect(self.gameStatus)
        self.runParent.board.nextSignal[object].connect(self.getNext)
        self.runParent.board.getHoldSignal[object].connect(self.getHold)
        self.runParent.board.placeHoldSignal[bool].connect(self.placeHold)
        self.runParent.board.scoreSignal[int].connect(self.getScore)
        self.runParent.board.scoreSignal[int].connect(self.getRowsCleared)
        self.width, self.height = self.runParent.width, self.runParent.height
        self.buttons = dict.fromkeys(['START', 'PAUSE', 'LOGIN'], None)
        self.setFixedSize(self.width + 100, self.height + 100)

        self.font = QFont('Helvetica', 20, QFont.Weight.DemiBold)
        self.font2 = QFont('Helvetica', 20, QFont.Weight.Medium)

        self.userLabel, self.scoreLabel, self.rowsLabel = None, None, None
        self.pausedLabel, self.gameOver = None, False

        self.nextPieceObject = None
        self.heldPieceObject, self.placeHoldPiece = None, None

        self.hcenter = Qt.AlignmentFlag.AlignHCenter
        self.vcenter = Qt.AlignmentFlag.AlignVCenter
        self.top = Qt.AlignmentFlag.AlignTop

        self.vbox = QVBoxLayout()
        self.ctrlInit()

    def gameStatus(self, gameStatus):
        if self.pausedLabel:
            if gameStatus['paused']:
                self.pausedLabel.setText("PAUSED")
            else:
                self.pausedLabel.setText("PLAYING")
        if gameStatus['over']:
            self.gameOver = True

    def getUser(self):
        if self.userLabel:
            self.userLabel.setText("Harriet")
        self.update()

    def getNext(self, nextPiece):
        self.nextPieceObject = nextPiece

    def getHold(self, heldPiece):
        self.heldPieceObject = heldPiece
        self.update()

    def placeHold(self, place: bool):
        self.placeHoldPiece = place

    def getScore(self, score):
        if self.scoreLabel:
            self.scoreLabel.setText(str(score))
        self.update()

    def getRowsCleared(self, rows):
        if self.rowsLabel:
            self.rowsLabel.setText(str(rows))
        self.update()

    def ctrlInit(self):
        labelGIF = QLabel(self)
        GIF = QMovie("tetris.gif")
        if labelGIF is not None:
            labelGIF.setMovie(GIF)
            GIF.start()
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        labelGIF.setGraphicsEffect(shadow)
        self.vbox.addWidget(labelGIF, alignment=self.hcenter | self.top)
        self.buttonBox()
        # statsBox = QHBoxLayout()
        # statsBox.setAlignment(self.hcenter)
        self.infoWidget = self.addRoundedWidget(560, 370)
        # self.scoreWidget = self.addRoundedWidget(260, 120, 'SCORE')
        # self.rowsWidget = self.addRoundedWidget(260, 120, 'ROWS CLEARED')
        # statsBox.addWidget(self.scoreWidget)
        # statsBox.addWidget(self.rowsWidget)
        self.vbox.addWidget(self.infoWidget)
        self.vbox.addStretch()
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.vbox)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(self.font)
        self.drawPreviewBox(painter)

    def drawPreviewBox(self, painter):
        origin = QPointF(45, 600)  # 410
        self.runParent.board.drawBackground(painter, width=560, height=250, start=origin)
        painter.drawText(120, 640, "NEXT PIECE")
        painter.drawText(380, 640, "HOLD QUEUE")
        if not self.gameOver:
            self.drawNextPiece(painter)
            self.drawHeldPiece(painter)

    def drawNextPiece(self, painter):
        if self.nextPieceObject:
            nextPiece = self.nextPieceObject
            nextColors = self.runParent.board.getCurrentPieceColors(nextPiece)
            nextBlist = nextPiece.getPiece()
            for i in range(len(nextBlist)):
                for j in range(len(nextBlist[0])):
                    if nextBlist[i][j]:
                        hue = nextColors['hue']
                        self.runParent.board.drawCell(painter, i, j, hue, piece="next")
                        self.runParent.board.drawPiecePart(painter, i, j, hue, piece="next")

    def drawHeldPiece(self, painter):
        if self.heldPieceObject:
            heldPiece = self.heldPieceObject
            heldColors = self.runParent.board.getCurrentPieceColors(heldPiece)
            heldBlist = heldPiece.getPiece()
            for i in range(len(heldBlist)):
                for j in range(len(heldBlist[0])):
                    if heldBlist[i][j]:
                        if self.placeHoldPiece:
                            hue = heldColors['hue']
                            self.runParent.board.drawCell(painter, i, j, hue, piece="hold")
                            self.runParent.board.drawPiecePart(painter, i, j, hue, piece="hold")
                        else:
                            white = QColor("#FFFFFF")
                            white.setAlpha(30)
                            self.runParent.board.drawCell(painter, i, j, white, piece="outline")

    def buttonBox(self):
        hbox = QHBoxLayout()
        hbox.setAlignment(self.hcenter)
        for btn in self.buttons:
            button = QPushButton(btn, self)
            button.setFont(self.font)
            button.setObjectName("button")
            button.setStyleSheet(open('styles.qss').read())
            button.setFixedSize(160, 40)
            hbox.addWidget(button)
        self.vbox.addLayout(hbox)

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
