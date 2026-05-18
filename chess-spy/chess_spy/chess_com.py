import io
import logging
import time
from functools import cached_property

from chess import pgn
import requests

ARCHIVES_URL = "https://api.chess.com/pub/player/{username}/games/archives"

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# requests -> urllib3 logger
logging.getLogger("urllib3").setLevel(logging.DEBUG)


class ChessCom:
    def __init__(self, username):
        self.username = username
        self.games = []

        # Set up session with proper headers to avoid 403 errors
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/91.0.4472.124 Safari/537.36"
                ),
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Referer": "https://www.chess.com/",
            }
        )

        self.import_data()

    @cached_property
    def archives(self):
        response = self.session.get(ARCHIVES_URL.format(username=self.username))
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json().get("archives", [])

    def import_data(self):
        for archive in self.archives[-3:]:
            # Add delay to avoid rate limiting
            time.sleep(1)

            response = self.session.get(archive)
            response.raise_for_status()

            for game_data in response.json().get("games", []):
                self.ingest_game(game_data)

    def ingest_game(self, game_data):
        pgn_io = io.StringIO(game_data["pgn"])
        game = pgn.read_game(pgn_io)
        self.games.append(game)
