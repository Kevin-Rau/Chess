#!/usr/local/bin/python3

# Code by Eric Fossas

# Download colorama, cd into the colorama folder and run: python3 setup.py install

import colorama
from colorama import Fore, Back, Style

# Black Pieces: Back.BLACK + Fore.WHITE + 
# White Pieces: Back.WHITE + Fore.RESET + 
# Board: Style.RESET_ALL



# id = P pawn, R rook, N knight, B bishop, Q queen, K king
# color = False black, True white
# state = False dead, True alive
class Piece:
	
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

# piece function are essentially just validations of orig->dest moves
# if valid, return a list of squares the piece must traverse, so board can validate those squares are empty
def King(orig,dest):
	return False

def Queen(orig,dest):
	return False

def Bishop(orig,dest):
	return False

def Knight(orig,dest):
	return False

def Rook(orig,dest):
	if orig[0] == dest[0]:
		return True
	elif orig[1] == dest[1]:
		return True
	else:
		return False

def UpPawn(orig,dest):
	if(orig[0] - 1 == dest[0]):
		return True
	else:
		return False
	
def DownPawn(orig,dest):
	if(orig[0] + 1 == dest[0]):
		return True
	else:
		return False

class Board:
	# board will store piece positions
	# death will store dead pieces
	_board = [[' ' for x in range(8)] for x in range(8)]
	_death = []
	
	def __init__(self):
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
			if(piece.getColor()):
				print(Back.WHITE + Fore.RESET + " " + piece.getID() + " ",end="")
				print(Style.RESET_ALL + "",end="")
			else:
				print(Back.BLACK + Fore.WHITE +  " " + piece.getID() + " ",end="")
				print(Style.RESET_ALL + "",end="")
	
	def printBoard(self):
		print("---------------------------------")
		for i in range(8):
			for j in range(8):
				print("|",end="")
				self.printPiece(Board._board[i][j])
			print("|")
			print("---------------------------------")
			
	def getPiece(self,row,col):
		return self._board[row][col]
		
	def setPiece(self,row,col,piece):
		self._board[row][col] = piece
	
	def execute(self,orig,dest):
		print(orig)
		print(dest)
		
		# get origin piece
		piece = self.getPiece(orig[0],orig[1])
		if(type(piece) is str):
			print("No Origin Piece Selected")
			return False
		
		# get list of squares piece should move
		squares = piece.moveType(orig,dest)
		if(squares == False):
			print("Invalid Move")
			return False
		elif(squares == True):
			pass # single square move, no check needed
		else:
			### board needs to check that those spaces are empty ###
			pass
		
		# kill the piece at destination if there was one there
		attacked = self.getPiece(dest[0],dest[1])
		if(type(attacked) is not str):
			attacked.setState(False)
		
		# move the piece to the destination
		self.setPiece(orig[0],orig[1],' ')
		self.setPiece(dest[0],dest[1],piece)
		self._board[dest[0]][dest[1]] = piece
		
		return True
	
class Game:
	
	_playerturn = True
	_origin = [None] * 2
	_destination = [None] * 2
	_input = ''
	
	def __init__(self):
		self._playerturn = True
	
	def printPlayerTurn(self):
		if(self._playerturn):
			print(Back.WHITE + Fore.RESET + "Player White ->",end="")
			print(Style.RESET_ALL + "")
		else:
			print(Back.BLACK + Fore.WHITE + "Player Black ->",end="")
			print(Style.RESET_ALL + "")
	
	def switchPlayerTurn(self):
		self._playerturn = not self._playerturn
	
	# converts chess square "c2" into string of number for board array "12" -> [1][2] (number switch is due to "col,row" -> [row][col])
	# parameter: True = origin, False = destination
	def chessToMatrix(self,bool):
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
				if(bool):
					self._origin = result
					return True
				else:
					self._destination = result
					return True
			else:
				return False

	def askSquareOrigin(self):
		self._input = input('Origin: ')
		valid = self.chessToMatrix(True)
		while(not valid):
			self._input = input('Incorrect Input. Try Again.\nOrigin: ')
			valid = self.chessToMatrix(True)
			### validate that player selected their own piece ###
			
		
	def askSquareDestination(self):
		self._input = input('Destination: ')
		valid = self.chessToMatrix(False)
		while(not valid):
			self._input = input('Incorrect Input. Try Again.\nDestination: ')
			valid = self.chessToMatrix(True)
		
	def getOrigin(self):
		return self._origin

	def getDestination(self):
		return self._destination
		
	def execPlayerTurn(self,board):
		valid = False
		while(not valid):
			self.askSquareOrigin()
			self.askSquareDestination()
			valid = board.execute(self._origin,self._destination)
		self.switchPlayerTurn()
			
# This is the actual program code
def main():
	# start up procedure
	print(Style.RESET_ALL + "",end="") # in case user uses non-white terminal
	chess = Board()
	game = Game()
	
	battle = True
	
	chess.printBoard()
	
	# game logic goes here
	while(battle):
		# player turn
		game.printPlayerTurn()
		game.execPlayerTurn(chess)
		
		# result of turn
		chess.printBoard()

# The program executes here
if __name__ == "__main__":
    main()

