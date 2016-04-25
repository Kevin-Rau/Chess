#!/usr/local/bin/python3

##############################
# Code by: 
# Eric Fossas
# 
# 
# 
# 
##############################

'''
INSTRUCTIONS:

Download colorama @ https://pypi.python.org/pypi/colorama, cd into the colorama folder and run: python3 setup.py install

Download curses-menu @ https://pypi.python.org/pypi/curses-menu/0.5.0, cd into menu folder, and run: python3 setup.py install

'''

###
### MODULES
###
import datetime
import time
import sys
import json
import csv
import socket
import colorama
from colorama import Fore, Back, Style
from cursesmenu import SelectionMenu

###
### HELPER FUNCTIONS
###

def checkEmpty(squares,board):
	for square in squares:
		piece = board[square[0]][square[1]]
		if type(piece) is not str:
			return False
	return True

###
### PIECE TRANSLATION DICTIONARIES
###

unicode_to_piece = {'\u2659':'UpPawn','\u265F':'DownPawn','\u265C':'Rook','\u2656':'Rook','\u265E':'Knight','\u2658':'Knight','\u265D':'Bishop','\u2657':'Bishop','\u265B':'Queen','\u2655':'Queen','\u265A':'King','\u2654':'King'}
unicode_to_id = {'\u2659':'p','\u265F':'P','\u265C':'R','\u2656':'R','\u265E':'N','\u2658':'N','\u265D':'B','\u2657':'B','\u265B':'Q','\u2655':'Q','\u265A':'K','\u2654':'K'}
id_to_piece = {'p':'UpPawn','P':'DownPawn','R':'Rook','N':'Knight','B':'Bishop','Q':'Queen','K':'King'}
id_to_blackUnicode = {'P':'\u265F','R':'\u265C','N':'\u265E','B':'\u265D','Q':'\u265B','K':'\u265A'}
id_to_whiteUnicode = {'p':'\u2659','R':'\u2656','N':'\u2658','B':'\u2657','Q':'\u2655','K':'\u2654'}

###
### PIECE
###
class Piece:
	
	# id = P pawn, R rook, N knight, B bishop, Q queen, K king
	# color = False black, True white
	# state = False dead, True alive
	_id = ''
	_color = False
	_state = False
	_move = None
	
	def __init__(self,id,color,move):
		self.setID(id)
		self.setColor(color)
		self.setState(1)
		self.moveType = move
		
	def setID(self,id):
		self._id = id
		
	def getID(self):
		return self._id
		
	def setColor(self,color):
		self._color = color
		
	def getColor(self):
		return self._color
		
	def setState(self,state):
		self._state = state

	def getState(self):
		return self._state
	
	# this will be needed for upgrading pawn, need to change id as well...
	def setMove(self,move):
		self.moveType = move
	
	def moveType(self,orig,dest):
		pass
		
	# this is for debugging only!!
	def printPiece(self):
		if(self._color):
			c = 'white'
		else:
			c = 'black'
		if(self._state):
			s = 'alive'
		else:
			s = 'dead'
		print("id: " + self._id + " | color: " + c + " | state: " + s)


###
### PIECE MOVETYPES
###
def King(orig,dest,board):
	if dest[0] > orig[0] + 1 or dest[0] < orig[0] - 1:
		return False
	elif dest[1] > orig[1] + 1 or dest[1] < orig[1] - 1:
		return False
	else:
		return True

