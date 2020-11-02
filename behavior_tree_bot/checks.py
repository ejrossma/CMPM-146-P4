def if_enemy_fleet(state):
    for fleet in state.enemy_fleets():
        for planet in state.my_planets():
            if fleet.destination_planet == planet.ID:
            	return True
    return False

def if_neutral_planet_available(state):
    return any(state.neutral_planets())

def if_free_planet(state):
    for target in state.enemy_planets():
        totalDefense = target.num_ships
        for fleet in state.enemy_fleets():
            if fleet.destination_planet == target.ID:
                totalDefense += fleet.num_ships
        for planet in state.my_planets():
            if planet.num_ships * 0.75 > totalDefense + 1:
                return True
    return False