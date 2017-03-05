import numpy as np


class Rules:
    # returns true if the game is over. false otherwise
    def isGameOver(self, matrix):
        if(__isFull(matrix)):
            return True
        if(not __canMove(matrix)):
            return True
        return False
        
    #Checks to see if a move is a legal move or not.
    #x and y are the values from the matrixB
    #matrixB is the board
    #turn is the person's turn to move ('W' or 'B')
    #move is the direction that the search is attempting to go.
    def isLegalMove(self,x,y,matrixB,turn):
        if(matrixB[x,y] != '-'):
            return False

        if(self.__isLegalHelp(x,y,matrixB,turn,'U',0)):
            return True
        if(self.__isLegalHelp(x,y,matrixB,turn,'UR',0)):
            return True
        if(self.__isLegalHelp(x,y,matrixB,turn,'R',0)):
            return True
        if(self.__isLegalHelp(x,y,matrixB,turn,'DR',0)):
            return True
        if(self.__isLegalHelp(x,y,matrixB,turn,'D',0)):
            return True
        if(self.__isLegalHelp(x,y,matrixB,turn,'DL',0)):
            return True
        if(self.__isLegalHelp(x,y,matrixB,turn,'L',0)):
            return True
        if(self.__isLegalHelp(x,y,matrixB,turn,'UL',0)):
            return True
        return False

    #returns the edited x and y coordinates for the function __isLegalHelp
    def __getCoordinate(self,x,y,move):
        if(move=='U'):
            x-=1
        elif(move == 'UR'):
            y+=1
            x+=1
        elif(move == 'R'):
            y+=1
        elif(move == 'DR'):
            x+=1
            y+=1
        elif(move == 'D'):
            x+=1
        elif(move == 'DL'):
            y-=1
            x+=1
        elif(move == 'L'):
            y-=1
        elif(move == 'UL'):
            x-=1
            y-=1
        return x,y

    #x and y are the values from the matrixB
    #matrixB is the board
    #turn is the person's turn to move ('W' or 'B')
    #score is the amount of chips to be fliped,if any
    #move is the direction that the search is attempting to go.
    def __isLegalHelp(self,x,y,matrixB,turn,move,score):
        if turn == "W":
            opp = "B"
        elif(turn == 'B'):
            opp = "W"

        x,y = self.__getCoordinate(x,y,move)

        try:
            if(matrixB[x,y] == opp):
                score+=1
                return self.__isLegalHelp(x,y,matrixB,turn,move,score)
            elif(matrixB[x,y] == turn):
                return score > 0
            else:
                return False
        #if out of bounds
        except:
            return False

    # checks if a proposed move is valid
    def checkLegalMove(self, matrix, x, y):
        return True

    # given a previous state matrix and coordinates for insertion,
    # makes a move and flips all necessary chips according to
    # othello rules
    def insertMove(self, turn, matrix, x, y):
        matrix = self.__makeMove(turn, matrix, x, y)
        return self.__fixBoard(turn, matrix, x, y)


    #
    # PRIVATE BELOW
    #

    # inserts the move into the matrix. Returns new matrix
    def __makeMove(self,turn, matrix, x, y):
        matrix[x,y] = turn
        return matrix

    # flips all necessary chips after a move has been made.
    # retuns resulting matrix.
    def __fixBoard(self,turn,matrix,x,y):
        return matrix


    # flips the color of the chip in the x,y location of the
    # passed in matrix. returns resulting matrix
    def __flipChip(self, matrix,x,y):
        assert(matrix[x,y] != '-')

        if(matrix[x,y] == 'W'):
            matrix[x,y] = 'B'
        else:
            matrix[x,y] = 'W'

        return matrix

    # returns true if all spaces on the board are occupied
    # false otherwise. Big-O sucks.
    def __isFull(self, matrix):
        for i in range(1,9):
            for j in range(1,9):
                if(matrix[i,j] == '-'):
                    return False
        return True

    # returns true if there exists a space in which a player
    # can legally move. False otherwise.
    def __canMove(self, matrix):
        pass
