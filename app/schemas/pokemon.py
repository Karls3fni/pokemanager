from pydantic import BaseModel, UUID4, ConfigDict
from typing import List


class PokemonOutput(BaseModel):
    uuid: UUID4
    name: str
    types: List[str]
    ability: str
    nature: str

    model_config = ConfigDict(from_attributes=True)