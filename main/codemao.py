import requests
import json
import bs4

headers = {
    "Content-Type": "application/json",
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17'
}


def login(username: int, password: str) -> bool:
    def pid():
        res = requests.get('https://shequ.codemao.cn', headers=headers)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        data = json.loads(soup.find_all("script")[0].string.split("=")[1])
        return data['pid']

    value = requests.post(url="https://api.codemao.cn/tiger/v3/web/accounts/login",
                          data=json.dumps({
                              'identity': username,
                              'password': password,
                              'pid': pid()
                          }),
                          headers=headers).text
    return 'auth' in json.loads(value).keys()
