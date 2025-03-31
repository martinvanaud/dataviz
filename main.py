import csv
import random
from operator import contains

from matplotlib import pyplot as plt

from commands.get_player_league_points import get_player_league_points
from commands.get_player_rank import get_player_rank
from riot.api.error import RiotErrorDTO
from riot.api.game.match import get_match
from riot.api.game.matches import get_matches
from riot.api.summoner.profile import get_profile, get_profile_by_puuid
from riot.dto.game.matches import RiotMatchesDTO
from riot.dto.summoner.profile import RiotAccountDTO
from riot.dto.summoner.rank import QueueType, tier_colors, Tier, Rank


def save_to_csv(profile: RiotAccountDTO, match_id: str, participants: list[str]):
    # Open the CSV file in append mode ('a') to add data without overwriting
    with open(f"2_{profile.puuid}_teammates.csv", mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write the match_id and its participants into the CSV file
        writer.writerow([match_id, *participants])


def load_participants(matches: RiotMatchesDTO):
    for idx, match_id in enumerate(matches.muuid, start=1):
        try:
            match = get_match(match_id)
            print(f"Game {idx}: {match.metadata.participants}")

            save_to_csv(profile, match_id, match.metadata.participants)
        except RiotErrorDTO as e:
            print(f"An error occurred for match {match_id}\nError: {e}")
            continue


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
                match_id, *participants = row
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
    profile = get_profile("French Touch", "EUW2")

    player_rank = get_player_rank(profile, QueueType.RANKED_SOLO)
    player_league_points = get_player_league_points(Tier(player_rank.tier), Rank(player_rank.rank), player_rank.leaguePoints)
    print(profile.gameName, player_rank.tier, player_rank.rank, player_league_points, "lp", tier_colors[Tier(player_rank.tier)])

    matches = get_matches(profile.puuid)

    print(len(matches.muuid))

    for id in matches.muuid:
        match = get_match(id)
        save_to_csv(profile, id, match.metadata.participants)

    # unique_puuid = get_unique_player_ids(f"{profile.puuid}_teammates.csv")
    # teammates = []
    # teammates.append(profile)
    #
    # total = len(unique_puuid)
    # for idx, id in enumerate(unique_puuid, start=1):
    #     profile = get_profile_by_puuid(id)
    #     print(f"{idx}/{total}", profile.gameName)
    #     teammates.append(profile)
    #
    # compare_gg_graph(teammates)
