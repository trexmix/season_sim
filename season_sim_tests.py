###############################################################################
#  This is a testing suite for the Season Sim program. Run it like a normal   #
#  python program to ensure correctness                                       #     
###############################################################################

import unittest
import os

import season_sim as ss
import season_sim_io as ss_io
import team

class TestRRScheduling(unittest.TestCase):
    # We set up a 5 team round robin schedule. Should generalize this method
    # to n teams and iterate
    def setUp(self):
        self.sched = ss.round_robin_schedule(5)
        self.all_teams = [0, 1, 2, 3, 4, 'BYE']

    # Check that we get a 5 week schedule, as expected
    def test_schedule_length(self):
        self.assertEqual(len(self.sched), 5)

    def test_team_opponents(self):
        # This test ensures that each team has the correct opponents
        for team in range(5):
            opponents = []
            # We have to make a new list here to avoid mutations
            correct_opponents = self.all_teams[:]
            correct_opponents.remove(team)

            # We go in here and add in whichever team we face every week
            for week in self.sched.keys():
                opponents.append(ss.check_opponent(team, self.sched, week))

            # We need to check for two things- a) that no opponent is faced
            # more than once and that b) every opponent, including a bye, is
            # faced once! Uses subText context manager to isolate instances in 
            # which only some teams have incorrect schedules
            with self.subTest(team=team):
                self.assertFalse(any(opponents.count(x) > 1 for x in opponents))
                self.assertEqual(set(opponents), set(correct_opponents))


class TestMatchups(unittest.TestCase):
    def setUp(self):
        self.teams = []

        self.teams.append(team.Team("Team A"))
        self.teams.append(team.Team("Team B"))
        self.teams.append(team.Team("Team C"))
        self.teams.append(team.Team("Team D"))
        self.teams.append(team.Team("Team E"))

        self.schedule = ss.round_robin_schedule(5)

    def test_single_matchup(self):
        # Test a single game in which the home team wins
        ss.simulate_matchup(self.teams[0], self.teams[1], ss.home_win)

        # Ensure team stats are correct
        self.assertEqual(self.teams[0].results['win'], 1)
        self.assertEqual(self.teams[0].results['loss'], 0)
        self.assertEqual(self.teams[0].results['tie'], 0)

        self.assertEqual(self.teams[1].results['win'], 0)
        self.assertEqual(self.teams[1].results['loss'], 1)
        self.assertEqual(self.teams[1].results['win'], 0)

    def test_season(self):
        ss.state['teams'] = self.teams

        ss.simulate_season(self.schedule)

        wins = 0
        losses = 0

        # Iterate through every team and make sure they've played 4 games
        for team in ss.state['teams']:
            #print(teams.name, " ", teams.results)
            self.assertEqual(sum(team.results.values()), 4)

            wins += team.results['win']
            losses += team.results['loss']

        # Make sure we have the same number of wins and losses
        self.assertEqual(wins, losses)

class TestUtilities(unittest.TestCase):
    def test_rotation(self):
        l = [1, 2, 3]
        self.assertEqual(ss.rotate(l, 1), [3, 1, 2])    

class TestIO(unittest.TestCase):
        
    def setUp(self):
        # We need to remove old dump to ensure that we are writing to a clean
        # file
        if os.path.isfile("testing.ssd"):
            os.remove("testing.ssd")

        self.teams = []

        self.teams.append(team.Team("Team A"))
        self.teams.append(team.Team("Team B"))
        self.teams.append(team.Team("Team C"))
        self.teams.append(team.Team("Team D"))
        self.teams.append(team.Team("Team E"))

        self.schedule = ss.round_robin_schedule(5)

        self.state = {}
        self.state['teams'] = self.teams
        self.state['schedule'] = self.schedule
        self.state['current_week'] = 0

    def tearDown(self):
        # Don't want any traces of testing
        if os.path.isfile("testing.ssd"):
            os.remove("testing.ssd")

    def test_save(self): 
        ss_io.save_state(self.state, "testing.ssd")

        # Initially, we just want to check that the output is *something*
        # May add more testing later but it seems to work
        self.assertTrue(os.path.isfile("testing.ssd"))

    def test_loading_init_data(self):
        ss_io.save_state(self.state, "testing.ssd")
        new_state = ss_io.load_state("testing.ssd")

        # Note that we have edited team class to check for deep equality rather
        # than shallow equality
        self.assertTrue(new_state == self.state)

    def test_loading_mid_season(self):
        ss.state['teams'] = self.teams

        ss.simulate_week(self.schedule, 1)
        ss.simulate_week(self.schedule, 2)

        ss_io.save_state(self.state, "testing.ssd")
        new_state = ss_io.load_state("testing.ssd")

        # TODO: weird inconsistencies where we have some objects in ss's state
        # object while others are free. Need to check against season sim's
        # state because the teams will be updated
        self.assertTrue(new_state['teams'] == ss.state['teams'])



if __name__ == '__main__':
    unittest.main()