

import numpy as np
from rules import Rules


#Highlights the font when printed
class color:
    WARNING = '\033[93m'
    END = '\033[0m'


# turn can flip between 'W' and 'B'
class Turn:

    def __init__(self, turn='B'):
        self.turn = turn

    def flip(self):
        if(self.turn == 'W'):
            self.turn = 'B'
        else:
            self.turn = 'W'
    def getTurn(self):
        return self.turn

class ScoreBoard:

    # player and AI are either 'W' or 'B'. They cannot be the same
    def __init__(self, player, AI):
        assert(player != AI)
        self.whiteScore = 0
        self.blackScore = 0
        self.player = player
        self.AI = AI

    def updateScore(self, w, b):
        self.whiteScore = w
        self.blackScore = b

    def displayScore(self):
        print "----ScoreBoard----"
        if(self.player == 'W'):
            print ("Player Score: " + str(self.whiteScore))
            print ("AI Score: " + str(self.blackScore))
            print "------------------"
        else:
            print ("Player Score: " + str(self.blackScore))
            print ("AI Score: " + str(self.whiteScore))
            print "------------------"

class Board:

    # Constructor for the Board. Turn defaults to Black.
    # player and AI are either 'W' or 'B'.
    # config is either 1 or 2. 1 if 'W' starts top left, 2 if flipped.
    def __init__(self, player, AI, config, turn='B'):
        # initialize scoreboard with correct player names
        self.scoreboard = ScoreBoard(player, AI)
        # import rules of Othello
        self.rules = Rules()
        #making the board matrix
        self.matrixB = np.chararray((9,9))
        #whose turn it is; 'B' for black and 'W' for white.
        self.turn = Turn(turn)
        # set up the game and initial Board
        self.__gameSetUp(config)

    #this print function will display the contents of the board, matrixB
    def printBoard(self):
        print self.matrixB
        self.scoreboard.displayScore()

    #returns the value of turn, either B for black or W for white.
    def getTurn(self):
        return self.turn.getTurn()

    #highlights the changes that were made in the previous move
    def highLight(self,oldMatrix):
        for i in range(0,9):
            for j in range(0,9):
                if(self.matrixB[i,j] != oldMatrix[i,j]):
                    print(color.WARNING + self.matrixB[i,j] + color.END),
                else:
                    print self.matrixB[i,j],
            print
    def getNumberOfChanges(self,oldMatrix):
        count = 0
        for i in range(0,9):
            for j in range(0,9):
                if(self.matrixB[i,j] != oldMatrix[i,j]):
                    count+=1
        return count
    #x and y are the coordinate points that correspond to the matrix.
    #The ____move____s alternate so it's easy to have two people, or one and an A.I. play
    def move(self,x,y):
        #should be a check legal __move__ function here for the x and y coordinate

        if(self.__isLegalMove(x,y)):
            y = self.__changeY(y)

            self.matrixB = self.rules.insertMove(self.turn.getTurn(), self.matrixB, x, y)
            oldMatrix = np.copy(self.matrixB)

            self.matrixB,score = self.rules.flipChipString(x,y,self.matrixB,self.turn.getTurn())
            self.highLight(oldMatrix)
            print("changes! : ",self.getNumberOfChanges(oldMatrix))

            #flips the turns
            self.turn.flip()
            #scorring the game
            wScore,bScore = self.getScore()
            self.scoreboard.updateScore(wScore,bScore)

        else:
            raise Exception("Move Error")

    # returns the score as two integer returns: white score followed by black.
    def getScore(self):
        whiteScore = 0
        blackScore = 0
        for i in range(1,9):
            for j in range(1,9):

                if(self.matrixB[i,j] == 'W'):
                    whiteScore += 1
                elif(self.matrixB[i,j] == 'B'):
                    blackScore += 1

        return whiteScore,blackScore


    ############################
            #PRIVATE
    ############################

    #Running the initial set ups for the game.
    def __gameSetUp(self, config=1):
        self.__createBoard()
        self.__startingBoard(config)

    #adds the values onto the Othello Board for references.
    def __createBoard(self):
        self.matrixB[:] = '-'
        self.matrixB[0,0] = '*'
        for i in range(1,9):
            self.matrixB[0,i] =  chr(ord('A')+i-1)
        for i in range(1,9):
            self.matrixB[i,0] = i

    #Sets the starting pieces to the game without toggling the turn.
    # if config == 1, begins with 'B' in top left.
    # if config == 2, begins with 'W' in top left
    def __startingBoard(self, config):
        if(config == 1):
            self.matrixB[4,5] = 'B'
            self.matrixB[4,4] = 'W'
            self.matrixB[5,4] = 'B'
            self.matrixB[5,5] = 'W'
        elif(config == 2):
            self.matrixB[4,5] = 'W'
            self.matrixB[4,4] = 'B'
            self.matrixB[5,4] = 'W'
            self.matrixB[5,5] = 'B'
        else:
            raise Exception("startingConfig bound error")

        self.scoreboard.updateScore(2,2)



    #changes the value of the uptop letters to integers in order to
    #let the matrix have the correct input.
    def __changeY(self,y):
        #need to establish this as an integer otherwise it may cause errors
        return int(chr(ord(y)-16))


    # checks if a submitted move is legal.
    # - checks valid input characters
    # - checks if the spot is open
    # - checks if the move is Othello-legal
    def __isLegalMove(self,x,y):
        if(self.__checkInput(x,y) and self.__isSpotOpen(x,y)):
            y = self.__changeY(y)
            return self.rules.isLegalMove(x,y,self.matrixB,self.turn.getTurn())
        return False

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
    b = Board( 'W', 'B', 1, 'B')
    b.printBoard()
    print b.getTurn()
    b.move(3,'D')


    
    b.move(3,'C')
    b.printBoard()
    b.move(4,'C')
    b.printBoard()
    print(b.getTurn())
    b.move(5,'C')
    b.printBoard()
    b.move(4,'B')
    b.move(2,'D')
    print(b.getTurn())
    b.printBoard()
    b.move(2,'C')
    b.printBoard()
    b.move(4,'A')
    b.printBoard()
    b.move(1,'D')
    b.printBoard()
    b.move(2,'B')
    b.printBoard()
    b.move(6,'D')
    b.printBoard()
    b.move(3,'E')
    b.printBoard()
    b.move(4,'F')
    b.printBoard()
    b.move(2,'E')
    b.printBoard()
    b.move(1,'E')
    b.printBoard()
    b.move(4,'G')
    b.printBoard()
    print b.getTurn()
