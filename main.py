from random import randint, shuffle
import pygame
import RPi.GPIO as GPIO
from time import sleep, time
from math import floor

# Initialize pygame
pygame.init()
blue = (0, 0, 255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
button_clicked = False
player_count = 0
############################################
################# CLASSES ##################
############################################
class Player(object):
    # Player object
    def __init__(self, number):
        # List of cards in hand
        self.hand = []
        self.number = number
        self.money = 5000
        self.bet = 1000


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
    # The deck in the form of a Stack object
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

    def avgval(self):
        # Returns the average value of the cards in the deck
        mysum = 0
        for card in self.cards:
            mysum += card.value[0]
        return mysum/float(len(self.cards))

    
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
        '''
        for j in range(0, 5):
            for i in range(0, len(self.cards) - 1):
                random_index = randint(0, len(self.cards) - 1)
                self.cards[i], self.cards[random_index] = self.cards[random_index], self.cards[i]
        '''
        shuffle(self.cards)


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
    def __init__(self, num, R, G, B):
        self.number = num   # Corrisponding player
        self.r = R          # Red pin
        self.g = G          # Green pin
        self.b = B          # Blue pin
        self.state = ""     # Current LED state
    
    def red(self):                      # red led means bust
        # Turn on red pin. Turn off other pins.
        GPIO.output(self.r,True)
        GPIO.output(self.g,False)
        GPIO.output(self.b,False)
        self.state = "red"
    
    def green(self):                    # green led means blackjack or win
        # Turn on green pin. Turn off other pins.
        GPIO.output(self.r,False)
        GPIO.output(self.g,True)
        GPIO.output(self.b,False)
        self.state = "green"
        
    def blue(self):                     # blue led means its the current players turn
        # Turn on blue pin, Turn off other pins.
        GPIO.output(self.r,False)
        GPIO.output(self.g,False)
        GPIO.output(self.b,True)
        self.state = "blue"
        
    def off(self):
        # Turn off all pins.
        GPIO.output(self.r,False)
        GPIO.output(self.g,False)
        GPIO.output(self.b,False)
        self.state = "off"

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


def win():
	# Input: player object
	# Output: none
	# Purpose: prints who won the game and asks the player(s) if they want to play again
    global deck
    global RGB_LEDS
    global players
    global bets_tallied
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

    beat_dealer = False

    if(get_score(dealer.hand) > 21):
        for player in players:
            if get_score(player.hand) < 22:
                place_text("Player {} won".format(player.number), x, y)
                RGB_LEDS[player.number-1].green()
                if(bets_tallied == False):
                    player.money += player.bet
            else:
                place_text("Player {} lost".format(player.number), x, y)
                RGB_LEDS[player.number-1].red()
                if(bets_tallied == False):
                    player.money -= player.bet
            y += 50
    else:
        for player in players:
            if(get_score(player.hand) >= get_score(dealer.hand) and (get_score(player.hand) < 22)):
                beat_dealer = True

        if(beat_dealer and (bets_tallied == False)):
            sound_victory[randint(0,len(sound_victory)-1)].play()

        if(beat_dealer):
            for player in players:
                if(get_score(player.hand) > get_score(dealer.hand) and (get_score(player.hand) < 22)):
                    # that player won
                    place_text("Player {} won".format(player.number), x, y)
                    RGB_LEDS[player.number-1].green()
                    if(bets_tallied == False):
                        player.money += player.bet

                elif get_score(player.hand) == get_score(dealer.hand):
                    # that player tied
                    place_text("Player {} tied the dealer".format(player.number), x, y)
                    RGB_LEDS[player.number-1].blue()
                
                else:
                    # that player lost
                    place_text("Player {} lost".format(player.number), x, y)
                    RGB_LEDS[player.number-1].red()
                    if(bets_tallied == False):
                        player.money -= player.bet
                y += 50
        else:
            # Players lose
            if(not bets_tallied):
                sound_loss[randint(0,len(sound_loss)-1)].play()
            for led in RGB_LEDS:
                led.red()
            place_text("The dealer is the winner", x, y)   
    bets_tallied = True 


def dealer_turn():
    # Input: none
    # Output: none
    # Purpose: simulates the dealer's turn based on the dealer's and player's cards
    # note: dealer will always hit if the player has a higher score and sometimes hit when tied
    global dealer
    global players
    dealer_done = False
    # dealer only has 1 card, hit
    hit(dealer)
    place_card(0,0,background_image)
    render_cards()
    pygame.display.update()
    clock.tick(60)
    sound_draw_card[randint(0,len(sound_draw_card)-1)].play()
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
        return

    # iterate through players
    for player in players:
        # if player did not bust and has a higher score than the lowest
        if((get_score(player.hand) < 22) and (get_score(player.hand) > highest)):
            highest_player = player
            highest = get_score(player.hand)
    
    player = highest_player

    # if the dealer is beating enough players it will stop
    while((get_score(dealer.hand) <= get_score(player.hand)) and (get_score(dealer.hand)!=21)):
        if(get_score(dealer.hand) > 21):
            break
        if(dealer_done):
            break
        for player in players:
            losers = 0
            if(get_score(dealer.hand) > get_score(player.hand)):
                losers+=1
        if(losers >= floor(len(players)/2.0)):
           dealer_done = True
           break

        
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
        place_card(0,0,background_image)
        render_cards()
        pygame.display.update()
        clock.tick(60)
        rand = randint(0,2)
        sound_draw_card[randint(0,len(sound_draw_card)-1)].play()
        sleep(2.5)


def place_card(x, y, image):
    # Input: x and y coordinates, path to image
    # Output: places a card on the specified location
    # Purpose: pygame function to place cards on the screen
    gameDisplay.blit(image, (x,y))
        

def place_text(text, x, y):
    # Input: text, x and y coordinates
    # Output: places text on the specified location
    # Purpose: pygame function to place text on the screen
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)

    textsurface = myfont.render(text, False, (0,0,0))
    gameDisplay.blit(textsurface,(x,y))