def Queen(orig,dest,board):
	squares = []

	# orthogonal

	# horizontal
	if orig[0] == dest[0]:
		x = orig[1]
		y = dest[1]
		
		# grab direction
		if y > x:
			incr = 1
		else:
			incr = -1
		
		# grab squares
		x = x + incr
		while x != y:
			squares.append((orig[0],x))
			x = x + incr
		
		# check squares
		valid = checkEmpty(squares,board)
		if valid:
			return True
		else:
			return False
		
	# vertical
	elif orig[1] == dest[1]:
		x = orig[0]
		y = dest[0]
		
		# grab direction
		if y > x:
			incr = 1
		else:
			incr = -1
		
		# grab squares
		x = x + incr
		while x != y:
			squares.append((x,orig[1]))
			x = x + incr

		# check squares
		valid = checkEmpty(squares,board)
		if valid:
			return True
		else:
			return False
		
	# diagonal

	# left to right decrease (bi-directional)
	elif dest[0] - orig[0] == dest[1] - orig[1]:
		x = orig[0]
		y = orig[1]
		z = dest[0]
		
		# grab direction
		if z > x:
			incr = 1
		else:
			incr = -1

		# grab squares
		x = x + incr
		y = y + incr
		while x != z:
			squares.append((x,y))
			x = x + incr
			y = y + incr
		
		# check squares
		valid = checkEmpty(squares,board)
		if valid:
			return True
		else:
			return False
	
	# left to right increase (bi-directional)
	elif abs(dest[0] - orig[0]) == abs(dest[1] - orig[1]):
		x = orig[0]
		y = orig[1]
		z = dest[0]
		
		# grab direction
		if z > x:
			row = 1
			col = -1
		else:
			row = -1
			col = 1

		# grab squares
		x = x + row
		y = y + col
		while x != z:
			squares.append((x,y))
			x = x + row
			y = y + col
		
		# check squares
		valid = checkEmpty(squares,board)
		if valid:
			return True
		else:
			return False
	
	else:
		return False

def Bishop(orig,dest,board):
	squares = []
	
	# left to right decrease (bi-directional)
	if dest[0] - orig[0] == dest[1] - orig[1]:
		x = orig[0]
		y = orig[1]
		z = dest[0]
		
		# grab direction
		if z > x:
			incr = 1
		else:
			incr = -1

		# grab squares
		x = x + incr
		y = y + incr
		while x != z:
			squares.append((x,y))
			x = x + incr
			y = y + incr

		# check squares
		valid = checkEmpty(squares,board)
		if valid:
			return True
		else:
			return False
	
	# left to right increase (bi-directional)
	elif abs(dest[0] - orig[0]) == abs(dest[1] - orig[1]):
		x = orig[0]
		y = orig[1]
		z = dest[0]
		
		# grab direction
		if z > x:
			row = 1
			col = -1
		else:
			row = -1
			col = 1

		# grab squares
		x = x + row
		y = y + col
		while x != z:
			squares.append((x,y))
			x = x + row
			y = y + col
		
		# check squares
		valid = checkEmpty(squares,board)
		if valid:
			return True
		else:
			return False
	
	else:
		return False

def Knight(orig,dest,board):
	#two vertical spaces, one horizontal
	if abs(dest[0] - orig[0]) == 2 and abs(dest[1] - orig[1]) == 1: 
		return True
	#one verical space, two horizontal	
	elif  abs(dest[0] - orig[0]) == 1 and abs(dest[1] - orig[1]) == 2:
		return True
	else: 
		return False

def Rook(orig,dest,board):
	squares = []
	
	# horizontal
	if orig[0] == dest[0]:
		x = orig[1]
		y = dest[1]
		
		# grab direction
		if y > x:
			incr = 1
		else:
			incr = -1
		
		# grab squares
		x = x + incr
		while x != y:
			squares.append((orig[0],x))
			x = x + incr
		
		# check squares
		valid = checkEmpty(squares,board)
		if valid:
			return True
		else:
			return False
		
	# vertical
	elif orig[1] == dest[1]:
		x = orig[0]
		y = dest[0]
		
		# grab direction
		if y > x:
			incr = 1
		else:
			incr = -1
		
		# grab squares
		x = x + incr
		while x != y:
			squares.append((x,orig[1]))
			x = x + incr

		# check squares
		valid = checkEmpty(squares,board)
		if valid:
			return True
		else:
			return False
		
	else:
		return False

