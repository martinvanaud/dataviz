import csv
import os.path
from time import sleep

from matplotlib import pyplot as plt

from commands.get_game_stats import get_player_game_info
from commands.get_player_league_points import get_player_league_points
from commands.get_player_rank import get_player_rank
from riot.api.error import RiotErrorDTO
from riot.api.game.match import get_match
from riot.api.game.matches import get_matches
from riot.api.summoner.profile import get_profile, get_profile_by_puuid
from riot.dto.game.match import RiotMatchDTO
from riot.dto.game.matches import RiotMatchesDTO
from riot.dto.summoner.profile import RiotAccountDTO
from riot.dto.summoner.rank import QueueType, tier_colors, Tier, Rank


def save_to_csv(profile: RiotAccountDTO, match: RiotMatchDTO):
    # Open the CSV file in append mode ('a') to add data without overwriting
    with open(f"{profile.puuid}_teammates.csv", mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        game_info = get_player_game_info(match.info, profile.puuid)

        # Write the match_id and its participants into the CSV file
        writer.writerow([
            match.metadata.matchId,
            match.info.gameMode,
            game_info.game_duration,
            game_info.win,
            game_info.champion_played,
            game_info.kills,
            game_info.deaths,
            game_info.assists,
            *match.metadata.participants
        ])


def get_unique_player_ids(file_path: str) -> set:
    unique_player_ids = set()

    # Open the CSV file in read mode
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        # Skip the header row (if you have headers)
        next(reader, None)  # Skips the first row which is the header

        # Read through each row and collect the player_id (assuming player_id is the first column)
        for row in reader:
            if row:  # Make sure the row is not empty
                match_id, game_mode, game_duration, win, champion_played, kills, deaths, assists, *participants = row
                for participant in participants:
                    unique_player_ids.add(participant)

    return unique_player_ids


def compare_gg_graph(profiles: list[RiotAccountDTO]):
    x_points = []  # List to hold player league points (x-axis)
    y_points = []  # List to hold player league points (y-axis, same as x in this case)
    colors = []     # List to hold the color of each point (based on tier)
    labels = []     # List to hold the game names for labels
    player_data = []  # List to store player data for CSV

    # Collecting data for each player profile
    for profile in profiles:
        player_rank = get_player_rank(profile, QueueType.RANKED_SOLO)
        player_league_points = get_player_league_points(
            Tier(player_rank.tier), Rank(player_rank.rank), player_rank.leaguePoints
        )

        # Add data to lists
        x_points.append(player_league_points)
        y_points.append(player_league_points)
        colors.append(tier_colors[Tier(player_rank.tier)])  # Use color based on the tier
        labels.append(profile.gameName)  # Game name for labeling

        # Store player data for CSV
        player_data.append([
            profile.gameName,
            player_rank.tier,
            player_rank.rank,
            player_league_points
        ])

    # Create the scatter plot
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(x_points, y_points, c=colors, s=100, edgecolor='black')

    # Adding labels to the points (game names)
    for i, label in enumerate(labels):
        plt.text(x_points[i] + 10, y_points[i] + 10, label, fontsize=9)

    # Setting titles and labels
    plt.title('Player League Points by Tier', fontsize=14)
    plt.xlabel('Player League Points', fontsize=12)
    plt.ylabel('Player League Points', fontsize=12)

    # Add color legend
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in tier_colors.values()]
    labels = [tier.name for tier in tier_colors.keys()]
    plt.legend(handles, labels, title="Tiers", loc="upper left")

    # Save the player data to a CSV file
    with open(f"{profiles[0].puuid}_league_data.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Game Name', 'Tier', 'Rank', 'LP'])

        for row in player_data:
            writer.writerow(row)

    print("CSV file and graph saved successfully.")

    plt.savefig(f"{profiles[0].puuid}_compare_gg.png", format='png', dpi=300)
    plt.show()


if __name__ == "__main__":
    try:
        profile = get_profile("French Touch", "EUW2")
        print(profile.puuid)

        player_rank = get_player_rank(profile, QueueType.RANKED_SOLO)
        player_league_points = get_player_league_points(Tier(player_rank.tier), Rank(player_rank.rank), player_rank.leaguePoints)
        print(profile.gameName, player_rank.tier, player_rank.rank, player_league_points, "lp", tier_colors[Tier(player_rank.tier)])

        # processed_match_ids = set()
        #
        # if not os.path.exists(f"{profile.puuid}_teammates.csv"):
        #
        #     counter = 0
        #     matches = get_matches(profile.puuid)
        #     print(f"Found {len(matches.muuid)} games")
        #
        #     for match_id in matches.muuid:
        #         if match_id in processed_match_ids:
        #             print(f"Skipping already processed match {match_id}")
        #             continue
        #
        #         sleep(1.10)
        #         match = get_match(match_id)
        #         print(f"Game {counter}: {match.metadata.matchId}")
        #         save_to_csv(profile, match)
        #
        #         # Add match ID to processed set to prevent duplicate processing
        #         processed_match_ids.add(match_id)
        #         counter += 1

        if not os.path.exists(f"{profile.puuid}_league_data.csv"):
            unique_puuid = get_unique_player_ids(f"{profile.puuid}_teammates.csv")
            teammates = []
            teammates.append(profile)

            total = len(unique_puuid)
            for idx, id in enumerate(list(unique_puuid)[0:100], start=1):
                profile = get_profile_by_puuid(id)
                print(f"{idx}/{total}", profile.gameName)

                player_rank = get_player_rank(profile, QueueType.RANKED_SOLO)
                player_league_points = get_player_league_points(
                    Tier(player_rank.tier), Rank(player_rank.rank), player_rank.leaguePoints
                )

                # Save the player data to a CSV file
                with open(f"{teammates[0].puuid}_league_data.csv", mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([profile.gameName, player_rank.rank, player_rank.tier, player_league_points])

                # teammates.append(profile)
                sleep(1.1)

            # compare_gg_graph(teammates)

    except Exception as e:
        print(e)
