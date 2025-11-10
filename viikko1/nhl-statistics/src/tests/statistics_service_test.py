import unittest
from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_search_finds_existing_player(self):
        player = self.stats.search("Semenko")
        self.assertIsNotNone(player)
        self.assertEqual(player.name, "Semenko")

    def test_search_returns_none_for_nonexistent_player(self):
        player = self.stats.search("Nonexistent")
        self.assertIsNone(player)

    def test_team_returns_players_from_correct_team(self):
        edm_players = self.stats.team("EDM")
        self.assertEqual(len(edm_players), 3)
        for player in edm_players:
            self.assertEqual(player.team, "EDM")

    def test_team_returns_empty_list_for_nonexistent_team(self):
        players = self.stats.team("NYR")
        self.assertEqual(len(players), 0)

    def test_top_returns_correct_number_of_players(self):
        top_players = self.stats.top(2)
        self.assertEqual(len(top_players), 3)

    def test_top_returns_players_sorted_by_points(self):
        top_players = self.stats.top(4)
        self.assertEqual(top_players[0].name, "Gretzky")
        self.assertEqual(top_players[1].name, "Lemieux")
        self.assertEqual(top_players[2].name, "Yzerman")
        self.assertEqual(top_players[3].name, "Kurri")
        self.assertEqual(top_players[4].name, "Semenko")

    def test_top_with_zero_returns_first_player(self):
        top_players = self.stats.top(0)
        self.assertEqual(len(top_players), 1)
        self.assertEqual(top_players[0].name, "Gretzky")