def UpPawn(orig,dest,board):
	squares = []
	
	# first move double space move
	if orig[0] == 6 and orig[1] == dest[1] and orig[0] - 2 == dest[0]:
		squares.append((orig[0] - 1,dest[1]))
		squares.append((dest[0],dest[1]))
		valid = checkEmpty(squares,board)
		if valid:
			return True
		else:
			return False
	# regular singe single space move
	elif orig[0] - 1 == dest[0] and orig[1] == dest[1]:
		squares.append((dest[0],dest[1]))
		valid = checkEmpty(squares,board)
		if valid:
			return True
		else:
			return False
	# diagnoal attack
	elif orig[0] - 1 == dest[0] and (orig[1] == dest[1] + 1 or orig[1] == dest[1] - 1):
		squares.append((dest[0],dest[1]))
		valid = checkEmpty(squares,board)
		if valid:
			return False
		else:
			return True
	else:
		return False
	
def DownPawn(orig,dest,board):
	squares = []
	
	# first move double space move
	if orig[0] == 1 and orig[1] == dest[1] and orig[0] + 2 == dest[0]:
		squares.append((orig[0] + 1,dest[1]))
		squares.append((dest[0],dest[1]))
		valid = checkEmpty(squares,board)
		if valid:
			return True
		else:
			return False
	# regular singe single space move
	elif orig[0] + 1 == dest[0] and orig[1] == dest[1]:
		squares.append((dest[0],dest[1]))
		valid = checkEmpty(squares,board)
		if valid:
			return True
		else:
			return False
	# diagnoal attack
	elif orig[0] + 1 == dest[0] and (orig[1] == dest[1] + 1 or orig[1] == dest[1] - 1):
		squares.append((dest[0],dest[1]))
		valid = checkEmpty(squares,board)
		if valid:
			return False
		else:
			return True
	else:
		return False

