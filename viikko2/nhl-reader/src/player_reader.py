import requests
from player import Player

class PlayerReader:
    def __init__(self, url):
        self.url = url

    def get_players(self):
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return [Player(player_dict) for player_dict in data]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching players: {e}")
            return []
        except (KeyError, ValueError) as e:
            print(f"Error parsing player data: {e}")
            return []
