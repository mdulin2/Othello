from rules import Rules
#This is a specific way to grab the sides of the board. The issue is that the
#functions are gigantic. So, I thought they needed their own file

#If the game is in the form:
#       [--WBBB--] on the board in any direction of the game,
#where the opponent can't immediatly make a move on 2G in the case above,
#then it's a free XSquare that can't be hoped. If they try to hop the turn after
# then the other team will be giving up a free corner. This situation comes up a ton
#so I thought it should be hard coded in here.
class GrabSides:

############
#Notes:::::::::::::
#might need to check if the other player has played in that spot already.
#Could have played in that area already!
#Needs to be a little more touched up!
#############
    def __init__(self,myToken,oppToken):
        self.rules = Rules()
        self.__myToken = myToken
        self.__myToken = oppToken

    #The upper call for all of the functions. Gets the scoring scenarios
    def RunCheck(self,matrix,player,opposingPlayer):
        score = 0
        count = 0
        if(matrix[1][3] != '-' or matrix[1][6] != '-'):
            score = self.__moveUpTop(matrix,0,player,opposingPlayer)
            if(score > 0):
                count+=1
            topLeftScore = self.__moveUpTop(matrix,1,player,opposingPlayer)
            if(topLeftScore > 0):
                count+=1
            score += self.__moveUpTop(matrix,1,player,opposingPlayer)

        if(matrix[8][3] != '-' or matrix[8][6] != '-'):
            score = self.__moveUpBottom(matrix,0,player,opposingPlayer)
            score+= self.__moveUpBottom(matrix,1,player,opposingPlayer)
        return score,count


    ##################
    #PRIVATE
    #################


    #The game needs to capitalize on a few scenarios. Needs to be hard coded!
    def __moveUpTop(self,matrix,sectionType,player,opposingPlayer):
        count = 0
        blank = 0
        #left to right
        if(matrix[1][1] != opposingPlayer and matrix[1][8] != opposingPlayer):
            for i in range(2,8):
                if(matrix[1][i] == opposingPlayer):
                    return 0
                elif(matrix[1][i] == '-'):
                    blank+=1
                elif(matrix[1][i] == player):
                    count+=1
                else:
                    print "error?"
                #if the space is empty besides my pieces
                if(blank == 6):
                    return 1000
                #Some combination of my user pieces
                else:
                    return 10000
        return 0

    #The game needs to capitalize on a few scenarios. Needs to be hard coded!
    def __moveUpBottom(self,matrix,sectionType,player,opposingPlayer):
        count = 0
        blank = 0
        if(matrix[8][1] != opposingPlayer and matrix[8][8] != opposingPlayer):
            for i in range(2,8):
                if(matrix[8][i] == opposingPlayer):
                    return 0
                elif(matrix[8][i] == '-'):
                    blank+=1
                elif(matrix[8][i] == player):
                    count+=1
                else:
                    print "error?"

                #if the space is empty besides my pieces
                if(blank == 6):
                    return 1000
                #Some combination of my user pieces
                else:
                    return 10000


        return 0

    #checks the left side of the board for the sides
    def __moveUpLeft(self,matrix,sectionType,player,opposingPlayer):
        count = 0
        blank = 0
        if(matrix[1][1] != opposingPlayer and matrix[8][1] != opposingPlayer):
            for i in range(2,8):
                if(matrix[i][1] == opposingPlayer):
                    return 0
                elif(matrix[i][1] == '-'):
                    blank+=1
                elif(matrix[i][1] == player):
                    count+=1
                else:
                    print "error?"

                #if the space is empty besides my pieces
                if(blank == 6):
                    return 1000
                #Some combination of my user pieces
                else:
                    return 10000
        return 0

    #checks the right side of the board for the sides
    def __moveUpRight(self,matrix,sectionType,player,opposingPlayer):
        count = 0
        blank = 0
        if(matrix[1][8] != opposingPlayer and matrix[8][8] != opposingPlayer):
            for i in range(2,8):
                if(matrix[i][8] == opposingPlayer):
                    return 0
                elif(matrix[i][8] == '-'):
                    blank+=1
                elif(matrix[i][8] == player):
                    count+=1
                else:
                    print "error?"

                #if the space is empty besides my pieces
                if(blank == 6):
                    return 1000
                #Some combination of my user pieces
                else:
                    return 10000
        return 0
