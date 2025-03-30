
class RiotErrorDTO(Exception):
    def __init__(self, type: str, error: str):
        self.type = type
        self.error = error
        super().__init__(f"{type} error: {error}")
