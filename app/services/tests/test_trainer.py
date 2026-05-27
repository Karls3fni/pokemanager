from unittest import TestCase, mock
import uuid
from app.schemas.pokemon_schema import PokemonOutput

from app.services.trainer_service import (
    create_trainer,
    catch_pokemon,
    get_trainer_pokemons_query,
    TrainerNotFoundError,
    TrainerServiceError
)

from app.services import pokeapi
from app.models.trainer import Trainer
from app.schemas.trainer import TrainerCreate

class TestTrainerService(TestCase):

    def _get_trainer_data(self):
        return TrainerCreate(
            name="Ash",
            region="Kanto",
            genre="male"
        )

    def _get_pokemon_data(self):

        return PokemonOutput(
            uuid=uuid.uuid4(),
            name="Pikachu",
            types=["electric"],
            ability="static",
            nature="jolly"
        )
    
    def _get_trainer(self):
        return Trainer(
            id=1,
            uuid=uuid.uuid4(),
            name="Ash",
            region="Kanto",
            genre="male"
        )

    # ─────────────────────────────────────────────
    # CREATE TRAINER
    # ─────────────────────────────────────────────

    def test_create_trainer(self):

        db = mock.Mock()

        trainer = create_trainer(db, self._get_trainer_data())

        assert trainer.name == "Ash"
        assert trainer.region == "Kanto"
        assert trainer.genre == "male"

        db.add.assert_called_once()
        db.commit.assert_called_once()
        db.refresh.assert_called_once()

    # ─────────────────────────────────────────────
    # CATCH POKEMON
    # ─────────────────────────────────────────────

    def test_catch_pokemon(self):

        db = mock.Mock()
        trainer = self._get_trainer()

        db.query.return_value.filter.return_value.first.return_value = trainer

        fake_service = mock.Mock()
        fake_service.get_pokemon_randomly.return_value = self._get_pokemon_data()

        with mock.patch(
            "app.services.pokeapi.get_poke_service",
            return_value=fake_service
        ):

            pokemon = catch_pokemon(db, trainer.uuid)

            assert pokemon.name == "pikachu"
            assert pokemon.types == ["electric"]
            assert pokemon.ability == "static"
            assert pokemon.nature == "jolly"
            assert pokemon.trainer_id == 1

            db.add.assert_called_once()
            db.commit.assert_called_once()
            db.refresh.assert_called_once()

    def test_catch_pokemon_trainer_not_found(self):

        db = mock.Mock()
        db.query.return_value.filter.return_value.first.return_value = None

        with self.assertRaises(TrainerNotFoundError):
            catch_pokemon(db, uuid.uuid4())

    def test_catch_pokemon_pokeapi_error(self):

        db = mock.Mock()
        trainer = self._get_trainer()

        db.query.return_value.filter.return_value.first.return_value = trainer

        fake_service = mock.Mock()
        fake_service.get_pokemon_randomly.side_effect = pokeapi.PokeServiceError()

        with mock.patch(
            "app.services.pokeapi.get_poke_service",
            return_value=fake_service
        ):

            with self.assertRaises(TrainerServiceError):
                catch_pokemon(db, trainer.uuid)

    # ─────────────────────────────────────────────
    # GET POKEMONS
    # ─────────────────────────────────────────────

    def test_get_trainer_pokemons_query(self):

        db = mock.Mock()
        trainer = self._get_trainer()
        query_mock = mock.Mock()

        db.query.return_value.filter.return_value.first.return_value = trainer
        db.query.return_value.filter.return_value = query_mock

        query = get_trainer_pokemons_query(db, trainer.uuid)

        assert query == query_mock

    def test_get_trainer_pokemons_query_not_found(self):

        db = mock.Mock()
        db.query.return_value.filter.return_value.first.return_value = None

        with self.assertRaises(TrainerNotFoundError):
            get_trainer_pokemons_query(db, uuid.uuid4())