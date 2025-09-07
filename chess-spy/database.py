from sqlalchemy import Table, Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import registry, sessionmaker, scoped_session

mapper_registry = registry()
DatabaseTable = mapper_registry.generate_base()

# Create a default SQLite engine in the local project directory.
# Users can override via DATABASE_URL env var or by creating their own engine.
ENGINE = create_engine("sqlite:///chess_spy.db", echo=False, future=True)
SessionLocal = scoped_session(sessionmaker(bind=ENGINE, autoflush=False, autocommit=False, future=True))

association_tables = {
    "positions_games": Table(
        "positions_games",
        DatabaseTable.metadata,
        Column("position_id", ForeignKey("positions.id")),
        Column("game_id", ForeignKey("games.id")),
    ),
}


def init_db():
    """Create all tables using the configured ENGINE."""
    DatabaseTable.metadata.create_all(ENGINE)
