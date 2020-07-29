# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 19:02:08 2020

@author: Baran
"""

import pygame
from random import randrange

"""GLOBAL VARIABLES"""

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (127, 127, 127)

cellPixelWH = 50
borderWH = 2
width = 10
height = 10
mineCount = 20


"""END OF GLOBAL VARIABLES"""

class Cell:
    mine = False
    clicked = False
    marked = False
    neighbourMines = 0
    

class Minesweeper:
    
    width = 10
    height = 10
    mineCount = 10
    flagCount = 10
    uncoveredCells = 0
    firstClick = True
    gameOver = False
    gameWon = False
    field = []
    
    #Constructor: Sets the number of cells in the game as width*height and the number of mines to be placed
    def __init__(self, width, height, mineCount):
        self.width = width
        self.height = height
        self.mineCount = min(mineCount, width*height)
        self.flagCount = self.mineCount
        for x in range(width):
            self.field.append([])
            for y in range(height):
                self.field[x].append([])
                self.field[x][y] = Cell()
                             
    #Updates a given cell with the count of neighbouring mines
    def updateCellNeighbourCount(self, x, y):
        self.field[x][y].neighbourMines = self.getCellNeighbourMineCount(x, y)
             
    #Counts the number of surrounding mines
    def getCellNeighbourMineCount(self, x, y):
        mines = 0
        if x > 0:
            if (self.field[x-1][y].mine):
                mines += 1
            if y > 0:
                if (self.field[x-1][y-1].mine):
                    mines += 1
            if y < self.height - 1:
                if (self.field[x-1][y+1].mine):
                    mines += 1
        if y < self.height - 1:
            if (self.field[x][y+1].mine):
                mines += 1
        if y > 0:
            if (self.field[x][y-1].mine):
                mines += 1
        if x < self.width - 1:
            if (self.field[x+1][y].mine):
                mines += 1
            if y > 0:
                if (self.field[x+1][y-1].mine):
                    mines += 1
            if y < self.height - 1:
                if (self.field[x+1][y+1].mine):
                    mines += 1
        return mines
    
    #Resets the game state
    def resetField(self):
        self.flagCount = self.mineCount
        self.uncoveredCells = self.width*self.height
        self.gameOver = False
        self.gameWon = False
        self.firstClick = True
        for x in range(self.width):
            for y in range(self.height):
                self.field[x][y].mine = False
                self.field[x][y].clicked = False
                self.field[x][y].marked = False
                self.field[x][y].neighbourMines = 0
    
    #Generates the minefield, with no mine on safeX and safeY
    def generateField(self, safeX, safeY):
        minesToGenerate = self.mineCount
        while (minesToGenerate):
            x = randrange(self.width)
            y = randrange(self.height)
            if (x != safeX) and (y != safeY) and (self.field[x][y].mine == False):
                self.field[x][y].mine = True
                minesToGenerate -= 1
    
    #Sets a flag at the select location
    def setFlag(self, x, y):
        if (self.field[x][y].clicked) or (self.gameOver) or (self.gameWon):
            return
        if (not self.field[x][y].marked) and (self.flagCount > 0):
            self.field[x][y].marked = True
            self.flagCount -= 1
        elif (self.field[x][y].marked):
            self.field[x][y].marked = False
            self.flagCount += 1
    
    #Uncovers all surrounding fields that do not contain a mine
    def uncoverNeighbours(self, x, y):
        if x > 0:
            if (not self.field[x-1][y].mine):
                self.click(x-1, y)
            if y > 0:
                if (not self.field[x-1][y-1].mine):
                    self.click(x-1, y-1)
            if y < self.height - 1:
                if (not self.field[x-1][y+1].mine):
                    self.click(x-1, y+1)
        if y < self.height - 1:
            if (not self.field[x][y+1].mine):
                self.click(x, y+1)
        if y > 0:
            if (not self.field[x][y-1].mine):
                self.click(x, y-1)
        if x < self.width - 1:
            if (not self.field[x+1][y].mine):
                self.click(x+1, y)
            if y > 0:
                if (not self.field[x+1][y-1].mine):
                    self.click(x+1, y-1)
            if y < self.height - 1:
                if (not self.field[x+1][y+1].mine):
                    self.click(x+1, y+1)
    
    #Clicks a field and updates the game state accordingly (explodes a mine if one is present, uncovers neighbours if there are no surrounding mines, etc)
    def click(self, x, y):
        if (self.gameOver) or (self.gameWon):
            return
        if (self.firstClick):
            self.generateField(x, y)
            self.firstClick = False
            self.click(x, y)
        elif (not self.field[x][y].clicked):
            self.field[x][y].clicked = True
            self.uncoveredCells += 1
            if self.field[x][y].mine:
                self.gameOver = True
            else:
                self.updateCellNeighbourCount(x, y)
                if (self.field[x][y].neighbourMines == 0):
                    self.uncoverNeighbours(x, y)
                if (self.field[x][y].marked == True):
                    self.field[x][y].marked = False
                    self.flagCount += 1
                if (self.uncoveredCells == self.width*self.height - self.mineCount):
                    self.gameWon = True
                

#Takes a screen, font, and minesweeper instance and draws it. The font is needed for the number of surrounding mines
def drawMS(screen, font, ms):
    for x in range(ms.width):
        for y in range(ms.height):
            if ms.field[x][y].clicked:
                if ms.field[x][y].mine:
                    pygame.draw.rect(screen, red, (borderWH+(cellPixelWH+borderWH)*x,borderWH+(cellPixelWH+borderWH)*y,cellPixelWH,cellPixelWH), 0) 
                else:
                    pygame.draw.rect(screen, white, (borderWH+(cellPixelWH+borderWH)*x,borderWH+(cellPixelWH+borderWH)*y,cellPixelWH,cellPixelWH), 0) 
                    font.render(str(ms.field[x][y].neighbourMines), True, blue)
                    srf = font.render(str(ms.field[x][y].neighbourMines), True, blue)
                    screen.blit(srf, ((borderWH+(cellPixelWH+borderWH)*x+cellPixelWH//2.5,borderWH+(cellPixelWH+borderWH)*y+cellPixelWH//4)))
            else:
                pygame.draw.rect(screen, black, (borderWH+(cellPixelWH+borderWH)*x,borderWH+(cellPixelWH+borderWH)*y,cellPixelWH,cellPixelWH), 0) 
                if (ms.field[x][y].marked):
                    srf = font.render("!", True, white)
                    screen.blit(srf, ((borderWH+(cellPixelWH+borderWH)*x+cellPixelWH//2.5,borderWH+(cellPixelWH+borderWH)*y+cellPixelWH//4)))

#Converts mouse coordinates to cell coordinates within the minefield
def mouseToField(x, y):
    fieldX = int(x / (cellPixelWH+borderWH))
    fieldY = int(y / (cellPixelWH+borderWH))
    return [fieldX, fieldY]
          
pygame.init()
ms = Minesweeper(width, height, mineCount)
font = pygame.font.SysFont("comicsansms", 20)
font_gameStatus = pygame.font.SysFont("comicsansms", 40)
screen = pygame.display.set_mode((ms.width*(cellPixelWH+borderWH)+borderWH+200, ms.height*(cellPixelWH+borderWH)+borderWH))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Space bar to reset the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ms.resetField()
        fieldCoord = mouseToField(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        #Left click to uncover a mine field
        if pygame.mouse.get_pressed()[0]:
            if (fieldCoord[0] < ms.width) and (fieldCoord[1] < ms.height):
                ms.click(fieldCoord[0], fieldCoord[1])
        #Right click to flag a spot
        if pygame.mouse.get_pressed()[2]:
            if (fieldCoord[0] < ms.width) and (fieldCoord[1] < ms.height):
                ms.setFlag(fieldCoord[0], fieldCoord[1])
            
    screen.fill(grey)
    drawMS(screen, font, ms)
    srf = font.render("Spacebar to reset ", True, blue)
    screen.blit(srf, ((ms.width*(cellPixelWH+borderWH)+borderWH+10,ms.height*(cellPixelWH+borderWH)+borderWH-40)))
    srf = font.render("Flags: " + str(ms.flagCount), True, blue)
    screen.blit(srf, ((ms.width*(cellPixelWH+borderWH)+borderWH+10,40)))
    if (ms.gameOver):
        srf = font.render("BOOM - Game Over", True, blue)
        screen.blit(srf, ((ms.width*(cellPixelWH+borderWH)+borderWH+10,10)))
    if (ms.gameWon):
        srf = font.render("Game Won!", True, blue)
        screen.blit(srf, ((ms.width*(cellPixelWH+borderWH)+borderWH+10,10)))
    pygame.display.update()
    
pygame.quit()