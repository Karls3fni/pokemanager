from sqlalchemy import Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column 

class Base(DeclarativeBase):
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[Uuid] = mapped_column(Uuid, unique=True, nullable=False)
    