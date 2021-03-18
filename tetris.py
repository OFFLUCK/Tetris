#Libraries.
import pygame
import random


pygame.font.init()


#Consts.
sWidth = 800
sHeight = 700
blockSize = 30
playWidth = 10 * blockSize
playHeight = 20 * blockSize
topLeftX = (sWidth - playWidth) // 2
topLeftY = sHeight - playHeight


#Shapes: SZIOJLT, 0-6.
S = [
    ['.....',
     '.....',
     '..00.',
     '.00..',
     '.....'],
    ['.....',
     '..0..',
     '..00.',
     '...0.',
     '.....']
]


Z = [
    ['.....',
     '.....',
     '.00..',
     '..00.',
     '.....'],
    ['.....',
     '..0..',
     '.00..',
     '.0...',
     '.....']
]


I = [
    ['..0..',
     '..0..',
     '..0..',
     '..0..',
     '.....'],
    ['.....',
     '0000.',
     '.....',
     '.....',
     '.....']
]


O = [
    ['.....',
     '.....',
     '.00..',
     '.00..',
     '.....']
]


J = [
    ['.....',
     '.0...',
     '.000.',
     '.....',
     '.....'],
    ['.....',
     '..00.',
     '..0..',
     '..0..',
     '.....'],
    ['.....',
     '.....',
     '.000.',
     '...0.',
     '.....'],
    ['.....',
     '..0..',
     '..0..',
     '.00..',
     '.....']
]


L = [
    ['.....',
     '...0.',
     '.000.',
     '.....',
     '.....'],
    ['.....',
     '..0..',
     '..0..',
     '..00.',
     '.....'],
    ['.....',
     '.....',
     '.000.',
     '.0...',
     '.....'],
    ['.....',
     '.00..',
     '..0..',
     '..0..',
     '.....']
]


T = [
    ['.....',
     '..0..',
     '.000.',
     '.....',
     '.....'],
    ['.....',
     '..0..',
     '..00.',
     '..0..',
     '.....'],
    ['.....',
     '.....',
     '.000.',
     '..0..',
     '.....'],
    ['.....',
     '..0..',
     '.00..',
     '..0..',
     '.....']
]


shapes = [S, Z, I, O, J, L, T]
shapesColors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(object):
    #X and Y.
    rows = 20
    cols = 10


    def __init__(self, col, row, shape):
        self.x = col
        self.y = row
        self.shape = shape
        self.color = shapesColors[shapes.index(shape)]
        #Positions  0-3.
        self.rotation = 0


def gridCreation(lockedPositions={}):
    grid = [[(0, 0, 0) for i in range(0, 10)] for i in range(0, 20)]
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid)):
            if((i, j) in lockedPositions):
                a = lockedPositions[(i, j)]
                grid[j][i] = a
    return grid


def convertShapeFormat(shape):
    positions = []
    formats = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(formats):
        row = list(line)
        for j, col in enumerate(row):
            if(col == '0'):
                positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions


def validSpace(shape, grid):
    accPos= [[(j, i) for j in range(0, 10) if grid[i][j] == (0, 0, 0)] for i in range (20)]
    accPos = [j for i in accPos for j in i]
    formatted = convertShapeFormat(shape)
    for pos in formatted:
        if(not(pos in accPos)):
            if(pos[1] > -1):
                return False
    return True


def checkLoss(positions):
    for pos in positions:
        x, y = pos
        if(y < 1):
            return True
    return False


def getShape():
    global shapes, shapesColors
    return Piece(5, 0, random.choice(shapes))


def drawMiddleText(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (topLeftX + playWidth / 2 - (label.get_width() / 2), topLeftY + playHeight / 2 - label.get_height() / 2))


def drawGrid(surface, row, col):
    x = topLeftX
    y = topLeftY
    if(not(hardModeOn)):
        for i in range(0, row):
            #Rows.
            pygame.draw.line(surface, (128, 128, 128), (x, y + i * 30), (x + playWidth, y + i * 30))
            for j in range(0, col):
                #Cols.
                pygame.draw.line(surface, (128, 128, 128), (x + j * 30, y), (x + j * 30, y + playHeight))


def clearRows(grid, locked):
    #Checks if the row is empty, shifts above lines down.
    global score
    global linesCount
    global newLines
    newLines = 0
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if(not((0, 0, 0) in row)):
            inc = inc + 1
            ind = i
            for j in range(0, len(row)):
                try:
                    del locked[(j, i)]
                    linesCount = linesCount + 1
                    newLines = newLines + 1
                except Exception:
                    continue
    if(inc > 0):
        for i in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x, y = i
            if(y < ind):
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(i)


def drawNextShape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))
    x = topLeftX + playWidth + 50
    y = topLeftY + playHeight / 2 - 100
    form = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(form):
        row = list(line)
        for j, col in enumerate(row):
            if(col == '0'):
                pygame.draw.rect(surface, shape.color, (x + j * 30, y + i * 30, 30, 30), 0)
    surface.blit(label, (x + 10, y - 30))


