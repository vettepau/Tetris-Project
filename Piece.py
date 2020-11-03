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

import random

class Piece:
    pieces = [()] #
    body = [()] #coordinates of blocks
    skirt = [] # stores the lowest y value for each x value in the piece coordinate system
    width = 0
    height = 0
    next = () 
    color = ''
    
    def Piece(points):
        Piece.body = points
        width = 0
        height = 0
        
        for p in points:
            if p.x + 1 > width:
                width = p.x + 1
            if p.y + 1 > height:
                height = p.y + 1
                
        Piece.width = width
        Piece.height = height
        skirt = [0] * width
        
        for i in width:
            skirt[i] = height
            
        for i in width:
            for p in points:
                if p.x == i and p.y < skirt[i]:
                    skirt[i] = p.y
        Piece.skirt = skirt
        
        
    def getwidth():
        return Piece.width
    
    def getheight():
        return Piece.height
    
    def getskirt():
        return Piece.skirt
    
    def nextRotation():
        return Piece.next
    
    def getcolor():
        return Piece.color
        
    #generates new piece
    def getPiece(): 
        i = random.randrange(0,6)
        if i == 0:
            piece = [(0,0),(0,1),(0,2),(0,3)] #vertical line
            color = 'cyan'
        elif i == 1:
            piece = [(0,0),(0,1),(0,2),(1,0)] #right L
            color = 'blue'
        elif i == 2:
            piece = [(0,0),(1,0),(1,1),(1,2)] #left L
            color = 'orange'
        elif i == 3:
            piece = [(0,0),(0,1),(1,0),(1,1)] #cube
            color = 'yellow'
        elif i == 4:
            piece = [(0,0),(1,0),(1,1),(2,0)] #T
            color = 'purple'
        elif i == 5:
            piece = [(0,1),(1,0),(1,1),(2,0)] #left Dog 
            color = 'red'
        else:
            piece = [(0,0),(1,0),(1,1),(2,1)] #right dog
            color = 'green'
            
        Piece.color = color
        return piece
            
    def pieceRow(piece):
        temp = piece
        
        while(True):
            points = [(0,0)] * len(temp)
            
            for i in len(points):
                newX = (temp.height - 1) - temp.body[i].y
                newY = temp.body[i].x
                
                points[i] = (newX, newY)
                
            p = points
            temp.next = p
            temp = temp.next
    
    def toString():
        out = ''
        for p in Piece.body:
            out += '(' + p.x + ',' + p.y + ')'
        return out