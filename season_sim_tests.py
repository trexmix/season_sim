###############################################################################
#  This is a testing suite for the Season Sim program. Run it like a normal   #
#  python program to ensure correctness                                       #     
###############################################################################

import unittest
import season_sim as ss

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


class TestUtilities(unittest.TestCase):
    def test_rotation(self):
        l = [1, 2, 3]
        self.assertEqual(ss.rotate(l, 1), [3, 1, 2])            

if __name__ == '__main__':
    unittest.main()