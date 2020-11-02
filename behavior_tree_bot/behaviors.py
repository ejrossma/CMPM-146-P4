import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
from heapq import heappop, heappush
from math import ceil

'''
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
'''

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
    #check the cost from planet to neutral
    #find smallest value and check if less than best option
    #issue order on the best option

    best_options = []
    for planet in state.neutral_planets():
        possible_route = []
        for my_planet in state.my_planets():
            if my_planet.num_ships > planet.num_ships and not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets()):
                calculated_cost = planet.growth_rate * -1
                heappush(possible_route, (calculated_cost, my_planet, planet))

        if possible_route:
            best = heappop(possible_route)
            closest_enemy = 100
            for planet in state.enemy_planets():
                temp = state.distance(planet.ID, best[2].ID)
                if (temp < closest_enemy):
                    closest_enemy = temp
            closest_planet = 100
            for planet in state.my_planets():
                temp = state.distance(planet.ID, best[2].ID)
                if (temp < closest_enemy):
                    closest_planet = temp
            if closest_enemy >= closest_planet and not any(fleet.destination_planet == best[1].ID for fleet in state.enemy_fleets()):
                heappush(best_options, best)

    while best_options:
        order = heappop(best_options)
        issue_order(state, order[1].ID, order[2].ID, order[2].num_ships + 1)
        for route in best_options:
            if route[1].num_ships < route[2].num_ships:
                best_options.remove(route)
    return False

def howManyShips(planet):
    return planet.num_ships

def intercept_plan(state):
    if not state.enemy_fleets():
        return False
    closestAttack = 100
    enemy_fleets = state.enemy_fleets()
    closestFleet = enemy_fleets[0]

    for fleet in state.enemy_fleets():
        for planet in state.my_planets():
            if fleet.destination_planet == planet.ID:
                if fleet.turns_remaining < closestAttack:
                    closestAttack = fleet.turns_remaining
                    closestFleet = fleet

    #if not closestFleet.destination_planet == planet.ID:
        #return False
            
    defensePower = 0
    increaseScope = 0
    defendingPlanets = []
    ships = 0
    for planets in state.my_planets():
        ships += planets.num_ships
    if ships < closestFleet.num_ships:
        return False

    start_defense = 0
    dest_growth_rate = 0
    for planet in state.my_planets():
        if planet.ID == closestFleet.destination_planet:
            dest_growth_rate = planet.growth_rate
            start_defense = planet.num_ships + closestFleet.turns_remaining * planet.growth_rate
            defensePower = start_defense

    while defensePower < closestFleet.num_ships:
        defendingPlanets = [planet for planet in state.my_planets() if state.distance(planet.ID, closestFleet.destination_planet) <= closestFleet.turns_remaining + increaseScope]
        for planet in defendingPlanets:
            defensePower += planet.num_ships
        increaseScope += 1
        
    if not defendingPlanets:
        return False
    requiredContribution = ceil((closestFleet.num_ships + (increaseScope * dest_growth_rate) - start_defense)  / len(defendingPlanets)) + 1

    defendingPlanets.sort(key=howManyShips)

    final_check = []
    compensation = 0
    for planet in defendingPlanets:
        if planet.num_ships < requiredContribution:
            temp = requiredContribution - planet.num_ships - 1
            compensation += temp
            final_check.append((planet.num_ships - 1, planet))
        elif planet.num_ships > requiredContribution + compensation:
            final_check.append((requiredContribution + compensation, planet))
            compensation = 0
        else:
            temp = compensation - (requiredContribution + compensation - (planet.num_ships - 1))
            compensation -= temp
            final_check.append((requiredContribution + temp, planet))


    for planet in final_check:
        skip = 0
        for fleet in state.my_fleets():
            if fleet.source_planet == planet[1].ID and fleet.destination_planet == closestFleet.destination_planet:
                skip = 1
        if skip == 0:
            issue_order(state, planet[1].ID, closestFleet.destination_planet, planet[0])
    return False

def free_planet_plan(state):
    for myplanet in state.my_planets():
        for planet in state.enemy_planets():
            skip = 0
            distanceBetween = state.distance(myplanet.ID, planet.ID)
            if myplanet.num_ships * 0.75 >= planet.num_ships + distanceBetween * planet.growth_rate:
                for fleet in state.my_fleets():
                    if fleet.source_planet == myplanet.ID and fleet.destination_planet == planet.ID:
                        skip = 1
                if skip == 0:
                    return issue_order(state, myplanet.ID, planet.ID, 1 + planet.num_ships + distanceBetween * planet.growth_rate)
    return False