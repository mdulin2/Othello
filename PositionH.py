from GrabSides import GrabSides

#################
#Needs some major work done to it!!!
#Playing on wedges, giving up corners is terrible.
#This needs to be much better
##################

#This calculates the values of being on specific spots on the board
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
        myTotalScore,oppTotalScore,myChips,oppChips = self.__getPositionFactor(matrix,path)
        #altScore = self.alterations(matrix)
        myTotalScore =  myTotalScore / float(myChips * 44.675 * 4)
        oppTotalScore = oppTotalScore / float(oppChips * 44.675)
        finalScore = (myTotalScore / float(oppTotalScore))
        finalScore / (float(15))
        return finalScore

    #Gets the information about playing the corners poorly
    def alterations(self,matrix):
        total = 0
        total += self.__cornerH(matrix)
        myX,oppX = self.__XsqaureH(matrix)
        total+= myX and oppX
        total+= (self.__WedgeSquareH(matrix)*1000)
        total*=15
        return total


    ######################
    #PRIVATE
    ######################


    # position factor judges the position the AI is in. Analyzes
    # corners, edges. How to judge against bad spaces? Cannot get this to work the way I want!
    def __getPositionFactor(self, matrix,path):
        myTotalScore = 0
        oppTotalScore = 0
        myCount = 0
        oppCount = 1
        turnCount = self.__getMovedPlayed(matrix)
        for i in range(1,9):
            for j in range(1,9):
                if(matrix[i][j] == self.__myToken):
                    value = self.__positionScores[i-1][j-1]
                    myCount+=1
                    if (value > 90):
                        myTotalScore += 600
                    #might need to alter this in order to check if the rest is okay
                    elif(self.__isViable(path,i,j,matrix)):
                        myTotalScore += 200
                    elif(self.__isWedgeSquare(i,j,matrix,self.__myToken)):
                        #print "wedge at", i,j
                        myTotalScore = myTotalScore -800
                    elif(value < 11):
                        #need to really hate on this
                        myTotalScore = myTotalScore - 200
                    else:
                        myTotalScore+=value

                elif(matrix[i][j] == self.__oppToken):
                    value = self.__positionScores[i-1][j-1]
                    oppCount +=1
                    if (value > 90):
                        oppTotalScore += 800
                    elif(self.__isViable(path,i,j,matrix)):
                        oppTotalScore += 300
                    elif(self.__isWedgeSquare(i,j,matrix,self.__myToken)):
                        oppTotalScore = oppTotalScore - 200
                    #elif not sure if I want to check for the Xsquares or not
                    else:
                        oppTotalScore+=value
        if(oppTotalScore <= 0):
            oppTotalScore = 1
        #print oppCount
        #this could be better, for sure. Might just move it into the GrabSides file
        #countX = self.GrabSides.RunCheck(matrix)
        #if(value > 0):
            #totalScore +=3000


        return myTotalScore,oppTotalScore,myCount,oppCount

    #Discusses how many corners have been grabbed by each player;
    #The heuristic got the corner; need to make strict
    def __cornerH(self,matrix):
        myScore, oppScore = self.__getCorners(matrix)
        if(myScore == 4):
            return 100
        elif(myScore == oppScore and myScore == 0):
            return 0
        elif(myScore == 0 and oppScore == 1):
            return -1000
        elif(myScore == 0 and oppScore == 2):
            return -2000
        elif(myScore == 0 and oppScore == 3):
            return -3000
        elif(oppScore == 4):
            return -4000
        elif(myScore == 1 and oppScore == 0):
            return 40
        elif(myScore == 1 and oppScore == 1):
            return -40
        elif(myScore == 1 and oppScore == 2):
            return -70
        elif(myScore == 1 and oppScore == 3):
            return -50
        elif(myScore == 2 and oppScore == 0):
            return 50
        elif(myScore == 2 and oppScore == 1):
            return 10
        elif(myScore == 2 and oppScore == 2):
            return -30
        elif(myScore == 3 and oppScore == 1):
            return 80
        else:
            return 0
            print "What else is there?", myScore,oppScore


    #Gets the heuristic value of the other player and current player
    #having bad squares during the game
    def __XsqaureH(self,matrix):
        myScore = self.__XSquareCount(matrix,self.__myToken)
        oppScore = self.__XSquareCount(matrix,self.__oppToken)
        myScore = 12 / float(myScore + 1)
        oppScore = (oppScore / float(12)) * 4

        return myScore,oppScore


    #The heuristic for the worst square in the game!
    #Don't want this; want to force other players to take these
    def __WedgeSquareH(self,matrix):
        myWedge = self.__countWedgeSquares(matrix,self.__myToken)
        oppWedge = self.__countWedgeSquares(matrix,self.__oppToken)
        if(myWedge == 0 and oppWedge == 0):
            return 0
        elif(myWedge == 0 and oppWedge == 1):
            return 10
        elif(myWedge == 0 and oppWedge == 2):
            return 20
        elif(myWedge == 0 and oppWedge == 3):
            return 30
        elif(myWedge == 0 and oppWedge == 4):
            return 40
        elif(myWedge == 1 and oppWedge == 0):
            return -40
        elif(myWedge == 1 and oppWedge == 1):
            return -50
        elif(myWedge == 1 and oppWedge == 2):
            return -30
        elif(myWedge == 1 and oppWedge == 3):
            return 10
        elif(myWedge == 2 and oppWedge == 0):
            return -70
        elif(myWedge == 2 and oppWedge == 1):
            return -50
        elif(myWedge == 2 and oppWedge == 2):
            return -30
        elif(myWedge == 3 and oppWedge == 0):
            return -100
        elif(myWedge == 3 and oppWedge == 1):
            return -80
        elif(myWedge == 4):
            return -120
        elif(oppWedge == 4):
            return 60
        else:
            print "What else is here?", myWedge,oppWedge
            return 0

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

    #Gets if the current play is a wedge move
    def __isWedgeSquare(self,i,j,matrix,Token):
        if(i == 2 and j == 2):
            if(matrix[1][1] != Token):
                if(matrix[2][2] == Token):
                    return True
        elif(i == 2 and j == 7):
            if(matrix[1][8] != Token):
                if(matrix[2][7] == Token):
                    return True
        elif(i == 7 and j == 2):
            if(matrix[8][1] != Token):
                if(matrix[7][2] == Token):
                    return True
        elif(i == 7 and j == 7 ):
            if(matrix[8][8] != Token):
                if(matrix[7][7] == Token):
                    return True
        return False
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