def scoreOutput(surface):
    global score
    global newLines
    if(newLines == 40):
        score = score + 1200
    else:
        score = score + 4 * newLines
    newLines = 0
    font = pygame.font.SysFont('comicsans', 30)
    labelname = font.render('Score:', 1, (255, 255, 255))
    x = 50
    y = y = topLeftY + playHeight / 2 - 100
    label = font.render(str(score), 1, (255, 255, 255))
    surface.blit(labelname, (x + 10, y - 30))
    surface.blit(label, (x + 30, y))


def linesCountOutput(surface):
    global linesCount
    font = pygame.font.SysFont('comicsans', 30)
    labelname = font.render('Line Count:', 1, (255, 255, 255))
    x = 50
    y = y = topLeftY + playHeight / 2 - 100
    label = font.render(str(linesCount // 10), 1, (255, 255, 255))
    surface.blit(labelname, (x, y + 30))
    surface.blit(label, (x + 30, y + 60))


def drawWindow(surface):
    surface.fill((0, 0, 0))
    #Title.
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))
    surface.blit(label, (topLeftX + playWidth / 2 - (label.get_width() / 2), 30))
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid)):
            pygame.draw.rect(surface, grid[j][i], (topLeftX + i * 30, topLeftY + j * 30, 30, 30), 0)
    drawGrid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (topLeftX, topLeftY, playWidth, playHeight), 5)


def main():
    global grid
    global score
    global linesCount
    score = 0
    linesCount = 0
    lockedPositions = {}
    grid = gridCreation(lockedPositions)
    changePiece = False
    run = True
    currentPiece = getShape()
    nextPiece = getShape()
    clock = pygame.time.Clock()
    fallTime = 0
    while(run):
        fallSpeed = speed - score / 100000
        grid = gridCreation(lockedPositions)
        fallTime = fallTime + clock.get_rawtime()
        clock.tick()
        #Falling piece.
        if(not(fallTime / 1000 < fallSpeed)):
            fallTime = 0
            currentPiece.y = currentPiece.y + 1
            if(not(validSpace(currentPiece, grid)) and (currentPiece.y > 0)):
                currentPiece.y = currentPiece.y - 1
                changePiece = True
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False
                pygame.display.quit()
                quit()
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_LEFT):
                    currentPiece.x = currentPiece.x - 1
                    if(not(validSpace(currentPiece, grid))):
                        currentPiece.x = currentPiece.x + 1
                elif(event.key == pygame.K_RIGHT):
                    currentPiece.x = currentPiece.x + 1
                    if(not(validSpace(currentPiece, grid))):
                        currentPiece.x = currentPiece.x - 1
                elif(event.key == pygame.K_UP):
                    currentPiece.rotation = (currentPiece.rotation + 1) % len(currentPiece.shape)
                    if(not(validSpace(currentPiece, grid))):
                        currentPiece.rotation = (currentPiece.rotation - 1) % len(currentPiece.shape)
                elif(event.key == pygame.K_DOWN):
                    currentPiece.y = currentPiece.y + 1
                    if(not(validSpace(currentPiece, grid))):
                        currentPiece.y = currentPiece.y - 1
                elif(event.key == pygame.K_SPACE):
                    while(validSpace(currentPiece, grid)):
                        currentPiece.y = currentPiece.y + 1
                    currentPiece.y = currentPiece.y - 1
        shapePos = convertShapeFormat(currentPiece)
        for i in range(0, len(shapePos)):
            X, Y = shapePos[i][0], shapePos[i][1]
            if(Y > -1):
                grid[Y][X] = currentPiece.color
        if(changePiece):
            for pos in shapePos:
                p = (pos[0], pos[1])
                lockedPositions[p] = currentPiece.color
            currentPiece = nextPiece
            nextPiece = getShape()
            changePiece = False
            clearRows(grid, lockedPositions)
        drawWindow(win)
        drawNextShape(nextPiece, win)
        scoreOutput(win)
        linesCountOutput(win)
        pygame.display.update()
        if(checkLoss(lockedPositions)):
            run = False
    drawMiddleText("Game Over.", 40, (255, 255, 255), win)
    pygame.display.update()
    pygame.time.delay(2000)


def mainMenu():
    global speed
    global hardModeOn
    global score
    global linesCount
    score = 0
    linesCount = 0
    hardModeOn = False
    run = True
    while(run):
        win.fill((0, 0, 0))
        drawMiddleText('Press h key for hard mode, other key for easy mode', 30, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False
            elif(event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_h):
                    speed = 0.2
                    hardModeOn = True
                main()
    pygame.quit()


win = pygame.display.set_mode((sWidth, sHeight))
speed = 0.4
hardModeOn = False
linesCount = 0
newLines = 0
score = 0
pygame.display.set_caption('Tetris')
mainMenu()