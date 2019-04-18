import Tkinter, queue
from random import randint

# CLASSES
class Player():
    pass

class Stack:
    def __init__(self):
        self.cards = []

    def isempty(self):
        return self.cards == []

    def push(self, item):
        self.cards.append(item)

    def pop(self):
        return self.cards.pop()

    def peek(self):
        return self.cards[len(self.cards)-1]

    def size(self):
        return len(self.cards)
    
    def shuffle(self):
        for j in range(0, 520):
            for i in range(0, len(self.cards) - 1):
                random_index = randint(0, len(self.cards) - 1)
                self.cards[i], self.cards[random_index] = self.cards[random_index], self.cards[i]

    def print_deck(self):
        for card in self.cards:
            print("{}".format(card))


class Card():
    def __init__(self, name, suit, values):
        self.name = name
        self.suit = suit
        self.value = values
    
    def __str__(self):
        return "{} of {}".format(self.name, self.suit)


# FUNCTIONS
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
	# Purpose: takes the player's hand and adds a card to it. Detects a win/lose scenario and reacts accordingly.
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
############################################
################### Main ###################
############################################

##### Deck initialization ####
# Make deck as a stack object
deck = Stack()

# Card info
card_suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
card_names = ["Jack", "Queen", "King"]
# Create cards
for suit in card_suits:
    # Ace
    deck.push(Card("Ace", suit, [1,11]))

    # 2 - 11
    for i in range(2,11):
        deck.push(Card(str(i), suit, [i]))

    # Jack, Queen, King
    for name in card_names:
        deck.push(Card(name, suit, [10]))

deck.print_deck()
deck.shuffle()
print("\n\n")
deck.print_deck()