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
	
	def __init__(self,id,color):
		self.setID(id)
		self.setColor(color)
		self.setState(1)
		
	def setID(self,id):
		self._id = id
		
	def setColor(self,color):
		self._color = color
		
	def setState(self,state):
		self._state = state
		
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
	

class Board:
	 
	_board = [[' 0 ' for x in range(8)] for x in range(8)]
	
	def __init__(self):
		for i in range(8):
			self._board[1][i] = " P "
		
	def printBoard(self):
		print("---------------------------------")
		for i in range(8):
			for j in range(8):
				print("|" + Board._board[i][j],end="")
			print("|")
			print("---------------------------------")
			
chess = Board()
chess.printBoard()

pawn = Piece('Q',True)
pawn.printPiece()