def text_objects(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()

def make_button(msg, x, y, ac, ic, action = None, width = 175, height = 50):
    # creates a button using an x and y coordinate, witdth, height, color, and
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    #checks to see is the mouse is over a button
    if x+width > mouse[0] > x and y+height > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,width,height))

        #runs a function when the button is clicked
        if (click[0] == 1 and action != None):
            button_clicked = True
            action()
            sleep(0.5)
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,width,height))

    #text is put on button
    smallText = pygame.font.SysFont("comicsansms",40)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(width/2)), (y+(height/2)))
    gameDisplay.blit(textSurf, textRect)
        

def mainButtonPressed():
    global step
    step = "main_menu_2"

def quitGame():
    global crashed
    crashed = True
    GPIO.cleanup()
    pygame.quit()
    quit()

def playerCount1():
    global player_count
    player_count = 1
    #make_button("1 Player", display_width/2-150, display_height/2, black, black, None, 150)
    print "new button made"
    print player_count
def playerCount2():
    global player_count
    player_count = 2
    print player_count
def playerCount3():
    global player_count
    player_count = 3
    print player_count

def player_init():
    try:
        temp = player_count
    except:
        return
    global step
    step = "player_init"

def initialize():
    global step
    step = "initialization"
def gamerule_hide_cardsButton():
    global gamerule_hide_cards
    #if gamerule_hide_cards = Tr
    gamerule_hide_cards = not gamerule_hide_cards
    print gamerule_hide_cards
def gamerule_bettingButton():
    global gamerule_betting
    gamerule_betting = not gamerule_betting
def gamerule_charlieButton():
    global gamerule_charlie
    gamerule_charlie = not gamerule_charlie
def gamerule_bust_chanceButton():
    global gamerule_bust_chance
    gamerule_bust_chance = not gamerule_bust_chance
def gamerule_guess_cardButton():
    global gamerule_guess_card
    gamerule_guess_card = not gamerule_guess_card
    


def render_cards():
    # Render the cards on the table
    #### Print Player Cards ####
    y = 0
    global players
    for player in players:
        x = card_width
        for card in player.hand:
            if(gamerule_hide_cards and player.number - 1 >= player_turn):
                place_card(x, y, card_back)
            else:
                place_card(x, y, card.image)
            x += card_width
        y += card_height
    
    #### Turn Indicator ####
    if(step == "player_input"):
        x = 0
        y = card_height * player_turn
        place_card(x, y, turn_indicator)

    #### Print Dealer Cards ####
    if(step != "betting"):
        x = display_width - card_width
        for card in dealer.hand:
            place_card(x, 0, card.image)
            x -= card_width
        if(step == "player_input"):
            place_card(x, 0, card_back)


