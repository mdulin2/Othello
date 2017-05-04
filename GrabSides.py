
#This is a specific way to grab the sides of the board. The issue is that the
#functions are gigantic. So, I thought they needed their own file
class GrabSides:

    def __init__(self,myToken,oppToken):
        self.__myToken = myToken
        self.__oppToken = oppToken

    #The upper call for all of the functions
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
        if(matrix[1][1] == '-' and sectionType == 0):

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


                #might need to add more stuff here after a while for cases with the
                #the pieces on the edges
        #right to left
        if(matrix[1][8] == '-'  and sectionType == 1):


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
        if(matrix[8][1] == '-' and sectionType == 0):

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


                #might need to add more stuff here after a while for cases with the
                #the pieces on the edges
        #right to left
        if(matrix[8][8] == '-' and sectionType == 1):

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
