from app.services.pokeapi import PokeService

def test_get_pokemon_by_name():
    service = PokeService()

    pokemon = service.get_pokemon_by_name("pikachu")

    assert pokemon is not None
    assert pokemon.name == "pikachu"