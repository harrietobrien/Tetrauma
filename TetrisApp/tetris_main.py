import random
import sys


from PyQt6.QtCore import Qt
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from color_schemes import ColorSchemes
from defaults import defaults
from tetromino import Tetromino
from util import BKGDCell


class CtrlPanel(QGroupBox):
    def __init__(self, runTetrisParent) -> None:
        super(CtrlPanel, self).__init__(runTetrisParent)
        self.rows, self.score = 0, 0
        self.runParent = runTetrisParent
        self.runParent.board.scoreSignal[int].connect(self.getScore)
        self.runParent.board.scoreSignal[int].connect(self.getRowsCleared)
        self.width, self.height = self.runParent.width, self.runParent.height
        self.setContentsMargins(50, 50, 50, 50)
        self.setFixedSize(self.width + 100, self.height + 100)

        self.font = QFont('Helvetica', 20, QFont.Weight.DemiBold)
        self.font2 = QFont('Helvetica', 20, QFont.Weight.Medium)

        self.scoreLabel = None
        self.rowsLabel = None
        # alignments
        self.hcenter = Qt.AlignmentFlag.AlignHCenter
        self.vcenter = Qt.AlignmentFlag.AlignVCenter
        self.top = Qt.AlignmentFlag.AlignTop

        self.vbox = QVBoxLayout()
        self.ctrlInit()

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
        self.scoreWidget = self.addRoundedWidget(250, 120, 'SCORE')
        self.rowsWidget = self.addRoundedWidget(250, 120, 'ROWS CLEARED')
        statsBox.addWidget(self.scoreWidget)
        statsBox.addWidget(self.rowsWidget)
        previewBox = QHBoxLayout()
        previewBox.setAlignment(self.hcenter)
        self.nextWidget = self.addRoundedWidget(250, 250, 'NEXT PIECE')
        self.holdWidget = self.addRoundedWidget(250, 250, 'HOLD QUEUE')
        previewBox.addWidget(self.nextWidget)
        previewBox.addWidget(self.holdWidget)
        self.vbox.addLayout(statsBox)
        self.vbox.addLayout(previewBox)
        self.vbox.addStretch()
        self.setLayout(self.vbox)
        self.update()

    def description(self):
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


class RunTetris(QMainWindow):
    scoreSignal = pyqtSignal(int)
    rowSignal = pyqtSignal(int)
    key_pressed = pyqtSignal(QKeyEvent)
    paint_event = pyqtSignal(QPaintEvent)
    mouse_pressed = pyqtSignal()

    def __init__(self, rows=15, cols=10, margin=25, cellSize=50):
        super(RunTetris, self).__init__()
        # board configuration / dimensions
        self.timerDelay = None
        self.board = None
        self.ctrlPanel = None
        self.rows, self.cols = rows, cols
        self.cellSize, self.margin = cellSize, margin
        self.width = self.getWidth()
        self.height = self.getHeight()
        self.initGUI()

    def initGUI(self):
        # board components
        hbox = QHBoxLayout()
        layout = QWidget()
        self.board = Board(self)
        self.board.scoreSignal[int].connect(self.currentScore)
        self.board.rowSignal[int].connect(self.currentRowsRmv)
        self.ctrlPanel = CtrlPanel(self)
        hbox.addWidget(self.board)
        hbox.addWidget(self.ctrlPanel)
        layout.setLayout(hbox)
        self.setCentralWidget(layout)
        self.key_pressed.connect(self.board.onKeyPressEvent)
        blueGreen = QColor(9, 183, 152)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(blueGreen))
        self.setPalette(palette)
        self.setGeometry(0, 0, 1000, 1000)
        self.setWindowTitle('Tetrauma')
        self.show()

    def currentScore(self, score):
        self.scoreSignal.emit(score)
        # print("Score: ", score)

    def currentRowsRmv(self, rows):
        self.rowSignal.emit(rows)
        # print("Rows: ", rows)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.key_pressed.emit(event)
        return super().keyPressEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        self.paint_event.emit(event)
        return super().paintEvent(event)

    def __str__(self):
        print('width   -->', self.width)
        print('height  -->', self.height)
        print('cellSize ->', self.cellSize)
        print('margin  -->', self.margin)

    def getWidth(self):
        return (self.margin * 2) + (self.cellSize * self.cols)

    def getHeight(self):
        return (self.margin * 2) + (self.cellSize * self.rows)


