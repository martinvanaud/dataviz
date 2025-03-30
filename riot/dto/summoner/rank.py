from dataclasses import dataclass
from enum import Enum


class QueueType(Enum):
    RANKED_SOLO = "RANKED_SOLO_5x5"
    RANKED_FLEX = "RANKED_FLEX_SR"

class Tier(Enum):
    IRON = "IRON"
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"
    EMERALD = "EMERALD"
    DIAMOND = "DIAMOND"
    MASTER = "MASTER"
    GRANDMASTER = "GRANDMASTER"
    CHALLENGER = "CHALLENGER"

class Rank(Enum):
    I = "I"
    II = "II"
    III = "III"
    IV = "IV"

tier_colors = {
    Tier.IRON: "#C8C8C8",  # Grey for Iron
    Tier.BRONZE: "#B68D46",  # Bronze
    Tier.SILVER: "#B8B8B8",  # Silver
    Tier.GOLD: "#F6A900",  # Gold
    Tier.PLATINUM: "#00A1E5",  # Platinum
    Tier.EMERALD: "#1A7B3A",  # Emerald
    Tier.DIAMOND: "#1A91E2",  # Diamond
    Tier.MASTER: "#703F8C",  # Master
    Tier.GRANDMASTER: "#C1286C",  # Grandmaster
    Tier.CHALLENGER: "#D50032"  # Challenger
}

@dataclass
class RiotAccountRankDTO:
    leagueId: str
    queueType: QueueType
    tier: Tier
    rank: Rank
    summonerId: str
    puuid: str
    leaguePoints: int
    wins: int
    losses: int
    veteran: bool
    inactive: bool
    freshBlood: bool
    hotStreak: bool
