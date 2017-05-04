from rules import Rules
from Heuristic import Heuristic
from abPrune import ABPrune
from operator import itemgetter
import random as rand
import time
import copy

class OthelloAI:

    # initialize the AI to its proper token
    def __init__(self, AItoken, oppToken):
        self.heuristic = Heuristic(AItoken,oppToken)
        self.rules = Rules()
        self.abPrune = ABPrune()
        self.__myToken = AItoken
        self.__oppToken = oppToken
        self.__graph = {}           # holds children in a list
        self.__data = {}            # [value,isMax,parent,alpha,beta,x,y,token, path]
        self.__matrixState = {}     # holds matrix state at node
        self.__maxDepth = 5         # depth of search space used (must be odd)
        self.__midDepth = 3         # middle prune mark
        self.__nodePtr = 0          # 0 is root, used for naming nodes


    # pulls the matrix from board and chooses a move to make.
    # returns chosen move as an integer X and a char Y.
    def makeMove(self, board):
        #x,y = self.__simpleMove(board.matrixB)
        x,y = self.__deepMove(board.matrixB)
        return x, self.__changeY(y)

    #prints all of the possible move for the turn
    def printMoves(self,matrix,turn):
        print ("ALl of the moves: ")
        for i in range(1,9):
            for j in range(1,9):
                if(matrix[i][j] == '-'):
                    if(self.rules.isLegalMove(i,j,matrix,turn)):
                        print i,j


    # initialize all search space variables for new build and search
    def __resetValues(self,matrix, moveCount):
        self.abPrune = ABPrune()
        self.__graph = {}           # holds children in a list
        self.__data = {}            #[value,isMax,parent,alpha,beta,x,y,token, path]
        self.__nodePtr = 0          # 0 is root, used for naming nodes
        self.__graph[0] = []
        self.__data[0] = [-999999,True,"none",-999999,999999,0,0,self.__myToken, []]
        self.__setDepth(matrix, moveCount)
        self.heuristic.setDepth(self.__maxDepth)


    # performs a move using minimax and alpha beta pruning
    def __deepMove(self, matrix):
        moveCount = self.rules.getMoveCount(matrix,self.__myToken)
        if(moveCount == 0):
            return 999,'C'

        self.__resetValues(matrix, moveCount)
        self.__deepMoveBuilder(self.__midDepth, self.__nodePtr, 1, copy.deepcopy(matrix),[])
        self.__reorderChildren(0)

        if(self.__maxDepth > self.__midDepth):
            self.__pruneMiddle()
            self.__buildToMax(0, 1) # start node, start depth

        #self.__printGraph()
        #self.__printData()
        x,y = self.__getBestMove()
        return x,y


    # Set max tree depth, based on the amount of moves on the board.
    # moveCount: number of moves available to the AI
    def __setDepth(self,matrix, moveCount):
        movesToGo = 0
        for i in range(1,9):
            for j in range(1,9):
                if matrix[i][j] == '-':
                    movesToGo += 1

        if(moveCount >= 9 or movesToGo < 5):
            self.__maxDepth = 3
        else:
            self.__maxDepth = 5


    # recursively builds the graph to be searched. Limited to a depth
    # specified in self.__maxDepth
    # populates self.__graph with children data
    # populates self.__data
    def __deepMoveBuilder(self,stopDepth, parNode, curDepth, matrix, path):
        # if depth is reached, stop recursion
        if(stopDepth+1 == curDepth):
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
                    path.append([i,j])
                    self.__nodePtr += 1
                    self.__graph[self.__nodePtr] = []
                    self.__graph[parNode].append(self.__nodePtr)
                    nextMatrix = self.rules.insertMove(curToken, copy.deepcopy(matrix), i, j)

                    self.__setDataValues(curToken,curDepth,i,j,copy.deepcopy(nextMatrix),copy.deepcopy(path), parNode)

                    self.__deepMoveBuilder(stopDepth, self.__nodePtr,curDepth+1,nextMatrix,[])


    #sets the heuristic value
    def __setDataValues(self, curToken, curDepth, i, j, matrix, path, parent):
        sA = -999999
        sB = 999999

        #true if my token, false otherwise
        if(curToken == self.__myToken):
            token = False
            value = sB
        else:
            token = True
            value = sA

        #if at the max depth of the tree or for reordering the first
        if(curDepth == self.__maxDepth or curDepth == 1 or curDepth == self.__midDepth):
            value = self.heuristic.calculateValue(matrix,path)

        self.__data[self.__nodePtr] = [value,token,parent,sA,sB,i,j,curToken, path]
        self.__matrixState[self.__nodePtr] = copy.deepcopy(matrix)


    # given a node, reorders its children according to their heuristic value.
    # Best is on the left.
    def __reorderChildren(self, parent):
        childLst = self.__graph[parent]
        valueLst = []

        for child in childLst:
            valueLst.append((child, self.__data[child][0]))

        # sort the list
        if(len(valueLst) > 1):
            sortedLst = list(reversed(sorted(valueLst,key=itemgetter(1))))
            sortedLst = map(itemgetter(0), sortedLst)
            self.__graph[parent] = sortedLst


    # at the mid point of graph building, prune bad paths.
    def __pruneMiddle(self):
        self.abPrune = ABPrune()
        self.abPrune.initGraph(copy.deepcopy(self.__graph),copy.deepcopy(self.__data))
        visited = []
        visited = self.abPrune.minimax(0)
        self.abPrune.getBestPlace()

        graphCopy = copy.deepcopy(self.__graph)
        for node in graphCopy:
            if node not in visited:
                del self.__graph[node]
                del self.__data[node]
                del self.__matrixState[node]
            else:
                # remove child references
                for child in graphCopy[node]:
                    if child not in visited:
                        self.__graph[node].remove(child)
        return


    # performs an inorder traversal to visit all leaves.
    # once at the leaves, calls deepmovebulder to complete the graph to maxDepth.
    def __buildToMax(self, curNode, curDepth):
        children = self.__graph[curNode]

        # if at leaf node
        if(len(children) == 0):

            matrix = self.__matrixState[curNode]
            path   = self.__data[curNode][8] # full path list
            self.__deepMoveBuilder(self.__maxDepth, curNode, curDepth, matrix, path)

        else:
            # recursive call to visit all nodes
            for child in children:
                self.__buildToMax(child, curDepth+1)


    # returns the x and y of the best move as
    # searched by abPrune
    def __getBestMove(self):
        self.abPrune.initGraph(copy.deepcopy(self.__graph),copy.deepcopy(self.__data))
        visited = self.abPrune.minimax(0)
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
        return chr(int(y) + 64)


    def __printGraph(self):
        print "Graph: "
        for node in self.__graph:
            print node, self.__graph[node]


    def __printData(self):
        print "Data: "
        for node in self.__data:
            print node, self.__data[node]
