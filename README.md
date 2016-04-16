# Chess
An object oriented javascript chess game

##THINGS TO DO:

**Create a menu class:**

1. First
  - new game (yes/no)
  - load game (yes/no)
  - exit (yes/no)
2. Second
  - use unicode (yes/no)
3. Third
  - display this menu at the start of main(), and just store user input
  
avoiding usernames & stats for last, since this might require connecting to a database

**Create a save class:**

1. First
  - detect user pressing "s"
  - store board in file
  - display "game saved"
2. Second
  - detect user pressing "q"
  - display "are you sure?"
  - return to menu
  
**Create King Move Validation**

**Create Queen Move Validation**

**Create Bishop Move Validation**

**Create Knight Move Validation**
  
###Main Game Flow

The most important functions are Game.execPlayerturn() & board.execute(). They handle a lot of the game's logic flow

One: game.execPlayerTurn(chess)
  - get first square
  - get second square
  * board.execute(self._playerturn,self._origin,self._destination)

Two: board.execute(self._playerturn,self._origin,self._destination)
  - get piece at first square
  - check piece move is valid
  - kill piece at second square, if there
  - update the board, hence set squares according to move



