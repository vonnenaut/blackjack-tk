## TO-DO:
# image.crop(box)  used to get a portion of an image

# Mini-project #6 - Blackjack
import Tkinter as tk
import random
from PIL import Image

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = Image.open("cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = Image.open("card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
won = 0
lost = 0
deck = []

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    global in_play, card_back

    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        # draw all the cards
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
        # hide dealer's hole card if in play
        if in_play is True:
            canvas.draw_image(card_back, [CARD_BACK_CENTER[0], CARD_BACK_CENTER[1]], CARD_BACK_SIZE, [85, 118], CARD_BACK_SIZE)

    

# define hand class
class Hand:
    def __init__(self):
        """ creates Hand object """
        self.hand = [] # an empty list for Card objects constituting a hand

    def __str__(self):
        """ returns a string representation of a hand """
        string = "Hand contains "
        h = self.hand
        
        for i in range(len(h)):
            string += str(h[i].get_suit()) + str(h[i].get_rank()) + " "
        
        return string

    def add_card(self, card):
        """ adds a card object to a hand """
        self.hand.append(card)

    def get_value(self):
        """ computes the value of the hand, see Blackjack video counts aces as 1, if the hand has an ace, then adds 10 to hand value if it doesn't bust """
        global VALUES
        hand_value = 0
        has_ace = False

        for card in self.hand:
            v = VALUES[card.get_rank()]
            hand_value += v
            if card.get_rank() is 'A':
                has_ace = True

        if not has_ace:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
   
    def draw(self, canvas, pos):
        """ draw a hand on the canvas, use the draw method for cards """
        for card in self.hand:
            card.draw(canvas, pos)
        

# define deck class 
class Deck:
    def __init__(self):
        """ creates a Deck object """
        self.deck = []

        for i in SUITS:
            for j in RANKS:
                self.deck.append(Card(i, j))
        
    def shuffle(self):
        """ shuffles the deck """
        random.shuffle(self.deck)

    def deal_card(self):
        """ deals a card object from the deck """
        return self.deck.pop()
    
    def __str__(self):
        """ returns a string representing the deck """
        string = "Deck contains "

        for i in range(len(self.deck)):
            string += str(self.deck[i].get_suit()) + str(self.deck[i].get_rank()) + " "
        return string
        

# main application class
##
class BlackjackGame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.in_play = False
        self.outcome = tk.StringVar()
        self.outcome.set("")
        self.won = 0
        self.lost = 0
        self.deck = []
        self.makeWidgets()

    def makeWidgets(self):
        """ set up GUI, i.e., create widgets """
        # globals
        global CARD_WIDTH, CARD_HEIGHT      
            
        canvas.pack()
        # add buttons to the frame
        tk.Button(root, text='Deal', command=self.deal).pack(side="left")
        tk.Button(root, text='Hit', command=self.hit).pack(side="left")
        tk.Button(root, text='Stay', command=self.stay).pack(side="left")
        # add label which updates outcome
        tk.Label(root, textvariable=self.outcome, font=('Helvetica',12), fg='white', bg='black').pack(side="left")
        # now draw everything
        draw(canvas, self.deck)

    #define event handlers for buttons
    def deal(self):
        global outcome, in_play, deck, player_hand, dealer_hand, outcome, lost
        
        if in_play is not True:
            # creat a Deck object and shuffle all the cards
            deck = Deck()
            deck.shuffle()
            # create a player hand, adding two cards from the deck
            player_hand = Hand()
            player_hand.add_card(deck.deal_card())
            player_hand.add_card(deck.deal_card())
            # create a dealer hand, adding two cards from the deck
            dealer_hand = Hand()
            dealer_hand.add_card(deck.deal_card())
            dealer_hand.add_card(deck.deal_card())
            outcome = "Hit or stand?"
            in_play = True
        else:
            lost += 1
            outcome = "You have lost!  New deal?"
            in_play = False

    def hit(self):
        """ if the hand is in play, hits the player; if busted, assigns a message to outcome, update in_play and score """
        global in_play, deck, player_hand, dealer_hand, outcome, lost
    
        if in_play:
            player_hand.add_card(deck.deal_card())
    
            if player_hand.get_value() > 21:
                outcome = "You have busted!  Dealer wins.  New deal?"
                lost += 1

    def stay(self):
        """ if hand is in play, repeatedly hit dealer until his hand has value 17 or more; assign a message to outcome, update in_play and score """
        global dealer_hand, deck, outcome, in_play, won, lost
    
        if in_play:
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal_card())
    
            if dealer_hand.get_value() > 21:
                # print "Dealer is busted.\nPlayer wins."
                outcome = "Dealer is busted.  Player wins.  New deal?"
                won += 1
            elif player_hand.get_value() > 21:
                # print "Player is busted.\nDealer wins."
                outcome = "Player is busted.  Dealer wins.  New deal?"
                lost += 1
            elif dealer_hand.get_value() >= player_hand.get_value():
                # print "Dealer wins."
                outcome = "Dealer wins.  New deal?"
                lost += 1
            else:
                # print "Player wins."
                outcome = "Player wins!  New deal?"
                won += 1
    
        in_play = False




# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global player_hand, dealer_hand, CARD_SIZE, outcome, won, lost

    i = 0
    j = 0

    # draw player's hand
    for card in player_hand.hand:
        card.draw(canvas, [50 + (i * CARD_SIZE[0]), 340])
        i += 1    

    # draw dealer's hand
    for card in dealer_hand.hand:
        card.draw(canvas, [50 + (j * CARD_SIZE[0]), 70])
        j += 1

    # draw outcome message for player
    canvas.draw_text(outcome, [55, 250], 30, 'Black')

    # draw labels for the canvas
    canvas.draw_text("Blackjack", [10, 25], 25, 'Black')
    canvas.draw_text("Dealer's hand:", [50, 65], 15, 'Black')
    canvas.draw_text("Player's hand:", [50, 335], 15, 'Black')
    canvas.draw_text("Won/Lost: " + str(won) + "/" + str(lost), [155,25], 22, 'Black')


# draw handler
##
def draw(canvas, deck):
    """ draws cards on canvas """
    for card in deck:
        card.draw_Card(canvas)    

# start frame and game
##
if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background='black')
    
    # create canvas for drawing cards    
    canvas = tk.Canvas(root, width=600, height=600)    

    # tk magic follows here
    BlackjackGame(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
