from enum import Enum

import team
import random

# TODO parse args

class ScheduleType(Enum):
	ROUND_ROBIN = 1
	DOUBLE_ROUND_ROBIN = 2
	SINGLE_ELIMINATION = 3

class MatchupResult(Enum):
	HOME_WIN = 1
	AWAY_WIN = 2
	TIE = 3

def schedule(num_teams, type=ScheduleType.ROUND_ROBIN):
	# TODO schedule types, validate num_teams (do we do that in this function, 
	# or a higher one?)

	# Should we shuffle teams?

	'''
		This produces a schedule of the form map<int, list<tuple>>

		It maps week numbers to the weekly schedule for that week

		Weekly schedules are just lists of tuples containing the two teams 
		that are playing
	'''
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

	return schedule

# A basic matchup simulator
def flip_coin(home, away):
	flip = random.randint(0, 1)

	return (1, 0) if flip == 0 else (0, 1)

def simulate_matchup(home, away, simulator=flip_coin):
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

def home_win(home, away):
	return (1, 0)


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

#def main():
	#generated_schedule = schedule(5)
	#print(generated_schedule)

if __name__ == "__main__":
    # execute only if run as a script
    main()


