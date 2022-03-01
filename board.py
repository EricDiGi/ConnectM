import itertools as itt
import numpy as np
import os, sys

class Board:
    users = ["Robot","Human"] #Chips
    def __init__(self, first):
        self.players = [self.users[first], self.users[first-1]] # what chip goes first
        self.grid = np.full((int(os.environ['N']),int(os.environ['N'])), 0) # make the board
    
    def getRobot(self):
        return self.players.index("Robot")
    
    def robotReadable(self):
        return self.grid.copy()
    
    def getTurn(self,turn):
        return self.players[turn]

    # drop piece and let it fall till it collides
    def addPiece(self, col, piece):
        temp = self.grid.T
        if np.count_nonzero(temp[col]) == int(os.environ['N']):
            return -1
        for i,x in enumerate(temp[col]):
            if(x != 0):
                temp[col][i-1] = piece
                return
        temp[col][-1] = piece

    # self explanitory
    def printBoard(self):
      chips = [" ","X","O"]
      [print(" ",i,"", end='') for i in range(int(os.environ['N']))]
      print()
      for i in self.grid:
        print(''.join(["+---" for j in range(int(os.environ['N']))]) + "+")
        for j in i:
            print("| "+chips[j],"", end="")
        print("|\n", end="")
      print(''.join(["+---" for j in range(int(os.environ['N']))]) + "+")
    
    #check list for group of size M+
    def hasWinner(self, result):
        for player, value in result:
            if player != 0 and value >= int(os.environ['M']):
                print("Player %s wins!"%(self.players[player-1]))
                return True

    # Look up down left right and diagonally for a win state
    def gameComplete(self):
        # group by row
        for i in self.grid:
            result = [(n, sum(1 for n in group)) for n, group in itt.groupby(i)]
            if self.hasWinner(result):
                return True
        # group by column
        for i in self.grid.T:
            result = [(n, sum(1 for n in group)) for n, group in itt.groupby(i)]
            if self.hasWinner(result):
                return True
        # group by diagonal
        for y in range(int(os.environ['N'])):
            for x in range(int(os.environ['N'])):
                submatrixUp = self.grid[y:][x:]
                # TL -> BR
                result = [(n, sum(1 for n in group)) for n, group in itt.groupby(submatrixUp.diagonal())]
                if self.hasWinner(result):
                    return True
                # BL -> TR
                result = [(n, sum(1 for n in group)) for n, group in itt.groupby(np.flip(submatrixUp,0).diagonal())]
                if self.hasWinner(result):
                    return True
                submatrixDown = self.grid[y:][x:].T
                # TL -> BR
                result = [(n, sum(1 for n in group)) for n, group in itt.groupby(submatrixDown.diagonal())]
                if self.hasWinner(result):
                    return True
                # BL -> TR
                result = [(n, sum(1 for n in group)) for n, group in itt.groupby(np.flip(submatrixDown,1).diagonal())]
                if self.hasWinner(result):
                    return True
                
    # board is full when there are no more 0s
    def isFull(self):
        return (np.count_nonzero(self.grid==0) == 0)
