## Chess ![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg) ![Clone](https://img.shields.io/badge/clone%20count-23-green?logo=github)
Written in Python from scratch, utilizing Pygame interface

<img src="https://github.com/bryanlzl/chess-without-chess-libraries/assets/58539426/9fd7327d-8163-4d6b-a2ea-84772957f270" alt="chess sprites" width="40%">

### Game Modes
Single player: play against AI level 0 to 2, level 2 utilizing *minimax algorithm with alpha-beta pruning of 3 ply/moves* (AI looks 3 moves ahead)
Two players: play with your friend on the same PC!

<img src="https://github.com/bryanlzl/chess-without-chess-libraries/assets/58539426/07fd4be8-f4de-472c-a034-df000590d140" alt="chess-gameplay" width="60%">


### FEATURES:
- AI opponent (up to 4-ply minimax algorithm with alpha-beta pruning)
- Able to perform special moves such as castling, pawn en-passant captures
- Move pathing markers on any select piece, (no move markers appear = illegal move)
- Move history (in proper chess notation) displayed in a scrollable box
- Player's turn indicator (knight piece icon) on player's side if its their turn
- Game status notification (e.g. BOT is thinking, check, checkmate, stalemate)
- Undo moves

### Overview
White is player 1, Black is player 2
pieceid for p1 pawn 01-08, knight 11-12, bishop 13-14, rook 15-16, queen 17, king 18
pieceid for p2 pawn 21-28, knight 31-32, bishop 33-34, rook 35-36, queen 37, king 38
Once the game is concluded, player is brought to main menu after 3 seconds

### How to start:
1) Unzip zip file contents into any folder, run .exe file
or store all .py files and media into a folder, run Chess_main_menu.py

## FUTURE IMPROVEMENTS:
- Cutting down the massive processing time of AI level 2 (~5 mins/move)

Created by: bryanlzl
