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
    acceptedPositions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0) ] for i in range(20)] #A tuple of all accepted positions allowed in the grid. Did it this way was tired of nested for loops, sue me. 
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
            if position[1] > -1: #Incase Piece starts above the screen, otherwise the game would end before it started and thats no good. Would help with potentially needed offsets
                return False #I KEEP WANTING TO PUT SEMI COLONS AFTER RETURN AHHHHHHHHHHHHHHHHHHH
    return True #Because that means all must be true, all passed.

def sort(grid):
    '''
    the grid that gets sent from JBrainTetris it a list of tuples so because Seth used it for the colors so I have to
    create a new list that can give me a list of ints so that I know where blocks are based on if they are colored
    '''
    pos = [[0,0,0,0,0,0,0,0,0,0]*20]
    for k in range(len(grid)):
        for j in range(len(grid[k])):
            a,b,c = grid[k][j]
            if a and b and c != 0:
                pos[k][j] = 1
    return pos

def validPositions(piece, grid):
    pos = [[]]
    for i in range(10): #x cooridate of piece
        h = 20 - getColumnHeight(grid,i) #lowest possible y coorindate of piece
        for j in range(h,-1):
            piece.x = i
            piece.y = j
            if valid(piece, grid):
                pos += [i,j]
                break
    return pos

def getColumnHeight(grid, column):
    '''
    returns the height of the column
    '''
    h = 0
    c = column
    for i in (1,21):
        if grid[i][c] == 1:
            h = i
    return h

def Heights(grid):
    maxx = 0
    total = 0
    for i in range(10):
        x = getColumnHeight(grid, i)
        total += x
        if x > maxx:
            maxx = x
    return maxx, total/10

def clear(grid, maxx):
    for i in range(maxx):
        for j in range(10):
            x = 0

def rate(grid):
    maxx, avg = Heights(grid)
    hole = 0
    for i in range(10):
        h = getColumnHeight(grid,i) - 2 #where the first hole could be
        for j in range(h+1):
            if grid[j][i] == 0:
                hole += 1
    score = 8*maxx + 40*avg + 1.25*hole 
    return score
    
                
def best_position(piece,grid, x, y):
    pos = validPositions(piece, grid)
    for i in range(len(pos)):
        grid = grid
        
    return 0
                
def best_rotation(grid, piece):
    rotation = 0
    
    return 0



counter = 0
rotation = 0
def run(grid, x, y, shape):
    p = Piece(x, y, shape) #create same piece from JTetris
    global counter
    counter += 1
    if counter < 3: #slow the brain down
        return []
    counter = 0
    global rotation
    
    grid = sort(grid)
    
    '''
    position = best_position(grid,x,y)

    #if bestRotation(grid) != rotation:
    #    e = Event(pygame.KEYDOWN, pygame.K_UP)
    if position < x:
        e = Event(pygame.KEYDOWN, pygame.K_RIGHT)
    elif position > x:
        e = Event(pygame.KEYDOWN, pygame.K_LEFT)
    else:
        e = Event(pygame.KEYDOWN, pygame.K_DOWN)
        '''
    e = Event(pygame.KEYDOWN, pygame.K_DOWN)
    return [e]
