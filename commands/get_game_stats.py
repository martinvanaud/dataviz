from dataclasses import dataclass

from riot.dto.game.match import RiotMatchInfoDTO


@dataclass
class RiotMatchDetailsDTO:
    game_duration: str
    win: bool
    champion_played: str
    kills: int
    deaths: int
    assists: int


def get_player_game_info(game_data: RiotMatchInfoDTO, player_uuid: str) -> RiotMatchDetailsDTO | None:
    """
    Extracts relevant data for a player based on player_uuid.

    Args:
        game_data: The game data containing details of players.
        player_uuid: The UUID of the player whose details are to be extracted.

    Returns:
        A dictionary with game duration, win/lose status, and player's character, kills, assists, deaths.
    """
    # Dummy player mapping for example, replace with actual player_uuid mapping logic
    # Example, assuming player_uuid maps to participantId
    player_data = None
    for player in game_data.participants:
        if str(player["puuid"]) == player_uuid:
            player_data = player

    if player_data:
        game_duration_minutes = game_data.gameDuration // 60
        game_duration_seconds = game_data.gameDuration % 60

        game_details = {
            "game_duration": f"{game_duration_minutes}m {game_duration_seconds}s",
            "win": player_data["win"],
            "champion_played": player_data["championName"],
            "kills": player_data["kills"],
            "deaths": player_data["deaths"],
            "assists": player_data["assists"]
        }

        return RiotMatchDetailsDTO(**game_details)
    else:
        return None
