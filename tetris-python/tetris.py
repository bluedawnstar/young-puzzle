import sys
import time
import random
from tkinter import *

class Cell:
    TYPE_I = 0
    TYPE_L = 1
    TYPE_J = 2
    TYPE_T = 3
    TYPE_Z = 4
    TYPE_S = 5
    TYPE_O = 6
    TYPE_WALL = 7
    TYPE_BLANK = 8
    TYPE_BLANK2 = 9

    CELL_COLORS = ['#800000',   #Cell.TYPE_I
                   '#808000',   #Cell.TYPE_L
                   '#808000',   #Cell.TYPE_J
                   '#008080',   #Cell.TYPE_T
                   '#008000',   #Cell.TYPE_Z
                   '#008000',   #Cell.TYPE_S
                   '#000080',   #Cell.TYPE_O
                   '#000000',   #Cell.TYPE_WALL
                   '#FFFFFF',   #Cell.TYPE_BLANK
                   '#DFDFDF']   #Cell.TYPE_BLANK2

    def __init__(self, cellType, x, y, w, h, canvas):
        self.cellType = cellType
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.canvas = canvas;
        self.color = Cell.getColor(cellType)
        self.id = 0
        self.createRect()

    def createRect(self):
        self.id = self.canvas.create_rectangle(self.x, self.y, self.x + self.w, self.y + self.h,
                                               fill=self.color, outline=self.color)

    def changeCellType(self, cellType):
        if self.cellType != cellType:
            self.cellType = cellType;
            self.color = Cell.getColor(cellType)
            self.canvas.itemconfig(self.id, fill=self.color, outline=self.color)

    def getColor(cellType):
        return Cell.CELL_COLORS[cellType]
    
