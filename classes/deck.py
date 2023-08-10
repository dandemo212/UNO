# builds the deck
from cards import *
import numpy as np

class Deck:

    size = 0
    cards = []

    def __init__(self):
        self.size = 0
        self.cards = []
    
    def add_card(self,card: Card) -> None:
        self.cards.append(card)
        self.size = self.size + 1
    
    def shuffle(self):
        np.random.shuffle(self.cards)

    def draw(self) -> Card:
        self.size = self.size - 1
        return self.cards.pop() # provide top card & remove it from the deck
    
    def draw_at(self,idx:int) -> Card:
        self.size = self.size - 1
        # move the card to the end
        tmp = self.cards[idx]
        self.cards[idx] = self.cards[len(self.cards)-1]
        self.cards[len(self.cards)-1] = tmp
        return self.cards.pop() # provide card & remove it from the deck
    
    def peek(self) -> Card:
        return self.cards[len(self.cards)-1] # provide top card without removing from the deck
    
    def get_size(self) -> int:
        return self.size
    
    def __str__(self):
        string = "---- DECK :: " + str(len(self.cards)) + " CARDS ----\n\n"
        for i in self.cards:
            string += str(i) + "\n"
        return string
    
def build_deck():
    deck = Deck()
    # first, build the colored cards
    colors = [CardColor.BLUE,CardColor.GREEN,CardColor.RED,CardColor.YELLOW]
    for color in colors:
        # for each color, build the numbers
        # 1 zero
        zero_card = Card(color,CardType.NUMBER,0)
        deck.add_card(zero_card)
        # 2 draw 2
        dr2 = Card(color,CardType.DRAWTWO,-1)
        deck.add_card(dr2)
        deck.add_card(dr2)
        # 2 reverse
        rev = Card(color,CardType.REVERSE,-1)
        deck.add_card(rev)
        deck.add_card(rev)
        # 2 skip
        skip = Card(color,CardType.SKIP,-1)
        deck.add_card(skip)
        deck.add_card(skip)
        # 2 of each number 1-9
        for i in range(1,10):
            new_card = Card(color,CardType.NUMBER,i)
            deck.add_card(new_card)
            deck.add_card(new_card)
    # add wild cards
    # 4 normal wild
    wild = Card(CardColor.WILD,CardType.WILD,-1)
    deck.add_card(wild)
    deck.add_card(wild)
    deck.add_card(wild)
    deck.add_card(wild)
    # 4 draw 4
    draw4 = Card(CardColor.WILD,CardType.DRAWFOUR,-1)
    deck.add_card(draw4)
    deck.add_card(draw4)
    deck.add_card(draw4)
    deck.add_card(draw4)

    return deck