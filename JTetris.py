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

# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Instructions
left arrow or a key moves piece left
right arrow or d key moves piece right
up arrow or w key rotates piece
holding down the down arrow or s key will cause the piece to fall twice as fast
Press Space to store a piece once per turn.
"""

"""
Things still left to do:
Add the music to the game
Add a Menu Before the Game Starts
Add an AI to play and get better at the game.
"""
import pygame
import random

#Intialize
pygame.init()

clock = pygame.time.Clock()

#Global Variables
score = 0 #Initialized to be 0 for new game.
windowWidth = 800
windowHeight = 600
playWidth = 300  # meaning 300 // 10 = 30 width per block
playHeight = 600  # meaning 600 // 20 = 20 height per blo ck
blockSize = 30
topLeftOfPlayX = (windowWidth - playWidth) // 2
isPieceStored = False

#Create font Object
fontObj = pygame.font.Font('8-BIT WONDER.ttf', 30)
fontObjSmall = pygame.font.Font('8-BIT WONDER.ttf', 20)
fontObjSmallest = pygame.font.Font('8-BIT WONDER.ttf', 15)
#creates Window 800 X 600
screen = pygame.display.set_mode((windowWidth, windowHeight)) #Named it screen as nostalgia from the Java Days. 
pygame.display.set_caption("Aggie Land Tetris!")
windowIcon = pygame.image.load("Texas A&M Logo.png")
pygame.display.set_icon(windowIcon)

high = open('High Score.txt', 'r')
leader = high.readline()
leader = leader.strip()
highscore = high.readline()
player1 = leader + ' ' + highscore
high.close()

"""
Lists currently empty unitl Paul creates the shape grids, need to make sure the order is correct, and that we match the 
order of the shapes with the order of the colors. This will be passed into the piece class, also need his variable names.
"""
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
colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(object):
   # x = 20
    #y = 10
    def __init__(self, x, y, shape): #self is like this from java, funny enough turns out you can do other words not self, but to keep it easy for Dr. Ritchey to Grade I say we keep it as self.
        self.x  = x
        self.y = y
        self.shape = shape
        self.color = colors[shapes.index(shape)] # Returns the color of the shape being passed
        self.rotation = 0 #Defaulted to 0, will incremint when up arrow is pressed, number will refrence which list to display.

    

def main(screen):
    lockedPositions = {} #Initialize Locked Postitions as a blank dictionary
    grid = createGrid(lockedPositions) #Passes the dictionary into our method 
    
    isStored = False
    storedThisTurn = False
    storedPiece = 0
    holdPiece = 0
    
    changePiece = False #default this false or else itll constantly change pieces, will use this as a check later to know when to change piece.
    run = True #Initialize run for our while loop later, game will run while thise is true, stop when false.
    
    clock = pygame.time.Clock()# Sarahs clock that actually ended up being needed for controlling the falling piece
    fallTime = 0 #Will be refrenced later to controll when the piece drops.
    
    currentPiece = getShape() #Literally the only remaining part of the original code other than the window, changed to fit the getShape Method.
    nextPiece = getShape() #A benifit of this I just noticed is we only have to keep track of two sets of self. keeps memory relatively free. Only two objectives of the shape Class. 
    fastFall = 1
    
    #THE GAME LOOP, AS FROM THE ORIGINAL BUILD, BEFORE EVERYTHING WENT BAD
    while run:
        fallCheck = 0.30/fastFall #should divide by fast fall, speed * fastFall during fast fall
        grid = createGrid(lockedPositions) #Called because we need to update the grid BEFORE ANYTHING ELSE
        fallTime += clock.get_rawtime() #Adds how much time has passed since last tick
        clock.tick() # Resets the raw time for next fall time update. 
        
        if fallTime / 1000 > fallCheck:  # in ms so divide by 1000
            fallTime = 0 #reset this for next interval
            currentPiece.y += 1 #In squares not pixels, Remember Y goes down so plus not minus.
            if not(valid(currentPiece, grid)) and currentPiece.y > 0: #Checks if touching invalid spot, so long as not above screen
                currentPiece.y += -1 #move it back up to valid, gonna just go ahead and slide that bad boy back up there
                changePiece = True #I knew this would come in handy, *pats self on back*
                storedThisTurn = False
        
        for event in pygame.event.get(): #Pygame makes this so so sweet
            if event.type == pygame.QUIT:
                run = False #this breaks out of the while Loop
                
                
            if event.type == pygame.KEYDOWN: #means if key is being pressed, not down key
                #there will be or's to check for wasd and arrow key control :)    
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    currentPiece.x += -1 #Moves Left One Square
                    if not ( valid(currentPiece, grid) ):
                        currentPiece.x += 1 #Oppisite of the movement from key
                    
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    currentPiece.x += 1 #Moves Right One Square
                    if not ( valid(currentPiece, grid) ):
                        currentPiece.x += -1 #Oppisite of the movement from key
                        
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    fastFall = 7 #The higher this number the faster the fall
                    
                if event.key == pygame.K_SPACE:
                    if not isStored:
                        storedPiece = currentPiece
                        currentPiece = nextPiece
                        storedThisTurn = True
                        isStored = True
                    elif not storedThisTurn:
                        holdPiece = storedPiece
                        storedPiece = currentPiece
                        currentPiece = Piece(5,0, holdPiece.shape)
                        storedThisTurn = True
                        
                    
                
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    currentPiece.rotation += 1 #Changes the rotation cycles the layouts of shape. 
                    if not (valid(currentPiece, grid)):
                        currentPiece.rotation += -1
            if event.type == pygame.KEYUP: #When Key Is let go, used to reset fast fall
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    fastFall = 1 #Should return drop to normal speed
        
        shapePosition = convertShape(currentPiece)
        
        for i in range(len(shapePosition)):
             x, y = shapePosition[i]
             if y > -1:
                grid[y][x] = currentPiece.color   #y,x not x,y. We are about learning from our mistakes.
        
        
        if changePiece: #time for foresite to pay off, note only do this if automatic next,not user store will need other method for that.
            for pos in shapePosition: # SO MANY POS VARIABLES TO KEEP TRACK OF AHHAHAHHAHAHAH 
                p = (pos[0], pos[1])
                lockedPositions[p] = currentPiece.color #updates the tuple dictionary, note can be equal because the piece colors have already been passed
            
            #Enable the game to display next piece like in Real Tetris
            currentPiece = nextPiece
            nextPiece = getShape()
            changePiece = False #because we don't want to rapid change, have to reset this to default.
            
            #Call Clear Rows here because this is when piece stops.
            clearRows(grid, lockedPositions)
            
         
        #Our Draw Method Calls
        
        drawWindow(screen, grid)
        drawNextShape(nextPiece, screen)
        drawScore(screen)
        drawHighScore(screen)
        drawStoredShape(screen, storedPiece, isStored)
        
        pygame.display.update()
        
        if  checkLost(lockedPositions): #We pass locked positions because they will contain all positions.
            run = False #Will exit the game Loop, the While Loop.
    
    
    #Need this or the kernel will die when the window closes, or game over. 
    #Really whenever we exit the game loop. But ITS IMPORTANT SO REMEMBER KEEP THIS AS LAST LINE AFTER THE GAME LOOP
    pygame.display.quit()     
        
   
    #End of Main Functon.

def createGrid(lockedPositions = {}):
    grid = [[(0,0,0,) for x in range(10)] for y in range(20)] #Draws a 20 X 10 Black-(0,0,0) Grid
    
    #Checks the grid for already played pieces
    for i in range(20):
        for j in range(10):
            if (j, i) in lockedPositions:
                pointColor = lockedPositions[(j,i)] #pointColor refferring to the color of the piece at that point
                grid[i][j] = pointColor
                
    return grid #returns the black grid with all the played pieces on it.


def getShape():
    global shapes, colors

    return Piece(5, 0, random.choice(shapes))
    """
    Passes an object into the piece class and return the corrisponding set of values.
    Object values passed are x, y, shape
    is 5 and 0 because we are refferencing squares on the board not pixels
    """


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

def checkLost(positions):
    for position in positions: #Note Singular versus Plural, this is important !!!!!!!
        x, y = position
        if y < 1: #Checks to see if above screen
            return True  #Uh OH Thats A Game Over, Once we code that part...
        
    return False #you may live, for now -_-
        


def clearRows(grid, lockedPositions ):
    #ALot harder than I though because of gravity, but I think I found a useful method, need to Test with Puals Shapes.
    
    count = 0
    for i in range(19, -1, -1): #Counting Backwards, check to see if I did the math right Please. Count backwards to not overwrite rows.
        row = grid[i]
        if (0,0,0,) not in row: # If there are no blank black spaces
            count += 1
            remember = i
            for j in range(10):
                try: 
                    del lockedPositions[(j,i)] #the current position
                except:
                    continue #Im pretty sure we needed a try as part of our grade, this was the best spot I could think of
    
    """
    To Paul,
    If you dont understand how python handles Global variable refrence and how we keep the function from 
    creating its own local variable, these two links might help give insight. - Seth
    https://www.python-course.eu/python3_global_vs_local_variables.php
    https://stackoverflow.com/questions/10506973/can-not-increment-global-variable-from-function-in-python
    """
    global score#DO NOT REMOVE, This is needed or else it keeps trying to create a local variable score and the whole things crashes when you clear a line
     
    
    
    if count > 0: #Meaning we cleared at least one line
    #Score increase from clearing lines
        if count == 1:
            score += 100
        if count == 2:
            score += 250
        if count == 3:
            score += 400
        if count == 4:
            score += 600
    
        
    
        """"
        This next line basically sorts elements of the list be their Y values, it's a bit trippy and weird to explain but it works like this
        unsorted (1,2) , (5,3) (9,1)
        sorted (9,1) , (1,2) , (5,3)
        
       
        I didn't Use i and j because it needs to be key for that lamda sort. Hopefully it is easier to follow than write.
        For information on the sorts check these two websites, they had useful info, especially the first one.
        https://docs.python.org/3/howto/sorting.html
        https://stackoverflow.com/questions/3766633/how-to-sort-with-lambda-in-python
        """
        for key in sorted(list(lockedPositions), key = lambda x: x[1])[::-1]: #Definitely had to look this up, converted it to work with our variables and matrix based data, that lambda stuff is funky. Probably best to not touch, convert things to work with this not vise verse
            x,y = key #Because key is a touple because of our 2D Matrix
            if y < remember:
                newkey = (x, y + count)
                lockedPositions[newkey] = lockedPositions.pop(key)
            
        return score

def drawGrid(surface, grid):
    
    #Draws A Grid Of Lines
    for i in range(20):
        pygame.draw.line(surface, (255, 255, 255), (topLeftOfPlayX, i * blockSize), (topLeftOfPlayX + playWidth, i * blockSize)) #Horizontal Line
        for j in range(10):
             pygame.draw.line(surface, (255, 255, 255), (topLeftOfPlayX + j * blockSize, 0), (topLeftOfPlayX + j * blockSize, playHeight)) #vert lines
            
   


def drawNextShape(shape, surface):
    textSurfaceObj = fontObj.render('Next', True, (255, 255, 255))#Next Shape wouldn't fit, changed to Next
   
    
    nextPieceX = topLeftOfPlayX + playWidth + 50
    nextPieceY = playHeight // 2 - 270
    
    surface.blit(textSurfaceObj, (nextPieceX +20, nextPieceY))#Prints out Next Shape in white 8-bit letter
    
    form = shape.shape[shape.rotation % len(shape.shape)] #Same line as in convert shape, See that for Documentation
    
    for i, line in enumerate(form):
        row = list(line)
        for j, column in enumerate(row):
            if column == "1":
                #Rather than add postion, which we care not for, we will draw it, simmilar to the line in the drawWindow method below. wave at it, its a friend.
                pygame.draw.rect(surface, shape.color, (nextPieceX + j * blockSize, nextPieceY + i*blockSize + 45, blockSize, blockSize), 0) 
    
def drawStoredShape(surface, shape, check):
    textSurfaceObj = fontObj.render('Stored', True, (255, 255, 255))
   
    
    storedPieceX = topLeftOfPlayX + playWidth + 50
    storedPieceY = playHeight // 2 + 30
    
    surface.blit(textSurfaceObj, (storedPieceX - 10, storedPieceY))#Prints out stored in white 8-bit letter

    if check:
        
        form = shape.shape[shape.rotation % len(shape.shape)] #Same line as in convert shape, See that for Documentation
    
        for i, line in enumerate(form):
            row = list(line)
            for j, column in enumerate(row):
                if column == "1":
                    #Rather than add postion, which we care not for, we will draw it, simmilar to the line in the drawWindow method below. wave at it, its a friend.
                    pygame.draw.rect(surface, shape.color, (storedPieceX + j * blockSize, storedPieceY + i*blockSize + 45, blockSize, blockSize), 0)

def drawWindow(surface, grid):
    surface.fill((67,0,48))
     
    for i in range(20):
        for j in range(10):
            #Draws onto surface the color of grid[i][j], at the correct position, height and width of the draw, and the 0 at the end to make sure it filles the draw, without it it only draws borders
            pygame.draw.rect(surface, grid[i][j], (topLeftOfPlayX + j * blockSize, i * blockSize, blockSize, blockSize), 0) 
            
            
    
    
    
    drawGrid(surface, grid) #Calls the draw grid method, to draw the grid 
    

def drawScore(surface):
     textSurfaceObj = fontObj.render('Score', True, (255, 255, 255) )
     surface.blit(textSurfaceObj,( 40,330))#Prints out Score in white 8-bit letters
     
     #Format where the score is drawn based on its length
     digits = 0
     holder = score
     while holder >= 10:
         holder = holder // 10
         digits += 1
     textSurfaceObj = fontObj.render(str(score), True, (255, 255, 255) )
     surface.blit(textSurfaceObj,( 100 - digits * 12.5 ,380))

def drawHighScore(surface):
     textSurfaceObj = fontObjSmall.render('Leaderboard', True, (255, 255, 255) )
     surface.blit(textSurfaceObj,(15,30))#Prints out Score in white 8-bit letters
     
     #Format where the score is drawn based on its length
     digits = len(player1)
     textSurfaceObj = fontObjSmallest.render(player1, True, (255, 255, 255) )
     surface.blit(textSurfaceObj,(180 - digits * 12.5,80))

def mainMenu(screen): 
    main(screen) #Passes from the window that was created and passed to main menu
    

mainMenu(screen)  # Runs to start the game
