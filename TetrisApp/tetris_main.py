import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from board import Board
from server import Server
from ctrl_panel import CtrlPanel


class RunTetris(QMainWindow):
    startBoardSignal = pyqtSignal(bool)
    pauseBoardSignal = pyqtSignal(bool)
    userSignal = pyqtSignal(str)
    scoreSignal = pyqtSignal(int)
    rowSignal = pyqtSignal(int)
    key_pressed = pyqtSignal(QKeyEvent)
    paint_event = pyqtSignal(QPaintEvent)
    mouse_pressed = pyqtSignal(QMouseEvent)

    def __init__(self, rows=15, cols=10, margin=25, cellSize=50):
        super(RunTetris, self).__init__()
        self.timerDelay = None
        self.board = None
        self.ctrlPanel = None
        self.rows, self.cols = rows, cols
        self.cellSize, self.margin = cellSize, margin
        self.width = self.getWidth()
        self.height = self.getHeight()
        self.paused, self.started = False, False
        self.initGUI()
        self.startServer()

    def initGUI(self):
        self.board = Board(self)
        self.board.scoreSignal[int].connect(self.currentScore)
        self.board.rowSignal[int].connect(self.currentRowsRmv)
        self.ctrlPanel = CtrlPanel(self)
        self.ctrlPanel.startRTSignal[bool].connect(self.startBoard)
        self.ctrlPanel.pauseRTSignal[bool].connect(self.pauseBoard)
        # board components
        hbox = QHBoxLayout()
        layout = QWidget()
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

    def startBoard(self, started: bool):
        self.started = started
        self.startBoardSignal.emit(self.started)

    def pauseBoard(self, paused: bool):
        self.paused = paused
        self.pauseBoardSignal.emit(self.paused)

    def startServer(self):
        Server(self)

    def currentScore(self, score):
        self.scoreSignal.emit(score)
        # print("Score: ", score)

    def currentRowsRmv(self, rows):
        self.rowSignal.emit(rows)
        # print("Rows: ", rows)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.key_pressed.emit(event)
        return super().keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.mouse_pressed.emit(event)
        return super().mousePressEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        self.paint_event.emit(event)
        return super().paintEvent(event)

    def getWidth(self):
        return (self.margin * 2) + (self.cellSize * self.cols)

    def getHeight(self):
        return (self.margin * 2) + (self.cellSize * self.rows)

    def __str__(self):
        print('width   -->', self.width)
        print('height  -->', self.height)
        print('cellSize ->', self.cellSize)
        print('margin  -->', self.margin)


def playTetris():
    app = QApplication(sys.argv)
    RunTetris(rows=15, cols=10, margin=25, cellSize=50)
    app.exec()


if __name__ == '__main__':
    playTetris()
