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


# Este endpoint es para crear un nuevo entrenador. 
# Recibe un objeto TrainerCreate y devuelve el entrenador creado.
@router.post("/")
def create_trainer_endpoint(
    trainer: TrainerCreate,
    db: Session = Depends(get_db)
) -> TrainerOutput:
    """Create a new trainer.

    Args:
        trainer (TrainerCreate): The data for the trainer to be created.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        TrainerOutput: The newly created trainer.
    """
    trainer_db = trainer_service.create_trainer(db, trainer)
    return TrainerOutput.model_validate(trainer_db)


# Este endpoint es para que un entrenador atrape un Pokémon. 
# Recibe el UUID del entrenador.
@router.post("/{trainer_uuid}/pokemons/catch")
def catch_pokemon(
    trainer_uuid: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Allow a trainer to catch a random Pokémon from the PokeAPI.

    Args:
        trainer_uuid (uuid.UUID): UUID of the trainer who wants to catch a Pokémon.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the trainer with the specified UUID is not found in the database, a 404 error is raised.
        HTTPException: If there is an error fetching a random Pokémon from the PokeAPI, a 503 error is raised.

    Returns:
        PokemonOutput: The Pokémon caught by the trainer.
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
    Args:
        trainer_uuid (uuid.UUID): UUID of the trainer whose pokemons we want to retrieve
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the trainer with the specified UUID is not found in the database, a 404 error is raised.

    Returns:
        _type_: Paginated list of pokemons caught by the trainer
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