class Board:
    BOARD_TOP_CELLS = 4
    BOARD_COLS = 15
    BOARD_ROWS = 25

    BOARD_TOTAL_ROWS = (BOARD_TOP_CELLS + BOARD_ROWS + 1)
    BOARD_TOTAL_COLS = (BOARD_COLS + 2)
    
    CELL_WIDTH = 20
    CELL_HEIGHT = 20

    NEXT_SHAPE_COLS = 4
    NEXT_SHAPE_ROWS = 4

    WIN_LEFT_MARGIN   = 50
    WIN_RIGHT_MARGIN  = 50
    WIN_TOP_MARGIN    = 30
    WIN_BOTTOM_MARGIN = 30
    
    WIN_NEXT_SHAPE_X = WIN_LEFT_MARGIN
    WIN_NEXT_SHAPE_Y = WIN_TOP_MARGIN
    WIN_NEXT_SHAPE_W = CELL_WIDTH * NEXT_SHAPE_COLS
    WIN_NEXT_SHAPE_H = CELL_HEIGHT * NEXT_SHAPE_ROWS

    WIN_NEXT_SHAPE_RIGHT_MARGIN = CELL_WIDTH

    WIN_BOARD_X = WIN_NEXT_SHAPE_X + WIN_NEXT_SHAPE_W + WIN_NEXT_SHAPE_RIGHT_MARGIN
    WIN_BOARD_Y = WIN_TOP_MARGIN
    WIN_BOARD_W = CELL_WIDTH * (BOARD_COLS + 2)
    WIN_BOARD_H = CELL_HEIGHT * (BOARD_ROWS + BOARD_TOP_CELLS + 1)

    WIN_SCORE_LEFT_MARGIN = CELL_WIDTH
    WIN_SCORE_X = WIN_BOARD_X + WIN_BOARD_W + WIN_SCORE_LEFT_MARGIN
    WIN_SCORE_Y = WIN_BOARD_Y
    WIN_SCORE_W = 100
    WIN_SCORE_H = 50

    WIN_W = WIN_SCORE_X + WIN_SCORE_W + WIN_RIGHT_MARGIN
    WIN_H = WIN_BOARD_Y + WIN_BOARD_H + WIN_BOTTOM_MARGIN

    def __init__(self, tk):
        self.canvas = Canvas(tk, width=Board.WIN_W, height=Board.WIN_H, bd=0, highlightthickness=0)
        self.canvas.pack()

        # make array
        self.cells = []
        self.cellTypes = []
        for i in range(0, Board.BOARD_ROWS + Board.BOARD_TOP_CELLS + 1):
            self.cells.append([None] * (Board.BOARD_COLS + 2))
            self.cellTypes.append([Cell.TYPE_BLANK] * (Board.BOARD_COLS + 2))
        self.cellTypes.append([Cell.TYPE_WALL] * (Board.BOARD_COLS + 2))
            
        # fill upper region
        y1 = Board.WIN_BOARD_Y
        for i in range(0, Board.BOARD_TOP_CELLS):
            x1 = Board.WIN_BOARD_X
            self.cells[i][0] = self._makeCell(Cell.TYPE_WALL, x1, y1)
            self.cellTypes[i][0] = Cell.TYPE_WALL
            for j in range(1, Board.BOARD_COLS + 1):
                x1 += Board.CELL_WIDTH
                self.cells[i][j] = self._makeCell(Cell.TYPE_BLANK2, x1, y1)
                self.cellTypes[i][j] = Cell.TYPE_BLANK2
            x1 += Board.CELL_WIDTH
            self.cells[i][Board.BOARD_COLS + 1] = self._makeCell(Cell.TYPE_WALL, x1, y1)
            self.cellTypes[i][Board.BOARD_COLS + 1] = Cell.TYPE_WALL
            y1 += Board.CELL_HEIGHT
     
        # fill board region
        for i in range(Board.BOARD_TOP_CELLS, Board.BOARD_TOTAL_ROWS - 1):
            x1 = Board.WIN_BOARD_X
            self.cells[i][0] = self._makeCell(Cell.TYPE_WALL, x1, y1)
            self.cellTypes[i][0] = Cell.TYPE_WALL
            for j in range(1, Board.BOARD_COLS + 1):
                x1 += Board.CELL_WIDTH
                self.cells[i][j] = self._makeCell(Cell.TYPE_BLANK, x1, y1)
                self.cellTypes[i][j] = Cell.TYPE_BLANK
            x1 += Board.CELL_WIDTH
            self.cells[i][Board.BOARD_COLS + 1] = self._makeCell(Cell.TYPE_WALL, x1, y1)
            self.cellTypes[i][Board.BOARD_COLS + 1] = Cell.TYPE_WALL
            
            y1 += Board.CELL_HEIGHT
            
        # fill board bottom wall
        x1 = Board.WIN_BOARD_X
        for j in range(0, Board.BOARD_COLS + 2):
            self.cells[Board.BOARD_TOTAL_ROWS - 1][j] = self._makeCell(Cell.TYPE_WALL, x1, y1)
            self.cellTypes[Board.BOARD_TOTAL_ROWS - 1][j] = Cell.TYPE_WALL
            x1 += Board.CELL_WIDTH

        # make array
        self.nextCells = []
        for i in range(0, Board.NEXT_SHAPE_ROWS):
            self.nextCells.append([None] * Board.NEXT_SHAPE_COLS)
            
        # fill next shape region
        y1 = Board.WIN_NEXT_SHAPE_Y
        for i in range(0, Board.NEXT_SHAPE_ROWS):
            x1 = Board.WIN_NEXT_SHAPE_X
            for j in range(0, Board.NEXT_SHAPE_COLS):
                self.nextCells[i][j] = self._makeCell(Cell.TYPE_BLANK, x1, y1)
                x1 += Board.CELL_WIDTH
            y1 += Board.CELL_HEIGHT
 
        # score board
        self.scoreBoard = self.canvas.create_rectangle(Board.WIN_SCORE_X,
                                                       Board.WIN_SCORE_Y,
                                                       Board.WIN_SCORE_X + Board.WIN_SCORE_W,
                                                       Board.WIN_SCORE_Y + Board.WIN_SCORE_H,
                                                       fill="#FFFFFF", outline="#FFFFFF")
        self.scoreText = self.canvas.create_text(Board.WIN_SCORE_X + Board.WIN_SCORE_W // 2,
                                                 Board.WIN_SCORE_Y + Board.WIN_SCORE_H // 2,
                                                 font="Times 14 bold",
                                                 text="0")     

    def _makeCell(self, typ, x1, y1):
        return Cell(typ, x1, y1, Board.CELL_WIDTH, Board.CELL_HEIGHT, self.canvas)

    def getCell(self, row, col):
        return self.cells[row][col]

    def getNextCell(self, row, col):
        return self.nextCells[row][col]

    def clearNextShape(self):
        for i in range(0, Board.NEXT_SHAPE_ROWS):
            for j in range(0, Board.NEXT_SHAPE_COLS):
                self.nextCells[i][j].changeCellType(Cell.TYPE_BLANK)

    def drawNextShape(self, shape):
        self.clearNextShape()

        baseX = Board.NEXT_SHAPE_COLS - 2
        baseY = Board.NEXT_SHAPE_ROWS - 2
        if shape.getType() == Shape.TYPE_O:
            baseX = baseX - 1
            baseY = baseY - 1
        
        positions = shape.getPosDeltaList(0)[0]
        for i in range(0, 4):
            c = baseX + positions[i].x
            r = baseY + positions[i].y
            self.nextCells[r][c].changeCellType(shape.getType())

    def clearCurrShape(self, shape):
        for i in range(0, 4):
            c = shape.basePos.x + shape.cellPosDelta[i].x
            r = shape.basePos.y + shape.cellPosDelta[i].y
            self.cells[r][c].changeCellType(self.cellTypes[r][c])

    def drawCurrShape(self, shape):
        for i in range(0, 4):
            c = shape.basePos.x + shape.cellPosDelta[i].x
            r = shape.basePos.y + shape.cellPosDelta[i].y
            self.cells[r][c].changeCellType(shape.getType())

    def placeShape(self, shape):
        for i in range(0, 4):
            c = shape.basePos.x + shape.cellPosDelta[i].x
            r = shape.basePos.y + shape.cellPosDelta[i].y
            self.cellTypes[r][c] = shape.getType()

    def clearBoard(self):
        # clear upper region
        for i in range(0, Board.BOARD_TOP_CELLS):
            self.cells[i][0].changeCellType(Cell.TYPE_WALL)
            self.cellTypes[i][0] = Cell.TYPE_WALL
            for j in range(1, Board.BOARD_COLS + 1):
                self.cells[i][j].changeCellType(Cell.TYPE_BLANK2)
                self.cellTypes[i][j] = Cell.TYPE_BLANK2
            self.cells[i][Board.BOARD_COLS + 1].changeCellType(Cell.TYPE_WALL)
            self.cellTypes[i][Board.BOARD_COLS + 1] = Cell.TYPE_WALL
     
        # clear board region
        for i in range(Board.BOARD_TOP_CELLS, Board.BOARD_TOTAL_ROWS - 1):
            self.cells[i][0].changeCellType(Cell.TYPE_WALL)
            self.cellTypes[i][0] = Cell.TYPE_WALL
            for j in range(1, Board.BOARD_COLS + 1):
                self.cells[i][j].changeCellType(Cell.TYPE_BLANK)
                self.cellTypes[i][j] = Cell.TYPE_BLANK
            self.cells[i][Board.BOARD_COLS + 1].changeCellType(Cell.TYPE_WALL)
            self.cellTypes[i][Board.BOARD_COLS + 1] = Cell.TYPE_WALL
            
        # clear board bottom wall
        for j in range(0, Board.BOARD_COLS + 2):
            self.cells[Board.BOARD_TOTAL_ROWS - 1][j].changeCellType(Cell.TYPE_WALL)
            self.cellTypes[Board.BOARD_TOTAL_ROWS - 1][j] = Cell.TYPE_WALL
            
        # fill next shape region
        for i in range(0, Board.NEXT_SHAPE_ROWS):
            for j in range(0, Board.NEXT_SHAPE_COLS):
                self.nextCells[i][j].changeCellType(Cell.TYPE_BLANK)         

        self.changeScore(0)

    def changeScore(self, score):
        self.canvas.itemconfig(self.scoreText, text=str(score))
            
    def existFullRow(self):
        for i in range(Board.BOARD_TOP_CELLS, Board.BOARD_TOP_CELLS + Board.BOARD_ROWS):
            n = 0
            for j in range(1, 1 + Board.BOARD_COLS):
                if self.cells[i][j].cellType != Cell.TYPE_BLANK:
                    n += 1
            if n == Board.BOARD_COLS:
                return True
        
        return False

    def eraseFullRows(self):
        res = 0
        
        srcRow = Board.BOARD_TOTAL_ROWS - 2
        dstRow = Board.BOARD_TOTAL_ROWS - 2
        while srcRow >= Board.BOARD_TOP_CELLS:
            n = 0
            for j in range(1, 1 + Board.BOARD_COLS):
                if self.cells[srcRow][j].cellType != Cell.TYPE_BLANK:
                    n += 1
            if n == 0:
                break
            elif n >= Board.BOARD_COLS:
                srcRow -= 1
                res += 1
            else:
                if srcRow != dstRow:
                    for j in range(1, 1 + Board.BOARD_COLS):
                        self.cells[dstRow][j].changeCellType(self.cells[srcRow][j].cellType)
                        self.cellTypes[dstRow][j] = self.cellTypes[srcRow][j]
                srcRow -= 1
                dstRow -= 1
                    
        while dstRow > srcRow:
            for j in range(1, 1 + Board.BOARD_COLS):
                self.cells[dstRow][j].changeCellType(Cell.TYPE_BLANK)
                self.cellTypes[dstRow][j] = Cell.TYPE_BLANK
            dstRow -= 1                
        
        return res

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Shape:
    TYPE_I = Cell.TYPE_I    # 0
    TYPE_L = Cell.TYPE_L    # 1
    TYPE_J = Cell.TYPE_J    # 2
    TYPE_T = Cell.TYPE_T    # 3
    TYPE_Z = Cell.TYPE_Z    # 4
    TYPE_S = Cell.TYPE_S    # 5
    TYPE_O = Cell.TYPE_O    # 6

    ROTATION_0 = 0
    ROTATION_90 = 1
    ROTATION_180 = 2
    ROTATION_270 = 3

    def __init__(self, board):
        self.rotation = Shape.ROTATION_0
        self.board = board
        self.basePos = Position(0, 0)
        self.cellPosDelta = self.getPosDeltaList(0)[0]

    def _canMoveDelta(self, deltaX, deltaY):
        for i in range(0, 4):
            x = self.basePos.x + self.cellPosDelta[i].x + deltaX
            y = self.basePos.y + self.cellPosDelta[i].y + deltaY
            if self.board.cellTypes[y][x] < Cell.TYPE_BLANK:
                return False
        return True

    def _moveDelta(self, deltaX, deltaY):
        self.basePos.x += deltaX
        self.basePos.y += deltaY

    def _canRotateSimple(self):
        rot = (self.rotation + 1) % 4
            
        positions = self.getPosDeltaList(0)[rot]
        for i in range(0, 4):
            x = self.basePos.x + positions[i].x
            y = self.basePos.y + positions[i].y
            if self.board.cellTypes[y][x] < Cell.TYPE_BLANK:
                return False

        return True

    def _rotateSimple(self):
        self.rotation = (self.rotation + 1) % 4
        self.cellPosDelta = self.getPosDeltaList(0)[self.rotation]

    def _canRotateComplex(self):
        rot = (self.rotation + 1) % 4

        possible = True

        positions = self.getPosDeltaList(0)[rot]
        for i in range(0, 4):
            x = self.basePos.x + positions[i].x
            y = self.basePos.y + positions[i].y
            if self.board.cellTypes[y][x] < Cell.TYPE_BLANK:
                possible = False
                break

        if possible == True:
            return True

        positions = self.getPosDeltaList(1)[rot]
        for i in range(0, 4):
            x = self.basePos.x + positions[i].x
            y = self.basePos.y + positions[i].y
            if self.board.cellTypes[y][x] < Cell.TYPE_BLANK:
                return False

        return True

    def _rotateComplex(self):
        oldRot = self.rotation
        self.rotation = (self.rotation + 1) % 4

        rotType = 0

        positions = self.getPosDeltaList(0)[self.rotation]
        for i in range(0, 4):
            x = self.basePos.x + positions[i].x
            y = self.basePos.y + positions[i].y
            if self.board.cellTypes[y][x] < Cell.TYPE_BLANK:
                rotType = 1
                break;

        if rotType == 0:
            self.cellPosDelta = positions
        else:
            self.cellPosDelta = self.getPosDeltaList(1)[self.rotation]

    #def getType(self):
    #    return 0

    #def getPosDeltaList(self, index):
    #    return None

    def setInitPosition(self):
        self.rotation = 0
        self.basePos.x = Board.BOARD_COLS // 2 + 1
        self.basePos.y = Board.BOARD_TOP_CELLS - 2
        self.cellPosDelta = self.getPosDeltaList(0)[0]
    
    #def canRotate(self):
    #    pass

    #def rotate(self):
    #    pass

    def canMoveLeft(self):
        return self._canMoveDelta(-1, 0)

    def moveLeft(self):
        self._moveDelta(-1, 0)

    def canMoveRight(self):
        return self._canMoveDelta(1, 0)    

    def moveRight(self):
        self._moveDelta(1, 0)

    def canMoveDown(self):
        return self._canMoveDelta(0, 1)
    
    def moveDown(self):
        self._moveDelta(0, 1)

    def dropDown(self):
        n = 0
        while self.canMoveDown():
            n += 1
            self.moveDown()
        return n

