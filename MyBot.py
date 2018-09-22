# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 13:55:16 2018
@author: Richard
"""

# keep these three import statements
import game_API
import fileinput
import json

# your import statements here
import random

first_line = True # DO NOT REMOVE

# global variables or other functions can go here
stances = ["Rock", "Paper", "Scissors"]
count_rock = 0
count_paper = 0
count_scissors = 0

def get_winning_stance(stance):
    if stance == "Rock":
        return "Paper"
    elif stance == "Paper":
        return "Scissors"
    elif stance == "Scissors":
        return "Rock"

def priority(monster):
    pos = a * monster.death_effects.health + b * monster.death_effects.speed + c * monster.death_effects.rock + d * monster.death_effects.paper + e * monster.death_effects.scissors
    neg = f * moves_to_get_there(monster) + g * moves_to_beat_monster(monster) + h * get_health_damage(monster)
    return pos - neg # formula

def moves_to_get_there(monster):
    path = game.shortest_paths(me.location, monster.location)
    moves = (7 - me.speed) * len(path[0])
    if monster.dead == False:
        return moves
    return monster.respawn_counter if monster.respawn_counter > moves else moves

def moves_to_beat_monster(monster):
    chosen_stance = get_winning_stance(monster.stance)
    if chosen_stance == "Paper":
        stat = me.paper 
    elif chosen_stance == "Scissors":
        stat = me.scissors
    elif chosen_stance == "Rock":
        stat = me.rock

    return monster.health / stat

def get_health_damage(monster):
    return moves_to_beat_monster(monster) * monster.attack

def predict_player_move():
    if count_rock > count_paper and count_rock > count_scissors and count_rock != 0:
        return("Paper")
    elif count_scissors > count_rock and count_scissors > count_paper and count_scissors != 0:
        return("Rock")
    elif count_paper > count_rock and count_paper > count_scissors and count_paper != 0:
        return("Scissors")
    else:
        return(stances[random.randint(0, 2)])




# main player script logic
# DO NOT CHANGE BELOW ----------------------------
"""
a = health benefits
b = speed benefits
c = rock benefits
d = paper benefits
e = scissor benefits
f = moves to get there
g = moves to beat monster
h = health damage

0 = Rock
1 = Paper
2 = Scissors
"""

for line in fileinput.input():
    if first_line:
        game = game_API.Game(json.loads(line))
        first_line = False
        continue
    game.update(json.loads(line))
# DO NOT CHANGE ABOVE ---------------------------

# code in this block will be executed each turn of the game
    
    me = game.get_self()
    opponent = game.get_opponent()
    a=0.1
    b=0.1
    c=0.1
    d=0.1
    e=0.1
    f=0.1
    g=0.1
    h=0.1

    if game.get_turn_num() <= 45:
    # prioritize speed for the first 45 turns
        a=0
        b=1
        c=0
        d=0
        e=0
        f=0
        g=0
        h=0

    if game.get_turn_num() >= 250:
        if me.health <= opponent.health:
        # prioritize health and health damage
            a=1
            b=0.1
            c=0.1
            d=0.1
            e=0.1
            f=0.5
            g=0.5
            h=1


    if me.location == me.destination: # check if we have moved this turn
    # create list of the priority level for each monster
        allmonsters = game.get_all_monsters()
        mlist = []
        for monster in allmonsters:
            mlist.append(priority(monster))

    # choose monster with max priority
        maxpriority = mlist.index(max(mlist))
        target = allmonsters[maxpriority]

    # get the set of shortest paths to that monster
        paths = game.shortest_paths(me.location, target.location)
        destination_node = paths[random.randint(0, len(paths)-1)][0]
    # choose monster with max priority
    else:
        destination_node = me.destination

    if opponent.location == me.location:
        if opponent.stance == "Rock":
            count_rock+=1
        elif opponent.stance == "Paper":
            count_paper+=1
        elif opponent.stance == "Scissors":
            count_scissors+=1



    if game.has_monster(me.location):
    # if there's a monster at my location, choose the stance that damages that monster
        chosen_stance = get_winning_stance(game.get_monster(me.location).stance)
    else:
    # otherwise, pick a random stance
        chosen_stance = predict_player_move()


# submit your decision for the turn (This function should be called exactly once per turn)
    game.submit_decision(destination_node, chosen_stance)