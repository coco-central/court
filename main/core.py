import time
from typing import Optional, List

official_list = []
central_list = []


class Ballot:
    def __init__(self, identity: int, value: Optional[bool]) -> None:
        self.identity = identity
        self.value = value


class Vote:
    def __init__(self, name: str, time_stamp: float):
        self.object = name
        self.time = time_stamp
        self.ballots: List[Ballot] = []
        self.statistics = [[], [], []]

    def append(self, ballot: Ballot) -> None:
        self.ballots.append(ballot)

    def sort(self) -> None:
        official, central, common = [], [], []
        for ballot in self.ballots:
            if ballot in official_list:
                official.append(ballot)
            elif ballot in central_list:
                central.append(ballot)
            else:
                common.append(ballot)
        self.statistics = [official, central, common]

    @staticmethod
    def __judge(penalize: int, release: int) -> Optional[bool]:
        if penalize == release == 0:
            return None
        else:
            return penalize > release

    def __value(self, key: int) -> list:
        penalize, waiver, release = 0, 0, 0
        for ballot in self.statistics[key]:
            if ballot.value is None:
                waiver += 1
            else:
                if ballot.value:
                    penalize += 1
                else:
                    release += 1
        result = self.__judge(penalize, release)
        return [penalize, waiver, release, result]

    def result(self):
        official = self.__value(0)
        central = self.__value(1)
        common = self.__value(2)

        if official[3] is not None:
            return {
                'source': 'official',
                'state': 'final',
                'data': official
            }
        else:
            if time.time() - self.time > 6 * 3600:
                state = 'final'
            else:
                state = 'voting'

            if central[3] == common[3]:
                merge = [
                    central[0] + common[0],
                    central[1] + common[1],
                    central[2] + common[2],
                ]
                merge[3] = self.__judge(central[0], central[2])
                return {
                    'source': 'all',
                    'state': state,
                    'data': merge
                }
            else:
                central_n = central[0] + central[2]
                common_n = common[0] + common[2]
                if common_n - central_n >= 3 or central_n == 0:
                    return {
                        'source': 'common',
                        'state': state,
                        'data': common
                    }
                else:
                    return {
                        'source': 'central',
                        'state': state,
                        'data': central
                    }


class Event:
    def __init__(self, title: str, time_stamp: float, content: str):
        self.title = title
        self.time = time_stamp
        self.content = content
        self.images: List[str] = []
        self.votes: List[Vote] = []


class Court:
    def __init__(self):
        self.events: List[Event] = []

    def number(self):
        return len(self.events)
