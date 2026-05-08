from pydantic import BaseModel, UUID4, ConfigDict

class TrainerCreate(BaseModel):
    name: str
    region: str
    genre: str


class CatchPokemonRequest(BaseModel):
    pokemon_id: int


class TrainerOutput(TrainerCreate):
    uuid: UUID4

    model_config = ConfigDict(from_attributes=True)