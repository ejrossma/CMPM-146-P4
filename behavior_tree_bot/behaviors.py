import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
from heapq import heappop, heappush


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_until_advantaged(state):
    # (1) return false if the player's total growth per turn is greater than the opponents possible growth per turn
    # (2) iterate through all of the planets and do a strength calculation (that judges ships lost vs distance traveled) to find most efficient planet to travel to
    # (3) send out a fleet equal to the cost of the target planet + 1
    #TODO NEED TO IMPLEMENT A BETTER CALCULATION ON WHERE TO SPREAD
    #ALSO NEED TO READ WHERE ENEMY IS SENDING FLEETS AND SEND OURS TO ARRIVE JUST AFTER 
    #SO THEY DO THE WORK ON THE NEUTRAL PLANETS FOR US
    
    player_growth_rate = 0
    for planet in state.my_planets():
        player_growth_rate += planet.growth_rate

    enemy_possible_growth_rate = 0
    for planet in state.enemy_planets():
        enemy_possible_growth_rate += planet.growth_rate
    for planet in state.neutral_planets():
        enemy_possible_growth_rate += planet.growth_rate

    if enemy_possible_growth_rate < player_growth_rate:
        return False
    
    #go through all neutral planets
    #for each planet in my planets
    #check the distance from planet to neutral
    #find smallest value and check if less than best option
    #issue order on the best option

    best_options = []
    for planet in state.neutral_planets():
        possible_route = []
        for my_planet in state.my_planets():
            if my_planet.num_ships > planet.num_ships and not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets()):
                calculated_cost = state.distance(planet.ID, my_planet.ID) + planet.num_ships + (planet.num_ships / planet.growth_rate)
                heappush(possible_route, (calculated_cost, my_planet, planet))
        if possible_route:
            best = heappop(possible_route)
            heappush(best_options, best)
    if best_options:
        order = heappop(best_options)
        return issue_order(state, order[1].ID, order[2].ID, order[2].num_ships + 1)
    else:
        return False
    '''
    while best_options:
        order = heappop(best_options)
        issue_order(state, order[1].ID, order[2].ID, order[2].num_ships + 1)
        for route in best_options
            if route[1].num_ships < route[2].num_ships:
                best_options.remove(route)
    return False
    '''