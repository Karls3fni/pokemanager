from __future__ import annotations
from typing import List, TYPE_CHECKING
from app.models.associations import movement_pokemon_association
from sqlalchemy import ForeignKey   
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base  

if TYPE_CHECKING:
    from app.models.trainer import Trainer
    from app.models.movement import Movement

class Pokemon(Base):
    __tablename__ = "pokemon"

    # id and uuid are inherited from Base
    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    ability: Mapped[str] = mapped_column(nullable=False)
    nature: Mapped[str] = mapped_column(nullable=False)
    
    trainer_id: Mapped[int] = mapped_column(ForeignKey("trainer.id"), nullable=False)

    trainer: Mapped[Trainer] = relationship("Trainer", back_populates="pokemons")
    movements: Mapped[List[Movement]] = relationship(secondary=movement_pokemon_association, back_populates="pokemons")
