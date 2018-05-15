from enum import Enum

import team
import random
import season_sim_io as ss_io
import season_sim_errors as ss_err

# TODO parse args

# Contains the state of the current simulation- teams, week, right now
state = {}

state['active'] = False
state['teams'] = []
state['schedule'] = {}
state['current_week'] = 0
# A list of games- should have home team, away team, home score, and
# away score. Not implemented
state['game_log'] = []

state['config'] = {}

state['config']['POINTS_ON_WIN'] = 3
state['config']['POINTS_ON_LOSS'] = 0
state['config']['POINTS_ON_TIE'] = 1

class ScheduleType(Enum):
	ROUND_ROBIN = 1
	DOUBLE_ROUND_ROBIN = 2
	SINGLE_ELIMINATION = 3

class MatchupResult(Enum):
	HOME_WIN = 1
	AWAY_WIN = 2
	TIE = 3

# This should run whenever intepreter is fired up
def startup():
	state['active'] = False
	state['teams'] = []
	state['schedule'] = {}
	state['current_week'] = 0
	# A list of games- should have home team, away team, home score, and
	# away score. Not implemented
	state['game_log'] = []

###############################################################################
# Scheduling functions                                                        #
###############################################################################

def schedule(num_teams=0, type=ScheduleType.ROUND_ROBIN):
	# TODO schedule types, validate num_teams (do we do that in this function, 
	# or a higher one?)

	# Should we shuffle teams?

	'''
		This produces a schedule of the form map<int, list<tuple>>

		It maps week numbers to the weekly schedule for that week

		Weekly schedules are just lists of tuples containing the two teams 
		that are playing
	'''

	# If number of teams is default argument, check the state to see how many
	# teams we should schedule for
	if num_teams == 0:
		num_teams = len(state['teams'])

	return round_robin_schedule(num_teams)