class ShapeI(Shape):
    # O
    # O
    # *
    # O
    POSITIONS0 = [[Position( 0, 1), Position( 0, 0), Position(0, -1), Position(0, -2)], # 0
                  [Position(-2, 0), Position(-1, 0), Position(0,  0), Position(1,  0)], # 90
                  [Position( 0, 1), Position( 0, 0), Position(0, -1), Position(0, -2)], # 180
                  [Position(-2, 0), Position(-1, 0), Position(0,  0), Position(1,  0)]] # 270
    # O
    # *
    # O
    # O
    POSITIONS1 = [[Position( 0, 2), Position( 0, 1), Position(0,  0), Position(0, -1)], # 0
                  [Position(-1, 0), Position( 0, 0), Position(1,  0), Position(2,  0)], # 90
                  [Position( 0, 2), Position( 0, 1), Position(0,  0), Position(0, -1)], # 180
                  [Position(-1, 0), Position( 0, 0), Position(1,  0), Position(2,  0)]] # 270
    
    def __init__(self, board):
        Shape.__init__(self, board)

    def getType(self):
        return Shape.TYPE_I

    def getPosDeltaList(self, index):
        if index == 0:
            return ShapeI.POSITIONS0
        else:
            return ShapeI.POSITIONS1

    def canRotate(self):
        return self._canRotateComplex()

    def rotate(self):
        self._rotateComplex()

