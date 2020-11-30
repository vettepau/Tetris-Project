'''
Tetris Project 
Creators:
    Paul Vetter, Seth Webb, Anna Woodruff, & Sarah Rosinbaum
Engr 102 final project

The game will consist of 6 different classes:
    Piece - a single tetris peice 
    JTetris - present the GUI for tetris in a window and do animation
    Brain - simple heuristic logic that knows how to play the tetris
    JBrainTetris - a subclass of JTetris that uses a brain to play the game w/ out a human player
    BrainTester - Possibly include this class to test our brain and implement machine learning

Using Tetris-Architecture.html for guidance and resources 
'''

import pygame


class Event():
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key
        
S = [['00000',
      '00000',
      '00110',
      '01100',
      '00000'],
     ['00000',
      '00100',
      '00110',
      '00010',
      '00000']]

Z = [['00000',
      '00000',
      '01100',
      '00110',
      '00000'],
     ['00000',
      '00100',
      '01100',
      '01000',
      '00000']]

I = [['00100',
      '00100',
      '00100',
      '00100',
      '00000'],
     ['00000',
      '11110',
      '00000',
      '00000',
      '00000']]

O = [['00000',
      '00000',
      '01100',
      '01100',
      '00000']]

J = [['00000',
      '01000',
      '01110',
      '00000',
      '00000'],
     ['00000',
      '00110',
      '00100',
      '00100',
      '00000'],
     ['00000',
      '00000',
      '01110',
      '00010',
      '00000'],
     ['00000',
      '00100',
      '00100',
      '01100',
      '00000']]

L = [['00000',
      '00010',
      '01110',
      '00000',
      '00000'],
     ['00000',
      '00100',
      '00100',
      '00110',
      '00000'],
     ['00000',
      '00000',
      '01110',
      '01000',
      '00000'],
     ['00000',
      '01100',
      '00100',
      '00100',
      '00000']]

T = [['00000',
      '00100',
      '01110',
      '00000',
      '00000'],
     ['00000',
      '00100',
      '00110',
      '00100',
      '00000'],
     ['00000',
      '00000',
      '01110',
      '00100',
      '00000'],
     ['00000',
      '00100',
      '01100',
      '00100',
      '00000']]

shapes = [S, Z, I, O, J, L, T]

class Piece(object):
   # x = 20
    #y = 10
    def __init__(self, x, y, shape): #self is like this from java, funny enough turns out you can do other words not self, but to keep it easy for Dr. Ritchey to Grade I say we keep it as self.
        self.x  = x
        self.y = y
        self.shape = shape
        self.rotation = 0 #Defaulted to 0, will
        
def convertShape(shape):
    positions = [] #new empty list
    form = shape.shape[shape.rotation % len(shape.shape)] #Modulus allows us to cycle through rotations :) hope that helps you in your design, Pual
    
    for i, line in enumerate(form): #had a lot of fun with this one. Sarcasm = True
        row = list(line)
        for j, column in enumerate(row):
            if column == '1':             # 1 being where block is, based on Pauls form. Note This *********IMPORTANT*********
                positions.append((shape.x + j, shape.y + i))
                
    for i, pos in enumerate(positions):
        positions[i] = (pos[0]-2 , pos[1] -4) #may or may not need offsets, will check when Paul passes his shapes
    
    return positions

def valid(shape, grid):
    #The ifgrid[i][j] == black checks if empty space, we only want to add empty spaces to our valid list, for obvious reasons.
    acceptedPositions = [[(j, i) for j in range(10) if grid[i][j] == 0 ] for i in range(20)] #A tuple of all accepted positions allowed in the grid. Did it this way was tired of nested for loops, sue me. 
    acceptedPositions = [j for sub in acceptedPositions for j in sub] #Had to look up how to do this, turns matrix into a list, 2D to 1D Emailed Ritchey to ask about will see when she responds
    """
    [[1,2] , [3,4]]
    becomes 
    [1,2,3,4]
    for refrence of before and after structure.
    """ 
    converted = convertShape(shape) #Makes the info Usable
    
    for position in converted:
        if position not in acceptedPositions: #Checks list of accepted positions
            return False 
    return True 

def sort(grid):
    '''
    the grid that gets sent from JBrainTetris it a list of tuples so because Seth used it for the colors so I have to
    create a new list that can give me a list of ints so that I know where blocks are based on if they are colored
    '''
    pos = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    for i in range(20):
        pos[i] = [0,0,0,0,0,0,0,0,0,0]
    for k in range(len(grid)):
        for j in range(len(grid[k])):
            a,b,c = grid[k][j]
            if a or b or c != 0:
                pos[k][j] = 1
    return pos

