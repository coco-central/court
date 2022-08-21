import time
from string import Template
from typing import Optional, List

official_list = []
central_list = []

a_minute = 60
a_hour = a_minute * 60
a_day = a_hour * 24
a_week = a_day * 7
a_month = a_day * 30


def template(name: str) -> str:
    """
    读取模板文件
    :param name: 模板名
    :return: 模板
    """
    file = open('static/template/' + name + '.html', 'r', encoding='utf-8')
    text = file.read()
    file.close()
    return text


def login_html() -> str:
    return Template(template('index')).safe_substitute(content=template('login'))


class Ballot:
    def __init__(self, identity: int, value: Optional[bool]):
        """
        票
        :param identity: 投票者id
        :param value: 投票值(True/False/None)
        """
        self.identity = identity
        self.value = value


class Vote:
    def __init__(self, name: str, time_stamp: float):
        """
        投票
        :param name: 投票对象
        :param time_stamp: 投票开始时间戳
        """
        self.object = name
        self.time = time_stamp
        self.ballots: List[Ballot] = []
        self.statistics = [[], [], []]

    def append(self, ballot: Ballot) -> None:
        """
        增添票
        :param ballot: 票
        :return: None
        """
        self.ballots.append(ballot)

    def sort(self) -> None:
        """
        分出官方票，中控台票，群员票
        :return: None
        """
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
        """
        判断当前投票结果
        :param penalize: 投处罚的人数
        :param release: 投放行的人数
        :return: True | False | None
        """
        if penalize == release == 0:
            return None
        else:
            return penalize > release

    def __value(self, key: int) -> list:
        """
        获取投票的值
        :param key: 选择官方(0)，中控台(1)，群员(2)
        :return: 投票结果条
        """
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

    def result(self) -> dict:
        """
        返回总的投票结果
        :return: 一个字典，包含数据来源(source)，投票阶段(state)，投票数据(data)
        """
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
        """
        发生的事件
        :param title: 事件名称
        :param time_stamp: 时间戳
        :param content: 事件内容
        """
        self.title = title
        self.time = time_stamp
        self.content = content
        self.images: List[str] = []
        self.votes: List[Vote] = []

    def get_time(self) -> str:
        """
        返回自然语言时间差异
        :return: str
        """
        now = time.time()
        diff = int(now) - int(self.time)
        month = diff / a_month
        week = diff / a_week
        day = diff / a_day
        hour = diff / a_hour
        minute = diff / a_minute
        if diff < 0:
            return '我在时间之外等你'
        elif month >= 1:
            return str(int(month)) + '个月前'
        elif week >= 1:
            return str(int(week)) + '周前'
        elif day >= 1:
            return str(int(day)) + '天前'
        elif hour >= 1:
            return str(int(hour)) + '小时前'
        elif minute >= 1:
            return str(int(minute)) + '分钟前'
        else:
            return '刚刚'

    def html(self):
        images_html = ''
        for image in self.images:
            images_html += Template(template('image')).safe_substitute(
                base64=image
            )
        temporary_html = Template(template('index')).safe_substitute(
            content=template('event')
        )
        time_text = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(self.time))
        return Template(temporary_html).safe_substitute(
            title=self.title,
            time=time_text,
            content=self.content,
            images=images_html
        )


class Court:
    def __init__(self):
        """
        众裁总数据类
        """
        self.events: List[Event] = []

    def number(self) -> int:
        """
        返回当前事件数
        :return: 事件数
        """
        return len(self.events)

    def html(self) -> str:
        events_html = ''
        for i in range(len(self.events)):
            events_html += Template(template('item')).safe_substitute(
                code=i,
                title=self.events[i].title,
                time=self.events[i].get_time()
            )
        return Template(template('hall')).safe_substitute(
            number=str(self.number()),
            events=events_html
        )