# This is based on the first algorithm found at 
# https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm
# We have two rows that correspond to matchups, and rotate the rows clockwise
# every week until we get every possible matchup
def round_robin_schedule(num_teams):
	schedule = {}

	top_row = list(range(0, num_teams // 2))
	bot_row = list(range(num_teams // 2, num_teams))

	# If we have an odd number of teams, need to insert a dummy team. We do it
	# in the top as that is the one that will have less elements in the odd
	# case
	if num_teams % 2 == 1:
		top_row.append("BYE")

	# Weird range- want to have a week 1 and not a week 0. In addition number
	# of weeks is dependent on the number on both the number of teams but also
	# the parity as odd teams will take one more. Adding the dummy guarentees 
	# that the combined length of the lists is correct
	for week in range(1, len(top_row) + len(bot_row)):
		# Get the weeks pairings- this is as easy as looping through every row
		weeks_pairings = []

		for matchup_number in range(len(top_row)):
			weeks_pairings.append((top_row[matchup_number], bot_row[matchup_number]))

		weeks_pairings = tuple(weeks_pairings)

		schedule[week] = weeks_pairings

		# Now we have to rotate the rows. We keep the first element in the top
		# row constant, but rotate the rest clockwise (to the right), whereas 
		# on the bottom, clockwise is to the left
		top_row = [top_row[0]] + rotate(top_row[1:], 1)
		bot_row = rotate(bot_row, -1)

		tmp = top_row[1]
		top_row[1] = bot_row[-1]
		bot_row[-1] = tmp

	state['schedule'] = schedule
	return schedule

###############################################################################
# Various simulators                                                          #
###############################################################################

# A basic matchup simulator
def flip_coin(home, away):
	flip = random.randint(0, 1)

	return (1, 0) if flip == 0 else (0, 1)

def biased_proportional(home, away, bias=10):
	home_score = 0
	away_score = 0

	for inning in range(5):
		home_attempt = random.randint(1, (int(home.offense) + int(away.defense) + 2 * bias))

		if (home_attempt <= int(home.offense) + bias):
			home_score += 1

		away_attempt = random.randint(1, (int(away.offense) + int(home.defense) + 2 * bias))

		if (away_attempt <= int(away.offense) + bias):
			away_score += 1

	return (home_score, away_score)

def home_win(home, away):
	# Basic schedule to always have the home team win for debugging
	return (1, 0)

###############################################################################
# Levels of simulation- matchup, week, seaons                                 #
###############################################################################

def simulate_matchup(home, away, simulator=biased_proportional):
	'''
	Simulates a matchup using the simulator function and updates home and away
	team results

	Simulator takes in home, away team objects and returns a tuple of the form
	(home_score, away_score)
	'''
	home_score, away_score = simulator(home, away)

	if home_score > away_score:
		home.results['win'] += 1
		away.results['loss'] += 1
	elif home_score < away_score:
		home.results['loss'] += 1
		away.results['win'] += 1
	elif home_score == away_score:
		home.results['tie'] += 1
		away.results['tie'] += 1

	game = {
		'home_team': home.name,
		'away_team': away.name,
		'home_score': home_score,
		'away_score': away_score,
	}

	return (home.name, home_score, away.name, away_score)

	#state['game_log'].append()

def simulate_week(schedule=None, week=None, advance=True):
	# Default variables will lead to the simulator drawing it from the current
	# state. Returns tuple of (home, home score, away, away score) to give the 
	# various GUIs the ability to display the results of the week

	if (schedule == None):
		schedule = state['schedule']

	if (week == None):
		week = state['current_week']

	if (week > len(schedule)):
		raise ss_err.EndOfSeasonError('Trying to simulate past end of season', None)
		return

	games = []

	for home, away in schedule[week]:
		# If the matchup does not involve a bye, we need to simulate it
		if ('BYE' not in (home, away)):
			games.append(simulate_matchup(state['teams'][home], state['teams'][away]))

	if advance:
			state['current_week'] += 1

	return games

def simulate_season(schedule=None):
	# Go through each week in the schedule
	if (schedule == None):
		schedule = state['schedule']

	games = []

	for week in range(state['current_week'], len(schedule) + 1):
		games.append(simulate_week(schedule, week))

###############################################################################
# Utilities                                                                   #
###############################################################################

# https://stackoverflow.com/questions/9457832/python-list-rotation gives this
# function- it rotates a list n positions to the right
def rotate(list, n):
    return list[-n:] + list[:-n]

# Utility function- given a team and schedule, it tells you who they play on
# that specific week
def check_opponent(team, schedule, week=1):
	weekly_schedule = schedule[week]

	for match in weekly_schedule:
		if team in match:
			if team == match[0]:
				return match[1]
			else:
				return match[0]

	# TODO add error handling here

def get_weekly_schedule(week=0):
	if (week == 0):
		week = state['current_week']

	return state['schedule'][week]

def add_team_to_state(team_name, team_off, team_def):
	state['teams'].append(team.Team(team_name, offense=team_off, defense=team_def))

def confirm_schedule(schedule):
	state['schedule'] = schedule

def init_league():
	state['active'] = True
	state['current_week'] = 1

def calc_team_points(team):
	return team.results['win'] * state['config']['POINTS_ON_WIN'] \
		+ team.results['tie'] * state['config']['POINTS_ON_TIE'] \
		+ team.results['loss'] * state['config']['POINTS_ON_LOSS']

###############################################################################
# I/O Wrappers                                                                #
###############################################################################

def save(save_name):
	ss_io.save_state(state, "%s.ssf" % save_name)

def load(ssf_file_name):
	# Needs to declare state as global or it will just create a local copy
	# of state that is destroyed at the end of the function
	global state

	state = ss_io.load_state("%s.ssf" % ssf_file_name)

	state['active'] = True

	if "config" not in state.keys():
		# Maintain backwards compatability with saves with no config
		state['config'] = {}

		state['config']['POINTS_ON_WIN'] = 3
		state['config']['POINTS_ON_LOSS'] = 0
		state['config']['POINTS_ON_TIE'] = 1