class ShapeL(Shape):
    # O
    # *
    # OO
    POSITIONS = [[Position( 0, 1), Position( 1, 1), Position(0,  0), Position( 0, -1)], # 0
                 [Position(-1, 0), Position( 0, 0), Position(1,  0), Position( 1, -1)], # 90
                 [Position( 0, 1), Position( 0, 0), Position(0, -1), Position(-1, -1)], # 180
                 [Position(-1, 1), Position(-1, 0), Position(0,  0), Position( 1,  0)]] # 270
    
    def __init__(self, board):
        Shape.__init__(self, board)

    def getType(self):
        return Shape.TYPE_L

    def getPosDeltaList(self, index):
        return ShapeL.POSITIONS

    def canRotate(self):
        return self._canRotateSimple()

    def rotate(self):
        self._rotateSimple()

class ShapeJ(Shape):
    #  O
    #  *
    # OO
    POSITIONS = [[Position(-1,  1), Position( 0, 1), Position(0,  0), Position(0, -1)], # 0
                 [Position(-1,  0), Position( 0, 0), Position(1,  0), Position(1,  1)], # 90
                 [Position( 0,  1), Position( 0, 0), Position(0, -1), Position(1, -1)], # 180
                 [Position(-1, -1), Position(-1, 0), Position(0,  0), Position(1,  0)]] # 270
    
    def __init__(self, board):
        Shape.__init__(self, board)

    def getType(self):
        return Shape.TYPE_J

    def getPosDeltaList(self, index):
        return ShapeJ.POSITIONS

    def canRotate(self):
        return self._canRotateSimple()

    def rotate(self):
        self._rotateSimple()

