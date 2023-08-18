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
        # focus player plays
        if idx == -1:
            if self.draw_pile.get_size() == 0:
                self.draw_pile = self.discard_pile
                self.discard_pile = Deck()
                self.discard_pile.add_card(self.draw_pile.draw())
                self.draw_pile.shuffle()
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
            return -1

        player_num = player_num + (self.direction*inc_by)
        inc_by = 1

        while player_num % self.players != 0:
            pnum = player_num % self.players
            card_played = None
            inc_by = 1
            cardplaced = False
            next_player = self.decks[(pnum+(self.direction))%self.players]
            for j in range(0,self.decks[pnum].get_size()):
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
                    if self.decks[pnum].get_size() == 0:
                        return pnum
                    break

            if cardplaced == False:
                if self.draw_pile.get_size() == 0:
                    self.draw_pile = self.discard_pile
                    self.discard_pile = Deck()
                    self.discard_pile.add_card(self.draw_pile.draw())
                    self.draw_pile.shuffle()
                pulled_card = self.draw_pile.draw()
                self.draw_history[pnum].append(Card(pulled_card.get_color(),pulled_card.get_type(),pulled_card.get_number()))
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

                else:
                    self.decks[pnum].add_card(pulled_card)

            player_num = player_num + (self.direction*inc_by)

        return -1