import json
import pickle
import bs4
import requests
import fastapi
import uvicorn

headers = {
    "Content-Type": "application/json",
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17'
}

offical_list = []
central_list = []


def login(identity: int, password: str, headers=headers) -> bool:
    """
    编程猫登录
    Args:
        identity (int): [账号]
        password (str): [密码]
        headers (dict, optional): [请求头]. Defaults to headers.

    Returns:
        bool: [是否成功登录]
    """
    if headers is None:
        headers = headers

    def pid():
        res = requests.get('https://shequ.codemao.cn', headers=headers)
        soup = bs4.BeautifulSoup(res.text, 'ht'+'ml.parser')
        data = json.loads(soup.find_all("script")[0].string.split("=")[1])
        return data['pid']

    value = requests.post(url="https://api.codemao.cn/tiger/v3/web/accounts/login",
                          data=json.dumps({
                              'identity': identity,
                              'password': password,
                              'pid': pid()
                          }),
                          headers=headers).text
    return ('auth' in json.loads(value).keys())


class vote:
    def __init__(self, identity: int, value: None | bool) -> None:
        """
        初始化票对象
        Args:
            identity (int): [投票者id]
            value (None | bool): [投票型]
        """
        self.identity = identity
        self.value = value

    def is_offical(self) -> bool:
        """
        判断是否为官方
        Returns:
            bool
        """
        return(self.identity in offical_list)

    def is_central(self) -> bool:
        """
        判断是否为中控台
        Returns:
            bool
        """
        return(self.identity in central_list)


class Arbitration:
    def __init__(self) -> None:
        """
        初始化投票器
        """
        self.title = ""
        self.content = ""
        self.time = 0
        self.images = []
        self.votes = []

    def id_exist(self, identity: int) -> bool:
        for vote in self.votes:
            if vote.identity == identity:
                return(True)
        return(False)

    def vote(self, identity: int, value: None | bool) -> bool:
        """
        投票
        Args:
            identity (int): [投票者id]
            value (None): [投票]
        """
        if not self.id_exist(identity):
            self.votes.append(vote(identity, value))
            return(True)
        else:
            return(False)

    def statistics(self) -> dict:
        """
        Returns:
            dict: [分类选项]
        """
        analytes = {
            'offical': [],
            'central': [],
            'common': []
        }
        for vote in self.votes:
            if vote.is_offical():
                analytes['offical'].append(vote)
            elif vote.is_central():
                analytes['central'].append(vote)
            else:
                analytes['common'].append(vote)
        return(analytes)

    def result(self) -> dict:
        """
        输出投票结果
        Returns:
            dict: [投票结果]
        """
        analytes = self.statistics()

        result = {
            'state': '',  # 状态
            'value': (0, 0, 0)  # 值
        }

        def count(votes: list) -> tuple:
            """
            返回投票正反情况
            Args:
                votes (list): [投票列表]
            Returns:
                tuple: [投票计数]
            """
            process = 0
            not_process = 0
            abstention = 0
            for vote in votes:
                if vote.value == True:
                    process += 1
                if vote.value == False:
                    not_process += 1
                if vote.value == None:
                    abstention += 1
            result = (process, not_process, abstention)
            return(result)

        def judge(result: list) -> bool:
            """
            判断投票结果
            Args:
                result （list）: [单项投票列表]
            Returns:
                bool: [投票结果]
            """
            if count(result)[0] > count(result)[1]:
                return(True)
            else:
                return(False)

        def sum_up(a: tuple, b: tuple)->tuple:
            """
            合计投票结果
            Args:
                a,b (tuple): [投票数据]
            Returns:
                tuple: [合计结果]
            """
            result = [0, 0, 0]
            result[0] = count(a)[0] + count(b)[0]
            result[1] = count(a)[1] + count(b)[1]
            result[2] = count(a)[2] + count(b)[2]
            return(tuple(result))

        if len(analytes['offical']):
            result['state'] = 'offical'
            result['value'] = count(analytes['offical'])
        else:
            if len(analytes['common']) - len(analytes['central']) >= 3:
                if judge(analytes['central']) == judge(analytes['common']):
                    result['state'] = 'all'
                    result['value'] = sum_up(analytes['central'],analytes['common'])
                else:
                    result['state'] = 'common'
                    result['value'] = count(analytes['common'])
            else:
                result['state'] = 'central'
                result['value'] = count(analytes['central'])
        return(result)

class System:
    def __init__(self) -> None:
        self.arbitrations = []

    def load(self, file_name:str) -> None:
        file = open(file_name,"rb")
        self.arbitrations = pickle.load(file)
        file.close()

    def dump(self, file_name:str) -> None:
        file = open(file_name,"wb")
        pickle.dump(self.arbitrations, file)
        file.close()


app = fastapi.FastAPI()

@app.get('/login?identity={identity}&password={password}')
def get_login(identity: int = 0, password: str = ''):
    result = login(identity,password)
    return ({'detail':result})

@app.get("/", response_class=fastapi.responses.HTMLResponse)
async def server():
    html_file = open("index.html", 'r', encoding='utf-8').read()
    return (html_file)


if __name__ == '__main__':
    uvicorn.run(app=app,
                host="127.0.0.1",
                #port=8000,
                workers=1,
                root_path='')