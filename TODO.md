# TODO

## Import Behavior

- Make imports idempotent. Store Chess.com game metadata such as URL, UUID, dates,
  players, and result, then add a uniqueness constraint so repeat runs do not
  create duplicate `Game` rows.
- Replace the hardcoded three-month archive limit in `ChessCom.import_data` with
  a CLI option or configuration setting.
- Move network fetching out of `ChessCom.__init__` so callers can instantiate the
  client without immediately downloading every selected archive.
- Replace global debug logging in `chess_com.py` with module-level logger usage
  and CLI-controlled verbosity.

## Database & Configuration

- Make the `DATABASE_URL` override described in `database.py` actually work.
- Consider migrations before changing the schema beyond the current generated
  SQLite tables.

## Testing & Quality

- Add tests for duplicate import handling once game metadata is persisted.
- Add tests for CLI options once archive limit and database URL are configurable.
- Keep normal tests network-free by using fake Chess.com responses and temporary
  SQLite databases.
- Decide whether `chess-com-api/` should be tracked as developer documentation.

## Product Direction

- Define the first useful "scouting report": likely repeated positions,
  opening tendencies, color-specific summaries, and recent-game filters.
- Decide whether this remains a CLI-only tool or grows a richer report UI.
