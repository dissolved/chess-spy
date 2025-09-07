from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import relationship

from database import association_tables, DatabaseTable

# # https://chess.stackexchange.com/questions/30004/longest-possible-fen
MAX_STRIPPED_FEN_SIZE = 83

class Position(DatabaseTable):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True)
    stripped_fen = Column(String(MAX_STRIPPED_FEN_SIZE), unique=True, index=True)
    games = relationship(
        "Game",
        secondary=association_tables["positions_games"],
        back_populates="positions"
    )

    @classmethod
    def from_fen(cls, session, fen: str) -> "Position":
        """
        Return existing Position by stripped FEN or create it if missing.
        stripped_fen omits the half-move and full-move counters.
        """
        stripped_fen = " ".join(fen.split()[:-2])
        instance = session.query(cls).filter_by(stripped_fen=stripped_fen).one_or_none()
        if instance is None:
            instance = cls(stripped_fen=stripped_fen)
            session.add(instance)
            session.flush()  # ensure id is populated
        return instance

    def add_game(self, session, game: "Game") -> None:
        """Associate this position with a game if not already associated."""
        if game not in self.games:
            self.games.append(game)
            session.flush()


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # PREVIOUS IMPLEMENTATION
    # ⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎
    # positions = {}

    # @classmethod
    # def from_fen(cls, fen):
    #     # stripped_fen does not include the half move clock or whole move clock
    #     # ex:
    #     #     "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"
    #     #       becomes
    #     #     "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq -"
    #     stripped_fen = " ".join(fen.split()[:-2])
    #     position = cls.positions.get(stripped_fen)
    #     if not position:
    #         position = cls(stripped_fen)
    #         cls.positions[stripped_fen] = position
    #     return position

    # def __init__(self, stripped_fen):
    #     self.stripped_fen = stripped_fen
    #     self.games = []

    # def add_game(self, game):
    #     if not self.game_is_recorded(game):
    #         self.games.append(game)

    # def game_is_recorded(self, game):
    #     matches = sum(1 for saved_game in self.games if saved_game == game)
    #     return bool(matches)
