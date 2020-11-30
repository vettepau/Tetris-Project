'''
Brain - simple heuristic logic that knows how to play the tetris

The brain uses the current position of the piece and board to calc the best move based on criteria 
such as if the placement will create holes, the max and avg block height, and if it would clear any lines

I was unable implement machine learning due to a time restrant however will a little more time it could be implemented

The brain is by no means any good but it does make an effort to play which is a start

I didn't place any easter eggs in my code like Seth but I did include some jokes in some later comments ~ Paul
'''

import pygame
import copy as c

class Event():
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key
        
        
class Piece(object):
    '''
    Copied piece class from JTetris in order to recreate the piece for easier calculations
    for a deeper explanation look at JTetris docstring
    '''
    #x = 20
    #y = 10
    def __init__(self, x, y, shape): 
        self.x  = x
        self.y = y
        self.shape = shape
        self.rotation = 0 #Defaulted to 0
        
def convertShape(shape):
    '''
    Takes in piece and returns coorindates of that piece
    for deeper explanation look at Seth's in Jtetris
    
    Parameters
    ----------
    shape : Piece
        instance of the Piece class

    Returns
    -------
    positions : List of coordinates
        
    '''
    positions = [] #new empty list
    form = shape.shape[shape.rotation % len(shape.shape)] 
    
    for i, line in enumerate(form): 
        row = list(line)
        for j, column in enumerate(row):
            if column == '1':             
                positions.append((shape.x + j, shape.y + i))
                
    for i, pos in enumerate(positions):
        positions[i] = (pos[0]-2 , pos[1] -4) 
    
    return positions

def valid(shape, grid):
    '''
    similar to the method in JTetris however I had to make some changes 
    '''
    #The if grid[i][j] == (0,0,0) #Adjusted because grid is no longer a list of tuples but a list of ints
    acceptedPositions = [[(j, i) for j in range(10) if grid[i][j] == 0 ] for i in range(20)]  
    acceptedPositions = [j for sub in acceptedPositions for j in sub] 
    
    converted = convertShape(shape) 
    
    for position in converted:
        if position not in acceptedPositions:
            return False #removed additional if statement Seth had because I didn't want the brain to place blocks above the board
    return True 

def sort(grid):
    '''
    the grid that gets sent from JBrainTetris it a list of tuples because Seth used it for the colors so I
    create a new list that can give me a list of 0 & 1s so it is easier to deal with later on
    '''
    pos = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    for i in range(20):
        pos[i] = [0,0,0,0,0,0,0,0,0,0]
    for k in range(len(grid)):
        for j in range(len(grid[k])):
            a,b,c = grid[k][j]
            if a or b or c != 0: #if the block is colorless then it is empty
                pos[k][j] = 1
    return pos

def validPositions(piece, grid):
    '''
    Calcs all of the valid positions for the piece on the board

    Parameters
    ----------
    piece : instance of Piece class
        
    grid : Matrix

    Returns
    -------
    list of the lowest valid positions on the board

    '''
    pos = []
    counter = 0
    for i in range(10): #x cooridate of piece
        h = 21 - getColumnHeight(grid,i) #lowest possible y coorindate of piece
        #when the piece is a y = 21 the actual coordinates are at y = 19 usually 
        for j in range(h+1): #the board starts from around -2 at the top and goes down to 20
            k = h - j #start from the bottom
            piece.x = i
            piece.y = k #first piece should be 19
            if valid(piece, grid):
                pos.append([])
                pos[counter] = [i,k]
                counter += 1
                break #I only want the lowest piece otherwise I will create more work and slowdown the process 
    return pos #max length 10 with inside array of two ints

def getColumnHeight(grid, column):
    '''
    returns the height of the column
    '''
    h = 20
    c = column
    for i in range(20):
        if grid[i][c] == 0:
            h -= 1 #the board is inverse so the bottom is 19 and the top is 0
            #if there are blocks at 19 and 18 the height is 2
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
        if num > 8: #changed it to 9 or 10 so that if a line is almost cleared it rewards that too
            lines += 1
        num = 0
    return lines

