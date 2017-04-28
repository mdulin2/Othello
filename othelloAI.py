from rules import Rules
from Heuristic import Heuristic
from abPrune import ABPrune
import random as rand
import time
import copy

class OthelloAI:

    # initialize the AI to its proper token
    def __init__(self, AItoken, oppToken):
        self.heuristic = Heuristic(AItoken)
        self.rules = Rules()
        self.abPrune = ABPrune()
        self.__myToken = AItoken
        self.__oppToken = oppToken
        self.__graph = {}           # holds children in a list
        self.__data = {}            #[value,isMax,parent,alpha,beta,x,y,token]
        self.__maxDepth = 3 # depth of search space used (must be odd)
        self.__nodePtr = 0          # 0 is root, used for naming nodes


    # pulls the matrix from board and chooses a move to make.
    # returns chosen move as an integer X and a char Y.
    def makeMove(self, board):
        x,y = self.__deepMove(board.matrixB)
        return x, self.__changeY(y)


    def resetValues(self):
        self.abPrune = ABPrune()
        self.__graph = {}           # holds children in a list
        self.__data = {}            #[value,isMax,parent,alpha,beta,x,y,token]
        self.__maxDepth = 3 # depth of search space used (must be odd)
        self.__nodePtr = 0          # 0 is root, used for naming nodes
        self.__graph[0] = []
        self.__data[0] = [-999999,True,"none",-999999,999999,0,0,self.__myToken] # not sure what this should be yet


    # performs a move using minimax and alpha beta pruning
    def __deepMove(self, matrix):
        self.resetValues()
        self.__data = self.__deepMoveBuilder(self.__nodePtr, 1, copy.deepcopy(matrix))
        print "AI Graph: ", self.__graph
        #print "AI data:  ", self.__data
        #print "AI data: ",self.__data
        for key in self.__data:
            print key,self.__data[key][0],self.__data[key][5],self.__data[key][6]
        x,y = self.__getBestMove()

        print x,y
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
                    #self.__data[self.__nodePtr] = (i,j, curToken)
                    self.__data[self.__nodePtr] = self.__getDataValues(curToken,curDepth,i,j)
                    nextMatrix = self.rules.insertMove(curToken, copy.deepcopy(matrix), i, j)
                    #need to calculate
                    self.__deepMoveBuilder(self.__nodePtr,curDepth+1,nextMatrix)

        return self.__data

        
    #gets the parent of a nodes
    #this could be more efficient i just don't know how to do this
    def __getParent(self,curDepth):
        #print curDepth
        for key in self.__graph:
            for child in self.__graph[key]:
                if(self.__nodePtr == child):
                    return key



    #sets the data values to make the alpha beta prunning possible
    def __getDataValues(self,curToken,curDepth,i,j):
        sA = -999999
        sB = 999999

        #true if my token, false otherwise
        if(curToken == self.__myToken):
            token = False
            value = sB
        else:
            token = True
            value = sA

        #if at the max depth of the tree
        if(curDepth == self.__maxDepth):
            #value = heuristicValue
            value = rand.random() * 100
            #value = 0
        parent = self.__getParent(curDepth)
        #need to find the parent right here

        return [value,token,parent,sA,sB,i,j,curToken]


    # returns the x and y of the best move as
    # searched by abPrune
    def __getBestMove(self):
        self.abPrune.initGraph(self.__graph,self.__data)
        print self.abPrune.minimax(0)
        return self.abPrune.getBestPlace()


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
