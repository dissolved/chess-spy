from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database import association_tables, DatabaseTable

# # https://chess.stackexchange.com/questions/30004/longest-possible-fen
MAX_STRIPPED_FEN_SIZE = 83


class Position(DatabaseTable):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True)
    stripped_fen = Column(String(MAX_STRIPPED_FEN_SIZE), unique=True, index=True)
    games = relationship(
        "Game",
        secondary=association_tables["positions_games"],
        back_populates="positions",
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
            session.flush()
        return instance

    def add_game(self, session, game) -> None:
        """Associate this position with a game if not already associated."""
        if game not in self.games:
            self.games.append(game)
            session.flush()
