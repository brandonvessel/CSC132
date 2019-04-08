import Tkinter, queue
from random import randint



def get_score():
	# Input: list of card objects
	# Output: possible scores as list of integers
	# Purpose: parse the list of card objects and return their values
    pass

def get_bust_chance():
	# Input: list of hand card objects (list)
	# Output: percentage as integer in form 100 (ex: 80% would be 80)
	# Purpose: with the current hand, return the lowest bust chance. This makes use of the get_score() function
    pass

def shuffle_cards():
	# Input: none
	# Output: none
	# Purpose: empties the cards in the deck and creates a new deck
    pass

def hit():
	# Input: player object
	# Output: none
	# Purpose: takes the player’s hand and adds a card to it. Detects a win/lose scenario and reacts accordingly.
    pass

def lose():
	# Input: player object
	# Output: none
	# Purpose: removes a player from the game, if there is only one player left, win(last player)
    pass

def win():
	# Input: player object
	# Output: none
	# Purpose: prints who won the game and asks the player(s) if they want to play again
    pass