from cards import *
from deck import *
import random

class Game:

    players = 0
    decks = []
    direction = 1 # 1 is CW, -1 is CCW
    ai_skipped = False
    # the AI will always be player 1 (self.deck index 0)

    discard_pile = Deck()

    draw_pile = None

    def __init__(self,players: int):
        self.draw_pile = build_deck(True)
        self.players = players
        for i in range(0,players):
            self.decks.append(Deck())
            # every player draws 7
            for j in range(0,7):
                self.decks[i].add_card(self.draw_pile.draw())
    
    def ai_deck(self):
        return self.decks[0]
    
    def get_draw_pile(self):
        return self.draw_pile
    
    def get_discard_pile(self):
        return self.discard_pile
    
    def get_compatible_cards(self,my_cards:Deck):
        compatible = []
        for card in my_cards.get_cards():
            if cards_compatible(self.discard_pile.peek(),card):
                compatible.append(card)
        return compatible
    
    def play_turn(self,idx:int) -> int:
        player_num = 0
        inc_by = 1
        # focus player plays
        if idx == -1:
            if self.draw_pile.get_size == 0:
                self.draw_pile = self.discard_pile.shuffle()
                self.discard_pile = Deck()
            self.decks[0].add_card(self.draw_pile.draw())
        elif cards_compatible(self.discard_pile.peek(),self.decks[0].peek_at(idx)):
            card_played = self.decks[0].draw_at(idx)
            if card_played.get_type() != CardType.NUMBER:
                next_player = self.decks[(self.direction)%self.players]
                # perform special action
                if card_played.get_type() == CardType.DRAWFOUR:
                    next_player.add_card(self.draw_pile.draw())
                    next_player.add_card(self.draw_pile.draw())
                    next_player.add_card(self.draw_pile.draw())
                    next_player.add_card(self.draw_pile.draw())
                elif card_played.get_type() == CardType.DRAWTWO:
                    next_player.add_card(self.draw_pile.draw())
                    next_player.add_card(self.draw_pile.draw())
                elif card_played.get_type() == CardType.REVERSE:
                    self.direction = -1*self.direction
                elif card_played.get_type() == CardType.SKIP:
                    inc_by = 2
                elif card_played.get_type() == CardType.WILD:
                    clrs = [CardColor.RED,CardColor.BLUE,CardColor.GREEN,CardColor.YELLOW]
                    card_played.set_color(random.choice(clrs))
            self.discard_pile.add_card(card_played)
            if self.decks[0].get_size() == 0:
                return 0
        else:
            print("Card not compatible")
            return -1

        player_num = player_num + (self.direction*inc_by)
        inc_by = 1

        while player_num % self.players != 0:
            pnum = player_num % self.players
            card_played = None
            inc_by = 1
            for j in range(0,self.decks[pnum].get_size()):
                if cards_compatible(self.discard_pile.peek(),self.decks[pnum].peek_at(j)):
                    card_played = self.decks[pnum].draw_at(j)
                    if card_played.get_type() != CardType.NUMBER:
                        next_player = self.decks[pnum+(self.direction)%self.players]
                        # perform special action
                        if card_played.get_type() == CardType.DRAWFOUR:
                            next_player.add_card(self.draw_pile.draw())
                            next_player.add_card(self.draw_pile.draw())
                            next_player.add_card(self.draw_pile.draw())
                            next_player.add_card(self.draw_pile.draw())
                        elif card_played.get_type() == CardType.DRAWTWO:
                            next_player.add_card(self.draw_pile.draw())
                            next_player.add_card(self.draw_pile.draw())
                        elif card_played.get_type() == CardType.REVERSE:
                            self.direction = -1*self.direction
                        elif card_played.get_type() == CardType.SKIP:
                            inc_by = 2
                        elif card_played.get_type() == CardType.WILD:
                            clrs = [CardColor.RED,CardColor.BLUE,CardColor.GREEN,CardColor.YELLOW]
                            card_played.set_color(random.choice(clrs))
                        self.discard_pile.add_card(card_played)
                        if self.decks[pnum].get_size() == 0:
                            return pnum+self.players
                    break
            # nothing found, draw one
            if self.draw_pile.get_size == 0:
                self.draw_pile = self.discard_pile.shuffle()
                self.discard_pile = Deck()
            pulled_card = self.draw_pile.draw()
            # if the card works, the player can place it. Otherwise, tough luck; you gotta keep the card
            if cards_compatible(self.discard_pile.peek(),pulled_card):
                self.discard_pile.add_card(pulled_card)
            else:
                self.decks[pnum].add_card(self.draw_pile.draw())

            player_num = player_num + (self.direction*inc_by)

        return -1




        # # idx refers to the index in the deck that the AI decides to play
        # # AI plays first
        # if idx == -1:
        #     # TODO :: integrate reverse, skip, and draw card actions
        #     # draw a card
        #     if self.draw_pile.get_size == 0:
        #         self.draw_pile = self.discard_pile.shuffle()
        #         self.discard_pile = Deck()
        #     self.decks[0].add_card(self.draw_pile.draw())
        # else:
        #     # play a card
        #     self.discard_pile.add_card(self.decks[0].draw_at(idx))
        # # all other players play
        # for i in range(1,self.players):
        #     # go thru their deck. If no playable cards, draw and move on
        #     for j in range(0,self.decks[i].get_size()):
        #         if cards_compatible(self.discard_pile.peek(),self.decks[i].peek_at(j)):
        #             self.discard_pile.add_card(self.decks[i].draw_at(j))
        #             break
        #     # nothing found, draw one
        #     if self.draw_pile.get_size == 0:
        #         self.draw_pile = self.discard_pile.shuffle()
        #         self.discard_pile = Deck()
        #     self.decks[i].add_card(self.draw_pile.draw())
            
        # # check to see if anyone won that round -- return -1 if no, otherwise, return idx of the player
        # for i in range(len(self.decks)):
        #     if self.decks[i].get_size() == 0:
        #         return i
        # return -1
