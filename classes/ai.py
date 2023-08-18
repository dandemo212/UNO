import numpy as np
import random
from game import *
from evaluate import *
from action import *
import sys

PLAYERS = 5 # number of players including AI

num_episodes = 10000
max_steps_per_episode = 100

learn_rate = 0.1
discount_rate = 0.99

exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate = 0.01

rewards_all_episodes = []

key_mapping = [] #dictionary mapping keys to indices on the q table



hash_list = get_hashlist()

q_table = np.zeros((len(hash_list),len(hash_list)))

def get_id(cardhash:Card):
    return hash_list.index(cardhash.hexdigest())

# def get_coords(state,action=None):
#     state_idx = 0
#     action_idx = 0
#     if state in key_mapping:
#         print(state.hexdigest(),"is in key mapping")
#         state_idx = key_mapping[state]
#     else:
#         print(state.hexdigest(),"is not in key mapping")
#         key_mapping.append({state.hexdigest():len(key_mapping)})
#         state_idx = len(key_mapping)
#     if action == None:
#         return int(state_idx)
#     if action in key_mapping:
#         action_idx = key_mapping[action]
#     else:
#         key_mapping.append({action.hexdigest():len(key_mapping)})
#         action_idx = len(key_mapping)
#     return (int(state_idx),int(action_idx))

# action as string (MD5)

for episode in range(num_episodes):
    # print("-------------")
    main_game = Game(PLAYERS)
    state = 0
    done = False
    rewards_current_episode = 0

    for step in range(0,max_steps_per_episode):
        # print("turn",step)
        exploration_rate_threshold = random.uniform(0,1)
        act = Action(main_game.all_decks(),main_game.get_draw_history(),main_game.get_direction(),main_game.get_compatible_cards(main_game.ai_deck()))
        if exploration_rate_threshold > exploration_rate:
            idx,reward = select_option(act,1)
        else:
            #explore
            idx,reward = select_option(act,0)

        # STATE -> card on board -> CardType, CardNumber, CardColor
        # ACTION -> selected card -> CardType, CardNumber, CardColor

        state_value = act.state_key(main_game.get_top_card())
        # print("state",main_game.get_top_card())
        if idx == main_game.ai_deck().get_size():
            idx = -1
            action_value = act.state_key("DRAW")
            #print("action","DRAW")
        else:
            action_value = act.state_key(main_game.ai_deck().peek_at(idx))
            #print("action",main_game.ai_deck().peek_at(idx))

        # make the move

        next_play = main_game.play_turn(idx)

        if next_play != -1:
            done = True

        new_state_value = act.state_key(main_game.get_top_card())

        # UPDATE THE Q TABLE

        # print("COORDS")
        # print(get_id(state_value),get_id(action_value))
        # print("QVAL---")
        # print(q_table[get_id(state_value),get_id(action_value)])
        # print((1 - learn_rate))
        # print(reward)
        # print(discount_rate)
        # print(np.max(q_table[get_id(new_state_value),:]))
        # print(
        #     str(
        #         int(
        #             q_table[get_id(state_value),get_id(action_value)]
        #             )
        #         * 
        #         (1 - learn_rate) 
        #         + 
        #         learn_rate
        #         *
        #         (
        #             reward
        #             +
        #             discount_rate
        #             *
        #             np.max(q_table[get_id(new_state_value),:])
        #         )
        #       )
        #     )

        q_table[get_id(state_value),get_id(action_value)] = int(q_table[get_id(state_value),get_id(action_value)]) * (1 - learn_rate) + learn_rate*(reward+discount_rate*np.max(q_table[get_id(new_state_value),:]))

        # add the reward

        rewards_current_episode += reward

        if done == True:
            #print("WE HAVE A WINNER",str(next_play))
            break

    exploration_rate = min_exploration_rate + (max_exploration_rate-min_exploration_rate*np.exp(-exploration_decay_rate*episode))

    rewards_all_episodes.append(rewards_current_episode)

rewards_per_thousand_episodes = np.split(np.array(rewards_all_episodes),num_episodes/1000)

count = 1000
print("********Average reward per thousand episodes********")
for r in rewards_per_thousand_episodes:
    print(count,":",str(sum(r/1000)))
    count += 1000

np.set_printoptions(threshold=sys.maxsize)
print("********Q-Table********")
print(q_table)