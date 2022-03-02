# ConnectM README
## Authors: Eric DiGioacchino & Nash Henry

### Dependencies
This program makes use of one third-party dependency - Numpy

`pip install numpy`

or

`conda install numpy`

### Running the program
To ensure this program reaches it's full potential, it needs to be run in a maintainable environment like Anaconda.

To start the game you can run the following command

`python connectM.py N M P`

or

`python3 connectM.py N M P`

N is the amount of rows and columns the player wishes for it to have, M is the win condition. A user needs to have M in a row to win.
It will create a board of **N x N**.
P is who you want to play first.
0 means the robot will play first and 1 or 'h' means that you the player will play first. Any number other input will result in the robot taking the first turn.

### Features
Right now you can only play against the robot since the focus of the project was programming an AI.
The game is verbose; so for each move, robot or player, the board will be printed out.
There are three types of end game. First being that the robot wins.Second being that the player wins. Lastly being that it is a tie game. For each of these end games a message will be displayed after the last move is made showing the final state and which end game has been reached.
