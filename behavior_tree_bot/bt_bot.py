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

    #Punish the Opponent Strategy:

        #if our effective attack power (distance, fleet power in distance, planet growth) 
        #is greater than 
        #our opponents effective defense power (distance, fleet power in distance, planet growth)
        #then capture the planet

        #if it isn't greater start to move resources towards the frontier


    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')

    acquire_freebies = Sequence(name= 'Free Planets Strategy')
    free_planet_check = Check(if_free_planet)
    attack = Action(free_planet_plan)
    acquire_freebies.child_nodes = [free_planet_check, attack]

    defensive_plan = Sequence(name='Defensive Strategy')
    enemy_fleet_check = Check(if_enemy_fleet)
    defend = Action(intercept_plan)
    defensive_plan.child_nodes = [enemy_fleet_check, defend]

    spread_sequence = Sequence(name='Spread Strategy')
    neutral_planet_check = Check(if_neutral_planet_available)
    spread_action = Action(spread_until_advantaged)
    spread_sequence.child_nodes = [neutral_planet_check, spread_action]

    root.child_nodes = [acquire_freebies, defensive_plan, spread_sequence]

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
