import requests

from api.client.ApiClient import APIClient
from riot.api.error import RiotErrorDTO
from riot.dto.game.match import RiotMatchDTO, RiotMatchMetadataDTO, RiotMatchInfoDTO


def get_match(match_id: str) -> RiotMatchDTO | RiotErrorDTO:
    try:
        api_client = APIClient("https://europe.api.riotgames.com", headers={"X-Riot-Token": ""})
        response = api_client.get(
            "/lol/match/v5/matches/{match_id}",
            path_params={"match_id": match_id}
        )

        metadata = RiotMatchMetadataDTO(**response['metadata'])
        info = RiotMatchInfoDTO(**response['info'])

        return RiotMatchDTO(metadata=metadata, info=info)
    except requests.exceptions.RequestException as e:
        # Handle network-related errors (e.g., connection error, timeout)
        return RiotErrorDTO(type="Request", error=e)

    except ValueError as e:
        # Handle errors such as invalid response or missing data
        return RiotErrorDTO(type="Value", error=e)

    except Exception as e:
        # Catch all other exceptions
        return RiotErrorDTO(type="Unexpected", error=e)