class ShapeT(Shape):
    #  O
    # O*
    #  O
    POSITIONS = [[Position( 0,  1), Position(-1, 0), Position(0, 0), Position(0, -1)], # 0
                 [Position(-1,  0), Position( 0, 0), Position(1, 0), Position(0,  1)], # 90
                 [Position( 0,  1), Position( 0, 0), Position(1, 0), Position(0, -1)], # 180
                 [Position( 0, -1), Position(-1, 0), Position(0, 0), Position(1,  0)]] # 270
    
    def __init__(self, board):
        Shape.__init__(self, board)

    def getType(self):
        return Shape.TYPE_T

    def getPosDeltaList(self, index):
        return ShapeT.POSITIONS

    def canRotate(self):
        return self._canRotateSimple()

    def rotate(self):
        self._rotateSimple()

class ShapeZ(Shape):
    #  O
    # O*
    # O
    POSITIONS0 = [[Position(-1,  1), Position(-1,  0), Position(0, 0), Position(0, -1)], # 0
                  [Position(-1,  0), Position( 0,  0), Position(0, 1), Position(1,  1)], # 90
                  [Position(-1,  1), Position(-1,  0), Position(0, 0), Position(0, -1)], # 180
                  [Position(-1,  0), Position( 0,  0), Position(0, 1), Position(1,  1)]] # 270
    #  O
    # *O
    # O
    POSITIONS1 = [[Position( 0,  1), Position( 0,  0), Position(1, 0), Position(1, -1)], # 0
                  [Position(-1, -1), Position( 0, -1), Position(0, 0), Position(1,  0)], # 90
                  [Position( 0,  1), Position( 0,  0), Position(1, 0), Position(1, -1)], # 180
                  [Position(-1, -1), Position( 0, -1), Position(0, 0), Position(1,  0)]] # 270
    
    def __init__(self, board):
        Shape.__init__(self, board)

    def getType(self):
        return Shape.TYPE_Z

    def getPosDeltaList(self, index):
        if index == 0:
            return ShapeZ.POSITIONS0
        else:
            return ShapeZ.POSITIONS1

    def canRotate(self):
        return self._canRotateComplex()

    def rotate(self):
        self._rotateComplex()

