import io
from functools import cached_property

from chess import pgn
import requests

ARCHIVES_URL = "https://api.chess.com/pub/player/{username}/games/archives"


class ChessCom:
    def __init__(self, username):
        self.username = username
        self.games = []
        self.import_data()

    @cached_property
    def archives(self):
        response = requests.get(ARCHIVES_URL.format(username=self.username))
        return response.json().get("archives", [])

    def import_data(self):
        for archive in self.archives:
            response = requests.get(archive)
            for game_data in response.json().get("games", []):
                self.ingest_game(game_data)

    def ingest_game(self, game_data):
        pgn_io = io.StringIO(game_data["pgn"])
        game = pgn.read_game(pgn_io)
        self.games.append(game)

    # def games(self):
    #     for game in self.games:
    #         yield game["pgn"]
