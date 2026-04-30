from sqlalchemy import ForeignKey, Table, Column
from app.models.base import Base

movement_pokemon_association = Table(
    "movement_pokemon",
    Base.metadata,
    Column("movement_id", ForeignKey("movement.id"), primary_key=True),
    Column("pokemon_id", ForeignKey("pokemon.id"), primary_key=True)
)