class ShapeS(Shape):
    # O
    # O*
    #  O
    POSITIONS0 = [[Position( 0, 1), Position(-1, 0), Position(0,  0), Position(-1, -1)], # 0
                  [Position(-1, 1), Position( 0, 1), Position(0,  0), Position( 1,  0)], # 90
                  [Position( 0, 1), Position(-1, 0), Position(0,  0), Position(-1, -1)], # 180
                  [Position(-1, 1), Position( 0, 1), Position(0,  0), Position( 1,  0)]] # 270
    # O
    # *O
    #  O
    POSITIONS1 = [[Position( 1, 1), Position( 0, 0), Position(1,  0), Position( 0, -1)], # 0
                  [Position(-1, 0), Position( 0, 0), Position(0, -1), Position( 1, -1)], # 90
                  [Position( 1, 1), Position( 0, 0), Position(1,  0), Position( 0, -1)], # 180
                  [Position(-1, 0), Position( 0, 0), Position(0, -1), Position( 1, -1)]] # 270
    
    def __init__(self, board):
        Shape.__init__(self, board)

    def getType(self):
        return Shape.TYPE_S

    def getPosDeltaList(self, index):
        if index == 0:
            return ShapeS.POSITIONS0
        else:
            return ShapeS.POSITIONS1

    def canRotate(self):
        return self._canRotateComplex()

    def rotate(self):
        self._rotateComplex()