###
### BOARD
###
class Board:
	# board will store piece positions
	_board = [[' ' for x in range(8)] for x in range(8)]
	_dead = []
	_active = True
	
	def __init__(self,option,gameType,loaddata):
		
		if gameType == 'loadgame':
			z = 1
			for x in range(8):
				for y in range(8):
					if option:
						if loaddata[z] != 'empty':
							if loaddata[z+1] == 'True':
								self._board[x][y] = Piece(id_to_whiteUnicode[loaddata[z]],True,id_to_piece[loaddata[z]])
							else:
								self._board[x][y] = Piece(id_to_blackUnicode[loaddata[z]],False,id_to_piece[loaddata[z]])
						else:
							self._board[x][y] = ' '
						z += 2
					else:
						if loaddata[z] != 'empty':
							self._board[x][y] = Piece(loaddata[z],'True' == loaddata[z+1],id_to_piece[loaddata[z]])
						else:
							self._board[x][y] = ' '
						z += 2
		else:
			if option:
				self._board[0][0] = Piece('\u265C',False,Rook)
				self._board[0][1] = Piece('\u265E',False,Knight)
				self._board[0][2] = Piece('\u265D',False,Bishop)
				self._board[0][3] = Piece('\u265B',False,Queen)
				self._board[0][4] = Piece('\u265A',False,King)
				self._board[0][5] = Piece('\u265D',False,Bishop)
				self._board[0][6] = Piece('\u265E',False,Knight)
				self._board[0][7] = Piece('\u265C',False,Rook)
				for i in range(8):
					self._board[1][i] = Piece('\u265F',False,DownPawn)
				for x in range(2,6):
					for y in range(8):
						self._board[x][y] = ' '
				for i in range(8):
					self._board[6][i] = Piece('\u2659',True,UpPawn)
				self._board[7][0] = Piece('\u2656',True,Rook)
				self._board[7][1] = Piece('\u2658',True,Knight)
				self._board[7][2] = Piece('\u2657',True,Bishop)
				self._board[7][3] = Piece('\u2655',True,Queen)
				self._board[7][4] = Piece('\u2654',True,King)
				self._board[7][5] = Piece('\u2657',True,Bishop)
				self._board[7][6] = Piece('\u2658',True,Knight)
				self._board[7][7] = Piece('\u2656',True,Rook)
			else:
				self._board[0][0] = Piece('R',False,Rook)
				self._board[0][1] = Piece('N',False,Knight)
				self._board[0][2] = Piece('B',False,Bishop)
				self._board[0][3] = Piece('Q',False,Queen)
				self._board[0][4] = Piece('K',False,King)
				self._board[0][5] = Piece('B',False,Bishop)
				self._board[0][6] = Piece('N',False,Knight)
				self._board[0][7] = Piece('R',False,Rook)
				for i in range(8):
					self._board[1][i] = Piece('P',False,DownPawn)
				for x in range(2,6):
					for y in range(8):
						self._board[x][y] = ' '
				for i in range(8):
					self._board[6][i] = Piece('p',True,UpPawn)
				self._board[7][0] = Piece('R',True,Rook)
				self._board[7][1] = Piece('N',True,Knight)
				self._board[7][2] = Piece('B',True,Bishop)
				self._board[7][3] = Piece('Q',True,Queen)
				self._board[7][4] = Piece('K',True,King)
				self._board[7][5] = Piece('B',True,Bishop)
				self._board[7][6] = Piece('N',True,Knight)
				self._board[7][7] = Piece('R',True,Rook)
	
	def printPiece(self,piece):
		# string = blank square, object = piece
		if(type(piece) is str):
			print(" " + piece + " ",end="")
		else:
			if piece.getColor():
				print(Back.WHITE + Fore.RESET + " " + piece.getID() + " ",end="")
				print(Style.RESET_ALL + "",end="")
			else:
				print(Back.BLACK + Fore.WHITE +  " " + piece.getID() + " ",end="")
				print(Style.RESET_ALL + "",end="")
	
	def printBoard(self):
		rowGrid = ['1', '2', '3', '4', '5', '6', '7', '8']
		print("")
		for piece in self._dead:
			if piece.getColor():
				self.printPiece(piece)
		print("")
		print("")		
		print("  A   B   C   D   E   F   G   H  ")
		print("---------------------------------")
		for i in range(8):
			for j in range(8):
				print("|",end="")
				self.printPiece(Board._board[i][j])
			print("| " + rowGrid[i])
			print("---------------------------------")
		print("")
		for piece in self._dead:
			if not piece.getColor():
				self.printPiece(piece)
		print("")
			
	def getPiece(self,row,col):
		return self._board[row][col]
		
	def setPiece(self,row,col,piece):
		self._board[row][col] = piece
		
	def getGameStatus(self):
		return self._active
		
	def setGameStatus(self,boolean):
		self._active = False
	
	def killPiece(self,attacked,player):
		if type(attacked) is not str:
			if attacked.getColor() == player:
				print("* You Cannot Attack Your Own Piece *")
				return False
			else:
				self._dead.append(attacked)
				attacked.setState(False)
				if attacked.getID() == 'K' or attacked.getID() == '\u265A' or attacked.getID() == '\u2654':
					self.setGameStatus(False)
				return True
		return True
	
	def execute(self,player,orig,dest):
		# get origin piece
		piece = self.getPiece(orig[0],orig[1])
		if type(piece) is str:
			print("* No Origin Piece Selected *")
			return False
		elif piece.getColor() != player:
			print("* Incorrect Origin Piece Color Selected *")
			return False
		
		# check that move is valid
		if not piece.moveType(orig,dest,self._board):
			print("Invalid Move")
			return False
		
		# kill the piece at destination if there was one there
		attacked = self.getPiece(dest[0],dest[1])
		if not self.killPiece(attacked,player):
			return False
		
		# move the piece to the destination
		self.setPiece(orig[0],orig[1],' ')
		self.setPiece(dest[0],dest[1],piece)
		
		return True

	def getBoardAsArray(self):
		array = []
		for row in self._board:
			for col in row:
				if type(col) is not str:
					if len(col.getID()) != 1:
						piece = unicode_to_id[col.getID()] + "," + str(col.getColor()) + ","
					else:
						piece = col.getID() + "," + str(col.getColor()) + ","
				else:
					piece = 'empty,empty,'
				array.append(piece)
				
		return array

	def getBoard(self):
		return self._board
	
