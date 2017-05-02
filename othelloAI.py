from rules import Rules
from Heuristic import Heuristic
from abPrune import ABPrune
import random as rand
import time
import copy
import numpy

class OthelloAI:

    # initialize the AI to its proper token
    def __init__(self, AItoken, oppToken):
        self.heuristic = Heuristic(AItoken,oppToken)
        self.rules = Rules()
        self.abPrune = ABPrune()
        self.__myToken = AItoken
        self.__oppToken = oppToken
        self.__graph = {}           # holds children in a list
        self.__data = {}            #[value,isMax,parent,alpha,beta,x,y,token]
        self.__maxDepth = 3 # depth of search space used (must be odd)
        self.__nodePtr = 0          # 0 is root, used for naming nodes
        self.__cornerArray = [False,False,False,False]


    # pulls the matrix from board and chooses a move to make.
    # returns chosen move as an integer X and a char Y.
    def makeMove(self, board):
        x,y = self.__deepMove(board.matrixB)
        return x, self.__changeY(y)

    #prints all of the possible move for the turn
    def printMoves(self,matrix,turn):
        print ("ALl of the moves: ")
        for i in range(1,9):
            for j in range(1,9):
                if(matrix[i,j] == '-'):
                    if(self.rules.isLegalMove(i,j,matrix,turn)):
                        print i,j

    def resetValues(self,matrix):
        self.abPrune = ABPrune()
        self.__graph = {}           # holds children in a list
        self.__data = {}            #[value,isMax,parent,alpha,beta,x,y,token]
        self.__nodePtr = 0          # 0 is root, used for naming nodes
        self.__graph[0] = []
        self.__data[0] = [-999999,True,"none",-999999,999999,0,0,self.__myToken] # not sure what this should be yet
        depth = self.__getDepth(matrix) #
        self.heuristic.setDepth(depth)

    # performs a move using minimax and alpha beta pruning
    def __deepMove(self, matrix):
        self.__setCornerArray(matrix)
        self.printMoves(matrix,self.__myToken)
        #my computer is too slow to run this. You can mess around with this though
        moveCount = self.rules.getMoveCount(matrix,self.__myToken)
        if(moveCount == 0):
            return 999,C
        self.resetValues(matrix)
        self.__data = self.__deepMoveBuilder(self.__nodePtr, 1, copy.deepcopy(matrix),[])
        #print "AI Graph: ", self.__graph
        #print "AI data:  ", self.__data
        #print "AI data: ",self.__data
        x,y = self.__getBestMove()
        return x,y

    #sets the corner values of the array; don't want to get too greedy!
    def __setCornerArray(self,matrix):

        if(matrix[1,1]== self.__myToken):
            self.__cornerArray[0] = True

        if(matrix[0,7]== self.__myToken):
            self.__cornerArray[1] = True

        if(matrix[7,0]== self.__myToken):
            self.__cornerArray[2] = True

        if(matrix[7,1]== self.__myToken):
            self.__cornerArray[3] = True

    #How deep the tree should branch, based on the amount of moves on the board
    def __getDepth(self,matrix):
        moveCount = self.rules.getMoveCount(matrix,self.__myToken)
        print "Moves left in the game:" , moveCount

        if(moveCount < 4):
            self.__maxDepth = 7
        elif(moveCount >= 4 and moveCount < 7):
            self.__maxDepth = 3
        else:
            self.__maxDepth = 3

        #if the depth goes to deep with no further moves then the game will crash
        #So, this if statement fixes that issue
        if(self.__maxDepth >= (moveCount)):
            self.__maxDepth = moveCount

        return self.__maxDepth


    # recursively builds the graph to be searched. Limited to a depth
    # specified in self.__maxDepth
    # populates self.__graph with children data
    # populates self.__data with x,y and token: [x,y,token]
    def __deepMoveBuilder(self,parNode, curDepth, matrix,path):
        # if depth is reached, stop recursion
        if(self.__maxDepth+1 == curDepth):
            return


        # set whose turn it is
        if(curDepth % 2 == 1): # odd current depth
            curToken = self.__myToken
        else:
            curToken = self.__oppToken

        #self.__isViable(matrix)
        # search for all possible moves
        for i in range(1,9):
            for j in range(1,9):
                if(self.rules.isLegalMove(i, j, matrix, curToken)):
                    path.append([i,j])
                    self.__nodePtr += 1
                    self.__graph[self.__nodePtr] = []
                    self.__graph[parNode].append(self.__nodePtr)
                    nextMatrix = self.rules.insertMove(curToken, copy.deepcopy(matrix), i, j)
                    #print i,j,
                    self.__data[self.__nodePtr] = self.__getDataValues(curToken,curDepth,i,j,copy.deepcopy(nextMatrix),copy.deepcopy(path))

                    self.__deepMoveBuilder(self.__nodePtr,curDepth+1,nextMatrix,[])


            #should do something if the AI is out of moves
        return self.__data


    #gets the parent of a nodes
    #this could be more efficient i just don't know how to do this
    def __getParent(self,curDepth):
        #print curDepth
        for key in self.__graph:
            for child in self.__graph[key]:
                if(self.__nodePtr == child):
                    return key

    #gets the heuristic value
    def __getDataValues(self,curToken,curDepth,i,j,matrix,path):
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
            value = self.heuristic.calculateValue(matrix,self.__cornerArray,path)
        parent = self.__getParent(curDepth)
        #need to find the parent right here

        return [value,token,parent,sA,sB,i,j,curToken]


    # returns the x and y of the best move as
    # searched by abPrune
    def __getBestMove(self):
        self.abPrune.initGraph(self.__graph,self.__data)
        self.abPrune.minimax(0)
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
