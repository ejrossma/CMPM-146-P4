#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn

# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():

    #Spreading Strategy:
        #ran at the beginning of the game
        #stop when our growth rate is greater than the enemies potential growth rate
            #player_growth_rate = 0
            #for planet in my_planets()
                #player_growth_rate += planet.growth_rate
            #enemy_growth_rate = 0    
            #for planet in my_planets()
                #enemy_growth_rate += planet.growth_rate


        #find closest planets
        #if possible fleet is greater than planet number
            #send fleet size equal to planet size + 1
        #send up to 4 at a time

    #Defending Strategy:
        
        #where enemy is sending fleets
        #how big the fleet is (and how much longer until it reaches planet)
        #calculate if we can defend by sending from planets that are a short enough distance away to reach in time 
            #(less than or equal to enemy_fleet.turns_remaining)

        #if we can't defend at a close distance increase the scope and try to defend with more planets


        #if we lose a planet trample it with all of our not defending resources

    #Punish the Opponent Strategy:

        #if our effective attack power (distance, fleet power in distance, planet growth) 
        #is greater than 
        #our opponents effective defense power (distance, fleet power in distance, planet growth)
        #then capture the planet

        #if it isn't greater start to move resources towards the frontier


    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')

    offensive_plan = Sequence(name='Offensive Strategy')
    largest_fleet_check = Check(have_largest_fleet)
    attack = Action(attack_weakest_enemy_planet)
    offensive_plan.child_nodes = [largest_fleet_check, attack]

    spread_sequence = Sequence(name='Spread Strategy')
    neutral_planet_check = Check(if_neutral_planet_available)
    spread_action = Action(spread_to_weakest_neutral_planet)
    spread_sequence.child_nodes = [neutral_planet_check, spread_action]

    root.child_nodes = [offensive_plan, spread_sequence, attack.copy()]

    logging.info('\n' + root.tree_to_string())
    return root

# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