###
### GAME
###
class Game:
	
	# playerturn False black, True white
	_playerturn = True
	
	# this player's color
	_thisPlayer = None
	
	_origin = [None] * 2
	_destination = [None] * 2
	_input = ''
	_command = ''
	_winner = None
	_loser = None
	
	def __init__(self,currentPlayer,player = True):
		self._thisPlayer = currentPlayer
		self._playerturn = player
	
	def getThisPlayerColor(self):
		return self._thisPlayer
	
	def getPlayerTurn(self):
		return self._playerturn
	
	def printPlayerTurn(self):
		if(self._playerturn):
			print(Back.WHITE + Fore.RESET + "WHITE ->",end="")
			print(Style.RESET_ALL + "")
		else:
			print(Back.BLACK + Fore.WHITE + "BLACK ->",end="")
			print(Style.RESET_ALL + "")
	
	def switchPlayerTurn(self):
		self._playerturn = not self._playerturn
	
	# converts chess square "c1" into array "02" -> [0][2] (number switch is due to "col,row" -> [row][col])
	# parameter "boolean": True = sets origin, False = sets destination
	def chessToMatrix(self,boolean):
		location = self._input
		result = [None] * 2
		if len(location) != 2:
			return False
		else:
			loc = list(location)
			letter = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
			number = {1:0,2:1,3:2,4:3,5:4,6:5,7:6,8:7}
			if loc[0].lower() in letter:
				result[1] = int(letter[loc[0].lower()])
			else:
				return False
			if int(loc[1]) in number:
				result[0] = int(number[int(loc[1])])
				if(boolean):
					self._origin = result
					return True
				else:
					self._destination = result
					return True
			else:
				return False

	def movesToChess(self):
		letter = {0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h"}
		number = {0:"1",1:"2",2:"3",3:"4",4:"5",5:"6",6:"7",7:"8"}
		moves = ''
		moves += letter[self._origin[1]]
		moves += number[self._origin[0]]
		moves += ","
		moves += letter[self._destination[1]]
		moves += number[self._destination[0]]
		return moves

	def readCommand(self):
		command = self._input.lower()
		if command == 's' or command == 'save':
			print("Game Saved")
			# run save command
			self._command = 's'
			return False
		elif command == 'q' or command == 'quit':
			self._command = 'q'
			return False
		elif command == 'f' or command == 'forfeit':
			self._command = 'f'
			return False
		else:
			return True

	def getCommand(self):
		return self._command

	# returns False if command is found, command stored in _command by readCommnand()
	def askSquareOrigin(self, board):
		self._input = input('Origin: ')
		valid = self.chessToMatrix(True)
		while not valid:
			if self.readCommand():
				self._input = input('Origin: ')
			else:
				return False
			valid = self.chessToMatrix(True)
		return True
		
	# returns False if command is found, command stored in _command by readCommnand()
	def askSquareDestination(self, board):
		self._input = input('Destination: ')
		valid = self.chessToMatrix(False)
		while not valid:
			if self.readCommand():
				self._input = input('Origin: ')
			else:
				return False
			valid = self.chessToMatrix(False)
		return True
		
	def getOrigin(self):
		return self._origin

	def getDestination(self):
		return self._destination
	
	# returns False if command was input or game is over
	def execCurrentPlayerTurn(self,board):
		valid = False
		while not valid :
			if not self.askSquareOrigin(board):
				return False
			if not self.askSquareDestination(board):
				return False
			valid = board.execute(self._playerturn,self._origin,self._destination)
			if not board.getGameStatus():
				self._command = 'w'
		self.switchPlayerTurn()
		return True
		
	def execOpponentPlayerTurn(self,board,origin,destination):
		self._input = origin
		self.chessToMatrix(True)
		self._input = destination
		self.chessToMatrix(False)
		board.execute(self._playerturn,self._origin,self._destination)
		if not board.getGameStatus():
			self._command = 'l'
		self.switchPlayerTurn()
		return True
	
	def execOpponentCommand(self,board,command):
		if command == 'w':
			self._command = "l" # loss
		elif command == 'f':
			self._command = 'v' # victory
		elif command == 'q':
			self._command = 'v' # victory
		else:
			print("Uh... got opponent command I don't know. Most likely a connection error.")
	
	def setWinner(self, winner):
		self._winner = winner

	def setLoser(self, loser):
		self._loser = loser

	def getWinner(self):
		return self._winner

	def getLoser(self):
		return self._loser


###
### Menu
###
class Menu:			

	_host = False
	_gameType = None
	_username = ''
	_opponentname = ''
	_unicode = None
	_loadfile = None
	_statsfile = None

	def printTitle(self):
		print("")
		print("      \u265F   L E T'S  P L A Y  \u2659")
		print(" ____   _    _   ____    ___    ___ ")
		print("/  __| | |  | | |  __|  /   \\  /   \\")
		print("| |    | |__| | | |_    \\ \\_/  \\ \\_/")
		print("| |    |  __  | |  _|   _\\ \\   _\\ \\ ")
		print("| |__  | |  | | | |__  / \\\\ \\ / \\\\ \\")
		print("\\____| |_|  |_| |____| \\____/ \\____/")
		print("")

	def gameMode(self):
		game_list = ["Host A New Game", "Load & Host A Game", "Connect To A Game", "Dispay Stats"]
		menu = SelectionMenu(game_list, "CHESS")
		menu.show()
		menu.join()
		self._gameType = menu.selected_option
		
	def runMode(self):
		if self._gameType == 0:
			### host a game ###
			return 'hosting'
		elif self._gameType == 1:
			array = []
			reader = csv.reader(open('chessGame.txt', 'r'), delimiter=',')
			for x in reader:
				array.append(x)
			self._loadfile = array[0]
			return 'loading'
		elif self._gameType == 2:
			### connect to a game ###
			return 'connecting'
		elif self._gameType == 3:
			array = []
			reader = csv.reader(open('stats.txt', 'r'), delimiter=',')
			for x in reader:
				array.append(x)
			self._statsfile = array[0]
			return 'displaying'
		elif self._gameType == 4:
			sys.exit()

	def getFileData(self):
		return self._loadfile

	def getStatsData(self):
		return self._statsfile

	def askPlayerName(self):
		self._username = input('Enter Username: ')
		
	def getUsername(self):
		return self._username
		
	def setOpponentName(self,name):
		self._opponentname = name
		
	def getOpponentName(self):
		return self._opponentname
	
	def getHost(self):
		return self._host
		
	def setHost(self):
		self._host = True
	
	def askUnicode(self):
		valid = False
		while not valid:
			unicode = input('Use Unicode Pieces? (y/n): ')
			if unicode.lower() == 'y':
				self._unicode = True
				valid = True
			elif unicode.lower() == 'n':
				self._unicode = False
				valid = True

	def getUnicode(self):
		return self._unicode
	
	def printOptions(self):
		print("")
		print("----------------------------------------------------")
		print("Options:")
		print("s or save - saves the game for later")
		print("q or quit - quits and exits the program")
		print("f or forfeit - forfeit the game and return to menu")
		print("----------------------------------------------------")
		print("Press Any Key To Continue")
		print("")
		input('')

	def saveGame(self,game,board):
		with open('chessGame.txt', 'w+') as f:
			f.write(str(game.getPlayerTurn()) + ",")
			for x in board.getBoardAsArray():
				f.write(x)
	
	def printLoss(self):
		print("\nYou Lost.")
		
	def printWin(self):
		print("\nYou Won!")
		
	def printForfeit(self):
		print("\nYou Forfeited. Game resetting in 3 seconds...")
		
	def printVictory(self):
		print("\nYour Opponent Forfeited. You Win!!")

	def printQuit(self):
		print("")
		print(" ██████╗  ██████╗  ██████╗ ██████╗ ██████╗ ██╗   ██╗███████╗ ")
		print("██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝ ")
		print("██║  ███╗██║   ██║██║   ██║██║  ██║██████╔╝ ╚████╔╝ █████╗   ")
		print("██║   ██║██║   ██║██║   ██║██║  ██║██╔══██╗  ╚██╔╝  ██╔══╝   ")
		print("╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝██████╔╝   ██║   ███████╗ ")
		print(" ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚══════╝ ")
		print("")

	def storeStats(self, game):
		today = datetime.date.today()
		with open('stats.txt', 'a') as f:
			f.write(game.getWinner() + "," + game.getLoser() + "," + str(today) + ",") 

	def displayStatsBoard(self):
		print("")
		print("██▓███   █     █░███▄    █     ▄▄▄▄    ▒█████   ▄▄▄       ██▀███  ▓█████▄   ")
		print("▓██░  ██▒▓█░ █ ░█░██ ▀█   █    ▓█████▄ ▒██▒  ██▒▒████▄    ▓██ ▒ ██▒▒██▀ ██▌ ")
		print("▓██░ ██▓▒▒█░ █ ░█▓██  ▀█ ██▒   ▒██▒ ▄██▒██░  ██▒▒██  ▀█▄  ▓██ ░▄█ ▒░██   █▌ ")
		print("▒██▄█▓▒ ▒░█░ █ ░█▓██▒  ▐▌██▒   ▒██░█▀  ▒██   ██░░██▄▄▄▄██ ▒██▀▀█▄  ░▓█▄   ▌ ")
		print("▒██▒ ░  ░░░██▒██▓▒██░   ▓██░   ░▓█  ▀█▓░ ████▓▒░ ▓█   ▓██▒░██▓ ▒██▒░▒████▓  ")
		print("▒▓▒░ ░  ░░ ▓░▒ ▒ ░ ▒░   ▒ ▒    ░▒▓███▀▒░ ▒░▒░▒░  ▒▒   ▓▒█░░ ▒▓ ░▒▓░ ▒▒▓  ▒  ")
		print("░▒ ░       ▒ ░ ░ ░ ░░   ░ ▒░   ▒░▒   ░   ░ ▒ ▒░   ▒   ▒▒ ░  ░▒ ░ ▒░ ░ ▒  ▒  ")
		print("░░         ░   ░    ░   ░ ░     ░    ░ ░ ░ ░ ▒    ░   ▒     ░░   ░  ░ ░  ░  ")
		print("             ░            ░     ░          ░ ░        ░  ░   ░        ░     ")
		print("                                      ░                              ░      ")
		print("")
		i = 0
		while i < len(self._statsfile)-2:
			print(self._statsfile[i] + " beat " + self._statsfile[i+1] + " - " + self._statsfile[i+2])
			i += 3
		print("")
		exit = input('Press any key to return to the main menu.')
		return
		
###
### Connect
###
class Connect:
	
	# this is the host, sort of
	_socket = None
	_host = None
	_port = None
	
	# this is the client, sort of
	_connection = None
	_addr = None
	
	# print(socket.gethostbyname(socket.gethostname()))
	
	def __init__(self):
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._host = socket.gethostname()
		self._port = 8080

	def hostGame(self):
		self._host = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
		self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self._socket.bind((self._host, self._port))
		self._socket.listen(1)
		
	def printHostName(self):
		print(Back.WHITE + Fore.BLACK + "\nTell Player 2 To Connect To This Address:")
		print(Back.BLUE + Style.BRIGHT + Fore.WHITE + self._host)
		print(Style.RESET_ALL + "",end="")

	def waitForClient(self):
		print("\nWaiting for connection...")
		self._connection, self._addr = self._socket.accept() # blocking, waits for connection

	def connectToGame(self,address):
		self._socket.connect((address, self._port))
	
	# client calls this
	def receiveFromHost(self):
		message = self._socket.recv(1024) # blocking, waits for connection
		return message.decode("utf-8")
		
	# host calls this
	def receiveFromClient(self):
		message = self._connection.recv(1024) # blocking, waits for connection
		return message.decode("utf-8")
		
	# client calls this
	def sendToHost(self,output):
		self._socket.send(str.encode(output))	
		
	# host calls this
	def sendToClient(self,output):
		self._connection.send(str.encode(output))
	
	# client closes their connection
	def clientCloseConnection(self):
		self._socket.close()

	# host closes client connection
	def hostCloseConnection(self):
		self._connection.close()
		self._socket.close()
		self._socket = None
		
	# reset the connection after a game ends
	def resetConnection(self):
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._host = socket.gethostname()
		self._port = 8080
	
###
### MAIN PROGRAM
###
def main():
	# start up procedure
	print(Style.RESET_ALL + "",end="") # in case user uses non-white terminal
	menu = Menu()
	conn = Connect()
	
	war = True # program flag
	while war:
		# determine game mode & load correctly
		menu.gameMode()
		mode = menu.runMode()
		
		if mode == 'loading':
			chess = Board(menu.getUnicode(),'loadgame',menu.getFileData())
			if menu.getFileData()[0] == 'True':
				game = Game(True,True)
			else:
				game = Game(True,False)
			menu.setHost()
			conn.hostGame()
			conn.printHostName()
			conn.waitForClient()
		elif mode == 'hosting':
			chess = Board(menu.getUnicode(),'newgame',None)
			game = Game(True)
			menu.setHost()
			conn.hostGame()
			conn.printHostName()
			conn.waitForClient()
		elif mode == 'connecting':
			chess = Board(menu.getUnicode(),'newgame',None)
			game = Game(False)
			address = input("\nEnter The Host's Address: ")
			conn.connectToGame(address)
		elif mode == 'displaying':
			menu.displayStatsBoard()	
			continue
		else:
			# you should never get here
			sys.exit()
		
		menu.printTitle()
		menu.askPlayerName()
		menu.askUnicode()
		
		# exchange user names here
		if menu.getHost():
			message = conn.receiveFromClient()
			menu.setOpponentName(message)
			conn.sendToClient(menu.getUsername())
		else:
			conn.sendToHost(menu.getUsername())
			message = conn.receiveFromHost()
			menu.setOpponentName(message)

		print(menu.getUsername())
		print(menu.getOpponentName())

		menu.printOptions()
		
		# game logic goes here
		battle = True # game flag
		while battle:
			
			# result of turn
			chess.printBoard()
			
			# player turn
			game.printPlayerTurn()
			
			# current player turn
			if game.getThisPlayerColor() == game.getPlayerTurn():
			
				# if False returned, process command
				if not game.execCurrentPlayerTurn(chess):
					if game.getCommand() == 'q':
						message = game.getCommand()
						menu.printQuit()
						battle = False
						war = False
					elif game.getCommand() == 's':
						menu.saveGame(game,chess)
						# continue will skip everything and return to input prompt
						continue
					elif game.getCommand() == 'f':
						message = game.getCommand()
						menu.printForfeit()
						time.sleep(3)
						battle = False
				else:
				
					# send the player's move to the opponent
					message = game.movesToChess()
					
				if menu.getHost():
					conn.sendToClient(message)
				else:
					conn.sendToHost(message)
					
				# check if the game is over
				if game.getCommand() == 'w':
					chess.printBoard()
					menu.printWin()
					game.setWinner(menu.getUsername())
					game.setLoser(menu.getOpponentName())
					menu.storeStats(game)
					input("\nPress Any Key To Continue")
					battle = False

			# wait for opponent
			else:
				
				print("Waiting for opponent to move...")
				
				# wait for opponent player, then get their turn
				if menu.getHost():
					message = conn.receiveFromClient()
				else:
					message = conn.receiveFromHost()

				moves = message.split(",")
				if len(moves) > 1:
					# print opponent's move
					print(message)
					
					origin = moves[0]
					destination = moves[1]
					
					# run the opponent's player turn
					game.execOpponentPlayerTurn(chess,origin,destination)
					
					# check if the game is over
					if game.getCommand() == 'l':
						chess.printBoard()
						menu.printLoss()
						game.setWinner(menu.getOpponentName())
						game.setLoser(menu.getUsername())
						menu.storeStats(game)
						input("\nPress Any Key To Continue")
						battle = False
				else:
					command = moves[0]
					game.execOpponentCommand(chess,command) ### need to update chess board if king was killed
					
					if game.getCommand() == "v":
						menu.printVictory()
						
					battle = False
					input("\nPress Any Key To Continue")
		
		# close the connections after game is over
		if menu.getHost():
			conn.hostCloseConnection()
			conn.resetConnection()
			del game
		else:
			conn.clientCloseConnection()
			conn.resetConnection()
			del game

###
### EXECUTE PROGRAM HERE
###
if __name__ == "__main__":
    main()
