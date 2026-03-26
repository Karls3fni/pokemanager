from app.services.pokeapi import PokeService
from unittest import mock

class TestPokeapi:
    def _get_movement_data(self):
        return {
            "id": 1,
            "name": "pound",
            "accuracy": 100,
            "effect_chance": None,
            "pp": 35,
            "priority": 0,
            "power": 40,
            "contest_combos": {
                "normal": {
                    "use_before": [
                        {
                            "name": "double-slap",
                            "url": "https://pokeapi.co/api/v2/move/3/",
                        },
                        {
                            "name": "headbutt",
                            "url": "https://pokeapi.co/api/v2/move/29/",
                        },
                        {
                            "name": "feint-attack",
                            "url": "https://pokeapi.co/api/v2/move/185/",
                        },
                    ],
                    "use_after": None,
                },
                "super": {"use_before": None, "use_after": None},
            },
            "contest_type": {
                "name": "tough",
                "url": "https://pokeapi.co/api/v2/contest-type/5/",
            },
            "contest_effect": {"url": "https://pokeapi.co/api/v2/contest-effect/1/"},
            "damage_class": {
                "name": "physical",
                "url": "https://pokeapi.co/api/v2/move-damage-class/2/",
            },
            "effect_entries": [
                {
                    "effect": "Inflicts [regular damage]{mechanic:regular-damage}.",
                    "short_effect": "Inflicts regular damage with no additional effect.",
                    "language": {
                        "name": "en",
                        "url": "https://pokeapi.co/api/v2/language/9/",
                    },
                }
            ],
            "effect_changes": [],
            "generation": {
                "name": "generation-i",
                "url": "https://pokeapi.co/api/v2/generation/1/",
            },
            "meta": {
                "ailment": {
                    "name": "none",
                    "url": "https://pokeapi.co/api/v2/move-ailment/0/",
                },
                "category": {
                    "name": "damage",
                    "url": "https://pokeapi.co/api/v2/move-category/0/",
                },
                "min_hits": None,
                "max_hits": None,
                "min_turns": None,
                "max_turns": None,
                "drain": 0,
                "healing": 0,
                "crit_rate": 0,
                "ailment_chance": 0,
                "flinch_chance": 0,
                "stat_chance": 0,
            },
            "names": [
                {
                    "name": "Pound",
                    "language": {
                        "name": "en",
                        "url": "https://pokeapi.co/api/v2/language/9/",
                    },
                }
            ],
            "past_values": [],
            "stat_changes": [],
            "super_contest_effect": {
                "url": "https://pokeapi.co/api/v2/super-contest-effect/5/"
            },
            "target": {
                "name": "selected-pokemon",
                "url": "https://pokeapi.co/api/v2/move-target/10/",
            },
            "type": {"name": "normal", "url": "https://pokeapi.co/api/v2/type/1/"},
            "learned_by_pokemon": [
                {"name": "clefairy", "url": "https://pokeapi.co/api/v2/pokemon/35/"}
            ],
            "flavor_text_entries": [
                {
                    "flavor_text": "Pounds with fore­\nlegs or tail.",
                    "language": {
                        "url": "https://pokeapi.co/api/v2/language/9/",
                        "name": "en",
                    },
                    "version_group": {
                        "url": "https://pokeapi.co/api/v2/version-group/3/",
                        "name": "gold-silver",
                    },
                }
            ],
        }

    def _get_pokeservice(self) -> PokeService:
        return PokeService()

    def test_get_movement_by_name(self):
        with mock.patch("app.services.pokeapi.httpx.Client.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = self._get_movement_data()
            poke_service = self._get_pokeservice()
            movement = poke_service.get_movement_by_name("pound")
            assert movement.name == "pound"
            assert movement.type == "normal"
            assert movement.category == "physical"
            assert movement.power == 40
            assert movement.success_rate == 100

    def test_get_movement_by_name_pokeservice_error(self):
        with mock.patch("app.services.pokeapi.httpx.Client.get") as mock_get:
            mock_get.return_value.status_code = 404
            poke_service = self._get_pokeservice()
            movement = poke_service.get_movement_by_name("pound")
            assert movement is None

    def test_get_movement_by_name_key_error(self):
        with mock.patch("app.services.pokeapi.httpx.Client.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {}
            poke_service = self._get_pokeservice()
            movement = poke_service.get_movement_by_name("pound")
            assert movement is None
