from rules import Rules

class OthelloAI:

    # initialize the AI to its proper token
    def __init__(self, AItoken):
        self.rules = Rules()
        self.__myToken = AItoken

    # pulls the matrix from board and chooses a move to make.
    # returns chosen move as two integers: x, y.
    def makeMove(self, board):
        matrix = board.matrixB

        x,y = self.__simpleMove(matrix)
        y = self.__changeY(y)
        return x, y


    # loops through the matrix and picks the first move that is available.
    # returns x and y coordinates of move to make.
    def __simpleMove(self, matrix):
        for i in range(1,9):
            for j in range(1,9):
                if(self.rules.isLegalMove(i, j, matrix, self.__myToken)):
                    return i,j
        # not sure how we will handle no moves available yet
        print("no moves available to AI")


    # convert Y into its proper board form (character)
    def __changeY(self,y):
        return chr(y + 64)
