from riot.api.summoner.rank import get_rank
from riot.dto.summoner.profile import RiotAccountDTO
from riot.dto.summoner.rank import QueueType, RiotAccountRankDTO


def get_player_rank(profile: RiotAccountDTO, queue_type: QueueType) -> RiotAccountRankDTO:
    ranks = get_rank(profile.puuid)
    player_rank = next((rank for rank in ranks if rank.queueType == queue_type.value), None)

    return player_rank
