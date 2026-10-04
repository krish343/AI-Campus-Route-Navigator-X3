"""Regression tests for the routing rules and search algorithms."""

import unittest

from agents import Orbit, Pathfinder
from campus_map import load_campus
from config import CSE_LIFT, CSE_ZONE, TOWER_ENTRIES


class RoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = load_campus()
        cls.pathfinder = Pathfinder(cls.graph)
        cls.orbit = Orbit(cls.graph)

    def test_known_route_is_found(self):
        result = self.orbit.solve("Canteen, CU Technology Campus", "New Building 2 (Workshop Building)")
        self.assertEqual(result.cost, 290)
        self.assertTrue(result.found)

    def test_cse_entry_uses_tower_lift_then_cse(self):
        result = self.orbit.solve("Entry Gate 1 (G1)", "CSE Laboratory")
        locations = result.route
        cse_index = next(i for i, name in enumerate(locations) if name in CSE_ZONE)
        self.assertGreaterEqual(cse_index, 2)
        self.assertEqual(locations[cse_index - 1], CSE_LIFT)
        self.assertIn(locations[cse_index - 2], TOWER_ENTRIES)

    def test_cse_start_must_exit_via_lift_and_tower_entry(self):
        result = self.orbit.solve("CSE_Reflexon Room", "Entry Gate 4 (G4)")
        route = result.route
        self.assertGreaterEqual(len(route), 4)
        # Starting inside CSE must follow the same controlled exit path.
        self.assertIn("Lift Area", route[1:])
        lift_index = route.index("Lift Area")
        self.assertGreater(lift_index, 0)
        self.assertIn(route[lift_index + 1], TOWER_ENTRIES)

    def test_both_agents_return_a_route_for_each_experiment(self):
        cases = (
            ("Reception of Calcutta University", "Library"),
            ("Library", "Canteen, CU Technology Campus"),
            ("CSE_Reflexon Room", "Entry Gate 4 (G4)"),
        )
        for start, goal in cases:
            self.assertTrue(self.pathfinder.solve(start, goal).found)
            self.assertTrue(self.orbit.solve(start, goal).found)


if __name__ == "__main__":
    unittest.main()
