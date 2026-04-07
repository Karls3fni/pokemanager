from unittest import mock, TestCase
import httpx

from app.services.pokeapi import PokeService, PokeServiceError, Movement, Pokemon


class TestPokeService(TestCase):

    # ─────────────────────────────────────────────
    # HELPERS (DATOS MOCK REALISTAS)
    # ─────────────────────────────────────────────

    def _get_pokeservice(self):
        return PokeService()

    def _get_movement_data(self):
        return {
            "id": 1,
            "name": "pound",
            "accuracy": 100,
            "power": 40,
            "damage_class": {"name": "physical"},
            "type": {"name": "normal"},
            "pp": 35,
            "priority": 0,
            "effect_chance": None
        }

    def _get_pokemon_data(self):
        return {
            "name": "pikachu",
            "types": [{"type": {"name": "electric"}}],
            "abilities": [{"ability": {"name": "static"}}],
            "moves": [
                {"move": {"name": "pound"}},
                {"move": {"name": "pound"}},
                {"move": {"name": "pound"}},
                {"move": {"name": "pound"}}
            ]
        }

    # ─────────────────────────────────────────────
    # TEST get_movement_by_name
    # ─────────────────────────────────────────────

    def test_get_movement_by_name(self):
        with mock.patch("app.services.pokeapi.httpx.Client.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = self._get_movement_data()
            mock_get.return_value.raise_for_status.return_value = None

            poke_service = self._get_pokeservice()
            movement = poke_service.get_movement_by_name("pound")

            assert movement.name == "pound"
            assert movement.type == "normal"
            assert movement.category == "physical"
            assert movement.power == 40
            assert movement.success_rate == 100

    def test_get_movement_by_name_request_error(self):
        with mock.patch("app.services.pokeapi.httpx.Client.get") as mock_get:
            mock_get.side_effect = httpx.RequestError("error")

            with self.assertRaises(PokeServiceError):
                self._get_pokeservice().get_movement_by_name("pound")

    def test_get_movement_by_name_key_error(self):
        with mock.patch("app.services.pokeapi.httpx.Client.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {}
            mock_get.return_value.raise_for_status.return_value = None

            with self.assertRaises(PokeServiceError):
                self._get_pokeservice().get_movement_by_name("pound")

    # ─────────────────────────────────────────────
    # TEST get_pokemon_by_name
    # ─────────────────────────────────────────────

    def test_get_pokemon_by_name(self):
        with mock.patch("app.services.pokeapi.httpx.Client.get") as mock_get, \
             mock.patch("app.services.pokeapi.random.sample", return_value=["pound","pound","pound","pound"]), \
             mock.patch("app.services.pokeapi.random.randint", return_value=0), \
             mock.patch("app.services.pokeapi.PokeService.get_natures_randomly", return_value="jolly"), \
             mock.patch("app.services.pokeapi.PokeService.get_movement_by_name") as mock_move:

            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = self._get_pokemon_data()
            mock_get.return_value.raise_for_status.return_value = None

            mock_move.return_value = Movement(
                name="pound",
                type="normal",
                category="physical",
                power=40,
                success_rate=100
            )

            pokemon = self._get_pokeservice().get_pokemon_by_name("pikachu")

            assert pokemon.name == "pikachu"
            assert pokemon.types == ["electric"]
            assert pokemon.ability == "static"
            assert pokemon.nature == "jolly"
            assert len(pokemon.movements) == 4

    def test_get_pokemon_by_name_http_error(self):
        with mock.patch("app.services.pokeapi.httpx.Client.get") as mock_get:
            mock_get.return_value.raise_for_status.side_effect = httpx.HTTPStatusError(
                "error", request=mock.Mock(), response=mock.Mock()
            )

            with self.assertRaises(PokeServiceError):
                self._get_pokeservice().get_pokemon_by_name("pikachu")

    def test_get_pokemon_by_name_key_error(self):
        with mock.patch("app.services.pokeapi.httpx.Client.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {}
            mock_get.return_value.raise_for_status.return_value = None

            with self.assertRaises(PokeServiceError):
                self._get_pokeservice().get_pokemon_by_name("pikachu")

    # ─────────────────────────────────────────────
    # TEST get_pokemon_randomly
    # ─────────────────────────────────────────────

    def test_get_pokemon_randomly(self):
        with mock.patch("app.services.pokeapi.random.randint", return_value=25), \
             mock.patch("app.services.pokeapi.PokeService.get_pokemon_by_name") as mock_get_pokemon:

            mock_get_pokemon.return_value = Pokemon(
                name="pikachu",
                types=["electric"],
                ability="static",
                nature="jolly",
                movements=[]
            )

            pokemon = self._get_pokeservice().get_pokemon_randomly()

            assert pokemon.name == "pikachu"

    def test_get_pokemon_randomly_error(self):
        with mock.patch("app.services.pokeapi.PokeService.get_pokemon_by_name") as mock_get_pokemon:
            mock_get_pokemon.side_effect = httpx.RequestError("error")

            with self.assertRaises(PokeServiceError):
                self._get_pokeservice().get_pokemon_randomly()

    # ─────────────────────────────────────────────
    # TEST get_natures_randomly
    # ─────────────────────────────────────────────

    def test_get_natures_randomly(self):
        with mock.patch("app.services.pokeapi.random.randint", return_value=1), \
             mock.patch("app.services.pokeapi.httpx.Client.get") as mock_get:

            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"name": "bold"}

            nature = self._get_pokeservice().get_natures_randomly()

            assert nature == "bold"

    def test_get_natures_randomly_fallback(self):
        with mock.patch("app.services.pokeapi.random.randint", return_value=1), \
             mock.patch("app.services.pokeapi.httpx.Client.get") as mock_get:

            mock_get.return_value.status_code = 500

            nature = self._get_pokeservice().get_natures_randomly()

            assert nature == "jolly"