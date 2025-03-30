import requests

from api.client.ApiClient import APIClient
from riot.api.error import RiotErrorDTO
from riot.dto.game.matches import RiotMatchesDTO


def get_matches(player_id: str) -> RiotMatchesDTO | RiotErrorDTO:
    try:
        api_client = APIClient("https://europe.api.riotgames.com", headers={"X-Riot-Token": ""})
        response = api_client.get(
            "/lol/match/v5/matches/by-puuid/{player_id}/ids?start=0&count=100&queue=420",
            path_params={"player_id": player_id}
        )

        return RiotMatchesDTO(muuid=response)
    except requests.exceptions.RequestException as e:
        # Handle network-related errors (e.g., connection error, timeout)
        return RiotErrorDTO(type="Request", error=e)

    except ValueError as e:
        # Handle errors such as invalid response or missing data
        return RiotErrorDTO(type="Value", error=e)

    except Exception as e:
        # Catch all other exceptions
        return RiotErrorDTO(type="Unexpected", error=e)

# 420: 5v5 Ranked Solo games
# 440: 5v5 Ranked Flex games
