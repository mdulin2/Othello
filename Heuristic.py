import copy
from rules import Rules
import math
'''
Filename:   Heuristic.py
Authors:    Jacob Krantz, Max Dulin
Date:       4/26/17
Description:
    calculates the value of a board state for a player of Othello.
    Initialized with the token to be analyzed for and called by
    function 'calculateValue'.
Heuristic factors:
- evaporation
- chip ratio
- mobility
- position
'''

class Heuristic:

    # initializes necessary data structures
    def __init__(self, myToken,oppToken):
        self.rules = Rules()
        self.__oppToken = oppToken
        self.__myToken   = myToken
        self.__positionScores   = [ [ 30,-25,12,5,5,12,-25, 30],
                                    [-25,-25, 1,1,1, 1,-25,-25],
                                    [ 12,  1, 10,2,2, 10,  1, 12],
                                    [  5,  1, 2,1,1, 2,  1,  5],
                                    [  5,  1, 2,1,1, 2,  1,  5],
                                    [ 12,  1, 10,2,2, 10,  1,12],
                                    [-25,-25, 1,1,1, 1,-25,-25],
                                    [ 30,-25,12,5,5,12,-25, 30] ]


        self.__positionScores   = [ [ 95,10,70,60,60,70,10,95],
                                    [10,10,35,35,35,35,10,10],
                                    [70,30,70,50,50,70,30,70],
                                    [60,30,40,40,40,40,30,60],
                                    [60,30,40,40,40,40,30,60],
                                    [70,30,70,50,50,70,30,70],
                                    [10,10,35,35,35,35,10,10],
                                    [95,10,70,60,60,70,10,95]]

    # calculates the value of a given board state.
    # higher score return, the better the position.
    # factors of success:
    # - evaporation
    # - chip ratio
    # - mobility
    # - position
    # **option: add a multiplier in front of each to adjust their
    #       individual affect on the score. All are currently
    #       normalized to 0 < score < 1
    def calculateValue(self, matrix,cornerArray):
        movesPlayed = self.getMovesPlayed(copy.deepcopy(matrix))
        score = 1
        self.__setPosition(matrix,cornerArray)
        if(movesPlayed < 17):
            stabVal = 1 # don't think i need this here
            posVal = 1

            mobilityVal = 1
            mobilityVal = self.__getMobilityFactor(copy.deepcopy(matrix))

            posVal = self.__getPositionFactor(copy.deepcopy(matrix),cornerArray)

            score = self.__getWeightStage1(stabVal,mobilityVal,posVal)

            #score = self.__getChipRatio(movesPlayed, copy.deepcopy(matrix))
            #score = self.__evaporation(movesPlayed,matrix)
        elif(movesPlayed >= 17 and movesPlayed <58):
            stabVal = self.__getUserStability(copy.deepcopy(matrix))
            mobilityVal = self.__getMobilityFactor(copy.deepcopy(matrix))
            posVal = self.__getPositionFactor(copy.deepcopy(matrix),cornerArray)
            score = self.__getWeightStage2(stabVal,mobilityVal,posVal)
        else:
            score = self.__getChipRatio(movesPlayed, copy.deepcopy(matrix))
            score *= self.__getMobilityFactor(copy.deepcopy(matrix))
            #score *= self.__getPositionFactor(copy.deepcopy(matrix))
            #score = self.__getUserStability(copy.deepcopy(matrix))
        #print '%.25f' % score
        return score

    def calculateBegin(self,matrix):
        stabVal = self.__getUserStability(copy.deepcopy(matrix))
        mobilityVal = 1
        #mobilityVal = self.__getMobilityFactor(copy.deepcopy(matrix))
        posVal = self.__getPositionFactor(copy.deepcopy(matrix))
        score = self.__getWeightStage2(stabVal,mobilityVal,posVal)

    #---------------------
    #  PRIVATE FUNCITONS
    #---------------------


    # counts all played turns on the board by looking for occupied spaces.
    def getMovesPlayed(self, matrix):
        movesPlayed = 0
        for i in range(1,9):
            for j in range(1,9):
                if(matrix[i,j] != '-'):
                    movesPlayed += 1
        return movesPlayed


    # returns the ratio of chips on the board that are myToken.
    def __getChipRatio(self, movesPlayed, matrix):
        myCount = 0
        for i in range(0,9):
            for j in range(1,9):
                if(matrix[i,j] == self.__myToken):
                    myCount += 1
        return myCount / float(movesPlayed)


    # inverse of chip ratio: at beginning of game, give away
    # more spaces to improve end game chances
    def __evaporation(self,movesPlayed,matrix):
        return 1 / float(self.__getChipRatio(movesPlayed,matrix))


    # gets the maximum number of moves for the user
    #along with the maximum number of moves for the other player
    #It's an approximation for the opponent so I added an offset
    def __getMobilityFactor(self,matrix):
        userMoves = 0
        opponentMoves = 1
        for i in range(1,9):
            for j in range(1,9):
                if(self.rules.isLegalMove(i, j, matrix, self.__myToken)):
                    userMoves += 1
                    #nextMatrix = self.rules.insertMove(self.__myToken, copy.deepcopy(matrix), i, j)
                if(self.rules.isLegalMove(i,j,matrix,self.__oppToken)):
                    opponentMoves +=1
        #gets the average amount of moves for the opponent

        #max number of moves possible in 28 for a player
        return (userMoves / opponentMoves)/float(24)


    '''
    This needs to be normalized by the stability of the previous move board
    of the user. This would check to see how good of a move
    it actually is. Otherwise, this will overestimate the hype
    '''
    #checks the stability of the players move
    def __getUserStability(self,matrix):
        stabCount = 1
        #checks the top left corner
        if(self.__myToken == matrix[1,1]):
            stabCount +=1
            stabCount += self.__triangles(matrix,0)
        #checks the bottom right corner
        if(self.__myToken == matrix[8,8]):
            stabCount +=1
            stabCount += self.__triangles(matrix,1)
        #checks the top right corner
        if(self.__myToken == matrix[1,8]):
            stabCount +=1
            stabCount += self.__triangles(matrix,2)
        #checks the bottom left corner
        if(self.__myToken == matrix[8,1]):
            stabCount +=1
            stabCount += self.__triangles(matrix,3)
        return stabCount/float(24) #24 is the maximum score possible here for a turn


    # mobility factor is the number of moves normalized to
    # the maximum number of moves possible. Ranges from 0->1
    def __getUserMobilityFactor(self, matrix):
        movesPossible = 0
        for i in range(1,9):
            for j in range(1,9):
                if(self.rules.isLegalMove(i, j, matrix, self.__myToken)):
                    movesPossible += 1
        return movesPossible / float(15)


    #gets the stability of every corner(only one layer deep)
    def __triangles(self,matrix,typeCheck):
        count = 0
        #gets the stability of the top left corner
        if(typeCheck == 0):
            if(self.__myToken == matrix[2,1]):
                count +=1
            if(self.__myToken == matrix[1,2]):
                count +=1
            if(count ==2):
                count +=3

        #checks the bottom right corner
        elif (typeCheck == 1):
            if(self.__myToken == matrix[7,8]):
                count +=1
            if(self.__myToken == matrix[8,7]):
                count +=1
            if (count == 2):
                count +=3
        #checks the top right corner
        elif (typeCheck == 2):
            if(self.__myToken == matrix[1,7]):
                count +=1
            if(self.__myToken == matrix[2,8]):
                count +=1
            if (count == 2):
                count +=3

        #checks the bottom left corner
        elif (typeCheck == 3):
            if(self.__myToken == matrix[7,1]):
                count +=1
            if(self.__myToken == matrix[8,2]):
                count +=1
            if (count == 2):
                count +=3
        return count

    #gets the oppenents mobility factor for a turn set
    def __getOppenentMobilityFactor(self,matrix):
        movesPossible = 0
        for i in range(1,9):
            for j in range(1,9):
                if(self.rules.isLegalMove(i, j, matrix, self.__oppToken)):
                    movesPossible += 1
        return movesPossible

    def __positionHelper(self,matrix,i,j):
        #leftCorner
        if(i == 1 or j == 1 or j ==2 or i == 2):
            if((i == 1 and j == 2)):
                if(matrix[i,j] != self.__myToken and matrix[i,j] != '-' ):
                    self.__positionScores[0][1] = 80
            if((i == 2 and j == 2)):
                #print "matrix: ",matrix[i,j]
                if(self.__oppToken):
                    self.__positionScores[1][1] = 80
            if((i == 2 and j == 1)):
                if(matrix[i,j] != self.__myToken and matrix[i,j] != '-' ):
                    self.__positionScores[1][0] = 80


        #right corner!
        if((i == 1 and j == 7)):
            if(matrix[i,j] != self.__myToken and matrix[i,j] != '-' ):
                self.__positionScores[0][7] = 80
        if((i == 2 and j == 7)):
            #print "matrix: ",matrix[i,j]
            if(matrix[i,j] != self.__myToken and matrix[i,j] != '-' ):
                self.__positionScores[1][6] = 80
        if((i == 2 and j == 8)):
            if(matrix[i,j] != self.__myToken and matrix[i,j] != '-' ):
                self.__positionScores[1][7] = 80

    # position factor judges the position the AI is in. Analyzes
    # corners, edges. How to judge against bad spaces? Cannot get this to work the way I want!
    def __getPositionFactor(self, matrix,cornerArray):
        totalScore = 0
        for i in range(1,9):
            for j in range(1,9):
                #self.__positionHelper(matrix,i,j)
                if(matrix[i,j] == self.__myToken):
                    value = self.__positionScores[i-1][j-1]

                    if (value > 90):
                        totalScore += 20000000#120
                    elif(self.__isViable(cornerArray,i,j)):
                        totalScore+=75
                    elif(value < 11):
                        totalScore =-20000000
                        #print totalScore
                    else:
                        totalScore+=value

        turnCount = self.getMovesPlayed(matrix)
        if(totalScore <= 0):
            normalized = 1 / float(44.6875 * turnCount * 100)
        else:

            normalized = totalScore / float(44.6875 * turnCount * 4)
            #print totalScore
            #print normalized
        return normalized

    #Would give the weights for each of the values put in for stage 1
    def __getWeightStage1(self,stabVal,mobilityVal,posVal):
        stabVal = stabVal * .20
        mobilityVal = mobilityVal *.30
        posVal = posVal * .50
        score = stabVal * mobilityVal * posVal
        return score

    #Would give the weights for each of the values for stage 2
    def __getWeightStage2(self,stabVal,mobilityVal,posVal):
        stabVal = stabVal * .30
        mobilityVal = mobilityVal *.35
        posVal = posVal * .35
        score = stabVal * mobilityVal * posVal
        return score
    #resets the value on the position table if the corner has been taken by the user
    def __setPosition(self,matrix,cornerArray):


        #top left
        if(self.__myToken == matrix[1,1] and cornerArray[0] == True):
            #print "here!"
            self.__positionScores[0][1] = 70
            self.__positionScores[1][0] = 70
            self.__positionScores[1][1] = 65
            self.__positionScores[0][2] = 60
            self.__positionScores[2][0] = 60

        #top right
        if(self.__myToken == matrix[1,8] and cornerArray[1] == True):
            self.__positionScores[0][6] = 80
            self.__positionScores[1][7] = 65
            self.__positionScores[1][6] = 80
            self.__positionScores[0][5] = 65
            self.__positionScores[2][7] = 65

        #bottom left
        if(self.__myToken == matrix[8,1] and cornerArray[2] == True):
            self.__positionScores[6][0] = 80
            self.__positionScores[7][1] = 80
            self.__positionScores[6][1] = 65
            self.__positionScores[5][0] = 65
            self.__positionScores[7][2] = 80


        #bottom right
        if(self.__myToken == matrix[8,8] and cornerArray[3] == True):
            self.__positionScores[6][7] = 80
            self.__positionScores[6][6] = 65
            self.__positionScores[7][6] = 80
            self.__positionScores[5][7] = 65
            self.__positionScores[7][5] = 65
        return

    #marks whether a move is viable based on the standards of having a corner played already
    def __isViable(self,cornerArray,i,j):

        if(((i ==2 and j ==1)or (i ==2 and j ==2)or (i ==1 and j ==2)) and cornerArray[0]):
            if(i ==2 and j ==1):
                return True
            if(i == 1 and j == 2):
                return True
            if(i==2 and j ==2):
                return True
        elif(((i == 1 and j == 7) or (i ==2 and j ==7)or (i ==2 and j ==8)) and cornerArray[1]):
            if(i ==1 and j ==7):
                return True
            if(i == 2 and j == 7):
                return True
            if(i==2 and j ==8):
                return True
        elif(((i == 7 and j == 1) or (i ==7 and j ==2)or (i ==8 and j ==2)) and cornerArray[2]):
            if(i ==7and j ==1):
                return True
            if(i == 7 and j == 2):
                return True
            if(i==8 and j ==2):
                return True
        elif(((i == 8 and j == 7) or (i == 7 and j ==8)or (i ==7 and j ==7)) and cornerArray[3]):
            if(i ==8and j ==7):
                return True
            if(i == 7 and j == 8):
                return True
            if(i==7 and j ==7):
                return True

        else:
            return False
        return False
