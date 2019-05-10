from random import randint
import pygame
import RPi.GPIO as GPIO
from time import sleep, time

# Initialize pygame
pygame.init()

############################################
################# CLASSES ##################
############################################
class Player(object):
    def __init__(self, number):
        # List of cards in hand
        self.hand = []
        self.number = number


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
    

    def __str__(self):
        return str(self.number)


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
        self.image = "./sprites/cards/2C.png"
        if(self.value[0] == 10 and self.name[0] == "1"):
            # Special case for the 10 because it is weird
            self.image = pygame.image.load("./sprites/cards/{}{}.png".format("10", suit[0]))
        else:
            # Get name of the card using its name and suit
            self.image = pygame.image.load("./sprites/cards/{}{}.png".format(name[0], suit[0]))
        
        # Change card size to fit on the screen
        self.image = pygame.transform.scale(self.image, (card_width, card_height))


    def __str__(self):
        # Ex: "King of Clubs"
        #     "2 of Diamonds"
        return "{} of {}".format(self.name, self.suit)


class Dealer(Player):
    def __init__(self):
        self.hand = []
    
    def __str__(self):
        return "Dealer"


class RGB():
    def __init__(self, R, G, B):
        self.r = R      # Red pin
        self.g = G      # Green pin
        self.b = B      # Blue pin
    
    def red(self):
        # Turn on red pin. Turn off other pins.
        GPIO.output(R,True)
        GPIO.output(G,False)
        GPIO.output(B,False)
    
    def green(self):
        # Turn on green pin. Turn off other pins.
        GPIO.output(R,False)
        GPIO.output(G,True)
        GPIO.output(B,False)
    
    def blue(self):
        # Turn on blue pin, Turn off other pins.
        GPIO.output(R,False)
        GPIO.output(G,False)
        GPIO.output(B,True)

    def off(self):
        # Turn off all pins.
        GPIO.output(R,False)
        GPIO.output(G,False)
        GPIO.output(B,False)

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
    #print scores
    if(hasAce):
        if(scores[1]<=21):
            #print scores[1]
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


def win(winners):
	# Input: player object
	# Output: none
	# Purpose: prints who won the game and asks the player(s) if they want to play again
    global deck
    x = 0
    y = 0
    while (y < display_height):
        #makes a card waterfall
        place_card(x, y, deck.cards[randint(0, len(deck.cards)-1)].image)
        place_card(x + card_width, y, deck.cards[randint(0, len(deck.cards)-1)].image)
        place_card(display_width - card_width, y, deck.cards[randint(0, len(deck.cards)-1)].image)
        place_card(display_width - card_width*2, y, deck.cards[randint(0, len(deck.cards)-1)].image)
        y += 50
        #each winner is printed to the screen
    x = display_width/2 - 75
    y = display_height/2-50
    if (len(winners) == 0):
        place_text("The dealer is the winner", x, y)
        
    elif (winners[len(winners) -1] == "tie"):
        winners.pop()
        for winner in winners:
            place_text("The dealer tied with Player {}".format(winner.number), x, y)
            y += 50
    
    for winner in winners:
        place_text("Player {} is a winner".format(winner.number), x, y)
        y += 50


def dealer_turn():
    # Input: none
    # Output: none
    # Purpose: simulates the dealer's turn based on the dealer's and player's cards
    # note: dealer will always hit if the player has a higher score and sometimes hit when tied
    global dealer
    global players

    # dealer only has 1 card, hit
    hit(dealer)
    render_cards()
    sleep(1.5)
    # find highest scoring player
    highest = 0
    highest_player = None

    # determine if any players have valid hands
    valid = 0
    for player in players:
        if(get_score(player.hand) < 22):
            valid += 1

    if(valid == 0):
        return "All players busted, dealer wins!", []

    # iterate through players
    for player in players:
        # if player did not bust and has a higher score than the lowest
        if((get_score(player.hand) < 22) and (get_score(player.hand) > highest)):
            highest_player = player
            highest = get_score(player.hand)
    
    player = highest_player
    

    while((get_score(dealer.hand) <= get_score(player.hand)) and (get_score(dealer.hand)!=21)):
        if(get_score(dealer.hand) == get_score(player.hand)):
            if(get_bust_chance(dealer.hand) < 50):
                print "tied but hit"
                hit(dealer)
            else:
                break
        else:
            print "score before: {}".format(get_score(dealer.hand))
            print "losing so hit"
            hit(dealer)
            print "score after: {}".format(get_score(dealer.hand))
        render_cards()
        sleep(1.5)
    
    if(get_score(dealer.hand) > highest and get_score(dealer.hand) < 22):
        return "Dealer wins!", []
    elif(get_score(dealer.hand) == highest):
        winners = []
        for player in players:
            if (get_score(player.hand) == highest):
                winners.append(player)
            winners.append("tie")
            return "tied dealer...", winners
                
    else:
        score = 0
        statement = ""
        winners = []
        for player in players:
            if(get_score(player.hand) < 22 and get_score(player.hand) > score):
                statement = statement + "Player {} wins!\n".format(player)
                winners.append(player)
        return statement, winners


def place_card(x, y, image):
    # Input: x and y coordinates, path to image
    # Output: places a card on the specified location
    # Purpose: pygame function to place cards on the screen
        gameDisplay.blit(image, (x,y))
        

def place_text(text, x, y):
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)

    textsurface = myfont.render(text, False, (0,0,0))
    gameDisplay.blit(textsurface,(x,y))


