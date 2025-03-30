import requests

from api.client.ApiClient import APIClient
from riot.api.error import RiotErrorDTO
from riot.dto.summoner.rank import RiotAccountRankDTO, QueueType


def get_rank(player_id: str) -> list[RiotAccountRankDTO] | RiotErrorDTO:
    try:
        api_client = APIClient("https://euw1.api.riotgames.com", headers={"X-Riot-Token": ""})
        response = api_client.get(
            "/lol/league/v4/entries/by-puuid/{player_id}",
            path_params={"player_id": player_id}
        )

        return [RiotAccountRankDTO(**rank) for rank in response]
    except requests.exceptions.RequestException as e:
        # Handle network-related errors (e.g., connection error, timeout)
        return RiotErrorDTO(type="Request", error=e)

    except ValueError as e:
        # Handle errors such as invalid response or missing data
        return RiotErrorDTO(type="Value", error=e)

    except Exception as e:
        # Catch all other exceptions
        return RiotErrorDTO(type="Unexpected", error=e)