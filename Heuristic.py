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
    def __init__(self, myToken):
        self.rules = Rules()
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

        if(movesPlayed < 10):
            score = self.__getChipRatio(movesPlayed, copy.deepcopy(matrix))
            #score = self.__evaporation(movesPlayed,matrix)
        else:
            if(movesPlayed > 55):
                #score = self.__getChipRatio(movesPlayed, copy.deepcopy(matrix))

            score *= self.__getMobilityFactor(copy.deepcopy(matrix))
            score *= self.__getPositionFactor(copy.deepcopy(matrix))

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
    def __getMobilityFactor(self, matrix):
        movesPossible = 0
        for i in range(1,9):
            for j in range(1,9):
                if(self.rules.isLegalMove(i, j, matrix, self.__myToken)):
                    movesPossible += 1
        return movesPossible / float(15)


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
