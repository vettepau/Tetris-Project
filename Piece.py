'''
Tetris Project 
Creators:
    Paul Vetter, Seth Webb, Anna Woodruff, & Sarah Rosinbaum
Engr 102 final project

The game will consist of 6 different classes:
    Piece - a single tetris peice 
    Board - the tetris board
    JTester - tester class for Piece and Board
    JTetris - present the GUI for tetris in a window and do animation
    Brain - simple heuristic logic that knows how to play the tetris
    JBrainTetris - a subclass of JTetris that uses a brain to play the game w/ out a human player
    BrainTester - Possibly include this class to test our brain and implement machine learning

Using Tetris-Architecture.html for guidance and resources 
'''
import random

class Piece:
    piece = [[]]
    body = [[]]
    width = 0
    height = 0
    skirt = []
    
    
    
    #generates new piece
    def newPiece(): 
        i = random.randrange(0,7)
        if i == 0:
            piece = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[1,1,1,1]] #horiz line
        elif i == 1:
            piece = [[0,0,0,0],[0,0,0,0],[1,0,0,0],[1,1,1,0]] #left L
        elif i == 2:
            piece = [[0,0,0,0],[0,0,0,0],[0,0,1,0],[1,1,1,0]] #right L
        elif i == 3:
            piece = [[0,0,0,0],[0,0,0,0],[1,1,0,0],[1,1,0,0]] #cube
        elif i == 4:
            piece = [[0,0,0,0],[0,0,0,0],[0,1,1,0],[1,1,0,0]] #S
        elif i == 5:
            piece = [[0,0,0,0],[0,0,0,0],[0,1,0,0],[1,1,1,0]] #T
        elif i == 6:
            piece = [[0,0,0,0],[0,0,0,0],[1,1,0,0],[0,1,1,0]] #Dog 
        else:
            piece = [[0,0,0,0],[0,0,0,0],[0,0,1,1],[1,1,0,0]] #Dog inverse
            
    def getwidth():
        return Piece.width
    
    def getheight():
        return Piece.width
    
    def getskirt():
        return Piece.skirt