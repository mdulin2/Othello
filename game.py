import numpy as np
from Board import Board
from Board import Turn
from othelloAI import OthelloAI
import threading
import time
import sys
import copy
from random import randint

'''
TODO max
'''

class Game:
    #needs to have a few more beginning options for the game.
    # initialize board conditions to game specifications.
    def __init__(self):
        self.__turn = Turn('B')
        self.__AIplayed = False
        self.__isAIturn = False
        self.__stopTimer = False
        self.__AIturnTime = 10      # in seconds
        self.__player = ''
        self.__AItoken = ''
        self.board = self.__getInit()
        self.__AI = OthelloAI(self.__AItoken, self.__player)
        self.turnCount = 4 #60


    # plays a standard game of Othello with an option to adjust the length
    # of a turn. Param: turnTime, seconds as an int.
    def playGame(self, turnTime):
        self.__AIturnTime = turnTime

        # create thread for the AI timer
        self.timeThread = threading.Thread(target=self.__timer, args=())
        self.timeThread.start()

        while(not self.board.isGameOver()):

            if(self.__player == self.__turn.getTurn()):
                print("Player's turn to move.")
                self.__playerTurn()
            else:
                print("AI's turn to move.")
                self.__runAI()

            self.__confirmMove()
            self.__turn.flip()
            #***The print is in move with the parameters being correct
            #self.board.highLightPrint()
        # join threads and finish the game
        self.__endGame()


    ############################
            #PRIVATE
    ############################

    def __getInit(self):
        board = Board('w','B', 'W', 'B')
        board.printBoard()
        self.__setPlayers()
        if(self.__player == 'B'):
            board = Board(self.__player, self.__AItoken, 'W', 'B')
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
                self.__AItoken = 'B'
                print("AI set to be: 'B'")
            elif(player == 'B' or player == 'b'):
                print("Player set to be: 'B'")
                self.__AItoken = 'W'
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
                x = int(raw_input("Enter number: "))
                y = str(raw_input("Enter character: "))

                if(x > 8):
                    x = 999 # code for no moves
                self.board.getLegalMoves()
                hasMoved = self.board.move(x,y)

            except:
                print "Bad inputs; please give a number and letter where it is asked"


    # asks the user for move confirmation. In the event of a dispute,
    # the board gets set to the previous state, and the current turn gets
    # replayed.
    def __confirmMove(self):
        choice = raw_input("Confirm Move.\n'q' to quit, 'r' to revert board: ")
        if(choice == 'q'):
            self.__endGame()
        elif(choice == 'r'):
            print "Board set to prior state."
            self.board.revertBoard()
            self.board.printBoard()
            self.__turn.flip()


    # counts down from 10, waiting for __AIplayed to be true.
    # if __AIplayed never evaluates to true, prints to terminal (currently).
    def __timer(self):
        while(not self.__stopTimer):
            if(self.__isAIturn):
                self.__isAIturn = False
                print "AI timer:"
                for i in range(self.__AIturnTime, 0, -1):
                    print i
                    time.sleep(1)
                    if(i == 1):
                        print "AI did not play in time. "
                    if(self.__AIplayed == True):
                        break


    # bot for making AI moves
    def __runAI(self):
        self.__AIplayed = False    # starts timer
        self.__isAIturn = True

        x,y = self.__AI.makeMove(copy.deepcopy(self.board))
        if(x != 999):
            print("AI move: " + str(x) + " " + y)
        else:
            print("no moves available to AI")

        self.__AIplayed = True      # stops timer
        self.board.move(x,y)
        self.__isAIturn = False


    # finish game and join all threads
    def __endGame(self):
        self.__stopTimer = True
        self.timeThread.join()
        sys.exit()


# runs the base game of Othello
if(__name__ == "__main__"):
    game = Game()
    game.playGame(10)