class ShapeO(Shape):
    # *O
    # OO
    POSITIONS = [[Position(0, 0), Position(1, 0), Position(0, 1), Position(1, 1)], # 0
                 [Position(0, 0), Position(1, 0), Position(0, 1), Position(1, 1)], # 90
                 [Position(0, 0), Position(1, 0), Position(0, 1), Position(1, 1)], # 180
                 [Position(0, 0), Position(1, 0), Position(0, 1), Position(1, 1)]] # 270
    
    def __init__(self, board):
        Shape.__init__(self, board)

    def getType(self):
        return Shape.TYPE_O

    def getPosDeltaList(self, index):
        return ShapeO.POSITIONS

    def canRotate(self):
        return False

    def rotate(self):
        pass

#-------------------------------------------------------------------------------

class Tetris:
    STATE_IDLE    = 0
    STATE_PLAYING = 1

    SCORE_OF_ERASED_LINES = [0,
                             10,    # 10 x 1
                             30,    # 10 x 2 x 1.5
                             60,    # 10 x 3 x 2
                             120]   # 10 x 4 x 3

    SHAPE_COUNT_PER_LEVEL = 20
    DOWN_TIME_MIN = 500             # ms
    DOWN_TIME_MAX = 50              # ms
    DOWN_TIME_DELTA = 50            # ms
    
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Tetris for Soomin")
        self.tk.resizable(0, 0)
        #self.tk.wm_attributes("-topmost", 1)

        random.seed()

        self.board = Board(self.tk)

        self.state = Tetris.STATE_IDLE
        self.score = 0

        self.downTime = Tetris.DOWN_TIME_MIN
        self.shapeCount = 0
        
    def _makeShape(self, shapeType):
        if shapeType == Shape.TYPE_I:
            return ShapeI(self.board)
        elif shapeType == Shape.TYPE_L:
            return ShapeL(self.board)
        elif shapeType == Shape.TYPE_J:
            return ShapeJ(self.board)
        elif shapeType == Shape.TYPE_T:
            return ShapeT(self.board)
        elif shapeType == Shape.TYPE_Z:
            return ShapeZ(self.board)
        elif shapeType == Shape.TYPE_S:
            return ShapeS(self.board)
        elif shapeType == Shape.TYPE_O:
            return ShapeO(self.board)

    def makeNextShape(self):
        self.nextShapeType = random.randint(Shape.TYPE_I, Shape.TYPE_O)
        self.nextShape = self._makeShape(self.nextShapeType)

    def makeCurrShape(self):
        self.currShapeType = random.randint(Shape.TYPE_I, Shape.TYPE_O)
        self.currShape = self._makeShape(self.currShapeType)

    def onLineErased(self, lines, dropRowCount):
        self.score += Tetris.SCORE_OF_ERASED_LINES[lines] + \
                      dropRowCount * lines * Tetris.SCORE_OF_ERASED_LINES[1]
        self.board.changeScore(self.score)

    def onEnd(self, byUser):
        btnStop.config(state="disabled")
        btnStart.config(state="normal")
        self.state = Tetris.STATE_IDLE

        result = simpledialog.askstring("입력", "이름을 입력해주세요.", parent=tetris.tk)
        if result != None:
            sys.stdout.write("name = " + result + "\n")

        # save score ...
        
    def onNewShape(self):
        if self.currShape._canMoveDelta(0, 0) == False:
            self.onEnd(False)
        else:
            self.shapeCount += 1
            if self.shapeCount > Tetris.SHAPE_COUNT_PER_LEVEL:
                self.shapeCount = 1
                self.downTime -= Tetris.DOWN_TIME_DELTA
                if self.downTime < Tetris.DOWN_TIME_MAX:
                    self.downTime = Tetris.DOWN_TIME_MIN

    def onTimer(self):
        if self.state != Tetris.STATE_PLAYING:
            return
           
        self.processMoveDown()
        self.tk.after(self.downTime, self.onTimer)

    def processShapeDrop(self, dropRowCount):
        if self.state != Tetris.STATE_PLAYING:
            return
        
        self.board.placeShape(self.currShape)
        lines = self.board.eraseFullRows()
        if lines > 0:
            self.onLineErased(lines, dropRowCount)

        self.currShape = self.nextShape
        self.makeNextShape()

        self.board.drawNextShape(self.nextShape)
        self.currShape.setInitPosition()
        self.board.drawCurrShape(self.currShape)

        self.onNewShape()

    def processRotate(self):
        if self.state != Tetris.STATE_PLAYING:
            return False
        
        if self.currShape.canRotate():
            self.board.clearCurrShape(self.currShape)
            self.currShape.rotate()
            self.board.drawCurrShape(self.currShape)
            return True
        return False

    def processMoveLeft(self):
        if self.state != Tetris.STATE_PLAYING:
            return False
        
        if self.currShape.canMoveLeft():
            self.board.clearCurrShape(self.currShape)
            self.currShape.moveLeft()
            self.board.drawCurrShape(self.currShape)
            return True
        return False

    def processMoveRight(self):
        if self.state != Tetris.STATE_PLAYING:
            return False
        
        if self.currShape.canMoveRight():
            self.board.clearCurrShape(self.currShape)
            self.currShape.moveRight()
            self.board.drawCurrShape(self.currShape)
            return True
        return False

    def processMoveDown(self):
        if self.state != Tetris.STATE_PLAYING:
            return False
        
        if self.currShape.canMoveDown():
            self.board.clearCurrShape(self.currShape)
            self.currShape.moveDown()
            self.board.drawCurrShape(self.currShape)
            return True
        else:
            self.processShapeDrop(0)
            return False

    def processDropDown(self):
        if self.state != Tetris.STATE_PLAYING:
            return 0

        dropRowCount = 0
        if self.currShape.canMoveDown():
            self.board.clearCurrShape(self.currShape)
            dropRowCount = self.currShape.dropDown()
            self.board.drawCurrShape(self.currShape)
        self.processShapeDrop(dropRowCount)

    def processStart(self):
        btnStart.config(state="disabled")
        btnStop.config(state="normal")

        self.state = Tetris.STATE_PLAYING

        self.score = 0
        self.board.clearBoard()

        self.downTime = Tetris.DOWN_TIME_MIN
        self.shapeCount = 1

        self.makeNextShape()
        self.makeCurrShape()
        
        self.board.drawNextShape(self.nextShape)
        self.currShape.setInitPosition()
        self.board.drawCurrShape(self.currShape)

        self.tk.after(self.downTime, self.onTimer)

    def processStop(self):
        self.onEnd(True)

    def play(self):
        self.tk.mainloop()

def processUpKey(event):
    tetris.processRotate()

def processLeftKey(event):
    tetris.processMoveLeft()

def processRightKey(event):
    tetris.processMoveRight()

def processDownKey(event):
    tetris.processMoveDown()

def processSpaceKey(event):
    tetris.processDropDown()
    
tetris = Tetris()

btnStart = Button(tetris.tk, text="Start", command=tetris.processStart)
btnStop = Button(tetris.tk, text="Stop", command=tetris.processStop)

btnStart.place(x=20, y=Board.WIN_NEXT_SHAPE_Y + Board.WIN_NEXT_SHAPE_H + 50, width=110, height=25)
btnStop.place(x=20, y=Board.WIN_NEXT_SHAPE_Y + Board.WIN_NEXT_SHAPE_H + 50 + 30, width=110, height=25)
btnStop.config(state="disabled")

tetris.tk.bind("<Key-Up>", processUpKey)
tetris.tk.bind("<Key-Left>", processLeftKey)
tetris.tk.bind("<Key-Right>", processRightKey)
tetris.tk.bind("<Key-Down>", processDownKey)
tetris.tk.bind("<Key- >", processSpaceKey)

tetris.play()
