import numpy as np
import random
from game import *
from evaluate import *
from action import *
import sys
import matplotlib.pyplot as plt

PLAYERS = 3 # number of players including AI

num_episodes = 10000
max_steps_per_episode = 100

learn_rate = 0.1
discount_rate = 0.99

exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate = 0.01

rewards_all_episodes = []
games_won = 0

# action as string (MD5)

hash_list = get_hashlist()

q_table = np.zeros((len(hash_list),len(hash_list)))

print("hashlist has length",len(hash_list))

def get_id(cardhash:Card):
    return hash_list.index(cardhash.hexdigest())

winners = []
winnersx = []

for episode in range(num_episodes):
    # print("-------------")
    main_game = Game(PLAYERS)
    state = 0
    done = False
    rewards_current_episode = 0

    for step in range(0,max_steps_per_episode):
        exploration_rate_threshold = random.uniform(0,1)
        act = Action(main_game.all_decks(),main_game.get_draw_history(),main_game.get_direction(),main_game.get_compatible_cards(main_game.ai_deck()))
        state_value = act.state_key(main_game.get_top_card())
        if exploration_rate_threshold > exploration_rate:
            #print("EXPLOIT")
            idx,reward = select_option(act,0,q_table,state_value)
        else:
            #print(exploration_rate_threshold,exploration_rate)
            idx,reward = select_option(act,1,q_table,state_value)

        # STATE -> card on board -> CardType, CardNumber, CardColor
        # ACTION -> selected card -> CardType, CardNumber, CardColor

        if idx == main_game.ai_deck().get_size():
            idx = -1
            action_value = act.state_key("DRAW")
        else:
            action_value = act.state_key(main_game.ai_deck().peek_at(idx))

        # make the move

        next_play = main_game.play_turn(idx)

        if next_play != -1:
            if next_play == 0:
                games_won += 1
            winners.append(games_won)
            winnersx.append(len(winnersx))
            done = True

        new_state_value = act.state_key(main_game.get_top_card())

        # UPDATE THE Q TABLE

        q_table[get_id(state_value),get_id(action_value)] = int(q_table[get_id(state_value),get_id(action_value)]) * (1 - learn_rate) + learn_rate*(reward+discount_rate*np.max(q_table[get_id(new_state_value),:]))

        # add the reward

        rewards_current_episode += reward

        if done == True:
            break

    #exploration_rate = min_exploration_rate + (max_exploration_rate-(min_exploration_rate*np.exp(-exploration_decay_rate*episode)))
    exploration_rate = exploration_rate - (max_exploration_rate-min_exploration_rate)/num_episodes
    rewards_all_episodes.append(rewards_current_episode)

rewards_per_thousand_episodes = np.split(np.array(rewards_all_episodes),num_episodes/10)

# x = []
# y = []

count = 10
print("********Average reward per thousand episodes********")
for r in rewards_per_thousand_episodes:
    # x.append(count)
    # y.append(sum(r/10))
    # print(count,":",str(sum(r/10)))
    count += 10

print("REWARDS",sum(rewards_per_thousand_episodes[0])/10,sum(rewards_per_thousand_episodes[-1])/10)

# plt.plot(x,y)
# plt.xlabel("Episode")
# plt.ylabel("Reward")
# plt.title("Average Reward Over Time")
# plt.show()

np.set_printoptions(threshold=sys.maxsize)
print("********Q-Table********")
# print(q_table)

# print("out of",num_episodes,"games played, the agent won",games_won)