Summary

The goal of this assignment is to provide a deeper understanding of the mechanics of minimax and alpha-beta search and the impact of an evaluation function on adversarial search. There will also be a contest in which your programs compete against that of your classmates!

Reversi (Othello)

For this assignment, you will be creating an agent that plays the game Reversi (also known by the trademark Othello). Reversi is a two-person, full information game. Rules, and some basic strategy, can be found here.

Your Assignment
For this assignment, you will create a file named .py, (where is your username) which contains the following two python functions:

nextMove(board, color, time)   where
board is a representation of the board:
The board will be represented as a list of list of strings (that is, a 2D array of strings). Each string will be "B" for black, "W" for white, or "." for an empty square.
color is either the string "B" or the string "W", representing the color to play
time is the time left on your tournament clock (in seconds).
nextMoveR(board, color, time)
Which is identical to nextMove, except it plays the Reversed game (Reversed Reversi) -- when the object is to end with as few pieces of your color as possible
Your nextMove (and nextMoveR) should return either a tuple representing the position on the board to move to, or the string "pass". (That is, if you return (3,4), you mean to set board[3][4] = your color). Note that a pass is only valid if there are no other moves to be made.

Your nextMove should do a minmax search, with alpha-beta pruning. You should also spend some time on a good evaluation function. Singular extensions and quiescent search may also be a good idea, but are not required. Note that either making an illegal move or running out of time will lose the match.

Provided Files
The following files are provided to help you get started:

gameplay.pyView in a new window Plays two agents against each other. From the command line, this function is invoked with:
   % python gameplay.py [-t ] [-v] [-r] player1 player2
Where player1.py and player2.py are python files that contain a nextMove and nextMoveR. The flags -v stands for verbose output (display the board after every turn, already implemented), and -r stands for "reversed" (use nextMoveR rather than nextMove).

randomPlay.pyView in a new window Sample agent that makes a random legal move
simpleGreedy.pyView in a new window Sample agent that uses a brain-dead evaluation function, with no search


For example, you could have two random players play against each other with:

% python gameplay.py randomPlay randomPlay


If you wanted to play simpleGreedy against randomPlay (with simpleGreedy going first), seeing all the moves, with a clock of 150 seconds:

% python gameplay.py -t150 -v simpleGreedy randomPlay