from app.models.trainer import Trainer
from app.models.pokemon import Pokemon
from app.services import pokeapi
import uuid

from typing import Any
from sqlalchemy.orm import Session, Query


class TrainerServiceError(Exception):
    pass


class TrainerNotFoundError(TrainerServiceError):
    pass


# Este método crea un nuevo entrenador en la base de datos. 
# Recibe un objeto TrainerCreate con los datos del entrenador a crear, y luego guarda el nuevo entrenador en la base de datos.

def create_trainer(db: Session, trainer_data: Any) -> Trainer:
    """ Create a new trainer in the database.

    Args:
        db (Session): Instance of the database session.
        trainer_data (Any): An instance of TrainerCreate containing the data for the trainer to be created.

    Returns:
        Trainer: An instance of the Trainer class representing the newly created trainer, including its details such as name, region, genre, and a unique UUID.
    """

    trainer = Trainer(
        uuid=uuid.uuid4(),
        name=trainer_data.name,
        region=trainer_data.region,
        genre=trainer_data.genre
    )

    db.add(trainer)
    db.commit()
    db.refresh(trainer)

    return trainer


# Este método permite a un entrenador atrapar un Pokémon aleatorio de la PokeAPI.
# Recibe el UUID del entrenador, consulta la PokeAPI para obtener un Pokémon al azar,
# lo crea en la base de datos si no existe, y lo asocia al entrenador.

def catch_pokemon(db: Session, trainer_uuid: uuid.UUID) -> Pokemon:
    """ Allow a trainer to catch a random Pokémon from the PokeAPI.
     The method receives the UUID of the trainer, queries the PokeAPI to get a random

    Args:
        db (Session): Instance of the database session.
        trainer_uuid (uuid.UUID): UUID of the trainer who wants to catch a Pokémon.

    Raises:
        TrainerNotFoundError: If the trainer with the specified UUID is not found in the database.
        TrainerServiceError:  If there is an error fetching a random Pokémon from the PokeAPI.

    Returns:
        Pokemon: An instance of the Pokemon class representing the Pokémon caught by the trainer, including its details such as name, types, ability, nature, and association with the trainer.
    """

    trainer: Trainer | None = db.query(Trainer).filter(Trainer.uuid == trainer_uuid).first()
    if not trainer:
        raise TrainerNotFoundError("Trainer not found")
    
    pokeapi_service: Any = pokeapi.get_poke_service()

    try:
        random_pokemon: Any = pokeapi_service.get_pokemon_randomly()
    except pokeapi.PokeServiceError:
        raise TrainerServiceError("Error fetching random Pokémon")

    pokemon = Pokemon(
        uuid=uuid.uuid4(),
        name=random_pokemon.name,
        types=random_pokemon.types,
        ability=random_pokemon.ability,
        nature=random_pokemon.nature,
        trainer_id=trainer.id
    )

    db.add(pokemon)
    db.commit()
    db.refresh(pokemon)

    return pokemon


# Este método obtiene los Pokémon de un entrenador dado su UUID. 
# Busca el entrenador en la base de datos y devuelve la lista de Pokémon asociados a ese entrenador.

def get_trainer_pokemons_query(db: Session, trainer_uuid: uuid.UUID) -> Query[Pokemon]:
    """ Retrieve the list of pokemons caught by a trainer given their uuid

    Args:
        db (Session): Instance of the database session.
        trainer_uuid (uuid.UUID): UUID of the trainer whose Pokémon are to be retrieved.

    Raises:
        TrainerNotFoundError: If the trainer with the specified UUID is not found in the database.

    Returns:
        Query: A SQLAlchemy query for retrieving the Pokémon associated with the trainer identified by the provided UUID.
    """

    trainer = db.query(Trainer).filter(Trainer.uuid == trainer_uuid).first()

    if not trainer:
        raise TrainerNotFoundError()

    return db.query(Pokemon).filter(Pokemon.trainer_id == trainer.id)