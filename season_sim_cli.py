import season_sim as ss
import team as team

def startup():
	print("Welcome to season sim!\nWould you like to create a new league (N), or load an old league (L)?")

	choice = ""

	while (not choice):
		choice = input().lower()

		if (choice == "n" or choice == "new"):
			new_league()
		elif (choice == "l" or choice == "load"):
			load_league() #TODO
		else:
			print("Invalid option- please enter in (N) to create a new league, or (L) to load an old league")
			choice = ""

def new_league():
	print("Setting up new league...")

	print("Would you like to (L)oad in a new team from an input file, or (E)nter in teams manually?")

	choice = ""

	while (not choice):
		choice = input().lower()

		if (choice == "l" or choice == "load"):
			load_json_template() #TODO
		elif (choice == "e" or choice == "enter"):
			enter_league()
		else:
			print("Invalid option- please select to either (L)oad in a new team from an input file, or (E)nter in teams manually")
			choice = ""

def enter_league():
	print("We will begin with entering teams")

	team_name == ""

	while (team_name != "Done")
		team_name = input("Enter in team name: ")

		if not team_name:
			print ("Invalid team name")
			continue

		team_off = input("Enter team offensive rating (integer value please: ")

		


def enter_team():


def main():
	startup()

if __name__ == "__main__":
    # execute only if run as a script
    main()

