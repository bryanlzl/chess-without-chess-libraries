      _                   
     | |                  
  ___| |__   ___  ___ ___ 
 / __| '_ \ / _ \/ __/ __|
| (__| | | |  __/\__ \__ \  on python -Beta ver 1.1.1-
 \___|_| |_|\___||___/___/
 
 *FOR ALL HISTORICAL UPDATES AND DEVELOPMENTS from day one, please visit Commits history*
                _   _               .-.        _
    o   o      | |_| |             .' '.      ( )        |\.  
o   /\ /\  o   |     |    .-"-.    (   )   .-. ^ .-.    /   '.     
\`.'  `  `'/   '-----'    `. .'    `. .'  :   `.'   :  /_.'-  \    
 \        /    |     |    .' '.     | |   `.       .'     /   |    
  \_.--._/    /_.---._\  .'___'.  ._' '_.  )_.---._(     /____|    
  '.____.'    '._____.'  `-----'  '--^--'  `._____.'    `.____.'

>>>English Chess written in python with pygame library for the interface<<<

Written without reference to chess libraries, utilizing numpy array as the chessboard with integers representing individual pieces, chess board in white's perspective. Once the game is concluded, player is brought to main menu after 3 seconds

White is player 1, Black is player 2
pieceid for p1 pawn 01-08, knight 11-12, bishop 13-14, rook 15-16, queen 17, king 18
pieceid for p2 pawn 21-28, knight 31-32, bishop 33-34, rook 35-36, queen 37, king 38

Single player: play against AI level 0 to 2, level 2 utilizing *minimax algorithm with alpha-beta pruning of 3 ply/moves* (AI looks 3 moves ahead)
Two players: play with your friend on the same PC!

Instructions:
1) Unzip zip file contents into any folder, run .exe file
or store all .py files and media into a folder, run Chess_main_menu.py

FEATURES:
- Able to perform special moves such as castling, pawn en-passant captures
- Move markers on any piece selected to show paths of possible movements, if no move markers appear, piece is unable to move (illegal moves)
- Real-time recording of players' moves in a history (in proper chess notation) displayed in a scrollable box (scroll with mousewheel)
- Player's turn indicator (knight piece icon) on player's side if its their turn
- Game status notification (e.g. BOT is thinking, check, checkmate, stalemate)
- Undo move button

FUTURE IMPROVEMENTS:
- Cutting down the massive processing time of AI level 2 (~5 mins/move)

created by: bryanlzl
