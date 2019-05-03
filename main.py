import Tkinter#, queue
from random import randint
import pygame

pygame.init()
player_count = 2

############################################
################# CLASSES ##################
############################################
class Player():
    def __init__(self):
        # List of cards in hand
        self.hand = []


    def get_score(self):
        # Input: a player's hand as a list
        # Output: possible scores as list of integers
        # Purpose: parse the list of card objects and return their values
        
        scores=[0]
        hasAce=False
        aceAdded=False

        # Iterate through cards, look for Ace
        for card in self.hand:
                if(card.name=="Ace"):
                    scores.append(0)
                    hasAce=True

        if(hasAce):
            for card in self.hand:
                if(card.name=="Ace" and not(aceAdded)): # Only adds an extra score possiblity for 1 ace
                    scores[1]+=card.value[1]
                    aceAdded=True
                else:
                    scores[1]+=card.value[0]
        for card in self.hand:
            scores[0]+=card.value[0]
        if(hasAce):
            if(scores[1]<=21):
                return scores[1]
        return scores[0]
    
    def reset(self):
        self.hand = []


class Stack:
    def __init__(self):
        # List of cards
        self.cards = []


    def isempty(self):
        # Return True if the deck is empty, returns False otherwise
        return self.cards == []


    def push(self, item):
        # Adds an item to the top of the deck
        self.cards.append(item)


    def pop(self):
        # Removes the top item and returns it
        return self.cards.pop()


    def peek(self):
        # Returns the top item
        return self.cards[len(self.cards)-1]


    def size(self):
        # Returns how many cards are in the deck
        return len(self.cards)

    
    def shuffle(self):
        # Input: none
        # Output: none
        # Purpose: empties the cards in the deck and creates a new deck
        # Shuffles all the cards in the deck multiple times

        # Clear the deck
        while(True):
            try:
                self.pop()
            except:
                break
        
        # Card info
        card_suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        card_names = ["Jack", "Queen", "King"]

        # Create cards
        for suit in card_suits:
            # Ace
            self.push(Card("Ace", suit, [1,11]))

            # 2 - 11
            for i in range(2,11):
                self.push(Card(str(i), suit, [i]))

            # Jack, Queen, King
            for name in card_names:
                self.push(Card(name, suit, [10]))
        for j in range(0, 52):
            for i in range(0, len(self.cards) - 1):
                random_index = randint(0, len(self.cards) - 1)
                self.cards[i], self.cards[random_index] = self.cards[random_index], self.cards[i]


    def print_deck(self):
        # Prints all the cards in the deck to the terminal
        for card in self.cards:
            print("{}".format(card))


class Card():
    def __init__(self, name, suit, values):
        self.name = name    # The name of the card
        self.suit = suit    # The suit of the card (Spades, Hearts, Diamonds, Clubs)
        self.value = values # The numerical value of the card (integer)
        if(self.value[0] == 10 and self.name[0] == "1"):
            # Special case for the 10 because it is weird
            self.image = pygame.image.load("./sprites/cards/{}{}.png".format("10", suit[0]))
        else:
            # Get name of the card using its name and suit
            self.image = pygame.image.load("./sprites/cards/{}{}.png".format(name[0], suit[0]))
        
        # Change card size to fit on the screen
        self.image = pygame.transform.scale(self.image, (229, 349))


    def __str__(self):
        # Ex: "King of Clubs"
        #     "2 of Diamonds"
        return "{} of {}".format(self.name, self.suit)


############################################
################ FUNCTIONS #################
############################################
def get_score(hand):
    # Input: a player's hand as a list
    # Output: most reasonable score
    # Purpose: parse the list of card objects and return the most reasonable value
    # Different from player class. This one only needs a hand, not player object
    scores=[0]
    hasAce=False
    aceAdded=False

    # Iterate through cards, look for Ace
    for card in hand:
            if(card.name=="Ace"):
                scores.append(0)
                hasAce=True

    if(hasAce):
        for card in hand:
            if(card.name=="Ace" and not(aceAdded)): # Only adds an extra score possiblity for 1 ace
                scores[1]+=card.value[1]
                aceAdded=True
            else:
                scores[1]+=card.value[0]
    for card in hand:
        scores[0]+=card.value[0]
    if(hasAce):
        if(scores[1]<=21):
            return scores[1]
    return scores[0]

    
def get_bust_chance(hand):
    # Input: list of hand card objects (list)
	# Output: percentage as integer in form 100 (ex: 80% would be 80)
	# Purpose: with the current hand, return the lowest bust chance. This makes use of the get_score() function
    
    ##keeps track of the cards that will make you bust
    bust_cards = 0
    #counts every card in the deck that will bust you
    for card in deck.cards:
        hand.append(card)
        if (get_score(hand) > 21):
            bust_cards += 1
        hand.pop(len(hand)-1)
    #calculates bust percentage 
    chance = float(bust_cards) / Stack.size(deck) * 100
    print "Bust Chance: {}%".format(chance)
    return chance


def hit(self):
	# Input: player object
	# Output: none
	# Purpose: takes the player's hand and adds a card to it. Detects a win/lose scenario and reacts accordingly.

	self.hand.append(deck.pop())
	

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


def dealer_turn():
        # Input: none
        # Output: none
        # Purpose: simulates the dealer's turn based on the dealer's and player's cards
        # note: dealer will always hit if the player has a higher score and sometimes hit when tied
        while(get_score(dealer.hand)<= get_score(player.hand) and get_score(dealer.hand)!=21):
            if(get_score(dealer.hand)==get_score(player.hand)):
                if(get_bust_chance(dealer.hand)<50):
                    print "tied but hit"
                    hit(dealer)
                else:
                    return
            else:
                print "score before: {}".format(get_score(dealer.hand))
                print "losing so hit"
                hit(dealer)
                print "score after: {}".format(get_score(dealer.hand))


def place_card(x, y, image):
    # Input: x and y coordinates
    # Output: places a card on the specified location
    # Purpose: pygame function to place cards on the screen
    gameDisplay.blit(image, (x,y))


############################################
############## INITIALIZATION ##############
############################################
##### Pygame Setup #####
display_width = 800
display_height = 600
x = 50
y = 300
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('pygame test')

black = (0,0,0)
green = (0,255,0)

clock = pygame.time.Clock()
crashed = False


##### Deck initialization ####
# Make deck as a stack object
deck = Stack()

#shuffle_cards()
deck.shuffle()
deck.print_deck()

print("\n\n")


##### Player Initialization ####
players = []
for i in range(player_count):
    players.append(Player())


############################################
################### Main ###################
############################################
##### Run Game ####
step = 0
while not crashed:
    # GAME CODE
    if step == 0:
        # shuffle deck
        deck.shuffle()
        # set 2 cards in each players hand
        for player in players:
            hit(player)
            hit(player)

    # END OF GAME CODE

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.fill(green)
    for card in me.hand:
        place_card(x, y, card.image)
        #x += 50

    pygame.display.update()
    clock.tick(60)
    step += 1
    
pygame.quit()
quit()