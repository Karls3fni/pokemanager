from unittest import TestCase, mock
from fastapi.testclient import TestClient
import uuid

from app.main import app
from app.models.trainer import Trainer
from app.models.pokemon import Pokemon
from app.services import trainer_service


client = TestClient(app)


class TestTrainerEndpoints(TestCase):

    def _get_trainer(self):
        return Trainer(
            id=1,
            uuid=uuid.uuid4(),
            name="Ash",
            region="Kanto",
            genre="male"
        )

    def _get_pokemon(self):
        return Pokemon(
            id=1,
            uuid=uuid.uuid4(),
            name="pikachu",
            types=["electric"],
            ability="static",
            nature="jolly",
            trainer_id=1
        )

    # ─────────────────────────────────────────────
    # CREATE TRAINER
    # ─────────────────────────────────────────────

    @mock.patch("app.routers.trainer.trainer_service.create_trainer")
    def test_create_trainer(self, mock_create_trainer):

        trainer = self._get_trainer()

        mock_create_trainer.return_value = trainer

        response = client.post(
            "/trainer/",
            json={
                "name": "Ash",
                "region": "Kanto",
                "genre": "male"
            }
        )

        assert response.status_code == 200

        data = response.json()

        assert data["name"] == "Ash"
        assert data["region"] == "Kanto"
        assert data["genre"] == "male"

        mock_create_trainer.assert_called_once()

    # ─────────────────────────────────────────────
    # CATCH POKEMON
    # ─────────────────────────────────────────────

    @mock.patch("app.routers.trainer.trainer_service.catch_pokemon")
    def test_catch_pokemon(self, mock_catch_pokemon):

        pokemon = self._get_pokemon()

        mock_catch_pokemon.return_value = pokemon

        trainer_uuid = uuid.uuid4()

        response = client.post(
            f"/trainer/{trainer_uuid}/pokemons/catch"
        )

        assert response.status_code == 200

        data = response.json()

        assert data["name"] == "pikachu"
        assert data["types"] == ["electric"]
        assert data["ability"] == "static"
        assert data["nature"] == "jolly"

        mock_catch_pokemon.assert_called_once()

    @mock.patch("app.routers.trainer.trainer_service.catch_pokemon")
    def test_catch_pokemon_trainer_not_found(self, mock_catch_pokemon):

        mock_catch_pokemon.side_effect = (
            trainer_service.TrainerNotFoundError()
        )

        response = client.post(
            f"/trainer/{uuid.uuid4()}/pokemons/catch"
        )

        assert response.status_code == 404

        data = response.json()

        assert data["detail"] == "Trainer not found"

    @mock.patch("app.routers.trainer.trainer_service.catch_pokemon")
    def test_catch_pokemon_service_error(self, mock_catch_pokemon):

        mock_catch_pokemon.side_effect = (
            trainer_service.TrainerServiceError()
        )

        response = client.post(
            f"/trainer/{uuid.uuid4()}/pokemons/catch"
        )

        assert response.status_code == 503

        data = response.json()

        assert data["detail"] == "Error fetching random Pokémon"

    # ─────────────────────────────────────────────
    # GET TRAINER
    # ─────────────────────────────────────────────

    @mock.patch("app.routers.trainer.trainer_service.get_trainer")
    def test_get_trainer(self, mock_get_trainer):

        trainer = self._get_trainer()

        mock_get_trainer.return_value = trainer

        response = client.get(
            f"/trainer/{trainer.uuid}"
        )

        assert response.status_code == 200

        data = response.json()

        assert data["name"] == "Ash"
        assert data["region"] == "Kanto"
        assert data["genre"] == "male"

        mock_get_trainer.assert_called_once()

    @mock.patch("app.routers.trainer.trainer_service.get_trainer")
    def test_get_trainer_not_found(self, mock_get_trainer):

        mock_get_trainer.side_effect = (
            trainer_service.TrainerNotFoundError()
        )

        response = client.get(
            f"/trainer/{uuid.uuid4()}"
        )

        assert response.status_code == 404

        data = response.json()

        assert data["detail"] == "Trainer not found"

    # ─────────────────────────────────────────────
    # GET POKEMONS
    # ─────────────────────────────────────────────

    @mock.patch("app.routers.trainer.paginate")
    @mock.patch(
        "app.routers.trainer.trainer_service.get_trainer_pokemons_query"
    )
    def test_get_trainer_pokemons(
        self,
        mock_get_query,
        mock_paginate
    ):

        mock_get_query.return_value = mock.Mock()

        mock_paginate.return_value = {
            "items": [],
            "total": 0,
            "page": 1,
            "size": 50,
            "pages": 0
        }

        trainer_uuid = uuid.uuid4()

        response = client.get(
            f"/trainer/{trainer_uuid}/pokemons"
        )

        assert response.status_code == 200

        mock_get_query.assert_called_once()
        mock_paginate.assert_called_once()

    @mock.patch(
        "app.routers.trainer.trainer_service.get_trainer_pokemons_query"
    )
    def test_get_trainer_pokemons_not_found(
        self,
        mock_get_query
    ):

        mock_get_query.side_effect = (
            trainer_service.TrainerNotFoundError()
        )

        response = client.get(
            f"/trainer/{uuid.uuid4()}/pokemons"
        )

        assert response.status_code == 404

        data = response.json()

        assert data["detail"] == "Trainer not found"