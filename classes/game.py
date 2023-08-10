from cards import *
from deck import *

class Game:

    players = 0
    decks = []
    # the AI will always be player 1 (self.deck index 0)

    discard_pile = Deck()

    draw_pile = None

    def __init__(self,players: int):
        self.draw_pile = build_deck()
        self.players = players
        for i in range(0,players):
            self.decks.append(Deck())
            # every player draws 7
            for j in range(0,7):
                self.decks[i].add_card(self.draw_pile.draw())
    
    def ai_deck(self):
        return self.decks[0]
    
    def last_card(self):
        return self.last_card
    
    def play_turn(self,idx:int) -> int:
        # idx refers to the index in the deck that the AI decides to play
        # AI plays first
        if idx == -1:
            # draw a card
            if self.draw_pile.get_size == 0:
                self.draw_pile = self.discard_pile.shuffle()
                self.discard_pile = Deck()
            self.decks[0].add_card(self.draw_pile.draw())
        else:
            # play a card
            self.discard_pile.add_card(self.decks[0].draw_at(idx))
        # all other players play
        for i in range(1,self.players):
            # go thru their deck. If no playable cards, draw and move on
            for j in range(len(self.decks[i])):
                if cards_compatible(self.discard_pile.peek(),self.decks[i][j]):
                    self.discard_pile.add_card(self.decks[i].draw_at(j))
                    break
            # nothing found, draw one
            if self.draw_pile.get_size == 0:
                self.draw_pile = self.discard_pile.shuffle()
                self.discard_pile = Deck()
            self.decks[i].add_card(self.draw_pile.draw())
            
        # check to see if anyone won that round -- return -1 if no, otherwise, return idx of the player
        for i in range(self.decks):
            if self.decks[i].get_size() == 0:
                return i
        return -1