def render_cards():
    #### Render the dealer drawing cards
    place_card(0,0,background_image)

    #### Print Player Cards ####
    y = 0
    for player in players:
        x = 0
        for card in player.hand:
            place_card(x, y, card.image)
            x += card_width
        y += card_height

    #### Print Dealer Cards ####
    x = display_width - card_width
    for card in dealer.hand:
        place_card(x, 0, card.image)
        x -= card_width
    if(step == "player_input"):
        place_card(x, 0, card_back)
    pygame.display.update()
    clock.tick(60)
    gameDisplay.fill(green)


############################################
############## INITIALIZATION ##############
############################################
##### Player Initialization ####
players = []
player_count = 3

# Put player objects into players[]
for i in range(player_count):
    # add a player until player count is met
    players.append(Player(i+1))

# Create dealer #
dealer = Dealer()


##### Deck initialization ####
# Make deck as a stack object
deck = Stack()

# Card values
card_width, card_height = 70, 106
card_backs = ["blue", "green", "gray", "purple", "red", "yellow"]

##### Pygame Setup #####
# Room values
#display_width = card_width * 10
#display_height = card_height * player_count
display_width = 800     # pi display width
display_height = 480    # pi display height
room_width = display_width      # just in case we decide to use these names later
room_height = display_height    # just in case we decide to use these names later

# Display
gameDisplay = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
pygame.display.set_caption('Gambling.. But With Math')

# Background
#black = (0,0,0)
#green = (0,100,0)
background_image = pygame.image.load("./sprites/background/background.png")

# Engine
clock = pygame.time.Clock()
crashed = False
end_duration = 5 # seconds to display the end/victory message


###########################################
############## GPIO setup #################
###########################################
buttons = [17, 16, 13]
RGB_LED = [18, 19, 20, 21, 22, 23, 24, 25, 26]

RGB_LED_INDICES = [18, 19, 20, 21, 22, 23, 24, 25, 26]

RGB1 = RGB(18,19,20)
RGB2 = RGB(21,22,23)
RGB3 = RGB(24,25,26)

RGB_LEDS = [RGB1, RGB2, RGB3]

GPIO.setmode(GPIO.BCM)
GPIO.setup(RGB_LED_INDICES, GPIO.OUT)
GPIO.setup(buttons, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


############################################
################### Main ###################
############################################
##### Run Game ####
step = "initialization"
while not crashed:
    # Background. Must run at the beginning of each frame.
    place_card(0,0,background_image)

    # ESCAPE
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                crashed = True
                GPIO.cleanup()
                pygame.quit()
                quit()


    ###################
    #### GAME CODE ####
    ###################

    if step == "initialization":
        #### Initialization ####
        # Beginning variables
        player_turn = 0
        winner = ""

        # Shuffle deck
        deck.shuffle()
        print "Deck shuffled"

        # Determine card backs
        card_back = pygame.image.load("./sprites/cards/{}_back.png".format(card_backs[randint(0, len(card_backs)-1)]))
        card_back = pygame.transform.scale(card_back, (card_width, card_height))

        # Set 2 cards in each players hand
        for player in players:
            hit(player)
            hit(player)
            x = 0
            for card in player.hand:
                print "Player: {} Card: {}".format(player, card)
        
        # Dealer "only gets 1 card." 1 card is added during the dealer's turn
        hit(dealer)
        step = "player_input"

    if step == "player_input":
        #### Player Input ####
        player = players[player_turn]
        led = RGB_LEDS[player_turn]
        
        if (get_score(player.hand) == 21):
            print ("Blackjack! Next player")
            player_turn += 1

        ## HIT ##
        if (GPIO.input(buttons[0]) == GPIO.HIGH):
            print("Player {} hit".format(player))
            hit(player)
            sleep(1)

            # change the player turn if the player busted
            if (get_score(player.hand) > 21):
                print("Player {} BUSTED!\n Next player".format(player))
                player_turn += 1
        
        ## STAY ##
        if (GPIO.input(buttons[1]) == GPIO.HIGH):
            print("Player {} stayed".format(player))
            player_turn += 1
            sleep(1)
            
        ## GET BUST CHANCE ##
        if (GPIO.input(buttons[2]) == GPIO.HIGH):
            chance = get_bust_chance(player.hand)
            place_text("Your bust chance is {}".format(str(chance)), display_width/2, display_height/2)
        
        # Determing if all players have gone and move forward.
        if(player_turn == len(players)):
                print("All players have gone.\nIt's the dealer's turn")
                step = "dealer_turn"

    #### Dealer Turn ####
    if step == "dealer_turn":
        # winner is the return value of dealer_turn()
        winner, winners = dealer_turn()
        print("\n\n" + winner)
        for player in players:
            player.reset()
        dealer.reset()
        step = "end1"

    if step == "end1":
        end_times = time()
        step = "end2"

    if step == "end2":
        win(winners)
        if((time() - end_times) > end_duration):
            step = "initialization"


    ##########################
    #### END OF GAME CODE ####
    ##########################

    #### DISPLAY SPRITES AND SCORES ####
    #### Print Player Cards ####
    y = 0
    for player in players:
        x = 0
        for card in player.hand:
            place_card(x, y, card.image)
            x += card_width
        y += card_height

    #### Print Dealer Cards ####
    x = display_width - card_width
    for card in dealer.hand:
        place_card(x, 0, card.image)
        x -= card_width
    if(step == "player_input"):
        place_card(x, 0, card_back)
    


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    # Render the game
    pygame.display.update()
    clock.tick(60)
    
GPIO.cleanup()
pygame.quit()
quit()