class Board(QGroupBox):
    scoreSignal = pyqtSignal(int)
    rowSignal = pyqtSignal(int)
    TRANSPARENT = "#00FFFFFF"
    SCHEMES = ColorSchemes()

    def __init__(self, runTetrisParent) -> None:
        super(Board, self).__init__(runTetrisParent)
        self.parent = runTetrisParent
        self.width, self.height = self.parent.width, self.parent.height
        self.rows, self.cols = self.parent.rows, self.parent.cols
        self.positions = [(i, j) for i in range(self.rows)
                          for j in range(self.cols)]
        self.cellSize = self.parent.cellSize
        self.margin = self.parent.margin
        inst = Tetromino(defaultNumber=1)
        self.scheme = Tetromino.colors
        self.fallingPieceStrux = inst.getStructs()
        self.n = len(self.fallingPieceStrux)
        # CURRENT FALLING PIECE
        self.currFallingPieceObj = None
        self.currFallingPieceBlist = None
        self.currFallingPieceColors = None
        self.currFallingPieceCol = 0
        self.currFallingPieceRow = 0
        self.rowPosition = 0
        self.colPosition = 0

        self.numRowsRemoved = 0
        self.started, self.paused = None, None
        self.timerDelay = 250  # ms
        self.gameOver = False

        self.score = 0
        self.timer = QBasicTimer()

        # self.setContentsMargins(50, 50, 50, 50)
        self.setFixedSize(self.width + 100, self.height + 100)
        self.grid = None
        self.hcenter = Qt.AlignmentFlag.AlignHCenter
        self.vcenter = Qt.AlignmentFlag.AlignVCenter
        # teaGreen = "#CAFFB9"
        self.bgColor = "#00FFFFFF"
        self.currentBoard = self.buildBoard(color=self.bgColor)
        self.permanentBoard = self.buildBoard(color=self.bgColor)
        self.startGame()
        self.show()

    def gridInit(self):
        self.grid = QGridLayout(self)
        self.grid.setSpacing(1)
        self.grid.setContentsMargins(50, 50, 50, 50)
        self.grid.setAlignment(self.grid, self.vcenter | self.hcenter)

    def startGame(self):
        if self.paused:
            return
        self.started = True
        self.numRowsRemoved = 0
        # generate/select first falling piece
        self.newFallingPiece()
        self.timer.start(self.timerDelay, self)

    def pauseGame(self):
        self.paused = not self.paused
        if self.paused:
            self.timer.stop()
        else:
            self.timer.start(self.timerDelay, self)
        self.update()

    # updates self.grid based on self.currentBoard
    def updateBoard(self):
        for position in self.positions:
            i, j = position
            permCell = self.permanentBoard[i][j]
            if permCell != self.bgColor and permCell != self.bgColor:
                self.currentBoard[i][j] = self.permanentBoard[i][j]
            currCell = self.currentBoard[i][j]
            self.grid.addWidget(BKGDCell(currCell, self.cellSize), *position)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setLayout(self.grid)

    # creates self.currentBoard; call on restart
    def buildBoard(self, color=None) -> list:
        rs, cs = self.rows, self.cols
        return [[color] * cs for _ in range(rs)]

    def drawBoard(self, painter):
        for row in range(self.rows):
            for col in range(self.cols):
                color = self.currentBoard[row][col]
                if color != self.bgColor:
                    self.drawCell(painter, row, col, color)
                    self.drawPiecePart(painter, row, col, color)
                else:
                    self.drawCell(painter, row, col, color)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        if not self.gameOver:
            self.drawBackground(painter)
            self.drawBoard(painter)
            self.drawFallingPiece(painter)
        else:
            self.drawBackground(painter)
            self.gameOverMessage(painter)

    def getCellBounds(self, row, col):
        x0 = self.margin + col * self.cellSize
        x1 = self.margin + (col + 1) * self.cellSize
        y0 = self.margin + row * self.cellSize
        y1 = self.margin + (row + 1) * self.cellSize
        return x0, x1, y0, y1

    def drawBackground(self, painter):
        path = QPainterPath()
        size = QSizeF(self.width, self.height)
        rect = QRectF(QPointF(50, 50), size)
        path.addRoundedRect(rect, 20, 20)
        color = QColor(151, 217, 0)
        color.setAlpha(59)
        pen = QPen(QColor("#333333"), 5)
        painter.setPen(pen)
        painter.fillPath(path, color)
        painter.drawPath(path)

    def drawCell(self, painter, row, col, color):
        (x0, x1, y0, y1) = self.getCellBounds(row, col)
        cellColor = QColor(color)
        topLeft = QPoint(x0 + 50, y0 + 50)
        # bottomRight = QPoint(x1, y1)
        cellSize = QSize(self.cellSize, self.cellSize)
        cell = QRect(topLeft, cellSize)
        painter.fillRect(cell, cellColor)

    def getInnerCellOffset(self):
        x = (8 * self.cellSize) / 9
        return self.roundHalfUp(x)

    @staticmethod
    def drawTriangle(painter, tl, tr, br, bl, tint=None, shade=None):
        triangle = QPolygonF([])
        if tint:
            color = tint
            brushStyle = Qt.BrushStyle.SolidPattern
            triangle << bl << br << tr
        else:
            assert (shade and not tint)
            color = shade
            brushStyle = Qt.BrushStyle.SolidPattern
            triangle << bl << tl << tr
        path = QPainterPath()
        pen = QPen(QColor(color))
        painter.setPen(pen)
        brush = QBrush()
        brush.setColor(QColor(color))
        brush.setStyle(brushStyle)
        path.addPolygon(triangle)
        painter.drawPolygon(triangle)
        painter.fillPath(path, brush)

    def drawPiecePart(self, painter, row, col, color):
        hue = color
        cs = Board.SCHEMES
        tint = cs.getTint(hue, stepPercent=20)
        shade = cs.getShade(hue)
        (x0, x1, y0, y1) = self.getCellBounds(row, col)
        tlCell = QPointF(x0 + 50, y0 + 50)
        trCell = QPointF(x0 + 50 + self.cellSize, y0 + 50)
        brCell = QPointF(x1, y1)
        blCell = QPointF(x1, y1 + self.cellSize)
        self.drawTriangle(painter, tlCell, trCell, brCell, blCell, tint=tint)
        self.drawTriangle(painter, tlCell, trCell, brCell, blCell, shade=shade)

    def drawFallingPiece(self, painter):
        if self.currFallingPieceBlist:
            for i in range(len(self.currFallingPieceBlist)):
                for j in range(len(self.currFallingPieceBlist[0])):
                    if self.currFallingPieceBlist[i][j]:
                        self.rowPosition = self.currFallingPieceRow + i
                        self.colPosition = self.currFallingPieceCol + j
                        hue = self.currFallingPieceColors['hue']
                        self.drawCell(painter, self.rowPosition, self.colPosition, hue)
                        self.drawPiecePart(painter, self.rowPosition, self.colPosition, hue)
                        # self.currentBoard[self.rowPosition][self.colPosition] = hue

    @staticmethod
    def roundHalfUp(d):
        import decimal
        rounding = decimal.ROUND_HALF_UP
        return int(decimal.Decimal(d).
                   to_integral_value(rounding=rounding))

    def getCurrentPieceColors(self, piece):
        for k in self.scheme:
            if piece == k:
                return self.scheme[k]
        return "NotFound"

    def newFallingPiece(self):
        randomIndex = random.randint(0, self.n - 1)
        # Set values to randomly indexed elements
        self.currFallingPieceObj = self.fallingPieceStrux[randomIndex]
        self.currFallingPieceBlist = self.currFallingPieceObj.getPiece()
        # Get current piece type
        self.currFallingPieceColors = self.getCurrentPieceColors(self.currFallingPieceObj)
        # Set top row of falling piece to top row of board
        self.currFallingPieceRow = 0
        # Set left column of falling piece to place in center of columns
        self.currFallingPieceCol = (self.cols // 2) - (len(self.currFallingPieceBlist[0]) // 2)

    def moveFallingPiece(self, drow, dcol):
        # Move falling piece a given number of rows/columns
        self.currFallingPieceRow += drow
        self.currFallingPieceCol += dcol
        # Check whether the new location is not legal
        if not self.fallingPieceIsLegal():
            # Undo move by resetting values to original
            self.currFallingPieceRow -= drow
            self.currFallingPieceCol -= dcol
            return False
        self.update()
        return True

    def fallingPieceIsLegal(self):
        # Returns True if all cells in the fallingPiece are legal
        for row in range(len(self.currFallingPieceBlist)):
            for col in range(len(self.currFallingPieceBlist[0])):
                # For falling piece cells (i.e. True values in list)
                if self.currFallingPieceBlist[row][col]:
                    # Add the offset of the left-top row and column
                    self.rowPosition = self.currFallingPieceRow + row
                    self.colPosition = self.currFallingPieceCol + col
                    if ((self.rowPosition > self.rows - 1) or
                            (self.colPosition > self.cols - 1) or
                            (self.rowPosition < 0) or (self.colPosition < 0) or
                            (self.currentBoard[self.rowPosition][self.colPosition]
                             != self.bgColor)):
                        return False
        self.update()
        return True

    def rotateFallingPiece(self):
        # Rotate falling piece 90 degrees counterclockwise
        oldPiece = self.currFallingPieceBlist
        oldRowPosition, oldColPosition = self.currFallingPieceRow, self.currFallingPieceCol
        oldNumRows, oldNumCols = len(self.currFallingPieceBlist), len(self.currFallingPieceBlist[0])
        # Calculate the center of the old piece
        oldCenterRow = oldRowPosition + oldNumRows // 2
        oldCenterCol = oldColPosition + oldNumCols // 2
        # Generate a new 2D list based filled with None values
        newPiece = []
        for row in range(oldNumCols):
            newPiece += [[None] * oldNumRows]
        # Iterate through original cells
        for row in range(oldNumRows):
            for col in range(oldNumCols - 1, -1, -1):
                # Move each value to its new location in the newPiece
                newPiece[oldNumCols - col - 1][row] = self.currFallingPieceBlist[row][col]
        # Set fallingPiece/other variables equal to new values
        self.currFallingPieceBlist = newPiece
        newNumRows, newNumCols = len(newPiece), len(newPiece[0])
        self.rowPosition = oldCenterRow - newNumRows // 2
        print(self.rowPosition)
        self.colPosition = oldCenterCol - newNumCols // 2
        print(self.colPosition)
        # Check whether the new piece is legal
        # self.update()
        if not self.fallingPieceIsLegal():
            # Restore the values based on old values stored above
            self.currFallingPieceBlist = oldPiece
            self.currFallingPieceRow = oldRowPosition
            self.currFallingPieceCol = oldColPosition
        self.update()

    def placeFallingPiece(self):
        # Load corresponding cells of falling piece onto the boards
        for row in range(len(self.currFallingPieceBlist)):
            for col in range(len(self.currFallingPieceBlist[0])):
                if self.currFallingPieceBlist[row][col]:
                    # Add the offset of the left-top row and column
                    self.rowPosition = self.currFallingPieceRow + row
                    self.colPosition = self.currFallingPieceCol + col
                    # Load the cells of fallingPiece on board w/ fallingPieceColor
                    hue = self.currFallingPieceColors['hue']
                    self.currentBoard[self.rowPosition][self.colPosition] = hue
                    self.update()
        self.removeFullRows()
        self.update()

    def removeFullRows(self):
        # Clear any full rows from the board
        newRow = self.rows - 1
        fullRows = 0
        for oldRow in range(newRow, -1, -1):
            if self.bgColor in self.currentBoard[oldRow]:
                for col in range(self.cols):
                    # copy row that contains transparent cells
                    self.currentBoard[newRow][col] = self.currentBoard[oldRow][col]
                newRow -= 1
            else:
                fullRows += 1
                self.score += (fullRows ** 2)
        self.numRowsRemoved += fullRows
        self.scoreSignal.emit(self.score)
        self.rowSignal.emit(self.numRowsRemoved)
        self.update()

    def clearBoard(self):
        self.update()

    def gameOverMessage(self, painter):
        mw = self.roundHalfUp(self.width / 2)
        mh = self.roundHalfUp(self.height / 2)
        offset = 30
        centerPt = QPoint(mw, mh + offset)
        gameOverTxt = "GAME OVER"
        painter.drawText(centerPt, gameOverTxt,)
        scoreTxt = "FINAL SCORE: " + str(self.score)
        scorePt = QPoint(mw, mh + 2 * offset)
        painter.drawText(scorePt, scoreTxt)
        retryTxt = "Press 'r' try again!"
        retryPt = QPoint(mw, mh + 3 * offset)
        painter.drawText(retryPt, retryTxt)

    def restartGame(self) -> None:
        self.update()

    def rewindFallingPiece(self):
        pass

    @pyqtSlot(QKeyEvent)
    def onKeyPressEvent(self, event: QKeyEvent) -> None:
        if not self.gameOver:
            if event.key() == Qt.Key.Key_Control.value and \
                    event.key() == Qt.Key.Key_Z.value:
                self.rewindFallingPiece()
            elif event.key() == Qt.Key.Key_Down.value:
                # down-arrow key press --> move down
                self.moveFallingPiece(1, 0)
            elif event.key() == Qt.Key.Key_Right.value:
                # right-arrow key press --> move right
                self.moveFallingPiece(0, 1)
            elif event.key() == Qt.Key.Key_Left.value:
                # left-arrow key press --> move left
                self.moveFallingPiece(0, -1)
            elif event.key() == Qt.Key.Key_Up.value:
                # up-arrow key press --> rotate piece
                self.rotateFallingPiece()
            elif event.key() == Qt.Key.Key_R.value:
                # 'r' key press --> restart game
                self.startGame()
            elif event.key() == Qt.Key.Key_P.value:
                # 'p' key press --> pause game
                self.pauseGame()
            elif event.key() == Qt.Key.Key_Space.value:
                # space bar --> hard drop
                pass
        else:
            if event.key() == Qt.Key.Key_R:
                # 'r' key press --> restart game
                self.startGame()
        self.update()

    def timerEvent(self, event) -> None:
        if event.timerId() == self.timer.timerId():
            if not self.moveFallingPiece(1, 0):
                self.placeFallingPiece()
                self.update()
                self.newFallingPiece()
                # Game over when the falling piece placed is illegal
                if not self.fallingPieceIsLegal():
                    self.gameOver = True
        else:
            super(Board, self).timerEvent(event)

    def mousePressEvent(self, event) -> None:
        pass


def playTetris():
    app = QApplication(sys.argv)
    RunTetris(rows=15, cols=10, margin=25, cellSize=50)
    app.exec()


if __name__ == '__main__':
    playTetris()
