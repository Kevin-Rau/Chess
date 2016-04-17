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
import sys
import json
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
		
		print(squares)
		
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
		
		print("hi!")
		
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
		
		print(squares)
		
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
		
		print(squares)
		
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
		
		print("hi!")
		
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
		
		print(squares)
		
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
	
	def __init__(self,unicode):
		if unicode:
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
			for i in range(8):
				self._board[6][i] = Piece('P',True,UpPawn)
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
		if type(attacked) is not str:
			if attacked.getColor() == player:
				print("* You Cannot Attack Your Own Piece *")
				return False
			else:
				self._dead.append(attacked)
				attacked.setState(False)
		
		# move the piece to the destination
		self.setPiece(orig[0],orig[1],' ')
		self.setPiece(dest[0],dest[1],piece)
		
		return True

	def getBoard(self):
		return self._board

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
	
###
### GAME
###
class Game:
	
	# playerturn False black, True white
	_playerturn = True
	_origin = [None] * 2
	_destination = [None] * 2
	_input = ''
	_saveRequested = False
	_quitRequested = False
	
	def __init__(self):
		self._playerturn = True
	
	def printPlayerTurn(self, menu):
		if(self._playerturn):
			print(Back.WHITE + Fore.RESET + menu._playerName1 + " ->",end="")
			print(Style.RESET_ALL + "")
		else:
			print(Back.BLACK + Fore.WHITE + menu._playerName2 + " ->",end="")
			print(Style.RESET_ALL + "")
	
	def switchPlayerTurn(self):
		self._playerturn = not self._playerturn
	
	# converts chess square "c1" into array "02" -> [0][2] (number switch is due to "col,row" -> [row][col])
	# parameter "boolean": True = sets origin, False = sets destination
	def chessToMatrix(self,boolean):
		location = self._input
		if location.lower() == 's':
			self._saveRequested = True

		if location.lower() == 'q':
			self._quitRequested = True	

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

	def askSquareOrigin(self, board):
		self._input = input('Origin: ')
		valid = self.chessToMatrix(True)
		while(not valid):
			if self._saveRequested: 
				Save.save(board)
				self._input = input('* Game Saved *\nOrigin: ')
				self._saveRequested = False
			elif self._quitRequested:
				self._input = input('Do you really want to quit? (y/n): ')
				if self._input == 'y':
					self._input = input('Would you like to save? (y/n): ')
					if self._input == 'y':
						Save.save(board)
					return
				self._quitRequested = False	
				self._input = input('Origin: ')		
			else:
				self._input = input('* Incorrect Input. Try Again. *\nOrigin: ')
			valid = self.chessToMatrix(True)
			
		
	def askSquareDestination(self, board):
		self._input = input('Destination: ')
		valid = self.chessToMatrix(False)
		while(not valid):
			if self._saveRequested:
				Save.save(board)
				self._input = input('* Game Saved *\nDestination: ')
				self._saveRequested = False
			elif self._quitRequested:
				self._input = input('Do you really want to quit? (y/n): ')
				if self._input == 'y':
					self._input = input('Would you like to save? (y/n): ')
					if self._input == 'y':
						Save.save(board)
					return
				self._quitRequested = False	
				self._input = input('Destination: ')		
			else:
				self._input = input('* Incorrect Input. Try Again. *\nDestination: ')	
			valid = self.chessToMatrix(False)
		
	def getOrigin(self):
		return self._origin

	def getDestination(self):
		return self._destination
		
	def execPlayerTurn(self,board):
		valid = False
		while(not valid):
			self.askSquareOrigin(board)
			if self._quitRequested:
				 break
			self.askSquareDestination(board)
			if self._quitRequested:
				 break
			valid = board.execute(self._playerturn,self._origin,self._destination)
		self.switchPlayerTurn()

	def printOptions(self):
		print("Enter \"q\" to quit or \"s\" to save")	

	def quitRequested(self):
		if self._quitRequested:
			return True
		return False	

###
### Save
###
class Save:
	#Save board state
	def save(board):
		with open('game.json', 'w') as outfile:
			json.dump(Board.to_JSON(board.getBoard()), outfile)
			json.dump(Game._playerturn, outfile)
		return True

###
### Menu
###
class Menu:			

	_gameType = None
	_username = ''
	_unicode = None
	
	self._username = input('Enter Username: ')

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
		game_list = ["Host A Game", "Load A Game", "Connect To A Game"]
		menu = SelectionMenu(game_list, "Select an option")
		menu.show()
		menu.join()
		self._gameType = menu.selected_option
		
	def runMode(self):
		if self._gameType == 0:
			print("Host A Game")
			pass
		elif self._gameType == 1:
			print("Load A Game")
			pass
		elif self._gameType == 2:
			print("Connect To A Game")
			pass
		elif self._gameType == 3:
			sys.exit()

	def askPlayerName(self):
		self._username = input('Enter Username: ')
		
	def askUnicode(self):
		valid = False
		while not valid:
			unicode = input('Use Unicode Pieces? (y/n): ')
			if unicode.lower() = 'y':
				self._unicode = True
				valid = True
			elif unicode.lower() = 'n':
				self._unicode = False
				valid = True
		
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
		self._host = socket.gethostname()
		self._socket.bind((self._host, self._port))
		self._socket.listen(1)

	def connectToGame(self,address):
		self._socket.connect((address, self._port))
	
	def waitForClient(self):
		self._connection, self._addr = self._connection.accept()
	
	def receiveFromClient(self):
		return self._connection.recv(1024)
		
	def sendToClient(self,output):
		self._connection.sendall(output)
	
	def closeClient(self):
		self._connection.close()
	
###
### MAIN PROGRAM
###
def main():
	# start up procedure
	print(Style.RESET_ALL + "",end="") # in case user uses non-white terminal
	chess = Board(False)
	menu = Menu()
	game = Game()
	conn = Connect()
	
	battle = True
	
	menu.gameMode()
	menu.runMode()
	
	menu.printTitle()
	menu.askPlayerName()
	menu.askUnicode()
	
	chess.printBoard()
	
	# game logic goes here
	while(battle):
		
		# player turn
		game.printPlayerTurn(menu)
		game.printOptions()
		game.execPlayerTurn(chess)
		if game.quitRequested():
			print("")
			print(" ██████╗  ██████╗  ██████╗ ██████╗ ██████╗ ██╗   ██╗███████╗ ")
			print("██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝ ")
			print("██║  ███╗██║   ██║██║   ██║██║  ██║██████╔╝ ╚████╔╝ █████╗   ")
			print("██║   ██║██║   ██║██║   ██║██║  ██║██╔══██╗  ╚██╔╝  ██╔══╝   ")
			print("╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝██████╔╝   ██║   ███████╗ ")
			print(" ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚══════╝ ")
			print("")
			return
		# result of turn
		chess.printBoard()

###
### EXECUTE PROGRAM HERE
###
if __name__ == "__main__":
    main()
