import copy

class Heuristic:

    def __init__(self, myToken):
        self.__myToken   = myToken
        self.__edgeSet   = []
        self.__cornerSet = []
        self.__badSet    = []
        self.__buildSets()


    # calculates the value of a given board state
    def calculateValue(self, matrix):
        mobility = self.__getMobilityFactor(copy.deepcopy(matrix))
        position = self.__getPositionFactor(copy.deepcopy(matrix))

        return mobility * position


    #---------------------
    #  PRIVATE FUNCITONS
    #---------------------

    # initializes the position sets for good and bad places
    def __buildSets(self):
        self.__cornerSet = [(1,1), (1,8), (8,1), (8,8)]

        self.__edgeSet   = [(1,3),(1,4),(1,5),(1,6), # standard edges
                            (3,1),(4,1),(5,1),(6,1),
                            (8,3),(8,4),(8,5),(8,6),
                            (3,8),(4,8),(5,8),(6,8)]

        self.__badSet    = [(1,2),(2,1),(2,2),       # surround the corner
                            (1,7),(2,7),(2,8),
                            (7,1),(7,2),(8,2),
                            (7,7),(7,8),(8,7)]


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
        cornerScore = self.__getCornerScore(copy.deepcopy(matrix))
        edgeScore   = self.__getEdgeScore(copy.deepcopy(matrix))
        badScore    = self.__getBadScore(copy.deepcopy(matrix))

        return cornerScore + edgeScore - badScore



    def __getCornerScore(self, matrix):
        pass

    def __getEdgeScore(self, matrix):
        pass
        
    def __getBadScore(self, matrix):
        pass
