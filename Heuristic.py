import copy
from rules import Rules
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
    def calculateValue(self, matrix):
        movesPlayed = self.__getMovesPlayed(copy.deepcopy(matrix))
        score = 1
        self.__setPosition(matrix)
        if(movesPlayed < 2):
            score = self.__getChipRatio(movesPlayed, copy.deepcopy(matrix))
            #score = self.__evaporation(movesPlayed,matrix)
        else:
            if(movesPlayed > 55):
                score = self.__getChipRatio(movesPlayed, copy.deepcopy(matrix))

            score *= self.__getMobilityFactor(copy.deepcopy(matrix))
            #score *= self.__getPositionFactor(copy.deepcopy(matrix))
            self.__getUserStability(copy.deepcopy(matrix))
        return score


    #---------------------
    #  PRIVATE FUNCITONS
    #---------------------

    # counts all played turns on the board by looking for occupied spaces.
    def __getMovesPlayed(self, matrix):
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


    # mobility factor is the number of moves normalized to
    # the maximum number of moves possible. Ranges from 0->1
    def __getUserMobilityFactor(self, matrix):
        movesPossible = 0
        for i in range(1,9):
            for j in range(1,9):
                if(self.rules.isLegalMove(i, j, matrix, self.__myToken)):
                    movesPossible += 1
        return movesPossible / float(15)

    def __getMobilityFactor(self,matrix):
        userMoves = 0
        opponentMoves = 0
        for i in range(1,9):
            for j in range(1,9):
                if(self.rules.isLegalMove(i, j, matrix, self.__myToken)):
                    userMoves += 1
                    #nextMatrix = self.rules.insertMove(self.__myToken, copy.deepcopy(matrix), i, j)
                if(self.rules.isLegalMove(i,j,matrix,self.__oppToken)):
                    opponentMoves +=1
        #gets the average amount of moves for the opponent
        #opponentMoves = opponentMoves/userMoves
        print userMoves,opponentMoves
        return (userMoves / opponentMoves)/float(15)


    '''
    This needs to be normalized by the stability of the previous move board
    of the user. This would check to see how good of a move
    it actually is. Otherwise, this will overestimate the hype
    '''
    #checks the stability of the players move
    def __getUserStability(self,matrix):
        stabCount = 0
        if(self.__myToken == matrix[1,1]):
            stabCount +=1
            stabCount += self.__triangles(matrix,0)
        if(self.__myToken == matrix[8,8]):
            stabCount +=1
            stabCount += self.__triangles(matrix,1)
        if(self.__myToken == matrix[1,8]):
            stabCount +=1
            stabCount += self.__triangles(matrix,2)
        if(self.__myToken == matrix[8,1]):
            stabCount +=1
            stabCount += self.__triangles(matrix,3)
        return stabCount/float(10) # don't know why

    #gets the stability of every corner
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
                print "yes! Left top corner"

        #checks the bottom right corner
        elif (typeCheck == 1):
            if(self.__myToken == matrix[7,8]):
                count +=1
            if(self.__myToken == matrix[8,7]):
                count +=1
            if (count == 2):
                count +=3
                print "yes! bottom left corner"
        #checks the top right corner
        elif (typeCheck == 2):
            if(self.__myToken == matrix[1,7]):
                count +=1
            if(self.__myToken == matrix[2,8]):
                count +=1
            if (count == 2):
                count +=3
                print "yes@! the top right corner"

        #checks the bottom left corner
        elif (typeCheck == 3):
            if(self.__myToken == matrix[7,1]):
                count +=1
            if(self.__myToken == matrix[8,2]):
                count +=1
            if (count == 2):
                count +=3
                print "yes! the bottom left corner"
        return count

    def __getOppenentMobilityFactor(self,matrix):
        movesPossible = 0
        for i in range(1,9):
            for j in range(1,9):
                if(self.rules.isLegalMove(i, j, matrix, self.__oppToken)):
                    movesPossible += 1
        return movesPossible
    # position factor judges the position the AI is in. Analyzes
    # corners, edges. How to judge against bad spaces?
    def __getPositionFactor(self, matrix):
        totalScore = 0
        for i in range(1,9):
            for j in range(1,9):
                if(matrix[i,j] == self.__myToken):
                    #totalScore+= self.__positionScores[]
                    totalScore += self.__positionScores[i-1][j-1]

        # normalize the score. Seem reasonable?
        if(totalScore < 0):
            totalScore = (totalScore / 450) + 1
        if(totalScore == 0):
            totalScore = 1
        normalized = totalScore / 296

        return normalized

    #resets the value on the position table if the corner has been taken by the user
    def __setPosition(self,matrix):

        #top left
        if(self.__myToken == matrix[1,1]):
            self.__positionScores[0][1] = 17
            self.__positionScores[1][0] = 17
            self.__positionScores[1][1] = 7

        #bottom right
        if(self.__myToken == matrix[8,8]):
            self.__positionScores[6][7] = 17
            self.__positionScores[7][7] = 17
            self.__positionScores[6][6] = 7

        #top right
        if(self.__myToken == matrix[1,8]):
            self.__positionScores[0][6] = 17
            self.__positionScores[1][7] = 17
            self.__positionScores[1][6] = 7
            
        #bottom left
        if(self.__myToken == matrix[8,1]):
            self.__positionScores[6][0] = 17
            self.__positionScores[7][1] = 17
            self.__positionScores[6][1] = 7

        print self.__positionScores
