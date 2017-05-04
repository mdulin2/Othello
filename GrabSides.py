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
        self.__oppToken = oppToken

    #The upper call for all of the functions. Gets the scoring scenarios
    def RunCheck(self,matrix):
        score = 0
        count = 0
        if(matrix[1][3] != '-' or matrix[1][6] != '-'):
            score = self.__moveUpTop(matrix,0)
            if(score > 0):
                count+=1
            topLeftScore = self.__moveUpTop(matrix,1)
            if(topLeftScore > 0):
                count+=1
            score += self.__moveUpTop(matrix,1)

        if(matrix[8][3] != '-' or matrix[8][6] != '-'):
            score = self.__moveUpBottom(matrix,0)
            score+= self.__moveUpBottom(matrix,1)
        return score,count


    ##################
    #PRIVATE
    #################


    #The game needs to capitalize on a few scenarios. Needs to be hard coded!
    def __moveUpTop(self,matrix,sectionType):
        count = 0
        #left to right
        if(matrix[1][1] == '-' and sectionType == 0 and self.rules.isLegalMove(1,7,matrix,self.__oppToken) == False):
            if(matrix[1][3] == self.__myToken):
                for i in range(3,8):
                    if(matrix[1][i] == self.__myToken):
                        count+=1
                    elif(matrix[1][i] == self.__oppToken):
                        return 0
                if(count >=3):
                    if(matrix[1][8] == '-'):
                        #guarenteed corner if this is true
                        return 1000
                    else:
                        return 100
                return 0
                    #fantastic move!
            if(matrix[1][3] == self.__oppToken):
                for i in range(4,8):
                    if(matrix[1][i] == self.__myToken):
                        count+=1
                    elif(matrix[1][i] == self.__oppToken):
                        return 0
                if(count >=3):
                    #guarenteed corner if this is true
                    return 1000

        #right to left
        if(matrix[1][8] == '-'  and sectionType == 1 and self.rules.isLegalMove(1,2,matrix,self.__oppToken) == False):
            if(matrix[1][6] == self.__myToken):
                for i in range(6,0,-1):
                    if(matrix[1][i] == self.__myToken):
                        count+=1
                    elif(matrix[1][i] == self.__oppToken):
                        return 0
                #this is legendary
                if(count >=3):
                    if(matrix[8][1] == '-'):
                        #guarenteed corner if this is true
                        return 1000
                    else:
                        return 100
                    #fantastic move!
            if(matrix[1][6] == self.__oppToken):
                for i in range(5,0,-1):
                    if(matrix[1][i] == self.__myToken):
                        count+=1
                    elif(matrix[1][i] == self.__oppToken):
                        return 0
                if(count >= 3):
                        #guarenteed corner if this is true
                    return 1000
                    #fantastic move!
        return 0

    #The game needs to capitalize on a few scenarios. Needs to be hard coded!
    def __moveUpBottom(self,matrix,sectionType):
        count = 0
        #left to right
        if(matrix[8][1] == '-' and sectionType == 0 and self.rules.isLegalMove(8,7,matrix,self.__oppToken) == False):
            if(matrix[8][3] == self.__myToken):
                for i in range(3,8):
                    if(matrix[8][i] == self.__myToken):
                        count+=1
                    elif(matrix[8][i] == self.__oppToken):
                        return 0
                if(count >=3):
                    if(matrix[8][8] == '-'):
                        #guarenteed corner if this is true
                        return 1000
                    else:
                        return 100
                return 0
                    #fantastic move!

            elif(matrix[8][3] == self.__oppToken):
                for i in range(4,8):
                    if(matrix[8][i] == self.__myToken):
                        count+=1
                    elif(matrix[8][i] == self.__oppToken):
                        return 0
                if(count >=3):
                    #guarenteed corner if this is true
                    return 1000

        #right to left
        if(matrix[8][8] == '-' and sectionType == 1 and self.rules.isLegalMove(8,2,matrix,self.__oppToken) == False):
            if(matrix[8][6] == self.__myToken):
                for i in range(6,0,-1):
                    if(matrix[8][i] == self.__myToken):
                        count+=1
                    elif(matrix[8][i] == self.__oppToken):
                        return 0
                #this is legendary
                if(count >=3):
                    if(matrix[8][8] == '-'):
                        #guarenteed corner if this is true
                        return 1000
                    else:
                        return 100
                    #fantastic move!
            elif(matrix[8][6] == self.__oppToken):
                for i in range(5,0,-1):
                    if(matrix[8][i] == self.__myToken):
                        count+=1
                    elif(matrix[8][i] == self.__oppToken):
                        return 0
                if(count >= 3):
                    #guarenteed corner if this is true
                    return 1000
                    #fantastic move!
        return 0

    def __moveUpRight(self,matrix,sectionType):
        pass
