# Blackjack using Tkinter
import Tkinter as tk
import random
from PIL import Image, ImageTk

# globals
##
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_images = None
card_sheet = None
card_back = None
in_play = False
outcome = ""
deck = []
xloc = 60 # x-coordinate of first card for dealer and player hands
p_yloc = 250
d_yloc = 100

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    global in_play, card_back, card_images, card_sheet, CARD_SIZE, CARD_CENTER, RANKS, SUITS, curr_card_image, xloc

    def __init__(self, suit, rank):
        # need to create instance reference to each image associated with a class or else they won't draw correctly
        self.curr_card_image = None
        self.card_back = None

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
        card_loc = (1+CARD_SIZE[0]*RANKS.index(self.rank), CARD_SIZE[1]*SUITS.index(self.suit), CARD_SIZE[0]*(RANKS.index(self.rank)+1), CARD_SIZE[1]*(SUITS.index(self.suit)+1))
        # load card sheet image
        card_sheet = Image.open("cards_jfitz.jpg")
        # crop sheet to current card-face's image
        pil_card_cropped = card_sheet.crop((card_loc))
        self.curr_card_image = ImageTk.PhotoImage(pil_card_cropped)
        # draw current card
        canvas.create_image(pos, image=self.curr_card_image)    

        # load card back image
        c_back = Image.open("card_jfitz_back.jpg")
        # crop
        pil_cropped = c_back.crop((1,0,72,96))
        self.card_back = ImageTk.PhotoImage(pil_cropped)   

        # hide dealer's hole card if in play by drawing card back
        if in_play is True:
            canvas.create_image((xloc,d_yloc), image=self.card_back)
    

# define hand class
class Hand:
    global xloc

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
   
    def draw(self, canvas, yloc):
        """ draw a hand on the canvas, use the draw method for cards """
        
        for card in self.hand:
            card.draw(canvas, (xloc+(self.hand.index(card)*CARD_SIZE[0]), yloc))
        

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
        self.won = 0
        self.lost = 0
        self.deck = []
        self.outcome = tk.StringVar()
        self.outcome.set("")
        self.score = tk.StringVar()
        self.score.set(str(self.won) + "/" + str(self.lost))
        self.makeWidgets()
        self.deal()

    def makeWidgets(self):
        """ set up GUI, i.e., create widgets """
        # globals
        global CARD_SIZE, card_images, card_back, card_sheet, pil_card_cropped, curr_card_image, xloc, d_yloc
        
        canvas.configure(background='green4')    
        canvas.pack()
        # add buttons to the frame
        tk.Button(root, text='Deal', command=self.deal).pack(side="left")
        tk.Button(root, text='Hit', command=self.hit).pack(side="left")
        tk.Button(root, text='Stay', command=self.stay).pack(side="left")
        # add label for dealer's hand
        canvas_label_d = canvas.create_text(30, (d_yloc - CARD_SIZE[1]/2), anchor="sw")
        canvas.itemconfig(canvas_label_d, text="Dealer's hand: ")
        # add label for player's hand
        canvas_label_p = canvas.create_text(30, (p_yloc - CARD_SIZE[1]/2), anchor="sw")
        canvas.itemconfig(canvas_label_p, text="Player's hand: ")
        # add label which updates outcome
        tk.Label(root, textvariable=self.outcome, font=('Helvetica',12), fg='white', bg='black').pack(side="left")
        # add label for updating score
        canvas_label_score = canvas.create_text(CANVAS_WIDTH - 50, 30, anchor="sw")
        canvas.itemconfig(canvas_label_score, text=self.score.get())

                

    #define event handlers for buttons
    def deal(self):
        global outcome, in_play, deck, player_hand, dealer_hand, outcome
        
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
            self.outcome.set("Hit or stay?")
            in_play = True

            # now draw everything
            draw(canvas)

            # Test
            print "Dealer hand: ", dealer_hand
            print "Player hand: ", player_hand
            
        else:
            lost += 1
            self.outcome.set("You have lost!  New deal?")
            in_play = False
            self.lost += 1
            self.score.set(str(self.won) + "/" + str(self.lost))
            draw(canvas)
        
    def hit(self):
        """ if the hand is in play, hits the player; if busted, assigns a message to outcome, update in_play and score """
        global in_play, deck, player_hand, dealer_hand, outcome, lost
    
        if in_play:
            player_hand.add_card(deck.deal_card())
    
            if player_hand.get_value() > 21:
                self.outcome.set("You have busted!  Dealer wins.  New deal?")
                self.lost += 1
                self.score.set(str(self.won) + "/" + str(self.lost))
                in_play = False
        draw(canvas)

        print "\nPlayer hand: ", player_hand
        print "Dealer hand: ", dealer_hand
        

    def stay(self):
        """ if hand is in play, repeatedly hit dealer until his hand has value 17 or more; assign a message to outcome, update in_play and score """
        global dealer_hand, deck, outcome, in_play
    
        if in_play:
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal_card())
    
            if dealer_hand.get_value() > 21:
                # print "Dealer is busted.\nPlayer wins."
                self.outcome.set("Dealer is busted.  Player wins.  New deal?")
                self.won += 1
                self.score.set(str(self.won) + "/" + str(self.lost))
            elif player_hand.get_value() > 21:
                # print "Player is busted.\nDealer wins."
                self.outcome.set("Player is busted.  Dealer wins.  New deal?")
                self.lost += 1
                self.score.set(str(self.won) + "/" + str(self.lost))
            elif dealer_hand.get_value() >= player_hand.get_value():
                # print "Dealer wins."
                self.outcome.set("Dealer wins.  New deal?")
                self.lost += 1
                self.score.set(str(self.won) + "/" + str(self.lost))
            else:
                # print "Player wins."
                self.outcome.set("Player wins!  New deal?")
                self.won += 1
                self.score.set(str(self.won) + "/" + str(self.lost))
        in_play = False
        draw(canvas)


# draw handler  
##  
def draw(canvas):
    global player_hand, dealer_hand, outcome

    # draw player's hand at y-location of 250
    player_hand.draw(canvas, p_yloc) 

    # draw dealer's hand at y-location of 100
    dealer_hand.draw(canvas, d_yloc)
    

# start frame and game
##
if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background='black')

    # create canvas for drawing cards    
    canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)    

    # tk magic follows here
    BlackjackGame(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
