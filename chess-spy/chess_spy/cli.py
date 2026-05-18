import typer

from .chess_com import ChessCom
from .position import Position
from .game import Game
from .database import SessionLocal, init_db


def main(username: str):
    print(f"Pulling scouting report for {username}")
    init_db()
    client = ChessCom(username)

    with SessionLocal() as session:
        for parsed_game in client.games:
            # breakpoint()
            game_row = Game()
            session.add(game_row)
            session.flush()

            board = parsed_game.board()
            for move in parsed_game.mainline_moves():
                board.push(move)
                pos = Position.from_fen(session, board.fen())
                pos.add_game(session, game_row)

        session.commit()


app = typer.Typer()


@app.command()
def run(username: str):
    main(username)
