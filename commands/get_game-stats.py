from riot.dto.game.match import RiotMatchInfoDTO


def get_player_game_info(game_data: RiotMatchInfoDTO, player_uuid: str) -> dict[str, any]:
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
        # Replace the logic below with your actual player_uuid mapping
        if str(player.participantId) == player_uuid:  # Adjust the condition based on actual UUID logic
            player_data = player
            break

    if player_data:
        game_duration_minutes = game_data.gameDuration // 60
        game_duration_seconds = game_data.gameDuration % 60

        return {
            "game_duration": f"{game_duration_minutes}m {game_duration_seconds}s",
            "win": player_data.win,
            "champion_played": player_data.championName,
            "kills": player_data.kills,
            "assists": player_data.assists,
            "deaths": player_data.deaths
        }
    else:
        return {"error": "Player UUID not found."}