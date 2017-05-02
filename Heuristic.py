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


        self.__positionScores   = [ [ 95,10,70,60,60,70,10,95],
                                    [10,10,45,45,45,45,10,10],
                                    [70,40,70,50,50,70,40,70],
                                    [60,40,40,40,40,40,40,60],
                                    [60,40,40,40,40,40,40,60],
                                    [70,40,70,50,50,70,40,70],
                                    [10,10,45,45,45,45,10,10],
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
    def calculateValue(self, matrix,cornerArray,path):
        #print path
        movesPlayed = self.getMovesPlayed(copy.deepcopy(matrix))
        score = 1
        self.__setPosition(matrix,cornerArray)
        if(movesPlayed < 17):
            stabVal = 1 # don't think i need this here
            posVal = 1

            mobilityVal = 1
            mobilityVal = self.__getMobilityFactor(copy.deepcopy(matrix))
            self.__getEdgeStability(matrix,self.__myToken)
            posVal = self.__getPositionFactor(copy.deepcopy(matrix),path)
            #self.XSquareCount(matrix)
            score = self.__getWeightStage1(stabVal,mobilityVal,posVal)

            #score = self.__getChipRatio(movesPlayed, copy.deepcopy(matrix))
            #score = self.__evaporation(movesPlayed,matrix)
        elif(movesPlayed >= 17 and movesPlayed <58):
            stabVal = self.__getUserStability(copy.deepcopy(matrix))
            mobilityVal = self.__getMobilityFactor(copy.deepcopy(matrix))
            posVal = self.__getPositionFactor(copy.deepcopy(matrix),path)
            score = self.__getWeightStage2(stabVal,mobilityVal,posVal)
        else:
            score = self.__getChipRatio(movesPlayed, copy.deepcopy(matrix))
            score *= self.__getMobilityFactor(copy.deepcopy(matrix))
            #score *= self.__getPositionFactor(copy.deepcopy(matrix))
            #score = self.__getUserStability(copy.deepcopy(matrix))
        #print '%.25f' % score
        return score

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

    #Would give the weights for each of the values put in for stage 1
    def __getWeightStage1(self,stabVal,mobilityVal,posVal):
        #print posVal
        stabVal = stabVal * .20
        mobilityVal = mobilityVal *.30
        posVal = posVal * .50
        score = stabVal * mobilityVal * posVal
        return score

    #Would give the weights for each of the values for stage 2
    def __getWeightStage2(self,stabVal,mobilityVal,posVal):
        stabVal = stabVal * .30
        mobilityVal = mobilityVal *.50
        posVal = posVal * 1
        score = stabVal * mobilityVal * posVal
        return score




    ###############################
    #Rating the amount of chips on the board
    ###############################

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


    ###########################
    #Mobility Rating
    ###########################

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

                if(self.rules.isLegalMove(i,j,matrix,self.__oppToken)):
                    opponentMoves +=1

        #not the best place to be at.So it's not a great result
        #this keep be improved if time for computation permits

        if(userMoves == opponentMoves-1):
            return .25/float(24)
        return (userMoves / float(opponentMoves))/float(24)

    # mobility factor is the number of moves normalized to
    # the maximum number of moves possible. Ranges from 0->1
    def __getUserMobilityFactor(self, matrix):
        movesPossible = 0
        for i in range(1,9):
            for j in range(1,9):
                if(self.rules.isLegalMove(i, j, matrix, self.__myToken)):
                    movesPossible += 1
        return movesPossible / float(15)

    #gets the oppenents mobility factor for a turn set
    def __getOppenentMobilityFactor(self,matrix):
        movesPossible = 0
        for i in range(1,9):
            for j in range(1,9):
                if(self.rules.isLegalMove(i, j, matrix, self.__oppToken)):
                    movesPossible += 1
        return movesPossible

    #####################################
    #Calculating the position of weight squares
    #####################################


    # position factor judges the position the AI is in. Analyzes
    # corners, edges. How to judge against bad spaces? Cannot get this to work the way I want!
    def __getPositionFactor(self, matrix,path):
        totalScore = 0
        turnCount = self.getMovesPlayed(matrix)
        for i in range(1,9):
            for j in range(1,9):
                #self.__positionHelper(matrix,i,j)
                if(matrix[i,j] == self.__myToken):
                    value = self.__positionScores[i-1][j-1]

                    if (value > 90):
                        totalScore += 300
                    elif(self.__isViable(path,i,j)):
                        totalScore += 100
                    elif(value < 11):
                        totalScore = totalScore - 50 * turnCount
                    else:
                        totalScore+=value


        if(totalScore <= 0):
            normalized = 1 / float(44.6875 * turnCount * 100)
        else:

            normalized = totalScore*8 / float(44.6875 * turnCount)

            #print totalScore
            #print normalized
        return normalized

    #Gets the amount of moves that are on the diagonal move from the
    #The corner.
    def countWedgeSquares(self,matrix):
        count = 0
        if(matrix[1,1] != self.__myToken):
            if(matrix[2,2] == self.__myToken):
                count+=1

        if(matrix[1,8] != self.__myToken):
            if(matrix[2,7] == self.__myToken):
                count+=1

        if(matrix[8,1] != self.__myToken):
            if(matrix[7,2] == self.__myToken):
                count+=1

        if(matrix[8,8] != self.__myToken):

            if(matrix[8,7] == self.__myToken):
                count+=1
        return count

    #gets the number of bad plays on the board; spots around the corner when
    # a corner move has not been played
    #might want to base this off of the first board state of the iteration
    def XSquareCount(self,matrix):
        count = 0
        if(matrix[1,1] != self.__myToken):
            if(matrix[1,2] == self.__myToken):
                count+=1
            if(matrix[2,1] == self.__myToken):
                count+=1
            if(matrix[2,2] == self.__myToken):
                count+=1

        if(matrix[1,8] != self.__myToken):
            if(matrix[1,7] == self.__myToken):
                count+=1
            if(matrix[2,7] == self.__myToken):
                count+=1
            if(matrix[2,8] == self.__myToken):
                count+=1

        if(matrix[8,1] != self.__myToken):
            if(matrix[7,1] == self.__myToken):
                count+=1
            if(matrix[7,2] == self.__myToken):
                count+=1
            if(matrix[8,2] == self.__myToken):
                count+=1

        if(matrix[8,8] != self.__myToken):
            if(matrix[7,8] == self.__myToken):
                count+=1
            if(matrix[8,7] == self.__myToken):
                count+=1
            if(matrix[7,7] == self.__myToken):
                count+=1
        return count


        #################################
        #Stability of the board functions
        #################################

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


    #gets the amount of corners for each player
    def __getCorners(self,matrix):
        corner = 0
        oppCorner = 0
        if(matrix[1,1] == self.__myToken):
            myCorner+=1
        if(matrix[1,1] == self.__oppToken):
            oppCorner+=1
        if(matrix[1,8] == self.__myToken):
            myCorner+=1
        if(matrix[1,8] == self.__oppToken):
            oppCorner+=1
        if(matrix[8,1] == self.__myToken):
            myCorner+=1
        if(matrix[8,1] == self.__oppToken):
            oppCorner+=1
        if(matrix[8,8] == self.__myToken):
            myCorner+=1
        if(matrix[8,8] == self.__oppToken):
            oppCorner+=1
        return myCorner,oppCorner


    #returns the number of __stable chips on the board
    def __getEdgeStability(self,matrix,token):
        count = 0
        if(matrix[1,1] == token):
            count += self.__stableRight(matrix,token,0)
            count += self.__stableBottom(matrix,token,0)
            count+=1
        if(matrix[1,8] == token):
            count += self.__stableLeft(matrix,token,0)
            count += self.__stableBottom(matrix,token,1)
            count+=1
        if(matrix[8,1] == token):
            count += self.__stableTop(matrix,token,0)
            count += self.__stableRight(matrix,token,1)
            count+=1
        if(matrix[8,8] == token):
            count += self.__stableLeft(matrix,token,1)
            count += self.__stableTop(matrix,token,1)
            count+=1
        return count

    #checks the stability of left (going to the left)
    def __stableLeft(self,matrix,token,direction):
        count = 0
        if(direction == 0):
            for i in range(7,2,-1):
                if(matrix[1,i] == token):
                    count+=1
                else:
                    return count
        else:
            for i in range(7,2,-1):
                if(matrix[8,i] == token):
                    count+=1
                else:
                    return count
        return count

    #Checking the stability of the right side stability (going to the right)
    def __stableRight(self,matrix,token,direction):
        count = 0
        if(direction == 0):
            for i in range(2,9):
                if(matrix[1,i] == token):
                    count+=1
                else:
                    return count
        else:
            for i in range(2,9):
                if(matrix[8,i] == token):
                    count+=1
                else:
                    return count
        return count

    #checks the stability of the top (going on)
    def __stableTop(self,matrix,token,direction):
        count = 0
        if(direction == 0):
            for i in range(7,1,-1):
                if(matrix[i,1] == token):
                    count+=1
                else:
                    return count
        else:
            for i in range(7,1,-1):
                if(matrix[i,8] == token):
                    count+=1
                else:
                    return count
        return count

    #checks the stability of the bottom (going down)
    def __stableBottom(self,matrix,token,direction):
        count = 0
        if (direction == 0):
            for i in range(2,8):
                if(matrix[i,1] == token):
                    count+=1
                else:
                    return count
        else:
            for i in range(2,8):
                if(matrix[i,8] == token):
                    count+=1
                else:
                    return count

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


    #########################
    #In progress/ needs mucho work
    ##############################

    #resets the value on the position table if the corner has been taken by the user
    def __setPosition(self,matrix,cornerArray):

        '''
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
        '''
        return

    #marks whether a move is viable based on the standards of having a corner played already
    def __isViable(self,path,i,j):

        if(((i ==2 and j ==1)or (i ==2 and j ==2)or (i ==1 and j ==2))):
            if([1,1] in path and [i,j] in path):
                print "Through the first if"
                if(path.index([1,1]) > path.index([i,j])):
                    print "Through the second if!", path.index([1,1]),path.index([i,j])
                    return True
                else:
                    return False
            else:
                return False

        elif(((i == 1 and j == 7) or (i ==2 and j ==7)or (i ==2 and j ==8))):
            if([1,8] in path and [i,j] in path):
                if(path.index([1,8]) > path.index([i,j])):
                    return True
                else:
                    return False
            else:
                return False
        elif(((i == 7 and j == 1) or (i ==7 and j ==2)or (i ==8 and j ==2))):
            if([8,1] in path and [i,j] in path):
                if(path.index([8,1]) > path.index([i,j])):
                    return True
                else:
                    return False
            else:
                return False
        elif(((i == 8 and j == 7) or (i == 7 and j ==8)or (i ==7 and j ==7))):
            if([8,8] in path and [i,j] in path):
                if(path.index([8,8]) > path.index([i,j])):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return True
        return False
