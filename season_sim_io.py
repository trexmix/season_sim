###############################################################################
#  This is the I/O module for season_sim. It's purpose is to convert to and   #
#  from the raw python into a human readable file. It should be called with   #
#  save_state() and load_state() - the rest is private implementation         #     
###############################################################################


import json
import team

def convert_to_serializable(state):
	# Teams is not serializable because they are objects. This will convert
	# them into dictionaries so that you can pass the state in to json
	serializable_state = {}
	serializable_state['schedule'] = state['schedule']
	serializable_state['current_week'] = state['current_week']

	serializable_state['teams'] = []

	for team in state['teams']:
		serializable_state['teams'].append(vars(team))

	return serializable_state

def save_state(state, save_name):
	# Saves the current state of the program
	serializable_state = convert_to_serializable(state)

	with open(save_name, "w") as save_file:
		json.dump(serializable_state, save_file)


def convert_from_serialized(serialized_state):
	# Converts teams back into a python object

	state = {}

	# This is pretty gross - json decodes back in as lists and not the tuples
	# that we were expecting so we have to convert schedule back to the 
	# dictionary mapping a number to puples of tuples
	state['schedule'] = {}

	for week, matchups in serialized_state['schedule'].items():
		list_of_matchups = []

		for matchup in matchups:
			list_of_matchups.append(tuple(matchup))

		tuple_of_matchups = tuple(list_of_matchups)

		state['schedule'][int(week)] = tuple_of_matchups

	state['current_week'] = serialized_state['current_week']

	# We also have to transform teams from a dictionary back into a Python
	# class
	state['teams'] = []

	for team_map in serialized_state['teams']:
		state['teams'].append(team.Team(team_map['name'],
			offense=team_map['offense'], 
			defense=team_map['defense'],
			wins=team_map['results']['win'],
			losses=team_map['results']['loss'], 
			tie=team_map['results']['tie']))

	return state


def load_state(save_name):
	# Loads the current state

	serialized_state = {}

	with open(save_name, "r") as save_file:
		serialized_state = json.load(save_file)

	return convert_from_serialized(serialized_state)




