from cards import *
from deck import *
import random

class Game:

    players = 0
    decks = []
    draw_history = [] # for AI state/action tracing
    direction = 1 # 1 is CW, -1 is CCW
    ai_skipped = False
    # the AI will always be player 1 (self.deck index 0)
    total_turns = 0

    discard_pile = Deck()

    draw_pile = None

    def __init__(self,players: int):
        self.draw_pile = build_deck(True)
        self.players = players
        for i in range(0,players):
            self.decks.append(Deck())
            self.draw_history.append([])
            # every player draws 7
            for j in range(0,7):
                self.decks[i].add_card(self.draw_pile.draw())
    
    def deck_sizes(self):
        for i in self.decks:
            print(i.get_size())
    
    def all_decks(self):
        return self.decks
    
    def get_draw_history(self):
        return self.draw_history
    
    def get_top_card(self):
        return self.discard_pile.peek()
    
    def get_direction(self):
        return self.direction

    def ai_deck(self):
        return self.decks[0]
    
    def get_draw_pile(self):
        return self.draw_pile
    
    def get_discard_pile(self):
        return self.discard_pile
  
    def get_compatible_cards(self,my_cards:Deck):
        compatible = []
        num = 0
        for card in my_cards.get_cards():
            if cards_compatible(self.discard_pile.peek(),card):
                compatible.append({"card":card,"idx":num})
            num = num + 1
        return compatible
    
    def play_turn(self,idx:int) -> int:
        self.total_turns = self.total_turns+1
        player_num = 0
        inc_by = 1
        #print("You played card",str(idx))
        #print(self.decks[0].peek_at(idx))
        # focus player plays
        if idx == -1:
            if self.draw_pile.get_size() == 0:
                self.draw_pile = self.discard_pile
                self.discard_pile = Deck()
                self.discard_pile.add_card(self.draw_pile.draw())
                self.draw_pile.shuffle()
                #print("SWAP SHUFFLE")
            drawn_card = self.draw_pile.draw()
            self.draw_history[0].append(Card(drawn_card.get_color(),drawn_card.get_type(),drawn_card.get_number()))
            self.decks[0].add_card(drawn_card)
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
                    inc_by = 2
                    clrs = [CardColor.RED,CardColor.BLUE,CardColor.GREEN,CardColor.YELLOW]
                    card_played.set_color(random.choice(clrs))
                elif card_played.get_type() == CardType.DRAWTWO:
                    next_player.add_card(self.draw_pile.draw())
                    next_player.add_card(self.draw_pile.draw())
                    inc_by = 2
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
            #print("Card not compatible :: ",self.discard_pile.peek(),self.decks[0].peek_at(idx))
            return -1

        player_num = player_num + (self.direction*inc_by)
        inc_by = 1

        while player_num % self.players != 0:
            #print("---------------------------------------")
            pnum = player_num % self.players
            #print("Player",pnum,"'s turn")
            card_played = None
            inc_by = 1
            cardplaced = False
            next_player = self.decks[(pnum+(self.direction))%self.players]
            #print("Searching",self.decks[pnum].get_size(),"cards")
            for j in range(0,self.decks[pnum].get_size()):
                #print(j,"of",self.decks[pnum].get_size())
                if cards_compatible(self.discard_pile.peek(),self.decks[pnum].peek_at(j)):
                    card_played = self.decks[pnum].draw_at(j)
                    # perform special action
                    if card_played.get_type() == CardType.DRAWFOUR:
                        next_player.add_card(self.draw_pile.draw())
                        next_player.add_card(self.draw_pile.draw())
                        next_player.add_card(self.draw_pile.draw())
                        next_player.add_card(self.draw_pile.draw())
                        inc_by = 2
                        clrs = [CardColor.RED,CardColor.BLUE,CardColor.GREEN,CardColor.YELLOW]
                        card_played.set_color(random.choice(clrs))
                    elif card_played.get_type() == CardType.DRAWTWO:
                        next_player.add_card(self.draw_pile.draw())
                        next_player.add_card(self.draw_pile.draw())
                        inc_by = 2
                    elif card_played.get_type() == CardType.REVERSE:
                        self.direction = -1*self.direction
                    elif card_played.get_type() == CardType.SKIP:
                        inc_by = 2
                    elif card_played.get_type() == CardType.WILD:
                        clrs = [CardColor.RED,CardColor.BLUE,CardColor.GREEN,CardColor.YELLOW]
                        card_played.set_color(random.choice(clrs))
                    self.discard_pile.add_card(card_played)
                    cardplaced = True
                    #print("PLAYER",pnum,"PLAYED:",card_played)
                    #print(self.decks[pnum])
                    if self.decks[pnum].get_size() == 0:
                        return pnum
                    #print("BREAKING")
                    break
                #else:
                    #print("PLAYER",pnum,"NOT COMPATIBLE",self.decks[pnum].peek_at(j))
            # nothing found, draw one
            #print("DONE CHECKING")
            if cardplaced == False:
                if self.draw_pile.get_size() == 0:
                    self.draw_pile = self.discard_pile
                    self.discard_pile = Deck()
                    self.discard_pile.add_card(self.draw_pile.draw())
                    self.draw_pile.shuffle()
                    #print("SWAP SHUFFLE")
                pulled_card = self.draw_pile.draw()
                self.draw_history[pnum].append(Card(pulled_card.get_color(),pulled_card.get_type(),pulled_card.get_number()))
                #print("PLAYER",pnum,"DREW A CARD.")
                #print(self.decks[pnum])
                # if the card works, the player can place it. Otherwise, tough luck; you gotta keep the card
                if cards_compatible(self.discard_pile.peek(),pulled_card):
                    # perform special action
                    if pulled_card.get_type() == CardType.DRAWFOUR:
                        next_player.add_card(self.draw_pile.draw())
                        next_player.add_card(self.draw_pile.draw())
                        next_player.add_card(self.draw_pile.draw())
                        next_player.add_card(self.draw_pile.draw())
                        inc_by = 2
                        clrs = [CardColor.RED,CardColor.BLUE,CardColor.GREEN,CardColor.YELLOW]
                        pulled_card.set_color(random.choice(clrs))
                    elif pulled_card.get_type() == CardType.DRAWTWO:
                        next_player.add_card(self.draw_pile.draw())
                        next_player.add_card(self.draw_pile.draw())
                        inc_by = 2
                    elif pulled_card.get_type() == CardType.REVERSE:
                        self.direction = -1*self.direction
                    elif pulled_card.get_type() == CardType.SKIP:
                        inc_by = 2
                    elif pulled_card.get_type() == CardType.WILD:
                        clrs = [CardColor.RED,CardColor.BLUE,CardColor.GREEN,CardColor.YELLOW]
                        pulled_card.set_color(random.choice(clrs))
                    self.discard_pile.add_card(pulled_card)
                    #print("PLAYER",pnum,"PLAYED (AD):",pulled_card)
                    #print(self.decks[pnum])

                else:
                    self.decks[pnum].add_card(pulled_card)

            player_num = player_num + (self.direction*inc_by)
            #print("---------------------------------------")

        return -1