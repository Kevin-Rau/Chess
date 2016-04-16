# Chess
An object oriented javascript chess game

##THINGS TO DO:

**Create a Menu class:**

O'Connell/Chase implementing Menu

0. Start
  - enter username (name)
  - exit (yes/no)
1. First
  - new game (yes/no)
  - load game (yes/no)
2. Second
  - use unicode (yes/no)
3. Third
  - display this menu at the start of main(), and just store user input

idea for connecting two players to a game:
  - in json file, have two flags that are decremented when a player checks the game out
  - that way, only two players can connect to a game
  - after every move, save the entire board to the .json file
  - when players exit, increment the flags

**Create a Save class:**

Ryan2 implementing Save

1. First
  - detect user pressing "s" (save)
  - store board as .json file
  - display "game saved"
2. Second
  - detect user pressing "q" (quit/forfeit)
  - display "are you sure?"
  - return to menu

**Create Knight Move Validation**

Ryan2 implementing Knight

**Update Pawn Piece:**

**Detect King Death:**

**Add Clock Class:**
  
###Main Game Flow

The most important functions are Game.execPlayerturn() & Board.execute(). They handle a lot of the game's logic flow

game.execPlayerTurn()
  - get first square
  - get second square
  * board.execute()
    - get piece at first square
    - check piece move is valid
    - kill piece at second square, if there
    - update the board, hence set squares according to move



