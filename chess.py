#!/usr/local/bin/python3

# Code by Eric Fossas

# Download colorama, cd into the colorama folder and run: python3 setup.py install

import colorama
from colorama import Fore, Back, Style

# Black Pieces: Back.BLACK + Fore.WHITE + 
# White Pieces: Back.RESET + Fore.RESET + 
# Style.RESET_ALL

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
		self.move = move
		
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
		self.move = move
	
	def move(self):
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

def King():
	pass

def Queen():
	pass

def Bishop():
	pass

def Knight():
	pass

def Rook():
	pass

def Pawn():
	pass

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
			self._board[1][i] = Piece('P',False,Pawn)
		for i in range(8):
			self._board[6][i] = Piece('P',True,Pawn)
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
				print(Back.RESET + Fore.RESET + " " + piece.getID() + " ",end="")
			else:
				print(Back.BLACK + Fore.WHITE +  " " + piece.getID() + " ",end="")
				print(Back.RESET + Fore.RESET +  "",end="")
	
	def printBoard(self):
		print("---------------------------------")
		for i in range(8):
			for j in range(8):
				print("|",end="")
				self.printPiece(Board._board[i][j])
			print("|")
			print("---------------------------------")
			
chess = Board()
chess.printBoard()
