from __future__ import annotations
from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.associations import movement_pokemon_association

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.pokemon import Pokemon

class Movement(Base):
    __tablename__ = "movement"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    power: Mapped[int] = mapped_column(default=0)
    accuracy: Mapped[int] = mapped_column(default=100)

    pokemons: Mapped[List[Pokemon]] = relationship(secondary=movement_pokemon_association, back_populates="movements")