class PlayerStats:
    def __init__(self, reader):
        self.players = reader.get_players()

    def top_scorers_by_nationality(self, nationality):
        players_by_nationality = [player for player in self.players if player.nationality == nationality]
        return sorted(players_by_nationality, key=lambda player: player.points, reverse=True)
