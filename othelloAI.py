from rules import Rules
from Heuristic import Heuristic
import time
import copy

class OthelloAI:

    # initialize the AI to its proper token
    def __init__(self, AItoken, oppToken):
        self.heuristic = Heuristic(AItoken)
        self.rules = Rules()

        self.__myToken = AItoken
        self.__oppToken = oppToken
        self.__data = {}            # holds [x, y, token at XY]
        self.__graph = {}           # holds children in a list
        self.__maxDepth = 5         # depth of search space used (must be odd)
        self.__nodePtr = 0          # 0 is root, used for naming nodes


    # pulls the matrix from board and chooses a move to make.
    # returns chosen move as an integer X and a char Y.
    def makeMove(self, board):
        x,y = self.__deepMove(board.matrixB)
        return x, self.__changeY(y)


    # performs a move using minimax and alpha beta pruning
    def __deepMove(self, matrix):
        self.__nodePtr = 0
        self.__graph[0] = []
        self.__data[0] = [] # not sure what this should be yet
        self.__deepMoveBuilder(self.__nodePtr, 1, copy.deepcopy(matrix))
        print "AI Graph: ", self.__graph
        print "AI Data:  ", self.__data
        x,y = self.__getBestMove(matrix)
        return x,y


    # recursively builds the graph to be searched. Limited to a depth
    # specified in self.__maxDepth
    # populates self.__graph with children data
    # populates self.__data with x,y and token: [x,y,token]
    def __deepMoveBuilder(self,parNode, curDepth, matrix):
        # if depth is reached, stop recursion
        if(self.__maxDepth+1 == curDepth):
            return

        # set whose turn it is
        if(curDepth % 2 == 1): # odd current depth
            curToken = self.__myToken
        else:
            curToken = self.__oppToken

        # search for all possible moves
        for i in range(1,9):
            for j in range(1,9):
                if(self.rules.isLegalMove(i, j, matrix, curToken)):
                    self.__nodePtr += 1
                    self.__graph[self.__nodePtr] = []
                    self.__graph[parNode].append(self.__nodePtr)
                    self.__data[self.__nodePtr] = (i,j, curToken)
                    nextMatrix = self.rules.insertMove(curToken, copy.deepcopy(matrix), i, j)
                    self.__deepMoveBuilder(self.__nodePtr,curDepth+1,nextMatrix)


    # not built yet, just calls simple for now
    def __getBestMove(self, matrix):
        return self.__simpleMove(matrix)


    # loops through the matrix and picks the first move that is available.
    # ran with : 'x,y = self.__simpleMove(matrix)'
    # returns x and y coordinates of move to make.
    def __simpleMove(self, matrix):
        time.sleep(2)
        for i in range(1,9):
            for j in range(1,9):
                if(self.rules.isLegalMove(i, j, matrix, self.__myToken)):
                    return i,j

        return 999,5 # no moves available


    # convert Y into its proper board form (character)
    def __changeY(self,y):
        return chr(y + 64)