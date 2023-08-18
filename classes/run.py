# this is where the main AI takes place
import numpy as np
from game import *
from action import *

# Create & sey up a game
def init_game(players):
    main_game = Game(players)
    turns = 0
    while turns <= 100:
        print("Your turn: ")
        print(main_game.ai_deck())
        act = Action(main_game.all_decks(),main_game.get_draw_history(),main_game.get_direction(),main_game.get_compatible_cards(main_game.ai_deck()))
        print(act)
        print(select_option(act,0))
        card_idx = int(input("Select a card (index starting at 0):"))
        turns = turns + 1
        winner = main_game.play_turn(card_idx)
        if winner == 0:
            print("YOU WON")
            break
        elif winner > 0:
            print("Player",winner,"won!")
            break

init_game(5)
