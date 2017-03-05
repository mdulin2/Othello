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

        while(not self.board.isFull()):

            if(self.__player == self.__turn.getTurn()):
                self.__playerTurn()
            else:
                self.__playAIturn()

            self.board.printBoard()


    ############################
            #PRIVATE
    ############################

    def __getInit(self):
        board = Board('w','B', 'W', 'B')
        board.printBoard()
        self.__player, self.__AI = self.__setPlayers()
        if(self.__player == 'B'):
            board = Board(self.__player, self.__AI, 'W', 'B')
        return board


    # asks the user who will be white or black between the player and the AI
    # repeats unitl proper input
    def __setPlayers(self):
        player = raw_input("Choose token for Player (W/B): ")

        if(player == 'W' or player == 'w'):
            print("Player set to be: 'W'")
            print("AI set to be: 'B'")
            return 'W', 'B'
        elif(player == 'B' or player == 'b'):
            print("Player set to be: 'B'")
            print("AI set to be: 'W'")
            return 'B', 'W'
        else:
            self.__setPlayers()



    # logic for a player's turn using terminal inputs.
    def __playerTurn(self):
        print("Player's turn to move.")
        x = raw_input("Enter X coordinate: ")
        y = raw_input("Enter Y coordinate: ")
        self.board.move(x,y)

        self.__turn.flip()


    # logic for calling the AI to make a move.
    def __playAIturn(self):
        self.__AIplayed == False
        print("AI's turn to move.")
        x = raw_input("Enter X coordinate: ")
        y = raw_input("Enter Y coordinate: ")
        self.board.move(x,y)
        '''
        timeThread = threading.Thread(target=self.__timer, args=())
        AIThread = threading.Thread(target=self.__runAI, args=())

        timeThread.start()
        AIThread.start()

        timeThread.join()
        AIThread.join()
        '''
        self.__turn.flip()


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
