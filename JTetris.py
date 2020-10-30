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

import pygame


#Intialize
pygame.init()

clock = pygame.time.Clock()

#creates Window 800 X 600
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Aggie Land Tetris!")
windowIcon = pygame.image.load("Texas A&M Logo.png")
pygame.display.set_icon(windowIcon)



running = True
#Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(( 128, 0, 0))
    clock.tick(60) 
    pygame.display.update()
    


pygame.quit()
