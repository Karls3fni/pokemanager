from __future__ import annotations
from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.pokemon import Pokemon

class Trainer(Base):
    __tablename__ = "trainer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    region: Mapped[str] = mapped_column(nullable=False)
    genre: Mapped[str] = mapped_column(nullable=False)
    
    pokemons: Mapped[List[Pokemon]] = relationship("Pokemon", back_populates="trainer")