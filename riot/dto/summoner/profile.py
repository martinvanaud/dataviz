from dataclasses import dataclass


@dataclass
class RiotAccountDTO:
    puuid: str
    gameName: str
    tagLine: str
