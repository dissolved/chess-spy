import typer


def main(username: str):
    print(f"Pulling scouting report for {username}")


if __name__ == "__main__":
    typer.run(main)
