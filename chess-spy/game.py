from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import relationship

from database import association_tables, DatabaseTable

class Game(DatabaseTable):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    positions = relationship(
        "Position",
        secondary=association_tables["positions_games"],
        back_populates="games"
    )
