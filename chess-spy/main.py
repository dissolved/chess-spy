import typer

from chess_com import ChessCom
from position import Position


def main(username: str):
    print(f"Pulling scouting report for {username}")
    client = ChessCom(username)
    for game in client.games:
        board = game.board()
        for move in game.mainline_moves():
            board.push(move)
            pos = Position.from_fen(board.fen())
            pos.add_game(game)


if __name__ == "__main__":
    typer.run(main)
