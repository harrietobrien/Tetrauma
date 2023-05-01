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
        self.runParent.board.nextSignal[object].connect(self.getNext)
        self.runParent.board.scoreSignal[int].connect(self.getScore)
        self.runParent.board.scoreSignal[int].connect(self.getRowsCleared)
        self.width, self.height = self.runParent.width, self.runParent.height
        self.setContentsMargins(50, 50, 50, 50)
        self.setFixedSize(self.width + 100, self.height + 100)

        self.font = QFont('Helvetica', 20, QFont.Weight.DemiBold)
        self.font2 = QFont('Helvetica', 20, QFont.Weight.Medium)

        self.userLabel = None
        self.scoreLabel = None
        self.rowsLabel = None

        self.nextPieceObject = None

        # alignments
        self.hcenter = Qt.AlignmentFlag.AlignHCenter
        self.vcenter = Qt.AlignmentFlag.AlignVCenter
        self.top = Qt.AlignmentFlag.AlignTop

        self.vbox = QVBoxLayout()
        self.ctrlInit()

    def getUser(self):
        if self.userLabel:
            self.userLabel.setText("Harriet")
        self.update()

    def getNext(self, nextPiece):
        self.nextPieceObject = nextPiece

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
        statsBox = QHBoxLayout()
        statsBox.setAlignment(self.hcenter)
        self.scoreWidget = self.addRoundedWidget(260, 120, 'SCORE')
        self.rowsWidget = self.addRoundedWidget(260, 120, 'ROWS CLEARED')
        statsBox.addWidget(self.scoreWidget)
        statsBox.addWidget(self.rowsWidget)
        self.vbox.addLayout(statsBox)
        self.vbox.addStretch()
        self.setLayout(self.vbox)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(self.font)
        self.drawPreviewBox(painter)

    def drawPreviewBox(self, painter):
        self.runParent.board.drawBackground(painter, width=520,
                                            height=250, start=QPointF(65, 410))
        painter.drawText(100, 450, "NEXT PIECE")
        self.drawNextPiece(painter)

    def drawNextPiece(self, painter):
        if self.nextPieceObject:
            nextPiece = self.nextPieceObject
            nextColors = self.runParent.board.getCurrentPieceColors(nextPiece)
            nextBlist = nextPiece.getPiece()
            for i in range(len(nextBlist)):
                for j in range(len(nextBlist[0])):
                    if nextBlist[i][j]:
                        hue = nextColors['hue']
                        self.runParent.board.drawCell(painter, i, j, hue, next=True)
                        self.runParent.board.drawPiecePart(painter, i, j, hue, next=True)

    def drawHeldPiece(self):
        pass

    def buttonBox(self):
        hbox = QHBoxLayout()
        hbox.setAlignment(self.hcenter)
        startButton = QPushButton("START GAME", self)
        startButton.setFont(self.font)
        startButton.setObjectName("button")
        startButton.setStyleSheet(open('styles.css').read())
        startButton.setFixedSize(250, 60)
        hbox.addWidget(startButton)
        pauseButton = QPushButton("PAUSE GAME", self)
        pauseButton.setFont(self.font)
        pauseButton.setObjectName("button")
        pauseButton.setStyleSheet(open('styles.css').read())
        pauseButton.setFixedSize(250, 60)
        hbox.addWidget(pauseButton)
        self.vbox.addLayout(hbox)

    def addRoundedWidget(self, width, height, label=""):
        box = QWidget()
        box.setAutoFillBackground(True)
        box.setFixedSize(width, height)
        path = QPainterPath()
        radius = 20.0
        path.addRoundedRect(QRectF(box.rect()), radius, radius)
        mask = QRegion(path.toFillPolygon().toPolygon())
        box.setMask(mask)
        box.setObjectName("outer-box")
        box.setStyleSheet(open('styles.css').read())
        vbox = QVBoxLayout()
        text = QLabel(label, box, alignment=self.hcenter | self.top)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        text.setGraphicsEffect(shadow)
        text.setFont(self.font2)
        text.setObjectName("text")
        text.setStyleSheet(open('styles.css').read())
        if label == 'SCORE':
            stats = QLabel(str(self.score), box)
            self.scoreLabel = stats
            stats.setFont(self.font2)
            vbox.addWidget(text, alignment=self.hcenter | self.top)
            vbox.addWidget(stats, alignment=self.hcenter | self.top)
        elif label == 'ROWS CLEARED':
            stats = QLabel(str(self.rows), box)
            self.rowsLabel = stats
            stats.setFont(self.font2)
            vbox.addWidget(text, alignment=self.hcenter | self.top)
            vbox.addWidget(stats, alignment=self.hcenter | self.top)
        else:
            vbox.addWidget(text, alignment=self.hcenter | self.top)
        vbox.setAlignment(self.hcenter)
        box.setLayout(vbox)
        return box
