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

N is the annount of columns the player wishes for it to have and M is the anount of rows that the player wishes for it to have.
It will create a board of **N x M** using whatever values you give it and the win condition is connecting m number of pieces before the your oponent does.
P is who you want to play first.
0 means the robot will play first and 1 means that you the player will play first.

### Features
Right now you can only play aainst the robot since the focus of the project was programming an AI.
For each move the board of whatever size the user dictated will be printed out. This applies for both the robot and the players moves so you can see each individual state that the board has been in leading up to the end of the game.
There are three types of end game. First being that the robot wins.Second being that the player wins. Lastly being that it is a tie game. For each of these end games a message will be displayed after the last move is made showing the final state and which end game has been reached.
