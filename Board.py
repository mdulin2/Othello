import numpy as np


class Board:

    #Constructor for the Board. Turn defaults to Black
    def __init__(self, turn='B'):
        #making the board matrix
        self.matrixB = np.chararray((9,9))
        #whose turn it is; 'B' for black and 'W' for white.
        self.turn = turn
        # set up the game and initial Board
        self.__gameSetUp()

    #this print function will display the contents of the board, matrixB
    def printBoard(self):
        scoreTup = self.getScore()
        print self.matrixB
        print("White score: " + str(scoreTup[0]))
        print("Black score: " + str(scoreTup[1]))

    #returns the value of turn, either B for black or W for white.
    def getTurn(self):
        return self.turn

    #x and y are the coordinate points that correspond to the matrix.
    #The ____move____s alternate so it's easy to have two people, or one and an A.I. play
    def move(self,x,y):
        y = self.__changeY(y)
        #should be a check legal __move__ function here for the x and y coordinate
        if(self.turn == 'B'):
            #the setting of the matrix starts at 0 and not 1. So a -1 is needed.
            self.matrixB[x,y] = 'B'
            self.turn = 'W'
        else:
            #the setting of the matrix starts at 0 and not 1. So a -1 is needed.
            self.matrixB[x,y] = 'W'
            self.turn = 'B'

    # displays the current score and also returns
    # the score as (whiteScore,blackScore)
    def getScore(self):
        whiteScore = 0
        blackScore = 0
        for i in range(1,9):
            for j in range(1,9):

                if(self.matrixB[i,j] == 'W'):
                    whiteScore += 1
                elif(self.matrixB[i,j] == 'B'):
                    blackScore += 1

        return (whiteScore,blackScore)


    ############################
            #PRIVATE
    ############################

    #Running the initial set ups for the game.
    def __gameSetUp(self):
        self.__createBoard()
        self.__startingBoard()

    #adds the values onto the Othello Board for references.
    def __createBoard(self):
        self.matrixB[:] = '-'
        self.matrixB[0,0] = '*'
        for i in range(1,9):
            self.matrixB[0,i] =  chr(ord('A')+i-1)
        for i in range(1,9):
            self.matrixB[i,0] = i

    #Sets the starting pieces to the game set up, as according to Othello himself
    def __startingBoard(self):
        self.move(4,'E')
        self.move(4,'D')
        self.move(5,'D')
        self.move(5,'E')

    #changes the value of the uptop letters to integers in order to
    #let the matrix have the correct input.
    def __changeY(self,y):
        #need to establish this as an integer otherwise it may cause errors
        return int(chr(ord(y)-16))

    #Checks to make sure that the x and y input are valid characters for the board.
    #Currently not in use but I thought it would be valuable to have.
    def __checkInput(self,x,y):
        if(int(x) < 1 or int(x) > 8):
            print "Bad x value input; keep in the range of 1-8."
            return False
        if(y >= 'A' and y <= 'H' or y>='a' and y <= 'h'):
            return True
        else:
            print "Bad y value input; keep in the range of A-H."
            return False

    #Returns true if the spot is open, false otherwise.
    def __isSpotOpen(self,x,y):
        y = self.__changeY(y)
        return(self.matrixB[x,y] == '-')


# if Board.py is top-level module, run main. (used only for testing)
if(__name__ == "__main__"):
    b = Board('W')
    b.printBoard()
    print b.getTurn()
    b.move(6,'E')
    b.printBoard()
    print b.getTurn()