def render_bets():
    # Render the bets on the table
    #### Print Player Bets ####
    x = 0
    y = 0
    for print_index in range(0, player_count):
        place_text("Chips: {}".format(players[print_index].money), x, y)
        y += card_height/2.0
        place_text("Bet: {}".format(players[print_index].bet), x, y)
        y += card_height/2.0


############################################
############## INITIALIZATION ##############
############################################
##### Deck initialization ####
# Make deck as a stack object
deck = Stack()

# Card values
card_width, card_height = 70, 106
card_backs = ["blue", "green", "gray", "blue", "red", "yellow"]

##### Pygame Setup #####
# Room values
display_width = 800     # pi display width
display_height = 480    # pi display height
room_width = display_width      # just in case we decide to use these names later
room_height = display_height    # just in case we decide to use these names later

# Display
gameDisplay = pygame.display.set_mode((display_width, display_height))#, pygame.FULLSCREEN)
pygame.display.set_caption('Gambling... But With Math')

# Turn Indicator
turn_indicator = pygame.image.load("./sprites/ui/turn_indicator.png")
turn_indicator = pygame.transform.scale(turn_indicator, (card_width, card_height))

# Background
background_image = pygame.image.load("./sprites/background/background.png")
logo_image = pygame.image.load("./sprites/ui/logo.png")
logo_image = pygame.transform.scale(logo_image, (646, 74))

# Engine
clock = pygame.time.Clock()
crashed = False
end_duration = 5 # seconds to display the end/victory message

# Game Opions
gamerule_hide_cards = False
gamerule_betting = False
gamerule_charlie = False
gamerule_bust_chance = True
gamerule_guess_card = True
gamerule_dank_memes = False


#### Sounds ####
# Play Music
pygame.mixer.music.load('./sounds/music/background_music.ogg')
pygame.mixer.music.play(-1)

# Sound Effects
sound_excited_aw = pygame.mixer.Sound('./sounds/effects/excited_aw.ogg')
sound_sad_aw = pygame.mixer.Sound('./sounds/effects/sad_aw.ogg')
sound_menu_click = pygame.mixer.Sound('./sounds/effects/menu_click.ogg')
sound_chip_clink = pygame.mixer.Sound('./sounds/effects/chip_clink.ogg')

# Draw Card
sound_draw_card1 = pygame.mixer.Sound('./sounds/effects/draw_card1.ogg')
sound_draw_card2 = pygame.mixer.Sound('./sounds/effects/draw_card2.ogg')
sound_draw_card = [sound_draw_card1, sound_draw_card2]

# Blackjack
sound_yes_yes = pygame.mixer.Sound('./sounds/effects/yes_yes.ogg')
sound_wilson_wow = pygame.mixer.Sound('./sounds/effects/wilson_wow.ogg')
sound_wally_wow = pygame.mixer.Sound('./sounds/effects/wally_wow.ogg')
sound_blackjack = [sound_yes_yes, sound_wilson_wow, sound_wally_wow]

# Victory
sound_heyey = pygame.mixer.Sound('./sounds/effects/HEYYEYAAEYAAAEYAEYAA.ogg')
sound_we = pygame.mixer.Sound('./sounds/effects/we_are_number_wow.ogg')
sound_john_cena = pygame.mixer.Sound('./sounds/effects/john_cena.ogg')
sound_guiles = pygame.mixer.Sound('./sounds/effects/guiles_theme.ogg')
sound_sweet_victory = pygame.mixer.Sound('./sounds/effects/sweet_victory.ogg')
sound_victory = [sound_heyey, sound_we, sound_john_cena, sound_guiles, sound_sweet_victory]

# Loss
sound_trololol = pygame.mixer.Sound('./sounds/effects/trololol.ogg')
sound_bustin = pygame.mixer.Sound('./sounds/effects/bustin.ogg')
sound_loss = [sound_trololol, sound_bustin]


###########################################
############## GPIO setup #################
###########################################
buttons = [17, 16, 13]
RGB_LED = [18, 19, 20, 21, 22, 23, 24, 25, 26]

RGB_LED_INDICES = [18, 19, 20, 21, 22, 23, 24, 25, 26]
RGB_LEDS = []



