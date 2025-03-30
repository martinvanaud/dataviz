import requests

from api.client.ApiClient import APIClient
from riot.api.error import RiotErrorDTO
from riot.dto.summoner.profile import RiotAccountDTO


def get_profile(game_name: str, game_tag: str) -> RiotAccountDTO | RiotErrorDTO:
    try:
        api_client = APIClient("https://europe.api.riotgames.com", headers={"X-Riot-Token": ""})
        response = api_client.get(
            "/riot/account/v1/accounts/by-riot-id/{game_name}/{game_tag}",
            path_params={"game_name": game_name, "game_tag": game_tag}
        )

        if not response or 'error' in response:
            raise ValueError(f"Error retrieving profile: {response.get('error', 'Unknown error')}")

        return RiotAccountDTO(**response)

    except requests.exceptions.RequestException as e:
        # Handle network-related errors (e.g., connection error, timeout)
        return RiotErrorDTO(type="Request", error=e)

    except ValueError as e:
        # Handle errors such as invalid response or missing data
        return RiotErrorDTO(type="Value", error=e)

    except Exception as e:
        # Catch all other exceptions
        return RiotErrorDTO(type="Unexpected", error=e)


def get_profile_by_puuid(player_id: str) -> RiotAccountDTO | RiotErrorDTO:
    try:
        api_client = APIClient("https://europe.api.riotgames.com", headers={"X-Riot-Token": "RGAPI-7b0e090d-98a5-417c-951d-975286c9c42a"})
        response = api_client.get(
            "/riot/account/v1/accounts/by-puuid/{player_id}",
            path_params={"player_id": player_id}
        )

        if not response or 'error' in response:
            raise ValueError(f"Error retrieving profile: {response.get('error', 'Unknown error')}")

        return RiotAccountDTO(**response)

    except requests.exceptions.RequestException as e:
        # Handle network-related errors (e.g., connection error, timeout)
        return RiotErrorDTO(type="Request", error=e)

    except ValueError as e:
        # Handle errors such as invalid response or missing data
        return RiotErrorDTO(type="Value", error=e)

    except Exception as e:
        # Catch all other exceptions
        return RiotErrorDTO(type="Unexpected", error=e)
