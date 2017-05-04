from GrabSides import GrabSides

#This calculates the values of being on specific spots on the board
#getScore should
class PositionH:

    def __init__(self,myToken,oppToken,positionScore):
        self.__myToken = myToken
        self.__oppToken = oppToken
        self.__positionScores = positionScore
        self.GrabSides = GrabSides(myToken,oppToken)
        self.__depth = 3

    #sets the depth of the Heuristic
    def setDepth(self,num):
        self.__depth = num

    #returns the position function score
    def getScore(self,matrix,path):
        turnCount = self.__getMovedPlayed(matrix)
        PositionScore = self.__getPositionFactor(matrix,path)
        altScore = self.alterations(matrix)
        if(altScore > 0):
            finalScore = PositionScore / float(turnCount * 44.675 * 4)
        else:
            finalScore = PositionScore /float(turnCount *1000)
        return finalScore


    def alterations(self,matrix):
        spotsScore = self.__cornerH(matrix)

        return spotsScore
    ######################
    #PRIVATE
    ######################


    # position factor judges the position the AI is in. Analyzes
    # corners, edges. How to judge against bad spaces? Cannot get this to work the way I want!
    def __getPositionFactor(self, matrix,path):
        totalScore = 0
        count = 0
        turnCount = self.__getMovedPlayed(matrix)
        for i in range(1,9):
            for j in range(1,9):
                #self.__positionHelper(matrix,i,j)
                if(matrix[i][j] == self.__myToken):
                    count+=1
                    value = self.__positionScores[i-1][j-1]

                    if (value > 90):
                        totalScore += 1050
                    elif(self.__isViable(path,i,j,matrix)):
                        totalScore += 100
                    elif(value < 11):
                        #need to really hate on this
                        totalScore = totalScore -1000
                    else:
                        totalScore+=value

        #this could be better, for sure. Might just move it into the GrabSides file
        value,countX = self.GrabSides.RunCheck(matrix)
        if(value > 0 and countX <= count):
            totalScore += countX *1000
        normalized = totalScore
        #this could be more precise(wedgesquares and Xsquare).
        #if(self.countWedgeSquares(matrix, self.__oppToken) > self.countWedgeSquares(matrix,self.__myToken)):
            #totalScore += 500

        #if(self.XSquareCount(matrix,self.__oppToken) > self.XSquareCount(matrix,self.__myToken)):
            #totalScore += 300

        #if(totalScore <= 0):
            #normalized = 1 / float(44.6875 * turnCount * 10000)
        #else:
            #normalized = totalScore*8 / float(44.6875 * count * 5)

            #print totalScore
            #print normalized
        return normalized

    #Discusses how many corners have been grabbed by each player;
    #The heuristic got the corner; need to make strict
    def __cornerH(self,matrix):
        myScore, oppScore = self.__getCorners(matrix)
        if(myScore == 4):
            return 12
        elif(myScore == oppScore and myScore == 0 ):
            return 0
        elif(myScore == 0 and oppScore == 1):
            return -5
        elif(myScore == 0 and oppScore == 2):
            return -8
        elif(myScore == 0 and oppScore == 3):
            return -12
        elif(oppScore == 4):
            return -15
        elif(myScore == 1 and oppScore == 0):
            return 3
        elif(myScore == 1 and oppScore == 1):
            return -2
        elif(myScore == 1 and oppScore == 2):
            return -5
        elif(myScore == 1 and oppScore == 3):
            return -10
        elif(myScore == 2 and oppScore == 0):
            return 8
        elif(myScore == 2 and oppScore == 1):
            return 3
        elif(myScore == 2 and oppScore == 2):
            return -2
        elif(myScore == 3 and oppScore == 1):
            return 10
        else:
            return 0
            print "What else is there?", myScore,oppScore


    #Gets the heuristic value of the other player and current player
    #having bad squares during the game
    def __XsqaureH(self,matrix):
        myScore = self.__XsqaureH(matrix,self.__myToken)
        oppWedge = self.__XsqaureH(matrix,self.__oppToken)


    #The heuristic for the worst square in the game!
    #Don't want this; want to force other players to take these
    def __WedgeSquareH(self,matrix):
        myWedge = self.__countWedgeSquares(matrix,self.__myToken)
        oppWedge = self.__countWedgeSquares(matrix,self.__oppToken)

    #marks whether a move is viable based on the standards of having a corner played already
    def __isViable(self,path,i,j,matrix):

        if((i ==2 and j ==1)or (i ==2 and j ==2)or (i ==1 and j ==2)):
            #if my token is the corner
            if(matrix[1][1] == self.__myToken and len(path) == self.__depth):
                #if not in path then just this flip is good; it will flip others around it
                if([1,1] in path and [i,j] in path):

                    #if contains the Xsquare as a prediction, then don't use it
                    #or if that's the move choosen
                    if(path.index([1,1]) < path.index([i,j])):
                        return True
                    else:
                        return False
                #if the matrix has the corner but doesn't have the other pieces in the path.
                #Good
                else:
                    return True
            else:
                return False

        elif(((i == 1 and j == 7) or (i ==2 and j ==7)or (i ==2 and j ==8))):
            if(matrix[1][8] == self.__myToken and len(path) == self.__depth):
                if([1,8] in path and [i,j] in path):
                    if(path.index([1,8]) < path.index([i,j])):
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                return False
        elif(((i == 7 and j == 1) or (i ==7 and j ==2)or (i ==8 and j ==2))):
            if(matrix[8][1] == self.__myToken and len(path) == self.__depth):

                if([8,1] in path and [i,j] in path):
                    if(path.index([8,1]) < path.index([i,j])):
                        return True
                    else:
                        return False
                else:
                    return True
            return False
        elif(((i == 8 and j == 7) or (i == 7 and j ==8)or (i ==7 and j ==7))):
            if(matrix[8][8] == self.__myToken and len(path) == self.__depth):
                if([8,8] in path and [i,j] in path):
                    if(path.index([8,8]) < path.index([i,j])):
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                return False

        return False

    #Gets the amount of moves that are on the diagonal move from the
    #The corner.
    def __countWedgeSquares(self,matrix,Token):
        count = 0
        if(matrix[1][1] != Token):
            if(matrix[2][2] == Token):
                count+=1

        if(matrix[1][8] != Token):
            if(matrix[2][7] == Token):
                count+=1

        if(matrix[8][1] != Token):
            if(matrix[7][2] == Token):
                count+=1

        if(matrix[8][8] != Token):
            if(matrix[8][7] == Token):
                count+=1
        return count

    #gets the number of bad plays on the board; spots around the corner when
    # a corner move has not been played
    #might want to base this off of the first board state of the iteration
    def __XSquareCount(self,matrix,Token):
        count = 0
        if(matrix[1][1] != Token):
            if(matrix[1][2] == Token):
                count+=1
            if(matrix[2][1] == Token):
                count+=1
            if(matrix[2][2] == Token):
                count+=1

        if(matrix[1][8] != Token):
            if(matrix[1][7] == Token):
                count+=1
            if(matrix[2][7] == Token):
                count+=1
            if(matrix[2][8] == Token):
                count+=1

        if(matrix[8][1] != Token):
            if(matrix[7][1] == Token):
                count+=1
            if(matrix[7][2] == Token):
                count+=1
            if(matrix[8][2] == Token):
                count+=1

        if(matrix[8][8] != Token):
            if(matrix[7][8] == Token):
                count+=1
            if(matrix[8][7] == Token):
                count+=1
            if(matrix[7][7] == Token):
                count+=1
        return count


    # counts all played turns on the board by looking for occupied spaces.
    def __getMovedPlayed(self, matrix):
        movesPlayed = 0
        for i in range(1,9):
            for j in range(1,9):
                if(matrix[i][j] != '-'):
                    movesPlayed += 1
        return movesPlayed

    #gets the amount of corners for each player
    def __getCorners(self,matrix):
        myCorner = 0
        oppCorner = 0
        if(matrix[1][1] == self.__myToken):
            myCorner+=1
        if(matrix[1][1] == self.__oppToken):
            oppCorner+=1
        if(matrix[1][8] == self.__myToken):
            myCorner+=1
        if(matrix[1][8] == self.__oppToken):
            oppCorner+=1
        if(matrix[8][1] == self.__myToken):
            myCorner+=1
        if(matrix[8][1] == self.__oppToken):
            oppCorner+=1
        if(matrix[8][8] == self.__myToken):
            myCorner+=1
        if(matrix[8][8] == self.__oppToken):
            oppCorner+=1
        return myCorner, oppCorner

    #########################
    #In progress/ needs mucho work
    ##############################

    #resets the value on the position table if the corner has been taken by the user
    def __setPosition(self,matrix):

        '''
        #top left
        if(self.__myToken == matrix[1][1] and cornerArray[0] == True):
            #print "here!"
            self.__positionScores[0][1] = 70
            self.__positionScores[1][0] = 70
            self.__positionScores[1][1] = 65
            self.__positionScores[0][2] = 60
            self.__positionScores[2][0] = 60

        #top right
        if(self.__myToken == matrix[1][8] and cornerArray[1] == True):
            self.__positionScores[0][6] = 80
            self.__positionScores[1][7] = 65
            self.__positionScores[1][6] = 80
            self.__positionScores[0][5] = 65
            self.__positionScores[2][7] = 65

        #bottom left
        if(self.__myToken == matrix[8][1] and cornerArray[2] == True):
            self.__positionScores[6][0] = 80
            self.__positionScores[7][1] = 80
            self.__positionScores[6][1] = 65
            self.__positionScores[5][0] = 65
            self.__positionScores[7][2] = 80


        #bottom right
        if(self.__myToken == matrix[8][8] and cornerArray[3] == True):
            self.__positionScores[6][7] = 80
            self.__positionScores[6][6] = 65
            self.__positionScores[7][6] = 80
            self.__positionScores[5][7] = 65
            self.__positionScores[7][5] = 65
        '''
        return
