import numpy as np
from Board import Board


class Game:

    def __init__(self):
        player, AI = self.__setPlayers()
        startConfig = self.__setConfig()
        startTurn = self.__setStartTurn()
        board = Board(player, AI, startConfig, startTurn)
        board.printBoard()

    def playGame(self):
        pass

    ############################
            #PRIVATE
    ############################

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


    # gets the decision of original board configuration from the user.
    # repeats until proper input
    def __setConfig(self):
        topLeft = raw_input("who starts upper left (W/B)? ")

        if(topLeft == 'W' or topLeft == 'w'):
            return 'W'
        elif(topLeft == 'B' or topLeft == 'b'):
            return 'b'
        else:
            self.__setConfig()

    # gets the decision of who plays first from the user
    # repeats until proper input
    def __setStartTurn(self):
        start = raw_input("Which token gets to play first (W/B)? ")

        if(start == 'W' or start == 'w'):
            return 'W'
        elif(start == 'B' or start == 'b'):
            return 'B'
        else:
            self.__setStartTurn()

if(__name__ == "__main__"):
    game = Game()
    game.playGame()
