#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 03:04:42 2018

@author: harrietobrien
"""

from tkinter import *
import random


def init(data):
    # Initialize board dimensions
    data.rows = 15
    data.cols = 10
    data.emptyColor = "azure"
    data.board = board(data)
    data.gameOver = False
    # Represent seven standard pieces (tetrominoes)
    data.iPiece = [[True, True, True, True]]
    data.jPiece = [[True, False, False], [True, True, True]]
    data.lPiece = [[False, False, True], [True, True, True]]
    data.oPiece = [[True, True], [True, True]]
    data.sPiece = [[False, True, True], [True, True, False]]
    data.tPiece = [[False, True, False], [True, True, True]]
    data.zPiece = [[True, True, False], [False, True, True]]
    # Place all 7 piece types into single 3D list - tetrisPieces
    data.tetrisPieces = ([data.iPiece, data.jPiece, data.lPiece, data.oPiece,
                          data.sPiece, data.tPiece, data.zPiece])
    # Define colors corresponding to pieces in same-size list
    data.tetrisPieceColors = (["cyan", "blue",
                               "orange", "yellow",
                               "lawn green",
                               "red", "magenta"])
    # Generate a falling piece
    # Select first falling piece of game
    newFallingPiece(data)
    # Value score - incremented in removeFullRows function
    data.score = 0


# Allocate board as 2D list filled with data.emptyColor ("blue")
def board(data):
    board = []
    for _ in range(data.rows):
        board += [[data.emptyColor] * data.cols]
    return board


# Creates board by calling drawCell for every row/column
# Displays score in the center of the top margin
def drawBoard(canvas, data):
    drawScore(canvas, data)
    for row in range(data.rows):
        for col in range(data.cols):
            color = data.board[row][col]
            drawCell(canvas, data, row, col, color)


# Creates text to be displayed above the board
def drawScore(canvas, data):
    txt = "SCORE: "
    # Creates string representation of data.score
    score = str(data.score)
    fnt = "Arial 18 bold"
    fll = "Navy"
    txt1 = "TETRIS"
    canvas.create_text(data.width / 2, 20, text=txt + score, font=fnt, fill=fll)
    canvas.create_text(data.width / 2, data.height - 20, text=txt1, font=fnt, fill=fll)


# Creates cell using the color stored for the given row/column
def drawCell(canvas, data, row, col, color):
    (x0, x1, y0, y1) = getCellBounds(row, col, data)
    # Draws rectangle with appropriate color
    canvas.create_rectangle(x0, y0, x1, y1, fill="black")
    canvas.create_rectangle(x0 + 2, y0 + 2, x1 - 2, y1 - 2, fill=color)


# Reference - http://www.cs.cmu.edu/~112m18/notes/notes-animations-part1.html
def getCellBounds(row, col, data):
    x0 = data.margin + col * data.cellSize
    x1 = data.margin + (col + 1) * data.cellSize
    y0 = data.margin + row * data.cellSize
    y1 = data.margin + (row + 1) * data.cellSize
    return (x0, x1, y0, y1)


# Creates the orange background on which the board is displayed
def drawBackground(canvas, data):
    backgroundFill = "lime green"
    w, h = data.width + (data.width / 2), data.height
    canvas.create_rectangle(0, 0, w, h, fill=backgroundFill)

# Randomly chooses new piece and sets its color
# Positions piece in the middle of the top row
def newFallingPiece(data):
    # Randomly choose an index from the tetrisPieces list
    randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
    # Set data values to randomly indexed elements
    data.fallingPiece = data.tetrisPieces[randomIndex]
    data.fallingPieceColor = data.tetrisPieceColors[randomIndex]
    # Set top row of falling piece to top row of board
    data.fallingPieceRow = 0
    # Set left column of falling piece to place in center of columns
    data.fallingPieceCol = (data.cols // 2) - (len(data.fallingPiece[0]) // 2)


# Draws falling piece over the board
def drawFallingPiece(canvas, data):
    # Iterate over each cell in data.fallingPiece
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            # If the value of the cell is True
            if data.fallingPiece[row][col]:
                # Define the color used as the color of the fallingPiece
                color = data.fallingPieceColor
                # Add the offset of the left-top row and column
                data.rowPosition = data.fallingPieceRow + row
                data.colPosition = data.fallingPieceCol + col
                # Call drawCell to draw the falling piece cell
                drawCell(canvas, data, data.rowPosition, data.colPosition, color)


# Move falling piece a given number of rows/columns
def moveFallingPiece(data, drow, dcol):
    # Modify the data values to increase/decrease the row/column
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    # Check whether the new location is not legal
    if not fallingPieceIsLegal(data):
        # Undo move by resetting data values to original
        data.fallingPieceRow -= drow
        data.fallingPieceCol -= dcol
        return False
    return True


# Returns True if all cells in the fallingPiece are legal
def fallingPieceIsLegal(data):
    # Iterate over every cell in data.fallingPiece
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            # For falling piece cells (i.e. True values in list)
            if data.fallingPiece[row][col]:
                # Add the offset of the left-top row and column
                data.rowPosition = data.fallingPieceRow + row
                data.colPosition = data.fallingPieceCol + col
                # Confirm that the cell is on the board
                # Confirm that the color is the emptyColor
                if ((data.rowPosition > data.rows - 1) or
                        (data.colPosition > data.cols - 1) or
                        (data.rowPosition < 0) or
                        (data.colPosition < 0) or
                        (data.board[data.rowPosition]
                         [data.colPosition] != data.emptyColor)):
                    return False
    return True


# Rotate falling piece 90 degrees counterclockwise
def rotateFallingPiece(data):
    # Store data associated with old piece
    oldPiece = data.fallingPiece
    oldRowPosition, oldColPosition = data.fallingPieceRow, data.fallingPieceCol
    oldNumRows, oldNumCols = len(data.fallingPiece), len(data.fallingPiece[0])
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
            newPiece[oldNumCols - col - 1][row] = data.fallingPiece[row][col]
    # Set fallingPiece/other variables equal to new values
    data.fallingPiece = newPiece
    newNumRows, newNumCols = len(newPiece), len(newPiece[0])
    data.rowPosition = oldCenterRow - newNumRows // 2
    data.colPosition = oldCenterCol - newNumCols // 2
    # Check whether the new piece is legal
    if not fallingPieceIsLegal(data):
        # Restore the values based on old values stored above
        data.fallingPiece = oldPiece
        data.fallingPieceRow = oldRowPosition
        data.fallingPieceCol = oldColPosition


# use event.char and event.keysym
def keyPressed(event, data):
    if not data.gameOver:
        # Move down in response to down-arrow key press
        if event.keysym == "Down":
            moveFallingPiece(data, 1, 0)
        # Move right in response to right-arrow key press
        elif event.keysym == "Right":
            moveFallingPiece(data, 0, 1)
        # Move left in response to left-arrow key press
        elif event.keysym == "Left":
            moveFallingPiece(data, 0, -1)
        # Rotate in response to up-arrow key press
        elif event.keysym == "Up":
            rotateFallingPiece(data)
        # Restart game at any time by hitting 'r'
        elif event.char == "r":
            init(data)
    else:
        # Restart game after completion by hitting 'r'
        if event.char == "r":
            init(data)


def timerFired(data):
    if not moveFallingPiece(data, 1, 0):
        placeFallingPiece(data)
        # Start a new falling piece from the top
        newFallingPiece(data)
        # Game over when the falling piece placed is illegal
        if not fallingPieceIsLegal(data):
            data.gameOver = True


# Load corresponding cells of falling piece onto the board
def placeFallingPiece(data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            print(data.fallingPiece)
            if data.fallingPiece[row][col]:
                # Add the offset of the left-top row and column
                data.rowPosition = data.fallingPieceRow + row
                data.colPosition = data.fallingPieceCol + col
                # Load the cells of fallingPiece on board w/ fallingPieceColor
                data.board[data.rowPosition][data.colPosition] = \
                    data.fallingPieceColor
    # Full rows are cleared - updates the board
    removeFullRows(data)


# Clear any full rows from the board
def removeFullRows(data):
    newRow = data.rows - 1
    # Number of full rows
    fullRows = 0
    for oldRow in range(newRow, -1, -1):
        # If row contains emptyColor
        if data.emptyColor in data.board[oldRow]:
            for col in range(data.cols):
                # Copy row that still contains cells of emptyColor
                data.board[newRow][col] = data.board[oldRow][col]
            # Move the rows above down
            newRow -= 1
        else:
            # Keep track of full rows removed
            fullRows += 1
            # Increment score by square of the number of full rows removed
            data.score += fullRows ** 2

def roundRectangle(x1, y1, x2, y2, r=25, **kwargs):    
    points = (x1+r, y1, x1+r, y1,
              x2-r, y1, x2-r, y1,
              x2, y1, x2, y1+r,
              x2, y1+r, x2, y2-r,
              x2, y2-r, x2, y2,
              x2-r, y2, x2-r, y2,
              x1+r, y2, x1+r, y2,
              x1, y2, x1, y2-r,
              x1, y2-r, x1, y1+r,
              x1, y1+r, x1, y1)
    return canvas.create_polygon(points, **kwargs, smooth=True)

# Creates message to be displayed when the game is complete
def gameOverMessage(canvas, data):
    txt1 = "YOU FAILED"
    fnt1 = "Arial 24 bold"
    canvas.create_text(data.width / 2, data.height / 2 - 30, text=txt1, font=fnt1)
    score = str(data.score)
    txt2 = "FINAL SCORE: " + score
    fnt2 = "Arial 18 bold"
    canvas.create_text(data.width / 2, data.height / 2 + 10, text=txt2, font=fnt2)
    txt3 = "Press 'r' try again!"
    canvas.create_text(data.width / 2, data.height / 2 + 40, text=txt3, font=fnt2)


def redrawAll(canvas, data):
    # If the game is not over (i.e. the current falling piece is legal)
    # scoreBox(canvas, data)
    if not data.gameOver:
        # Create background, board, and falling piece
        drawBackground(canvas, data)
        drawBoard(canvas, data)
        drawFallingPiece(canvas, data)
    else:
        # Create background and game over message
        drawBackground(canvas, data)
        gameOverMessage(canvas, data)

def mousePressed(event, data):
    pass


def run(width=450, height=650, margin=25, cellSize=50):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object):
    
        def __init__(self, width, height, margin, cellSize):
            self.width = width
            self.height = height
            self.margin = margin
            self.cellSize = cellSize
        
    data = Struct(width, height, margin, cellSize)
    data.timerDelay = 300  # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
    mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
    keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


# Defines the dimensions for the game
# Calls run() providng the appropriate computed window size
def playTetris(rows=15, cols=10):
    margin = 40
    cellSize = 50
    width = (margin * 2) + (cellSize * cols)
    height = (margin * 2) + (cellSize * rows)
    print(width, height)
    run(width, height, margin, cellSize)


playTetris()
