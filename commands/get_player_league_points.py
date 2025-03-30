from riot.dto.summoner.rank import Tier, Rank


def get_player_league_points(tier: Tier, rank: Rank, points: int) -> int:
    """
    Calculate LP for the player based on the tier, rank, and points given.

    Args:
        tier (Tier): The player's tier.
        rank (Rank): The player's rank within the tier.
        points (int): The points the player has for the current rank.

    Returns:
        int: The total LP for the player in the specified tier and rank.
    """
    # Cumulative LP across tiers and divisions
    tier_order = [Tier.IRON, Tier.BRONZE, Tier.SILVER, Tier.GOLD, Tier.PLATINUM, Tier.EMERALD, Tier.DIAMOND]
    divisions = [Rank.IV, Rank.III, Rank.II, Rank.I]

    LP_PER_TIER = 400
    LP_PER_DIVISION = 100

    # Calculate the base LP for the player's tier and division
    base_lp = (tier_order.index(tier) * LP_PER_TIER) + (divisions.index(rank) * LP_PER_DIVISION) + points

    return base_lp
