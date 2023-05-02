import random
from PyQt6.QtCore import Qt
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from color_schemes import ColorSchemes
from tetromino import Tetromino
from util import BKGDCell


class Board(QGroupBox):
    gameStatusSignal = pyqtSignal(object)
    nextSignal = pyqtSignal(object)
    heldSignal = pyqtSignal(object)
    scoreSignal = pyqtSignal(int)
    rowSignal = pyqtSignal(int)
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
        self.gameStatus = dict.fromkeys(['paused', 'over'], None)
        inst = Tetromino(defaultNumber=1)
        self.scheme = Tetromino.colors
        self.fallingPieceStrux = inst.getStructs()
        self.dummyHoldPieceObj = self.fallingPieceStrux[6]
        self.n = len(self.fallingPieceStrux)
        self.bgColor = "#00FFFFFF"
        # CURRENT FALLING PIECE
        self.nextFallingPieceObj = None
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

        self.setFixedSize(self.width + 100, self.height + 100)
        self.grid = None
        self.hcenter = Qt.AlignmentFlag.AlignHCenter
        self.vcenter = Qt.AlignmentFlag.AlignVCenter
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
            self.gameStatus['paused'] = True
            self.gameStatusSignal.emit(self.gameStatus)
        else:
            self.timer.start(self.timerDelay, self)
            self.gameStatus['paused'] = False
            self.gameStatusSignal.emit(self.gameStatus)
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

    # creates self.currentBoard
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

    def drawBackground(self, painter, width=None, height=None, start=None):
        if not width and not height:
            width = self.width
            height = self.height
            start = QPointF(50, 50)
        path = QPainterPath()
        size = QSizeF(width, height)
        rect = QRectF(start, size)
        path.addRoundedRect(rect, 20, 20)
        color = QColor(151, 217, 0)
        color.setAlpha(59)
        pen = QPen(QColor("#333333"), 5)
        painter.setPen(pen)
        painter.fillPath(path, color)
        painter.drawPath(path)

    def drawCell(self, painter, row, col, color, next=False, held=False):
        if next:
            x, y = 100, 460
        elif held:
            x, y = 350, 460
        else:
            x, y = 50, 50
        (x0, x1, y0, y1) = self.getCellBounds(row, col)
        cellColor = QColor(color)
        topLeft = QPoint(x0 + x, y0 + y)
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

    def drawPiecePart(self, painter, row, col, color, next=False, held=False):
        if next:
            x, y = 100, 460
        elif held:
            x, y = 350, 460
        else:
            x, y = 50, 50
        hue = color
        cs = Board.SCHEMES
        tint = cs.getTint(hue, stepPercent=15)
        shade = cs.getShade(hue, stepPercent=15)
        (x0, x1, y0, y1) = self.getCellBounds(row, col)
        tlCell = QPointF(x0 + x, y0 + y)
        trCell = QPointF(x0 + x + self.cellSize, y0 + y)
        brCell = QPointF(x1 + x - self.cellSize, y1 + y)
        blCell = QPointF(x1 + x, y1 + y)
        self.drawTriangle(painter, tlCell, trCell, brCell, blCell, shade=shade)
        self.drawTriangle(painter, tlCell, trCell, brCell, blCell, tint=tint)

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
        self.heldSignal.emit(self.dummyHoldPieceObj)
        randomIndex = random.randint(0, self.n - 1)
        # Set values to randomly indexed elements
        if not self.nextFallingPieceObj:
            self.nextFallingPieceObj = self.fallingPieceStrux[randomIndex]
            self.currFallingPieceObj = self.fallingPieceStrux[randomIndex]
        else:
            self.currFallingPieceObj = self.nextFallingPieceObj
            self.nextFallingPieceObj = self.fallingPieceStrux[randomIndex]
            self.nextSignal.emit(self.nextFallingPieceObj)

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
        # print(self.rowPosition)
        self.colPosition = oldCenterCol - newNumCols // 2
        # print(self.colPosition)
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
        painter.drawText(centerPt, gameOverTxt)
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

    def activateHoldQueue(self):
        # press Ctrl + C to activate hold queue
        # removes current piece from board
        # draws outline in hold queue
        # draws piece after next piece is placed
        pass

    @pyqtSlot(QKeyEvent)
    def onKeyPressEvent(self, event: QKeyEvent) -> None:
        if not self.gameOver:
            if event.key() == Qt.Key.Key_Control.value and \
                    event.key() == Qt.Key.Key_Z.value:
                self.rewindFallingPiece()
            elif event.key() == Qt.Key.Key_Control.value and \
                    event.key() == Qt.Key.Key_C.value:
                self.activateHoldQueue()
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
