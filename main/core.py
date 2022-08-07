from typing import Optional, List


class Ballot:
    def __init__(self, identity: int, value: Optional[bool]):
        self.identity = identity
        self.value = value


class Vote:
    def __init__(self):
        self.object: str
        self.ballots: List[Ballot]
