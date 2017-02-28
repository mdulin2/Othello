import numpy as np


class Rules:

    # returns true if the game is over. false otherwise
    def isGameOver(self, matrix):
        if(__isFull(matrix)):
            return True
        if(not __canMove(matrix)):
            return True
        return False


    def calcLegalMoves(self):
        pass

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
