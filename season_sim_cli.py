###############################################################################
#  Command line interface for season sim - it sets up an intepreter and       #
#  allows contextual commands to modify the internal state                    #     
###############################################################################


import season_sim as ss
import team as team
import season_sim_errors as ss_err
import os.path

def startup():
	print("Welcome to season sim!")
	ss.startup()

	idle()


# Our main idle loop. From here, all commands are parsed and checked for
# validity
def idle():
	while True:
		cmd = input("SS intepreter 0.1 -> ").lower()

		if cmd == "n" or cmd =="new":
			if is_active_league():
				# TODO implement errors
				print("League already in progress, use (c) or (check) to check " + 
					"state")
			else:
				new_league()

		if cmd == "c" or cmd == "check":
			check_status()

		if cmd == "s" or cmd == "save":
			if is_active_league():
				save_league()

			else:
				print("No active league- cannot save")

		if cmd == "l" or cmd == "load":
			if is_active_league():
				# Double check with user if they already have an active league
				confirm = input("League already active- really load new one -> ").lower()

				if confirm == "yes" or confirm == "y":
					load_league()
			else:
				load_league()

		if cmd == "w" or cmd == "week":
			if is_active_league():
				sim_week()
			else:
				print("No active league to simulate")

		if cmd == "t" or cmd == "table":
			if is_active_league():
				print_table()
			else:
				print("No active league to show standings for")

# Simulates games and then prints the output
def sim_week():
	try:
		games = ss.simulate_week()
	except ss_err.EndOfSeasonError:
		print('Error: Cannot sim more as you have reached the end of the season')
		return

	for matchup in games:
		print("%s %d-%d %s" % (matchup[0], matchup[1], matchup[3], matchup[2]))

def print_table():
	top_row = get_header()

	print(top_row)

	print(get_second_row())

	for team in sorted(ss.state['teams'], key=lambda team: -ss.calc_team_points(team)):
		print(get_team_table_row(team))
	

def get_header():
	longest_name = length_of_longest_name()

	list_to_stringify = []

	list_to_stringify.append("Name")

	for i in range(longest_name - 4):
		list_to_stringify.append(" ")

	list_to_stringify.append("|")

	list_to_stringify.append(" W | L | T | Pts")

	return ''.join(list_to_stringify)

def get_second_row():
	longest_name = length_of_longest_name()

	list_to_stringify = []

	for i in range(longest_name):
		list_to_stringify.append("-")

	list_to_stringify.append("+")

	list_to_stringify.append("---+---+---+----")

	return ''.join(list_to_stringify)

def get_team_table_row(team):
	list_to_stringify = []

	list_to_stringify.append(team.name)

	for i in range(length_of_longest_name() - len(team.name)):
		list_to_stringify.append(" ")

	list_to_stringify.append("|")

	list_to_stringify.append(str(team.results['win']).rjust(3))

	list_to_stringify.append("|")

	list_to_stringify.append(str(team.results['loss']).rjust(3))

	list_to_stringify.append("|")

	list_to_stringify.append(str(team.results['tie']).rjust(3))

	list_to_stringify.append("|")

	list_to_stringify.append(str(ss.calc_team_points(team)).rjust(4))

	return ''.join(list_to_stringify)

def length_of_longest_name():
	longest_name = 0

	for team in ss.state['teams']:
		longest_name = max(longest_name, len(team.name))

	return longest_name

# This is often run as a check for commands that depend on if a league is 
# currently loaded or not
def is_active_league():
	return ss.state['active']

# This corresponds to the "new" command. It will guide the user through setting
# up a new league, by selecting team insertion and competition type
def new_league():
	print("""Beginning league setup-
		This will begin with inputting team names
		This uses the format [name] [off] [def]""")

	status = True

	# First, get the teams
	while status:
		status = get_new_team()

	# Now, make the schedule
	league_type = input("What type of league would you like? RR, DRR, or SE -> ")
	league_type_enum = ss.ScheduleType.ROUND_ROBIN

	# Insert logic for switching league type

	# Schedule the season
	sched = ss.schedule(type=league_type_enum)
	
	print("League scheduled")

	# Begin the season and make it active
	ss.init_league()
	print("League initialized")


# This will get user input, clean it if needed, and then pass it to the main
# season sim to add it in
def get_new_team():
	team_info = input("Team info (type DONE to finish adding teams)-> ")

	# Check to see if they quit
	if (team_info == "DONE"):
		return False

	team_info = team_info.split()

	# Validate that we get 3 inputs, and then ensure the second and third are
	# really numbers
	if (len(team_info) != 3 or type(team_info) is not list):
		print ("Must input 3 attributes to insert a new team")
		return True

	if (not is_number(team_info[1])) or (not is_number(team_info[2])):
		print ("Attributes 2 and 3 (offense and defense) must be numeric")
		return True

	ss.add_team_to_state(team_info[0], team_info[1], team_info[2])
	return True

def check_status():
	# This just outputs a quick look at the current league teams and schedule
	if not is_active_league():
		print("No league loaded")
		return

	print("Teams")
	print("--------------------------------------------------")
	for team in ss.state['teams']:
		print(team.name)

	print("\nSchedule for Week %d" % ss.state['current_week'])
	print("--------------------------------------------------")

	for matchup in ss.get_weekly_schedule():
		if 'BYE' not in matchup:
			print("%s vs. %s" % (ss.state['teams'][matchup[0]].name,
			 	ss.state['teams'][matchup[1]].name))

def save_league():
	save_name = input("What would you like to name your league save -> ")
	ss.save(save_name)

	print("League saved!")

def load_league():
	# TODO: print a list for the user to choose from
	ssf_file_name = input("What league would you like to load? ")

	if os.path.isfile("%s.ssf" % ssf_file_name):
		ss.load(ssf_file_name)
		print("League loaded!")
	else:
		print("No file with name %s.ssf exists" % ssf_file_name)



# Number validation tool stolen from 
# https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def main():
	startup()

if __name__ == "__main__":
    # execute only if run as a script
    main()

