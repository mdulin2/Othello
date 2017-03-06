import numpy as np
from Board import Board
from Board import Turn
import threading
import time

'''
TODO max
'''

class Game:

    # initialize board conditions to game specifications.
    def __init__(self):
        self.__turn = Turn('B')
        self.__AIplayed = False
        self.__AIturnTime = 10      # in seconds
        self.__player = ''
        self.__AI = ''
        self.board = self.__getInit()


    # plays a standard game of Othello with an option to adjust the length
    # of a turn. Param: turnTime, seconds as an int.
    def playGame(self, turnTime):
        self.__AIturnTime = turnTime

        while(not self.board.isGameOver()):

            if(self.__player == self.__turn.getTurn()):
                print("Player's turn to move.")
                self.__playerTurn()
            else:
                print("AI's turn to move.")
                self.__playAIturn()

            self.__turn.flip()
            #***The print is happening in move with the parameters being correct
            #self.board.highLightPrint()


    ############################
            #PRIVATE
    ############################

    def __getInit(self):
        board = Board('w','B', 'W', 'B')
        board.printBoard()
        self.__setPlayers()
        if(self.__player == 'B'):
            board = Board(self.__player, self.__AI, 'W', 'B')
        return board


    # asks the user who will be white or black between the player and the AI
    # repeats unitl proper input
    def __setPlayers(self):
        player = ''
        while(not self.__validSetPlayers(player)):
            player = raw_input("Choose token for Player (W/B): ")

            self.__player = player
            if(player == 'W' or player == 'w'):
                print("Player set to be: 'W'")
                self.__AI = 'B'
                print("AI set to be: 'B'")
            elif(player == 'B' or player == 'b'):
                print("Player set to be: 'B'")
                self.__AI = 'W'
                print("AI set to be: 'W'")


    # checks input for setting the player tokens.
    # returns true for valid input.
    def __validSetPlayers(self, player):
        if(player == 'w' or player == 'W'):
            return True
        else:
            return (player == 'B' or player == 'b')


    # logic for a player's turn using terminal inputs.
    def __playerTurn(self):
        hasMoved = False
        while not hasMoved:
            try:
                x = int(raw_input("Enter X number: "))
                y = str(raw_input("Enter Y character: "))
                hasMoved = self.board.move(x,y)

            except:
                print "Bad inputs; please give a number and letter where it is asked"



    # logic for calling the AI to make a move. Temporarily is done
    # through user input.
    def __playAIturn(self):
        self.__AIplayed == False
        hasMoved = False
        while not hasMoved:
            try:
                x = int(raw_input("Enter X number: "))
                y = str(raw_input("Enter Y character: "))
                hasMoved = self.board.move(x,y)
            except:
                print "Bad inputs; please give a number and a letter where asked"
        '''
        timeThread = threading.Thread(target=self.__timer, args=())
        AIThread = threading.Thread(target=self.__runAI, args=())

        timeThread.start()
        AIThread.start()

        timeThread.join()
        AIThread.join()
        '''


    # counts down from 10, waiting for __AIplayed to be true.
    # if __AIplayed never evaluates to true, prints to terminal (currently).
    def __timer(self):
        print "AI timer:"
        for i in range(self.__AIturnTime, 0, -1):
            print i
            time.sleep(1)
            if(self.__AIplayed == True):
                return True
        print "AI did not play in time. "


    # temporary bot for an AI
    def __runAI(self):
        time.sleep(3)
        self.__AIplayed = True


# runs the base game of Othello
if(__name__ == "__main__"):
    game = Game()
    game.playGame(10)