def validPositions(piece, grid):
    pos = []
    counter = 0
    for i in range(10): #x cooridate of piece
        h = 21 - getColumnHeight(grid,i) #lowest possible y coorindate of piece
        for j in range(h+1): #the board starts from -2 at the top and goes down to 20
            k = h - j
            piece.x = i
            piece.y = k #first piece should be 20
            if valid(piece, grid):
                pos.append([])
                pos[counter] = [i,k]
                counter += 1
                break
    return pos #max length 10 with inside array of two ints

def getColumnHeight(grid, column):
    '''
    returns the height of the column
    '''
    h = 20
    c = column
    for i in range(20):
        if grid[i][c] == 0:
            h -= 1
    return h

def Heights(grid):
    '''
    returns the max height of the board and the avg height of the board
    '''
    maxx = 0
    total = 0
    for i in range(10):
        x = getColumnHeight(grid, i)
        total += x
        if x > maxx:
            maxx = x
    return maxx, total/10

def clear(grid, maxx):
    '''
    returns number of lines cleared
    '''
    lines = 0
    for i in range((20-maxx),20):
        num = 0
        for j in range(10):
            num += grid[i][j]
        if num == 10:
            lines += 1
        num = 0
    return lines

def rate(grid,loc):
    '''
    rates the position based of criteria and returns a score
    '''
    maxx, avg = Heights(grid)
    c = clear(grid, maxx)
    hole = 0
    for i in range(10):
        h = 19 - getColumnHeight(grid,i) + 2 #where the first hole could be
        if h > 19: #if there is no blocks on the board or only one level of blocks
            continue
        for j in range(h,20):
            if grid[j][i] == 0:
                hole += 1
    score = 8*maxx + 40*avg + 1.25*hole - 40*c #random values that will be perfected later with machine learning
    return score
    
import copy as c
def best_position(piece,grid):
    '''
    tests the positions that are valid and decides which one is the best.
    returns the score and x value of the best position
    '''
    bestscore = 100000 #lower the score the better
    best_x = 0
    pos = validPositions(piece, grid)
    for i in range(len(pos)):
        grid1 = c.deepcopy(grid) #this cost me like two hours of debugging ahhhhhhhh. I had originally used grid[:]
        #then I tried list(grid) then grid.copy() but it took me forever to find the source
        #I will forever remeber that when you copy a list it refrences the same place in memory
        #idk why grid[:] didn't work bc I would have never had any problems
        #if you have have an answer for me I would love to know Dr. Ritchey ~ Paul
        piece.x = pos[i][0]
        piece.y = pos[i][1]
        loc = convertShape(piece)
        for k in range(4):
            x, y = loc[k]
            grid1[y][x] = 1
        score = rate(grid1,loc)
        if score < bestscore:
            bestscore = score
            best_x = pos[i][0]
    return bestscore, best_x
            
                
def best_rotation(grid, piece):
    '''
    tests the best positions from each rotation and decides which rotation is the best.
    returns the rotation and x position
    '''
    #piece = Piece(x, y, shape)
    rotation = 0
    best_score = 100000
    num, x = best_position(piece, grid)
    piece.rotation += 1
    num1, x1 = best_position(piece, grid) 
    piece.rotation += 1
    num2, x2 = best_position(piece, grid) 
    piece.rotation += 1
    num3, x3 = best_position(piece, grid) 
    rotations = []
    rotations.append([num,0, x])
    rotations.append([num1,1, x1])
    rotations.append([num2,2, x2])
    rotations.append([num2,3, x3])
    for i in range(4):
        if rotations[i][0] < best_score:
            rotation = rotations[i][1]
            best_score = rotations[i][0]
    best_x = rotations[rotation][2]
    
    return rotation, best_x



counter = 0
def run(grid, x, y, shape):
    p = Piece(x, y, shape) #create same piece from JTetris
    global counter
    counter += 1
    if counter < 100: #slow the brain down, w/out slowing it down the window was crashing 
        return []
    counter = 0
    rotation = p.rotation
    grid = sort(grid)
    
    r, position = best_rotation(grid, p)

    if r != rotation:
        e = Event(pygame.KEYDOWN, pygame.K_UP)
    elif position < x:
        e = Event(pygame.KEYDOWN, pygame.K_LEFT)
    elif position > x:
        e = Event(pygame.KEYDOWN, pygame.K_RIGHT)
    else:
        e = Event(pygame.KEYDOWN, pygame.K_DOWN)

   # e = Event(pygame.KEYDOWN, pygame.K_DOWN)
    return [e]