GPIO.setmode(GPIO.BCM)
GPIO.setup(RGB_LED_INDICES, GPIO.OUT)
GPIO.setup(buttons, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


############################################
################### Main ###################
############################################
##### Run Game ####
step = "main_menu"
dealer = Dealer()
while not crashed:
    # Background. Must run at the beginning of each frame.
    place_card(0,0,background_image)
    

    # ESCAPE
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                step = "main_menu"
                dealer.reset()


    ###################
    #### Main Menu ####
    ###################

    if step == "main_menu":
        place_card(75,0,logo_image)
        players = []
        button_pressed = False

        # Start button
        make_button("start", display_width/2-100, display_height/2-100, blue, black, mainButtonPressed)
        
        # Quit button
        make_button("quit", display_width/2+100, display_height/2-100, blue, black, quitGame)

    
    if step == "main_menu_2":
        global player_count
        #### Player Management ####
        # Change to 1 player
            
        make_button("1 Player", display_width/2-200, display_height/2+100, black, blue, playerCount1, 150)
        if (player_count == 1):   
            make_button("1 Player", display_width/2-200, display_height/2+100, black, black, None, 150)
        
        # Change to 2 player
        make_button("2 Players", display_width/2, display_height/2+100, black, blue, playerCount2, 150)
        if (player_count == 2):   
            make_button("2 Players", display_width/2, display_height/2+100, black, black, None, 150)

        # Change to 3 player
        make_button("3 Players", display_width/2+200, display_height/2+100, black, blue, playerCount3, 150)
        if (player_count == 3):   
            make_button("3 Players", display_width/2+200, display_height/2+100, black, black, None, 150)

        # Next button
        make_button("NEXT", display_width/2, display_height/2-200, blue, black, player_init)
        
        if step == "player_init":
            ##### Player Initialization ####
            players = []

            # Put player objects into players[]
            for i in range(player_count):
                # add a player until player count is met
                players.append(Player(i+1))

            # Create dealer #
            dealer = Dealer()
            step = "main_menu_3"
        
    if step == "main_menu_3":
        # Game Options
       
        if (gamerule_hide_cards == True):
            make_button("Hide cards", 100, 100, blue, blue, gamerule_hide_cardsButton, 175)
        else:
             make_button("Hide cards", 100, 100, blue, black, gamerule_hide_cardsButton, 175)

        if (gamerule_betting == True):
            make_button("Betting", 100, 175, blue, blue, gamerule_bettingButton, 175)
        else:
            make_button("Betting", 100, 175, blue, black, gamerule_bettingButton, 175)

        if (gamerule_charlie == True):
            make_button("Charlie", 100, 250, blue, blue, gamerule_charlieButton, 175)
        else:
            make_button("Charlie", 100, 250, blue, black, gamerule_charlieButton, 175)

        if (gamerule_bust_chance == True):
            make_button("Bust chance", 300, 100, blue, blue, gamerule_bust_chanceButton, 175)
        else:
            make_button("Bust chance", 300, 100, blue, black, gamerule_bust_chanceButton, 175)

        if (gamerule_guess_card == True):
            make_button("Guess card", 300, 175, blue, blue, gamerule_guess_cardButton, 175)
        else:
            make_button("Guess card", 300, 175, blue, black, gamerule_guess_cardButton, 175)

        # Play button
        make_button("PLAY", display_width/2-50, display_height-175, blue, black, initialize)


    ###################
    #### GAME CODE ####
    ###################

    if step == "initialization":
        #### Initialization ####
        # Beginning variables
        player_turn = 0
        winner = ""
        bets_tallied = False

        RGB_LEDS = []

        for i in range(player_count):# needs to be changed to player count
            RGB_LEDS.append(RGB((i+1), (3*i)+18,(3*i)+19, (3*i)+20))

        # Shuffle deck
        deck.shuffle()        
        print "Deck shuffled"

        # Determine card backs
        card_back = pygame.image.load("./sprites/cards/{}_back.png".format(card_backs[randint(0, len(card_backs)-1)]))
        #card_back = pygame.image.load("./sprites/cards/tech_back.png")
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

        # LEDs are initially off
        for led in RGB_LEDS:
            led.off()

        # Change step
        if(gamerule_betting):
            step = "betting"
        else:
            step = "player_input"

    #### Player Betting ####
    if step == "betting":
        player = players[player_turn]
        led = RGB_LEDS[player_turn]

        # Revive all the players that suck
        if(player.money == 0):
            player.money = 1000

        # Regulate bets
        if(player.bet > player.money):
            player.bet -= 1000
        
        # Current player led is blue
        led.blue()

        ## BET MORE ##
        if (GPIO.input(buttons[0]) == GPIO.HIGH):
            print("Player {} bet".format(player))
            if(player.bet < player.money):
                player.bet +=  1000
                sound_chip_clink.play()
            else:
                led.red()
            sleep(0.2)
            led.blue()
        
        ## STOP BETTING ##
        if (GPIO.input(buttons[1]) == GPIO.HIGH):
            print("Player {} finished betting".format(player))
            led.green()
            player_turn += 1
            sleep(1)
            
        ## GO DOWN IN BET ##
        if (GPIO.input(buttons[2]) == GPIO.HIGH):
            if(player.bet != 1000):
                print("Player {} decreased their bet".format(player))
                player.bet -=  1000
                sound_chip_clink.play()
                sleep(0.2)
        
        # Determing if all players have gone and move forward.
        if(player_turn == len(players)):
                print("All players have betted")
                # Turn off LEDs
                for led in RGB_LEDS:
                    led.off()
                step = "player_input"
                player_turn = 0

    #### Player Turn ####
    if step == "player_input":
        player = players[player_turn]
        led = RGB_LEDS[player_turn]

        # current player led is blue
        led.blue()
        
        # if player has blackjack, continue to next player
        if (get_score(player.hand) == 21):
            print ("Blackjack! Next player")
            sound_blackjack[randint(0,len(sound_blackjack)-1)].play()
            led.green()
            player_turn += 1

        # gamerule_charlie check
        if(gamerule_charlie):
            if(len(player.hand) > 4):
                player_turn += 1

        ## HIT ##
        if (GPIO.input(buttons[0]) == GPIO.HIGH):
            print("Player {} hit".format(player))
            sound_draw_card[randint(0,len(sound_draw_card)-1)].play()
            hit(player)
            sleep(1)

            # change the player turn if the player busted
            if (get_score(player.hand) > 21):
                print("Player {} BUSTED!\n Next player".format(player))
                sound_sad_aw.play()
                led.red()
                player_turn += 1
        
        ## STAY ##
        if (GPIO.input(buttons[1]) == GPIO.HIGH):
            print("Player {} stayed".format(player))
            led.off()
            player_turn += 1
            sleep(1)
            
        ## GET BUST CHANCE ##
        if (GPIO.input(buttons[2]) == GPIO.HIGH):
            if(gamerule_bust_chance and not gamerule_guess_card):
                # just bustchance
                chance = get_bust_chance(player.hand)
                place_text("Your bust chance is {}".format(str(chance)), display_width/2, display_height/2)

            elif(gamerule_guess_card and not gamerule_bust_chance):
                # just guess_card
                chance = deck.avgval()
                place_text("You will probably get {}".format(chance), display_width/2, display_height/2)

            elif(gamerule_guess_card and gamerule_bust_chance):
                # bust chance and guess card
                chance = get_bust_chance(player.hand)
                place_text("Your bust chance is {}".format(str(chance)), display_width/2, display_height/2)
                chance = deck.avgval()
                place_text("You will probably get {}".format(chance), display_width/2, display_height/2 + 20)

        
        # Determing if all players have gone and move forward.
        if(player_turn == len(players)):
                print("All players have gone.\nIt's the dealer's turn")
                step = "dealer_turn"


    #### Dealer Turn ####
    if step == "dealer_turn":
        # winner is the return value of dealer_turn()
        dealer_turn()
        step = "end1"

    if step == "end1":
        end_times = time()
        step = "end2"

    if step == "end2":
        win()
        if((time() - end_times) > end_duration):
            step = "end3"
    
    if step == "end3":
        for player in players:
            player.reset()
        dealer.reset()
        step = "initialization"


    ##########################
    #### END OF GAME CODE ####
    ##########################

    #### DISPLAY SPRITES AND SCORES ####
    #### Print Player Cards ####
    if(step == "betting"):
        render_bets()
    else:
        if(step != "end2"):
            render_cards()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    # Render the game
    pygame.display.update()
    clock.tick(60)
    
GPIO.cleanup()
pygame.quit()
quit()
