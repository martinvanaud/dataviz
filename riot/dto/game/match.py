from dataclasses import dataclass


from dataclasses import dataclass

@dataclass
class RiotMatchMetadataDTO:
    dataVersion: str
    matchId: str
    participants: list[str]

@dataclass
class RiotMatchInfoDTO:
    endOfGameResult: str
    gameCreation: int
    gameDuration: int
    gameEndTimestamp: int
    gameId: int
    gameMode: str
    gameName: str
    gameStartTimestamp: int
    gameType: str
    gameVersion: str
    mapId: int
    participants: any
    platformId: str
    queueId: int
    teams: any
    tournamentCode: str

@dataclass
class RiotMatchDTO:
    metadata: RiotMatchMetadataDTO
    info: RiotMatchInfoDTO
