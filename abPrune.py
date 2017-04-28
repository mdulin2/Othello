'''
Team Leader: Jacob Krantz
Developer 1: Max Dulin
Assignment:  Alpha-Beta pruning (asgn12)
Date:        4/18/17

How to run:
    - enter on command line
        'python abPrune.py'
    - result
        nodes visited are printed out to console

notation supplement
    - names for nodes that started with only values:
        a: 42
        b: 2
        c: 3
        d: 5
        e: 100
        f: 0
        g: 2 (child of T)
        h: 1
        i: 9
        j: 11
'''

class ABPrune:

    # initialize the graph to De Palma's pruning example
    def __init__(self):
        self.__data = {}
        self.__graph = {}
        #self.initGraph()
        self.__inorderVisit = []

    # set to example 4 of AB Pruning notes
    def initGraph(self,graphIn,dataIn):
        self.__graph = graphIn

        '''
        self.__graph = {'C': ['A','D','E'],
                        'A': ['P','B'],
                        'D': ['R','a'],
                        'E': ['T','V'],
                        'P': ['b','c'],
                        'B': ['d','e'],
                        'R': ['f'],
                        'T': ['g','h'],
                        'V': ['i','j'],
                        'a': [],
                        'b': [],
                        'c': [],
                        'd': [],
                        'e': [],
                        'f': [],
                        'g': [],
                        'h': [],
                        'i': [],
                        'j': []}
        '''

        self.__data = dataIn
        '''
        sA = -999999
        sB = 999999
        # {node name: node data}
        # node data = [value, isMax, parentChar, alpha, beta]
        self.__data =  {'C': [sA,  True, "none", sA, sB],
                        'A': [sB,  False, 'C', sA, sB],
                        'D': [sB,  False, 'C', sA, sB],
                        'E': [sB,  False, 'C', sA, sB],
                        'P': [sA,  True,  'A', sA, sB],
                        'B': [sA,  True,  'A', sA, sB],
                        'R': [sA,  True,  'D', sA, sB],
                        'T': [sA,  True,  'E', sA, sB],
                        'V': [sA,  True,  'E', sA, sB],
                        'a': [42,  True,  'D', sA, sB],
                        'b': [2,   False, 'P', sA, sB],
                        'c': [3,   False, 'P', sA, sB],
                        'd': [5,   False, 'B', sA, sB],
                        'e': [100, False, 'B', sA, sB],
                        'f': [0,   False, 'R', sA, sB],
                        'g': [2,   False, 'T', sA, sB],
                        'h': [1,   False, 'T', sA, sB],
                        'i': [9,   False, 'V', sA, sB],
                        'j': [11,  False, 'V', sA, sB]}
        '''
        
    #node data = [value, isMax, parentChar, alpha, beta,x,y,token]
    # performs a depth-first traversal and returns the visited list
    # start is the node name to start with
    def depth_first(self,start):
        visited = []
        stack = [start]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.append(vertex)
                children = self.__graph[vertex]
                children.reverse()
                for item in children:
                    if item not in visited:
                        stack.append(item)
        return visited


    # performs an in-order taversal and returns the visited list
    def minimax(self,start):
        children = self.__graph[start]
        nodeValue = self.__data[start][0]
        isMax     = self.__data[start][1]
        par       = self.__data[start][2]
        x         = self.__data[start][5]
        y         = self.__data[start][6]

        if par != "none":
            parAlpha =  self.__data[par][3]
            parBeta =   self.__data[par][4]

        # if is leaf node
        if len(children) == 0:
            self.__inorderVisit.append(start)

            if(isMax): # if is max
                if parBeta > nodeValue:
                    self.__data[par][0] = nodeValue # set par value
                    self.__data[par][4] = nodeValue # set par beta
                   
                    self.__data[par][5] = x
                    self.__data[par][6] = y

            else: # is min
                if parAlpha < nodeValue:
                    self.__data[par][0] = nodeValue # set par value
                    self.__data[par][3] = nodeValue # set par alpha
                    self.__data[par][5] = x
                    self.__data[par][6] = y
            return

        else:
            # visit left first
            self.minimax(children[0])


            # visit itself
            self.__inorderVisit.append(start)
            #print "in node " + start, "value: ", self.__data[start][0], "beta: ", self.__data[start][4]


            # visit all the rest if not pruned
            if len(children) > 1:

                for i in range(1,len(children)):
                    # bubble down alpha and beta
                    self.__data[children[i]][3] = self.__data[start][3] # child alpha set to node alpha
                    self.__data[children[i]][4] = self.__data[start][4] # child beta set to node beta

                    if isMax:
                        if(self.__data[start][0] < self.__data[start][4]):  # if node value < node beta
                            self.minimax(children[i])

                    else: # is min
                        if(self.__data[start][0] > self.__data[start][3]):  # if node value > node alpha
                            self.minimax(children[i])

            # bubble up the bumbershoot
            nodeValue = self.__data[start][0]
            if par != "none":
                if(isMax): # if is max
                    if parBeta > nodeValue:
                        self.__data[par][0] = nodeValue # set par value
                        self.__data[par][4] = nodeValue # set par beta
                        self.__data[par][5] = x
                        self.__data[par][6] = y

                else: # is min
                    if parAlpha < nodeValue:
                        self.__data[par][0] = nodeValue # set par value
                        self.__data[par][3] = nodeValue # set par alpha
                        self.__data[par][5] = x
                        self.__data[par][6] = y

        return self.__inorderVisit


    def checkValue(self, node):
        return self.__data[node][0]

    #after the spanning of the tree has been done this returns the best x and y value to 
    #place on the board
    def getBestPlace(self):
        return self.__data[0][5],self.__data[0][6]

if(__name__ == "__main__"):
    test = ABPrune()
    print test.minimax('C')
