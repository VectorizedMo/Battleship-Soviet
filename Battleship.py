#Modules
import pygame
pygame.init()
import time
import threading
import random
import math
import copy

#Main Variables
HEIGHT = 700
WIDTH = 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
SCREEN.fill((20,82,20))
DEFAULTSHIPMAPPING = ["Battleship",1,4,"Cruiser", 2,3, "Destroyer", 3,2, "Submarine", 4,1]
pygame.display.set_caption("Battleship (Soviet)")
TextStore = []
Oswald = 'Oswald-Regular.ttf'
Font = pygame.font.Font('Oswald-Regular.ttf', 50)
Text = Font.render('Battleship',True,(255,255,255))
TextRect = Text.get_rect()
TextRect.center = (HEIGHT//2,WIDTH//15)

#Resetting Screen Lambda
RESETSCREEN = lambda x,y: pygame.draw.rect(SCREEN,(20,82,20),pygame.Rect(x,y,HEIGHT,WIDTH))

#Main Board Class
class Board:
    def __init__(self, length, width, SquareSizeX, SquareSizeY):
        self.length = length
        self.width = width
        self.Board = []
        self.Boardlist = [[0 for x in range(10)] for y in range(10)]
        self.SquareSizeX = SquareSizeX
        self.SquareSizeY = SquareSizeY
        self.CentreList = []
        self.ShipsAmount = ["Battleship",1,4,"Cruiser", 2,3, "Destroyer", 3,2, "Submarine", 4,1]
        self.FindShipWithLength = ["Battleship",4,"Cruiser",3, "Destroyer",2, "Submarine", 1]
        self.AIBoard = []

    def CreateSquares(self, window, Amount):
        MainRect = pygame.Rect(0,0,HEIGHT,WIDTH)
        self.Board.clear()
        #Important Info on the Squares
        SpaceInBetween = 4
        SquareWidth = math.ceil((self.length-(HEIGHT/self.SquareSizeX))/Amount)
        SquareLength = math.ceil((self.length-(HEIGHT/self.SquareSizeY))/Amount)
        InitialStartingPoint = math.ceil((HEIGHT - ((SquareLength+SpaceInBetween)*Amount))/2)
        InitialStartingPosX = math.ceil((HEIGHT - ((SquareLength+SpaceInBetween)*Amount))/2)
        InitialStartingPosY = math.ceil((HEIGHT - ((SquareLength+SpaceInBetween)*Amount))/1.2)
        SquareIncrementForSpace = SquareLength+SpaceInBetween
        ColorVal = 255
        ColorMapping = [(255,0,0),(0,0,255),(0,255,0),(255,255,0),(0,0,0),(87,8,97),(150,20,60),(60,70,120),(150,150,20),(255,192,203)]
        #Looping and creating the squares.
        for i in range(Amount):
            RowListRects = []
            RowlistCentres = []
            for j in range(Amount):
                Rect = pygame.Rect(InitialStartingPosX,InitialStartingPosY,SquareWidth,SquareLength)
                pygame.draw.rect(window, (ColorVal, ColorVal, ColorVal), Rect)
                for k,v in enumerate(ColorMapping):
                    if self.Boardlist[i][j] == k:
                        pygame.draw.circle(SCREEN,v,(InitialStartingPosX+(SquareLength/2), InitialStartingPosY+(SquareLength/2)), Amount/2)
                RowListRects.append(Rect)
                RowlistCentres.append((InitialStartingPosX+(SquareLength/2), InitialStartingPosY+(SquareLength/2)))
                InitialStartingPosX += SquareIncrementForSpace
                ColorVal -= 2
            self.Board.append(RowListRects)
            self.CentreList.append(RowlistCentres)
            InitialStartingPosX = InitialStartingPoint
            InitialStartingPosY += SquareIncrementForSpace

    def CheckTwoPoints(self, P1, P2, mode, Board):
        GoingAround = [(1,1), (1,0), (-1,0), (-1,-1), (0,1), (0,-1), (-1,1), (1,-1)]
        Suitable = True
        if P1 == P2:
            TypeOfShip = "Submarine"
            if self.ShipsAmount[self.ShipsAmount.index(TypeOfShip)+1] > 0:
                for coord in GoingAround:
                    try:
                        if P1[0]+coord[0] < 0 or P1[1]+coord[1] < 0:
                            continue
                        if Board[P1[0]+coord[0]][P1[1]+coord[1]] == 2:
                            Suitable = False
                    except IndexError:
                        pass
                if Suitable:
                    if not mode:
                        Board[P1[0]][P2[1]] = 2
                        self.ShipsAmount[self.ShipsAmount.index(TypeOfShip)+1] -= 1
                    return True
        if P1[0] == P2[0]:
            Length = abs(P1[1]-P2[1])+1
            if Length <= 4 and Length >= 2:
                TypeOfShip = self.FindShipWithLength[self.FindShipWithLength.index(Length)-1]
                if self.ShipsAmount[self.ShipsAmount.index(TypeOfShip)+1] > 0:
                    if(P1[1] - P2[1]) < 0:
                        for i in range(P1[1], P2[1]+1):
                            if Board[P1[0]][i] == 2:
                                Suitable = False
                            try:
                                if i == P1[1]:
                                    if Board[P1[0]][i-1] == 2 or Board[P1[0]-1][i] == 2 or Board[P1[0]+1][i] == 2 or Board[P1[0]-1][i-1] == 2 or Board[P1[0]+1][i-1] == 2:
                                        if i <= 0 and P1[0] <= 0:
                                            if Board[P1[0]+1][i] == 2:
                                                Suitable = False
                                        elif i <= 0:
                                            if Board[P1[0]-1][i] == 2 or Board[P1[0]+1][i] == 2:
                                                Suitable = False
                                        elif P1[0] <= 0:
                                            if Board[P1[0]][i-1] == 2 or Board[P1[0]+1][i] == 2 or Board[P1[0]+1][i-1] == 2:
                                                Suitable = False
                                        else:
                                            Suitable = False
                                if i == P2[1]:
                                    if Board[P1[0]][i+1] == 2 or Board[P1[0]-1][i] == 2 or Board[P1[0]+1][i] == 2 or Board[P1[0]-1][i+1] == 2 or Board[P1[0]+1][i+1] == 2:
                                        if i <= 0 and P1[0] <= 0:
                                            if Board[P1[0]+1][i] == 2 or Board[P1[0]][i+1] == 2 or Board[P1[0]+1][i+1] == 2:
                                                Suitable = False
                                        elif i <= 0:
                                            if Board[P1[0]-1][i] == 2 or Board[P1[0]-1][i+1] == 2:
                                                Suitable = False
                                        elif P1[0] <= 0:
                                            if Board[P1[0]+1][i] == 2 or Board[P1[0]][i+1] == 2 or Board[P1[0]+1][i+1] == 2:
                                                Suitable = False
                                        else:
                                            Suitable = False
                                if Board[P1[0]-1][i] == 2 or Board[P1[0]+1][i] == 2:
                                    if P1[0] <= 0:
                                        if Board[P1[0]+1][i] == 2:
                                            Suitable = False
                                    else:
                                        Suitable = False
                            except IndexError:
                                if P1[0] < 9 and P1[0] > 0:
                                    if Board[P1[0]+1][i] == 2 or Board[P1[0]-1][i] == 2:
                                        Suitable = False
                                    if i == P1[1]:
                                        if i < 0:
                                            if Board[P1[0]][i-1] == 2 or Board[P1[0]+1][i-1] == 2 or Board[P1[0]-1][i-1]:
                                                Suitable = False
                                    if i == P2[1]:
                                        if i < 9 and i < 0:
                                            if Board[P1[0]][i+1] == 2 or Board[P1[0]+1][i+1] == 2 or Board[P1[0]-1][i-1]:
                                                Suitable = False
                                elif i < 9 and i > 0:
                                    if i == P1[1]:
                                        if Board[P1[0]][i-1] == 2 or Board[P1[0]-1][i-1] == 2:
                                            Suitable = False
                                    if i == P2[1]:
                                        if i < 9:
                                            if Board[P1[0]][i+1] == 2 or Board[P1[0]-1][i+1] == 2:
                                                Suitable = False
                                    if Board[P1[0]-1][i] == 2:
                                        Suitable = False
                                else:
                                    if P1[0] < 9 and P1[0] < 0:
                                        if Board[P1[0]+1][i] == 2 or Board[P1[0]-1][i]:
                                            Suitable = False
                                    elif P1[0] < 9:
                                        if Board[P1[0]+1][i] == 2:
                                            Suitable = False
                                    else:
                                        if Board[P1[0]-1][i]:
                                            Suitable = False
                        if Suitable:
                            if not mode:
                                for i in range(P1[1], P2[1]+1):
                                    Board[P1[0]][i] = 2
                                self.ShipsAmount[self.ShipsAmount.index(TypeOfShip)+1] -= 1
                            return True
                            
                    else:
                        for i in range(P2[1], P1[1]+1):
                            if Board[P1[0]][i] == 2:
                                Suitable = False
                            try:
                                if i == P2[1]:
                                    if Board[P1[0]][i-1] == 2 or Board[P1[0]-1][i] == 2 or Board[P1[0]+1][i] == 2 or Board[P1[0]-1][i-1] == 2 or Board[P1[0]+1][i-1] == 2:
                                        if i <= 0 and P1[0] <= 0:
                                            if Board[P1[0]+1][i] == 2:
                                                Suitable = False
                                        elif i <= 0:
                                            if Board[P1[0]-1][i] == 2 or Board[P1[0]+1][i] == 2:
                                                Suitable = False
                                        elif P1[0] <= 0:
                                            if Board[P1[0]][i-1] == 2 or Board[P1[0]+1][i-1] == 2 or Board[P1[0]+1][i] == 2:
                                                Suitable = False
                                        else:
                                            Suitable = False
                                if i == P1[1]:
                                    if Board[P1[0]][i+1] == 2 or Board[P1[0]-1][i] == 2 or Board[P1[0]+1][i] == 2 or Board[P1[0]-1][i+1] == 2 or Board[P1[0]+1][i+1] == 2:
                                        if i <= 0 and P1[0] <= 0:
                                            if Board[P1[0]+1][i] == 2 or Board[P1[0]][i+1] == 2 or Board[P1[0]+1][i+1] == 2:
                                                Suitable = False
                                        elif i <= 0:
                                            if Board[P1[0]-1][i] == 2 or Board[P1[0]-1][i+1] == 2:
                                                Suitable = False
                                        elif P1[0] <= 0:
                                            if Board[P1[0]+1][i] == 2 or Board[P1[0]][i+1] == 2 or Board[P1[0]+1][i+1] == 2:
                                                Suitable = False
                                        else:
                                            Suitable = False
                                if Board[P1[0]-1][i] == 2 or Board[P1[0]+1][i] == 2:
                                    if P1[0] <= 0:
                                        if Board[P1[0]+1][i] == 2:
                                            Suitable = False
                                    else:
                                        Suitable = False
                            except IndexError:
                                if P1[0] < 9 and P1[0] > 0:
                                    if Board[P1[0]+1][i] == 2 or Board[P1[0]-1][i] == 2:
                                        Suitable = False
                                    if i == P2[1]:
                                        if i > 0:
                                            if Board[P1[0]][i-1] == 2 or Board[P1[0]+1][i-1] == 2 or Board[P1[0]-1][i-1]:
                                                Suitable = False
                                    if i == P1[1]:
                                        if i < 9:
                                            if Board[P1[0]][i+1] == 2 or Board[P1[0]+1][i+1] == 2 or Board[P1[0]-1][i-1]:
                                                Suitable = False

                                elif i < 9 and i > 0:
                                    if i == P2[1]:
                                        if Board[P1[0]][i-1] == 2 or Board[P1[0]-1][i-1] == 2:
                                            Suitable = False
                                    if i == P1[1]:
                                        if i < 9:
                                            if Board[P1[0]][i+1] == 2 or Board[P1[0]-1][i+1] == 2:
                                                Suitable = False
                                    if Board[P1[0]-1][i] == 2:
                                        Suitable = False
                                else:
                                    if P1[0] < 9 and P1[0] < 0:
                                        if Board[P1[0]+1][i] == 2 or Board[P1[0]-1][i]:
                                            Suitable = False
                                    elif P1[0] < 9:
                                        if Board[P1[0]+1][i] == 2:
                                            Suitable = False
                                    else:
                                        if Board[P1[0]-1][i]:
                                            Suitable = False
                        if Suitable:
                            if not mode:
                                for i in range(P2[1], P1[1]+1):
                                    Board[P1[0]][i] = 2
                                self.ShipsAmount[self.ShipsAmount.index(TypeOfShip)+1] -= 1
                            return True

                
        if P1[1] == P2[1]:
            Length = abs(P1[0]-P2[0])+1
            if Length <= 4 and Length >= 2:
                TypeOfShip = self.FindShipWithLength[self.FindShipWithLength.index(Length)-1]
                if self.ShipsAmount[self.ShipsAmount.index(TypeOfShip)+1] > 0:
                    if (P1[0]-P2[0]) < 0:
                        for i in range(P1[0], P2[0]+1):
                            if Board[i][P1[1]] == 2:
                                Suitable = False
                            try:
                                if i == P2[0]:
                                    if Board[i+1][P1[1]] == 2 or Board[i][P1[1]+1] == 2 or Board[i][P1[1]-1] == 2 or Board[i+1][P1[1]+1] == 2 or Board[i+1][P1[1]-1] == 2:
                                        if i <= 0 and P1[1] <= 0:
                                            if Board[i+1][P1[1]] == 2 or Board[i][P1[1]+1] == 2 or Board[i+1][P1[1]+1] == 2:
                                                Suitable = False
                                        elif i <= 0:
                                            if Board[i][P1[1]-1] == 2 or Board[i+1][P1[1]-1] == 2:
                                                Suitable = False
                                        elif P1[1] <= 0:
                                            if Board[i+1][P1[1]] == 2 or Board[i][P1[1]+1] == 2 or Board[i+1][P1[1]+1] == 2:
                                                Suitable = False
                                        else:
                                            Suitable = False
                                if i == P1[0]:
                                    if Board[i-1][P1[1]] == 2 or Board[i][P1[1]+1] == 2 or Board[i][P1[1]-1] == 2 or Board[i-1][P1[1]+1] == 2 or Board[i-1][P1[1]-1] == 2:
                                        if i <= 0 and P1[1] <= 0:
                                            if Board[i][P1[1]+1] == 2:
                                                Suitable = False
                                        elif i <= 0:
                                            if Board[i][P1[1]-1] == 2:
                                                Suitable = False
                                        elif P1[1] <= 0:
                                            if Board[i-1][P1[1]] == 2 or Board[i-1][P1[1]+1] == 2:
                                                Suitable = False
                                        else:
                                            Suitable = False
                                if Board[i][P1[1]+1] == 2 or Board[i][P1[1]-1] == 2:
                                    if P1[1] <= 0:
                                        if Board[i][P1[1]+1] == 2:
                                            Suitable = False
                                    else:
                                        Suitable = False
                            except IndexError:
                                if i < 9 and P1[1] > 0:
                                    if i == P1[0]:
                                        if i > 0:
                                            if Board[i-1][P1[1]] == 2 or Board[i-1][P1[1]-1] == 2:
                                                Suitable = False
                                    if i == P2[0]:
                                        if Board[i+1][P1[1]] == 2 or Board[i+1][P1[1]-1] == 2:
                                            Suitable = False
                                    if Board[i][P1[1]-1] == 2:
                                        Suitable = False
                                elif P1[1] < 9:
                                    if i == P1[0]:
                                        if Board[i-1][P1[1]] == 2 or Board[i-1][P1[1]-1] == 2 or Board[i-1][P1[1]+1] == 2:
                                            Suitable = False
                                    else:
                                        if Board[i][P1[1]-1] == 2 or Board[i][P1[1]+1] == 2:
                                            Suitable = False
                                else:
                                    if P1[1] < 9:
                                        if Board[i][P1[1]-1] == 2 or Board[i][P1[1]+1] == 2:
                                            Suitable = False
                                    else:
                                        if Board[i][P1[1]-1] == 2:
                                            Suitable = False
                        if Suitable:
                            if not mode:
                                for i in range(P1[0], P2[0]+1):
                                    Board[i][P1[1]] = 2
                                self.ShipsAmount[self.ShipsAmount.index(TypeOfShip)+1] -= 1 
                            return True  
                                
                    else:
                        for i in range(P2[0], P1[0]+1):
                            if Board[i][P1[1]] == 2:
                                Suitable = False
                            try:
                                if i == P1[0]:
                                    if Board[i+1][P1[1]] == 2 or Board[i][P1[1]+1] == 2 or Board[i][P1[1]-1] == 2 or Board[i+1][P1[1]+1] == 2 or Board[i+1][P1[1]-1] == 2:
                                        if i <= 0 and P1[1] <= 0:
                                            if Board[i+1][P1[1]] == 2 or Board[i][P1[1]+1] == 2 or Board[i+1][P1[1]+1] == 2:
                                                Suitable = False
                                        elif i <= 0:
                                            if Board[i][P1[1]-1] == 2 or Board[i+1][P1[1]-1] == 2:
                                                Suitable = False
                                        elif P1[1] <= 0:
                                            if Board[i+1][P1[1]] == 2 or Board[i][P1[1]+1] == 2 or Board[i+1][P1[1]+1] == 2:
                                                Suitable = False
                                        else:
                                            Suitable = False
                                if i == P2[0]:
                                    if Board[i-1][P1[1]] == 2 or Board[i][P1[1]+1] == 2 or Board[i][P1[1]-1] == 2 or Board[i-1][P1[1]+1] == 2 or Board[i-1][P1[1]-1] == 2:
                                        if i <= 0 and P1[1] <= 0:
                                            if Board[i][P1[1]+1] == 2:
                                                Suitable = False
                                        elif i <= 0:
                                            if Board[i][P1[1]-1] == 2:
                                                Suitable = False
                                        elif P1[1] <= 0:
                                            if Board[i-1][P1[1]] == 2 or Board[i-1][P1[1]+1] == 2:
                                                Suitable = False
                                        else:
                                            Suitable = False
                                if Board[i][P1[1]+1] == 2 or Board[i][P1[1]-1] == 2:
                                    if P1[1] <= 0:
                                        if Board[i][P1[1]+1] == 2:
                                            Suitable = False
                                    elif P1[1] < 9:
                                        if Board[i][P1[1]-1] == 2 or Board[i][P1[1]+1] == 2:
                                            Suitable = False
                            except IndexError:    
                                if i < 9 and P1[1] > 0:
                                    if i == P2[0]:
                                        if i > 0:
                                            if Board[i-1][P1[1]] == 2 or Board[i-1][P1[1]-1] == 2:
                                                Suitable = False
                                    if i == P1[0]:
                                        if Board[i+1][P1[1]] == 2 or Board[i+1][P1[1]-1] == 2:
                                            Suitable = False
                                    if Board[i][P1[1]-1] == 2:
                                        Suitable = False
                                elif P1[1] < 9:
                                    if i == P2[0]:
                                        if Board[i-1][P1[1]] == 2 or Board[i-1][P1[1]-1] == 2 or Board[i-1][P1[1]+1] == 2:
                                            Suitable = False
                                    else:
                                        if Board[i][P1[1]-1] == 2 or Board[i][P1[1]+1] == 2:
                                            Suitable = False
                                else:
                                    if P1[1] < 9:
                                        if Board[i][P1[1]-1] == 2 or Board[i][P1[1]+1] == 2:
                                            Suitable = False
                                    else:
                                        if Board[i][P1[1]-1] == 2:
                                            Suitable = False
                        if Suitable:
                            if not mode:
                                for i in range(P2[0], P1[0]+1):
                                    Board[i][P1[1]] = 2
                                self.ShipsAmount[self.ShipsAmount.index(TypeOfShip)+1] -= 1     
                            return True
                            
    def GenerateBoard(self):
        Board = [[0 for x in range(10)] for y in range(10)]
        Mapping = copy.deepcopy(DEFAULTSHIPMAPPING)
        RandomCoord2 = [0,0]
        Length = 0
        Subcount = 0
        #Horizontal
        while Mapping.count(0) != 4:
            RandomRow1 = random.randint(0,9)
            RandomColumn1 = random.randint(0,9)
            RandomCoord = (RandomRow1, RandomColumn1)
            HorOrVert = random.randint(1,2)
            if HorOrVert == 1:
                Length = random.randint(0,3)
                if RandomCoord[1] + Length <= 9:
                    RandomCoord2[0] = RandomCoord[0]
                    RandomCoord2[1] = RandomCoord[1] + Length
                    if self.CheckTwoPoints(RandomCoord, tuple(RandomCoord2), True, Board):
                        TypeOfShip = self.FindShipWithLength[self.FindShipWithLength.index(Length+1)-1]
                        if Mapping[Mapping.index(TypeOfShip)+1] > 0:
                            if TypeOfShip == "Submarine":
                                if Board[RandomCoord[0]][RandomCoord[1]] != 2:
                                    Board[RandomCoord[0]][RandomCoord[1]] = 2
                                    Mapping[Mapping.index(TypeOfShip)+1] -= 1
                            else:
                                for i in range(RandomCoord[1], RandomCoord2[1]+1):
                                    Board[RandomCoord[0]][i] = 2
                                Mapping[Mapping.index(TypeOfShip)+1] -= 1
            if HorOrVert == 2:
                Length = random.randint(0,3)
                if RandomCoord[0] + Length <= 9:
                    RandomCoord2[1] = RandomCoord[1]
                    RandomCoord2[0] = RandomCoord[0] + Length
                    if self.CheckTwoPoints(RandomCoord, tuple(RandomCoord2), True, Board):
                        TypeOfShip = self.FindShipWithLength[self.FindShipWithLength.index(Length+1)-1]
                        if Mapping[Mapping.index(TypeOfShip)+1] > 0:
                            if TypeOfShip == "Submarine":
                                if Board[RandomCoord[0]][RandomCoord[1]] != 2:
                                    Board[RandomCoord[0]][RandomCoord[1]] = 2
                                    Mapping[Mapping.index(TypeOfShip)+1] -= 1
                            else:
                                for i in range(RandomCoord[0], RandomCoord2[0]+1):
                                    Board[i][RandomCoord[1]] = 2
                                Mapping[Mapping.index(TypeOfShip)+1] -= 1
        self.AIBoard = Board

def CheckCondition(*args):
    count = 0
    for row in args[0]:
        for num in args:
            if type(num) == type(69):
                count += row.count(num)
    return count

#Create Text Function
def CreateTextandStore(*args):
    #ARGS: 1: NAME, 2: FONT SIZE, 3: COLOR, 4: CENTREPOSX, 5: CENTREPOSY
    Font = pygame.font.Font(Oswald, args[1])
    Text = Font.render(args[0], True, args[2])
    TextRect = Text.get_rect()
    TextRect.center = (args[3], args[4])
    TextStore.append(Text)
    TextStore.append(TextRect)
    for Item in args:
        TextStore.append(Item)
    return TextRect

def UpdateText():
    for i in range(0,len(TextStore),7):
        SCREEN.blit(TextStore[i], TextStore[i+1])

def ChangeText(*args):
    #ARGS: 1: NAME, 2: FONT SIZE, 3: COLOR, 4: CENTREPOSX, 5: CENTREPOSY, 6:INDEX
    Count = 0
    Font = pygame.font.Font(Oswald, args[1])
    Text = Font.render(args[0], True, args[2])
    TextRect = Text.get_rect()
    TextRect.center = (args[3], args[4])
    TextStore[args[5]] = Text
    TextStore[args[5]+1] = TextRect
    for i in range(2,7):
        TextStore[args[5]+i] = args[Count]
        Count += 1

def DeleteText(index):
    for i in range(index, index+7):
        TextStore.pop(index)

#Initializing Board
BattleshipBoard = Board(HEIGHT, WIDTH, 5,5)

#Main Game Function
def main():
    running = True
    MainNameRect = CreateTextandStore("BATTLESHIP", 50, (255,255,255), HEIGHT//2,WIDTH//15)
    PlayGameRect = CreateTextandStore("PLAY GAME", 32, (255,150,75), HEIGHT//1.2,WIDTH//15)
    Playing = False
    SelectedSquare = None
    PreviousSquare = None
    PlayGameDone = False
    FirstClick = False
    BattleshipBoard.CreateSquares(SCREEN, 10)
    BattleshipBoard.GenerateBoard()
    AttackPhase = False
    AttackPhaseEnter = False
    Attacking = False
    num = 0
    ColorsForShip = [2,7,8]
    AIAttackList = []
    PlayerAttackList = []
    #Main Loop
    while running:
        if BattleshipBoard.ShipsAmount.count(0) == 4:
            AttackPhase = True
            if not AttackPhaseEnter:
                Playing = False
                SelectedSquare = None
                PreviousSquare = None
                SCREEN.fill((0,0,0))
                DeleteText(TextStore.index('PLACE YOUR SHIPS')-2)
                MainNameRect = CreateTextandStore("ATTACK!", 50, (255,255,255), HEIGHT//2,WIDTH//15)
                AttackPhaseEnter = True
        BattleshipBoard.CreateSquares(SCREEN, 10)
        UpdateText()
        #For Loop for Inputs
        for event in pygame.event.get():
            #Input to Quit Game, running sets to false thereby stopping the main loop and quitting.
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                MousePosition = pygame.mouse.get_pos()
                ClickedPlay = PlayGameRect.collidepoint(MousePosition)
                Cancelled = None
                Reset = None
                try:
                    PreviousSquare = SelectedSquare
                except UnboundLocalError:
                    pass
                if ClickedPlay and not PlayGameDone:
                    Playing = True
                    RESETSCREEN(0,0)
                    BattleshipBoard.CreateSquares(SCREEN, 10)
                    DeleteText(TextStore.index(PlayGameRect)-1)
                    MainNameRect = ChangeText("PLACE YOUR SHIPS", 50, (255,255,255), HEIGHT//2,WIDTH//15, TextStore.index(MainNameRect)-1)
                    CancelRect = CreateTextandStore("PRESS TO CANCEL", 20, (255,255,255), HEIGHT//9,WIDTH//15)
                    ResetRect = CreateTextandStore("PRESS TO RESET", 20, (255,255,255), HEIGHT//1.12,WIDTH//15)
                    PlayGameDone = True

                #Detecting two squares chosen and drawing appropriate graphics
                if Playing:
                    Cancelled = CancelRect.collidepoint(MousePosition)
                    Reset = ResetRect.collidepoint(MousePosition)
                    for i in range(10):
                        for j in range(10):
                            #Selected Square Finding, Main Selection Code
                            if BattleshipBoard.Board[i][j].collidepoint(MousePosition) and BattleshipBoard.Board[i][j] != 1:
                                #Check if Selected Square is Green/Part of a ship
                                if BattleshipBoard.Boardlist[i][j] != 2:
                                    SelectedSquare = (i,j)
                                    BattleshipBoard.Boardlist[i][j] = 1
                                    if PreviousSquare != SelectedSquare and PreviousSquare and BattleshipBoard.Boardlist[PreviousSquare[0]][PreviousSquare[1]] != 2:
                                        BattleshipBoard.Boardlist[PreviousSquare[0]][PreviousSquare[1]] = 0
                                else:
                                    #If clicked on a green part/ship then reset selection
                                    if PreviousSquare:
                                        BattleshipBoard.Boardlist[PreviousSquare[0]][PreviousSquare[1]] = 0
                                    SelectedSquare = None
                                    PreviousSquare = None
                if AttackPhase:
                    Reset = False
                    for i in range(10):
                        for j in range(10):
                            if BattleshipBoard.Board[i][j].collidepoint(MousePosition) and BattleshipBoard.Board[i][j] != 1:
                                SelectedSquare = (i,j)
                                if SelectedSquare == PreviousSquare:
                                    if SelectedSquare in PlayerAttackList:
                                        continue
                                    PlayerAttackList.append(SelectedSquare)
                                    RandomHit = (random.randint(0,9), random.randint(0,9))
                                    while RandomHit in AIAttackList:
                                        RandomHit = (random.randint(0,9), random.randint(0,9))
                                    AIAttackList.append(RandomHit)
                                    if BattleshipBoard.AIBoard[SelectedSquare[0]][SelectedSquare[1]] == 2:
                                        if False:
                                            BattleshipBoard.Boardlist[RandomHit[0]][RandomHit[1]] = 9
                                            pass
                                        else:
                                            if BattleshipBoard.Boardlist[SelectedSquare[0]][SelectedSquare[1]] == 2:
                                                BattleshipBoard.Boardlist[SelectedSquare[0]][SelectedSquare[1]] = 8
                                            elif BattleshipBoard.Boardlist[SelectedSquare[0]][SelectedSquare[1]] in [7,8]:
                                                pass
                                            elif BattleshipBoard.Boardlist[SelectedSquare[0]][SelectedSquare[1]] == 4:
                                                BattleshipBoard.Boardlist[SelectedSquare[0]][SelectedSquare[1]] = 9
                                            else:
                                                BattleshipBoard.Boardlist[SelectedSquare[0]][SelectedSquare[1]] = 3

                                    if BattleshipBoard.Boardlist[SelectedSquare[0]][SelectedSquare[1]] == 4 and BattleshipBoard.AIBoard[SelectedSquare[0]][SelectedSquare[1]] != 2:
                                        BattleshipBoard.Boardlist[SelectedSquare[0]][SelectedSquare[1]] = 5
                                    if BattleshipBoard.Boardlist[SelectedSquare[0]][SelectedSquare[1]] == 0:
                                        BattleshipBoard.Boardlist[SelectedSquare[0]][SelectedSquare[1]] = 6
                                    if BattleshipBoard.Boardlist[SelectedSquare[0]][SelectedSquare[1]] == 2:
                                        BattleshipBoard.Boardlist[SelectedSquare[0]][SelectedSquare[1]] = 7
                                    if BattleshipBoard.Boardlist[RandomHit[0]][RandomHit[1]] in ColorsForShip:
                                        if BattleshipBoard.Boardlist[RandomHit[0]][RandomHit[1]] == 7:
                                            BattleshipBoard.Boardlist[RandomHit[0]][RandomHit[1]] = 5
                                        elif BattleshipBoard.Boardlist[RandomHit[0]][RandomHit[1]] == 8:
                                            BattleshipBoard.Boardlist[RandomHit[0]][RandomHit[1]] = 9
                                        else:
                                            BattleshipBoard.Boardlist[RandomHit[0]][RandomHit[1]] = 4
                #Graphical Stuff
                #Cancelling and resetting selection.
                if Cancelled and Playing:
                    if SelectedSquare:
                        BattleshipBoard.Boardlist[SelectedSquare[0]][SelectedSquare[1]] = 0
                    if PreviousSquare:
                        BattleshipBoard.Boardlist[PreviousSquare[0]][PreviousSquare[1]] = 0
                    PreviousSquare = None
                    SelectedSquare = None
                #Resetting Board
                if Reset and Playing:
                    SelectedSquare = None
                    PreviousSquare = None
                    BattleshipBoard.ShipsAmount = copy.deepcopy(DEFAULTSHIPMAPPING)
                    for i in range(10):
                        for j in range(10):
                            BattleshipBoard.Boardlist[i][j] = 0
                            
                #Actually Building the Ships
                if SelectedSquare:
                    if PreviousSquare:
                        ShipValue = BattleshipBoard.CheckTwoPoints(SelectedSquare,PreviousSquare, False, BattleshipBoard.Boardlist)
                        if ShipValue:
                            SelectedSquare = None
                            PreviousSquare = None
        if CheckCondition(BattleshipBoard.Boardlist,8,3,9) == 20:
            print("You won")
            quit()
        elif CheckCondition(BattleshipBoard.Boardlist,5,4,9) == 20:
            print("AI won")
            quit()
        pygame.display.update()
        
#Calling Main Function
main()
