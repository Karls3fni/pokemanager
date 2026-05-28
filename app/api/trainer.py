from http.client import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import uuid
from app.schemas.pokemon import PokemonOutput
from app.schemas.trainer import TrainerCreate, TrainerOutput
from app.services import trainer_service as trainer_service
from app.connections.database import get_db
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

router = APIRouter(prefix="/trainer", tags=["trainer"])


@router.post("/")
def create_trainer_endpoint(
    trainer: TrainerCreate,
    db: Session = Depends(get_db)
) -> TrainerOutput:
    """Create a new trainer.

    Responses:
        200: Trainer created successfully and returned in the response.
    """
    trainer_db = trainer_service.create_trainer(db, trainer)
    return TrainerOutput.model_validate(trainer_db)


@router.post("/{trainer_uuid}/pokemons/catch")
def catch_pokemon(
    trainer_uuid: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Allow a trainer to catch a random Pokémon from the PokeAPI.

    Responses:
        200: Pokémon caught successfully and returned in the response.
        404: Trainer with the specified UUID not found in the database.
        503: Error fetching a random Pokémon from the PokeAPI.
    """
    try:
        pokemon = trainer_service.catch_pokemon(db, trainer_uuid)
        return PokemonOutput.model_validate(pokemon)
    except trainer_service.TrainerNotFoundError:
        raise HTTPException(status_code=404, detail="Trainer not found")
    except trainer_service.TrainerServiceError:
        raise HTTPException(status_code=503, detail="Error fetching random Pokémon")



@router.get("/{trainer_uuid}/pokemons", response_model=Page[PokemonOutput])
def get_trainer_pokemons(
    trainer_uuid: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Retrieve the list of pokemons caught by a trainer given their uuid
    
    Responses:
        200: List of pokemons caught by the trainer returned successfully.
        404: Trainer with the specified UUID not found in the database.
    """

    try:
        query = trainer_service.get_trainer_pokemons_query(db, trainer_uuid)
        return paginate(db, query)
    except trainer_service.TrainerNotFoundError:
        raise HTTPException(status_code=404, detail="Trainer not found")



@router.get("/{trainer_uuid}")
def get_trainer(
    trainer_uuid: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Retrieve trainer given uuid

    Responses: 
        200: Trainer found and returned successfully.
        404: Trainer with the specified UUID not found in the database.
    """
    try:
        trainer = trainer_service.get_trainer(db, trainer_uuid)
        return TrainerOutput.model_validate(trainer)
    except trainer_service.TrainerNotFoundError:
        raise HTTPException(status_code=404, detail="Trainer not found")