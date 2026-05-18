# chess-spy

`chess-spy` is an early-stage Python CLI for building scouting reports from a
Chess.com player's public game archive. The current implementation downloads
recent monthly archives, parses PGNs with `python-chess`, and stores games,
positions, and game-position links in a local SQLite database.

The project is currently closer to an importer than a finished report generator.
See [TODO.md](TODO.md) for known gaps and next development steps.

## Project Layout

- `chess-spy/chess_spy/`: application package and CLI implementation.
- `tests/`: pytest tests for import, Chess.com client, and database behavior.
- `chess-com-api/`: Bruno collection for manually exploring Chess.com API
  endpoints.
- `AGENTS.md`: contributor and agent guidelines for working in this repository.

## Setup

Install dependencies with `uv`:

```bash
uv sync
```

The console script is defined in `pyproject.toml` as `chess-spy`.

## Run Locally

Run the importer for a Chess.com username:

```bash
uv run chess-spy dissolved-peat
```

By default, current development code is limited to the last three monthly
archives for faster manual testing. Data is written to `chess_spy.db` in the
repository root.

## Test and Lint

Run the test suite:

```bash
uv run pytest
```

Check formatting and linting:

```bash
uv run black --check chess-spy tests
uv run flake8 chess-spy tests
```

Format source and tests:

```bash
uv run black chess-spy tests
```

## Current Status

Working:

- Fetches public Chess.com monthly archives.
- Parses PGNs into `python-chess` game objects.
- Stores games, stripped FEN positions, and associations in SQLite.
- Has basic network-free pytest coverage.

Known limitations:

- Imports are not idempotent and can duplicate games.
- The archive limit is hardcoded for testing.
- `DATABASE_URL` is documented in code but not implemented.
- The report/scouting output itself is not built yet.

For the detailed backlog, read [TODO.md](TODO.md). For contribution practices,
read [AGENTS.md](AGENTS.md).
