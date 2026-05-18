import io

import pytest
from chess import pgn
from sqlalchemy import create_engine

from chess_spy import cli
from chess_spy import database
from chess_spy.game import Game
from chess_spy.position import Position


PGN = """
[Event "Live Chess"]
[Site "Chess.com"]
[Date "2026.05.17"]
[Round "-"]
[White "dissolved-peat"]
[Black "opponent"]
[Result "1-0"]

1. e4 e5 2. Nf3 Nc6 1-0
""".strip()


@pytest.fixture()
def isolated_database(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'chess_spy_test.db'}", future=True)
    database.ENGINE = engine
    database.SessionLocal.remove()
    database.SessionLocal.configure(bind=engine)
    database.DatabaseTable.metadata.create_all(engine)

    yield

    database.SessionLocal.remove()
    database.DatabaseTable.metadata.drop_all(engine)
    engine.dispose()


class FakeChessCom:
    def __init__(self, username):
        self.username = username
        self.games = [pgn.read_game(io.StringIO(PGN))]


def test_main_imports_games_positions_and_links(monkeypatch, isolated_database):
    monkeypatch.setattr(cli, "ChessCom", FakeChessCom)

    cli.main("dissolved-peat")

    with database.SessionLocal() as session:
        assert session.query(Game).count() == 1
        assert session.query(Position).count() == 4
        assert session.execute(
            database.association_tables["positions_games"].select()
        ).all()


def test_position_strips_move_counters_and_reuses_existing_row(isolated_database):
    fen_move_1 = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"
    fen_move_12 = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 8 12"

    with database.SessionLocal() as session:
        first = Position.from_fen(session, fen_move_1)
        second = Position.from_fen(session, fen_move_12)

        assert first.id == second.id
        assert session.query(Position).count() == 1
        assert first.stripped_fen == (
            "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq -"
        )
