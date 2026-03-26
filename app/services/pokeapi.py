from urllib import response

import httpx
import random
import typing
from dataclasses import dataclass

@dataclass
class Movement:
    name: str
    type: str
    category: typing.Literal["physical", "special"]
    power: int
    success_rate: int

@dataclass
class Pokemon:
    name: str
    types: typing.List[str]
    ability: str
    nature: str
    movements: typing.List[Movement]

class PokeServiceError(Exception):
    pass

class PokeService:

    URL_GET_POKEMON = "https://pokeapi.co/api/v2/pokemon"
    URL_GET_NATURE = "https://pokeapi.co/api/v2/nature"
    URL_GET_MOVEMENT = "https://pokeapi.co/api/v2/move"

    def __init__(self):
        self.client = httpx.Client()

    
    def get_movement_by_name(self, name: str) -> Movement:
        """_summary_

        Args:
            name (str): Introduce the name of the movement you want to retrieve.

        Raises:
            PokeServiceError: If there is an error retrieving the movement or parsing the data.
            PokeServiceError: If there is an error parsing the movement data.

        Returns:
            Movement: An instance of the Movement class containing the details of the movement with the specified name.
        """
        try:
            response = self.client.get(f"{self.URL_GET_MOVEMENT}/{name}")
            response.raise_for_status()
            data = response.json()
            return Movement(name=data["name"], 
                        type=data["type"]["name"], 
                        category=data["damage_class"]["name"], 
                        power=data["power"] or 0, 
                        success_rate=data["accuracy"] or 0)
        except httpx.RequestError:
            raise PokeServiceError(f"Error retrieving movement with name {name}.")
        except KeyError:
            raise PokeServiceError(f"Error parsing movement data for name {name}")


    def get_pokemon_by_name(self, name: str) -> Pokemon:
        """_summary_

        Args:
            name (str): Introduce the name of the Pokemon you want to retrieve.

        Raises:
            PokeServiceError: If there is an error retrieving the movement or parsing the data.
            PokeServiceError: If there is an error parsing the movement data.

        Returns:
            Pokemon: An instance of the Pokemon class containing the details of the Pokémon with the specified name, including its types, ability, nature, and a list of movements.
        """
        try:
            response = self.client.get(f"{self.URL_GET_POKEMON}/{name}")
            response.raise_for_status()
            data = response.json()
            movement_names = random.sample([x["move"]["name"] for x in data["moves"]], 4)
            abilities = data["abilities"] 
            num_ability = random.randint(0, len(abilities) - 1)
            return Pokemon(
                name=data["name"],
                types=[t["type"]["name"] for t in data["types"]],
                ability=abilities[num_ability]["ability"]["name"],
                nature=self.get_natures_randomly(),
                movements=[self.get_movement_by_name(name) for name in movement_names])
        except httpx.HTTPStatusError:
            raise PokeServiceError(f"Error retrieving Pokemon with name {name}")
        except KeyError:
            raise PokeServiceError(f"Error parsing Pokemon data for name {name}")


    #Método para obtener un Pokémon aleatoriamente, complementa el método get_pokemon_by_name para obtener un Pokémon aleatoriamente utilizando su ID

    def get_pokemon_randomly(self) -> Pokemon | None:
        """_summary_

        Raises:
            PokeServiceError: If there is an error retrieving the movement or parsing the data.
            PokeServiceError: If there is an error parsing the movement data.

        Returns:
            Pokemon | None: An instance of the Pokemon class containing the details of a randomly selected Pokémon, including its types, ability, nature, and a list of movements. 
            Returns None if there is an error during retrieval or parsing.
        """
        try:
            response.raise_for_status()
            pokemon_id = random.randint(1, 898)  # Hay 898 Pokémon en la PokéAPI
            return self.get_pokemon_by_name(str(pokemon_id))
        except httpx.RequestError:
            raise PokeServiceError("Error retrieving random Pokémon.")
        except KeyError:
            raise PokeServiceError("Error parsing Pokemon data for name")

    
    #Método para obtener una naturaleza aleatoriamente, complementa el método get_pokemon_by_name para asignar una naturaleza aleatoria al Pokémon obtenido.

    def get_natures_randomly(self) -> str:
        """_summary_

        Returns:
            str: Retrieves a random nature.
        """
        nature_id = random.randint(1, 25)
        response = self.client.get(f"{self.URL_GET_NATURE}/{nature_id}")
        if response.status_code != 200:
            return "jolly"  # Valor por defecto en caso de error
        data = response.json()
        return data["name"]

def get_poke_service() -> PokeService:
    return PokeService()