def rate(grid):
    '''
    rates the position based of number of holes created, avg and max height, and # of lines cleared
    and returns a score. The lower the score the better, like golf 
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
    score = 80*maxx + 40*avg + 1.25*hole - 500*c #random values that will be perfected later with machine learning
    return score
    
def best_position(piece,grid):
    '''
    tests the positions that are valid and decides which one is the best.
    returns the score and x value of the best position
    '''
    bestscore = 100000 #lower the score the better
    best_x = 9 #moves it to the far right in case of an error
    pos = validPositions(piece, grid)
    for i in range(len(pos)):
        grid1 = c.deepcopy(grid) #this cost me like two hours of debugging ahhhhhhhh. I had originally used grid[:]
        #then I tried list(grid) then grid.copy() but it took me forever to find the source of my error being grid[:]
        #I will forever remeber that when you copy a list it refrences the same place in memory
        #idk why grid[:] didn't work bc I would have never had any problems
        #if you have have an answer for me I would love to know Dr. Ritchey ~ Paul
        piece.x = pos[i][0]
        piece.y = pos[i][1]
        loc = convertShape(piece)
        for k in range(4): #assembles the new grid so that it can be rated
            x, y = loc[k] 
            grid1[y][x] = 1
        score = rate(grid1)
        if score < bestscore:
            bestscore = score
            best_x = pos[i][0]
    return bestscore, best_x
            
                
def best_rotation(grid, piece):
    '''
    tests the best positions from each rotation and decides which rotation is the best.
    returns the rotation and x position for that rotation
    '''
    #piece = Piece(x, y, shape)
    rotation = 0
    best_score = 100000
    rotations = []
    shape = c.deepcopy(piece.shape) #rotational orinentation of the original piece
    
    num, x = best_position(piece, grid)
    rotations.append([num,0, x])
    piece.rotation += 1
    shape2 = c.deepcopy(piece.shape) #rotational orinentation of the first rotation
    
    if shape != piece.shape: 
        num1, x1 = best_position(piece, grid)
        rotations.append([num1,1, x1])
    else: #if it is a cube all 4 will be the same so just return the original
        rotation = rotations[0][1]
        x = rotations[rotation][2]
        return rotation, x
    piece.rotation += 1
    
    if shape != piece.shape: #if it is a line then the original and the second will be the same
        num2, x2 = best_position(piece, grid)
        rotations.append([num2,2, x2])
    piece.rotation += 1
    
    if shape2 != piece.shape: #if it is a line the first rotation and the second will be the same
        num3, x3 = best_position(piece, grid) 
        rotations.append([num2,3, x3])
        
    for i in range(len(rotations)):
        if rotations[i][0] < best_score:
            rotation = rotations[i][1]
            best_score = rotations[i][0]
    best_x = rotations[rotation][2]
    
    return rotation, best_x


counter = 0
def run(grid, x, y, shape):
    '''
    Basically my main function. Creates a piece and gathers input from the other methods.
    Then returns the suggested movement based on the desired x pos and rotation
    '''
    p = Piece(x, y, shape) #create same piece from JTetris
    global counter
    counter += 1
    if counter < 70: #slow the brain down, w/out slowing it down the window was crashing 
        #in the end because this does hinder the brains ability
        #if I was to improve the brain later on I would find some ways to reduce the amount of calcutations 
        #it needs to make. If the window crashs mid game then it is because this number is not high enough
        #you can change it to 100 if you are having problems
        return []
    counter = 0
    rotation = int(p.rotation)
    grid = sort(grid) #converts the grid from tuple to int
    
    r, position = best_rotation(grid, p) #gets the desired x pos and rotation

    if r != rotation:
        e = Event(pygame.KEYDOWN, pygame.K_UP)
    elif position < x:
        e = Event(pygame.KEYDOWN, pygame.K_LEFT)
    elif position > x:
        e = Event(pygame.KEYDOWN, pygame.K_RIGHT)
    else: #if the piece is already in the desired position and rotation then it will drop the block to speed up the game
        e = Event(pygame.KEYDOWN, pygame.K_DOWN)

   # e = Event(pygame.KEYDOWN, pygame.K_DOWN)
    return [e]

'''
Why did the king draw a line?
    because he is the ruler
    
What is the coldest country in the world?
    Chile, bur
    
What is the most slippery country in the world?
    Greece, haha
'''

def MachineLearner(grid,a,b,c,d,e):
    '''
    I ran out of time however this would have been called by best_position instead of calling rate directly.
    This would have given rate the values established by brainTester
    '''
    score = rate(grid,a,b,c,d,e)
    return score