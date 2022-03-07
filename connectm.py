import itertools as itt
import numpy as np
import os, sys

from robot import Robot
from board import Board

def humanMove(turn):
    column = input("Column:")
    while(column == "" or int(column) > int(os.environ['N'])-1 or int(column) < 0 or B.addPiece(int(column), (turn%2)+1) == -1):
        print("Invlaid Move")
        column = input("Column:")

def robotMove(R, turn):
    column = R.run(B.robotReadable())
    print("Column: " + str(column))
    B.addPiece(column, (turn%2)+1)

if __name__ == "__main__":
    # program has correct number of arguments
    if(len(sys.argv) <= 3):
        print("Wrong number of command-line arguments")
        exit(0)
    os.environ['N'], os.environ['M'], os.environ['H'] = sys.argv[1:]
    print(os.environ['N'], os.environ['M'], os.environ['H'])

    #board is safe to build
    if((int(os.environ['M']) > int(os.environ['N'])-1) or (int(os.environ['N']) not in range(3,11)) ):
        print("Invalid Board, please try again...")
        exit(0)

    # we know who is starting
    first = 1 #human by default
    if(os.environ['H'].lower()[0] == "h" or int(os.environ['H']) == 1):
        print("Human plays first")
    else:
        first = 0
        print("Robot plays first")


    #Build the game space
    B = Board(first)
    R = Robot(B.getRobot())
    turn = 0

    # Play the game
    while(1):
        print("\n" + B.getTurn(turn%2))
        if B.getTurn((turn%2)) == "Human":
            humanMove(turn)
        else:
            robotMove(R, turn)
        
        B.printBoard()
        if (B.gameComplete() or B.isFull()):
            if B.isFull() and not B.gameComplete():
                print("Game is a draw!")
            break
        turn += 1