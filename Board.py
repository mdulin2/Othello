import numpy as np


class Board:

    #this print function will display the contents of the board, matrixB
    def printBoard(self):
        print self.matrixB

    #returns the value of turn, either B for black or W for white.
    def getTurn(self):
        return self.turn

    #Running the initial set ups for the game.
    def gameSetUp(self):
        self.__createBoard__()
        self.__startingBoard__()



    ############################
            #PRIVATE
    ############################




    #Constructor for the Board.
    def __init__(self):
        #making the class
        self.matrixB = np.chararray((9,9))
        #whose turn it is; B for black and W for white.
        self.turn = 'B'

    #changes the value of the uptop letters to integers in order to
    #let the matrix have the correct input.
    def __changeY__(self,y):
        #need to establish this as an integer otherwise it may cause errors
        return int(chr(ord(y)-16))


    #x and y are the coordinate points that correspond to the matrix.
    #The ____move____s alternate so it's easy to have two people, or one and an A.I. play
    def __move__(self,x,y):
        y = self.__changeY__(y)
        #should be a check legal __move__ function here for the x and y coordinate
        if(self.turn == 'B'):
            #the setting of the matrix starts at 0 and not 1. So a -1 is needed.
            self.matrixB[x,y] = 'B'
            self.turn = 'W'
        else:
            #the setting of the matrix starts at 0 and not 1. So a -1 is needed.
            self.matrixB[x,y] = 'W'
            self.turn = 'B'

    #adds the values onto the Othello Board for references.
    def __createBoard__(self):
        self.matrixB[:] = '-'
        self.matrixB[0,0] = '*'
        for i in range(1,9):
            self.matrixB[0,i] =  chr(ord('A')+i-1)
        for i in range(1,9):
            self.matrixB[i,0] = i

    #Sets the starting pieces to the game set up, as according to Othello himself
    def __startingBoard__(self):
        self.__move__(4,'E')
        self.__move__(4,'D')
        self.__move__(5,'D')
        self.__move__(5,'E')

    #Checks to make sure that the x and y input are valid characters for the board.
    #Currently not in use but I thought it would be valuable to have.
    def __checkInput__(self,x,y):
        if(int(x) < 1 or int(x) > 8):
            print "Bad x value input; keep in the range of 1-8."
            return False
        if(y >= 'A' and y <= 'H' or y>='a' and y <= 'h'):
            return True
        else:
            print "Bad y value input; keep in the range of A-H."
            return False

    #Returns true if the spot is open, false otherwise.
    def __isSpotOpen__(self,x,y):
        y = self.__changeY__(y)
        if(self.matrixB[x,y] == '-'):
            return True
        return False


def main():
    b = Board()
    b.gameSetUp()
    print b.__isSpotOpen__(8,'H')
    print b.printBoard()
    return 0

main()
