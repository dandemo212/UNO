# comprehensive action information storage class
import numpy as np
from cards import *
from deck import *
import random
import hashlib
from evaluate import *

class Action:

    decks = []
    draw_history = []
    compatible = []
    direction = 1

    def __init__(self,decks: list,draw_history:list,direction:int,compatible):
        # decks:list -- 2D list of all the decks
        # draw_history:list -- 2D list of the draw history of each player
        # direction:int -- -1 or 1 indicating the direction of gameplay
        # compatible:list -- dictionary of the compatible cards a player can play
        self.decks = decks
        self.direction = direction
        self.draw_history = draw_history
        self.compatible = compatible

    def __str__(self):
        return str(self.compatible)

    def state_key(self,top_card):
        if top_card == "DRAW":
            return hashlib.md5(b'DRAW')
        # convert the information in this action to an MD5 string so it can be compared with other similar actions
        return get_hashcode(top_card)

    def calculate_rewards(self):
        rewards = [-2]*(self.decks[0].get_size()+1)
        # THIS FUNCTION returns an array of size n+1, where n is the size of the deck. The highest index represents the reward for drawing a card
        # How many cards do you have
        # How many cards does the next person have (place a +? or skip?)
        # How many cards does the previous person have (avoid reverse?)
        # What color did the last person draw on (what color do they probably not have?)
        # What color is the majority of my deck?

        # always have the "draw card" action as a viable option
        rewards[-1] = 0
        
        # UNO!
        if self.decks[0].get_size() == 1 and len(self.compatible) == 0:
            rewards[-1] = 1
            return rewards
        elif self.decks[0].get_size() == 1:
            rewards[0] = 1
            return rewards
        
        # PREJUDICE -- #1 = no prejudice
        prejudice = {
            "plus2":1,
            "plus4":1,
            "wild":1,
            "skip":1,
            "blue":1,
            "reverse":1,
            "yellow":1,
            "red":1,
            "green":1
        }

        # TODO: If you can use the last card of a color, or use a card to change the color to a new color where you have more cards, it will favor the latter option
        
        next_person_num_cards = self.decks[self.direction].get_size()
        prev_person_num_cards = self.decks[-1*self.direction].get_size()
        my_num_cards = self.decks[0].get_size()
        # IF THE NEXT PERSON HAS LESS CARDS THAN U, FAVOR A + OR SKIP
        if next_person_num_cards < my_num_cards:
            prejudice['plus2'] += 2
            prejudice['plus4'] += 1
            prejudice['skip'] += 2
            prejudice['reverse'] += 1
            #4 is weighted less bc it's wild -- it could prove more useful in the future
        
        # IF THE PREVIOUS PERSON HAS LESS CARDS THAN U, DON'T FAVOR A REVERSE
        if prev_person_num_cards < my_num_cards:
            prejudice['reverse'] -= 1

        # IF YOU HAVE MULTIPLE CHOICES, PLAY WHAT THE NEXT PERSON DREW LAST
        if len(self.draw_history[self.direction]) > 0:
            npdc = self.draw_history[self.direction][-1].get_color()
            if npdc == CardColor.YELLOW:
                prejudice['yellow'] += 1
            elif npdc == CardColor.GREEN:
                prejudice['green'] += 1
            elif npdc == CardColor.BLUE:
                prejudice['blue'] += 1
            elif npdc == CardColor.RED:
                prejudice['red'] += 1

        # OTHERWISE, PLAY THE COLOR THE MAJORITY OF MY DECK IS IN

        # i would use a switch statement but idk how to do that in python
        my_c = [0,0,0,0] # yellow, red, green, blue
        for card in self.decks[0].get_cards():
            if card.get_color() == CardColor.YELLOW:
                my_c[0] += 1
            elif card.get_color() == CardColor.RED:
                my_c[1] += 1
            elif card.get_color() == CardColor.GREEN:
                my_c[2] += 1
            elif card.get_color() == CardColor.BLUE:
                my_c[3] += 1
        mc_idx = my_c.index(max(my_c))
        if mc_idx == 0:
            prejudice['yellow'] += 1
        elif mc_idx == 1:
            prejudice['red'] += 1
        elif mc_idx == 2:
            prejudice['green'] += 1
        elif mc_idx == 3:
            prejudice['blue'] += 1

        # ONLY PLAY A WILD WHEN I HAVE NO OTHER CARDS LEFT
        if self.decks[0].get_size() > 1:
            prejudice['wild'] -= 1

        # BUILD THE ARRAY
        for item in self.compatible:
            card = item['card']
            place_idx = item['idx']
            rw = 0
            if card.get_type() == CardType.DRAWFOUR:
                rw += prejudice['plus4']
            elif card.get_type() == CardType.DRAWTWO:
                rw += prejudice['plus2']
            elif card.get_type() == CardType.REVERSE:
                rw += prejudice['reverse']
            elif card.get_type() == CardType.SKIP:
                rw += prejudice['skip']
            elif card.get_type() == CardType.WILD:
                rw += prejudice['wild']
            elif card.get_type() == CardType.NUMBER:
                if card.get_color() == CardColor.GREEN:
                    rw += prejudice['green']
                elif card.get_color() == CardColor.BLUE:
                    rw += prejudice['blue']
                elif card.get_color() == CardColor.RED:
                    rw += prejudice['red']
                elif card.get_color() == CardColor.YELLOW:
                    rw += prejudice['yellow']
            
            rewards[place_idx] = rw
        
        return rewards

def select_option(action: Action,decision:int,qtable,state):
    # decision == 0 -> exploit
    # decision == 1 -> explore
    rewards = action.calculate_rewards()
    hash_list = get_hashlist()
    #print("REWARDS",rewards)
    if decision == 0:
        # exploit what is already known
        new_rewards = []
        for i in range(len(rewards)-1):
            if rewards[i] != -2:
                # do stuff
                new_rewards.append(rewards[i]+(2*qtable[hash_list.index(state.hexdigest()),(hash_list.index(action.state_key(action.decks[0].peek_at(i)).hexdigest()))]))
            else:
                new_rewards.append(-2)
        # don't forget draw
        new_rewards.append(rewards[-1]+(2*qtable[hash_list.index(state.hexdigest()),(hash_list.index(action.state_key("DRAW").hexdigest()))]))
        max_reward = new_rewards.index(max(new_rewards))
        #print(rewards)
        #print(new_rewards)
        #print("EXPLOIT",max_reward)
        return (max_reward,new_rewards[max_reward])
    else:
        # explore to find something new -- pick random that isn't -2
        possible_indexes = []
        for i in range(len(rewards)):
            if rewards[i] > -2:
                possible_indexes.append(i)
        random_reward = random.choice(possible_indexes)
        #print("EXPLORE",random_reward)
        return (random_reward,rewards[random_reward])
