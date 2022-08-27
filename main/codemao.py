import json
from typing import Optional

import requests

headers = {
    "Content-Type": "application/json",
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 '
                  'Safari/537.17 '
}


def login(username: str, password: str) -> Optional[str]:
    """
    编程猫登录
    :param username: 向服务器请求的用户名
    :param password: 向服务器请求的密码
    :return: 如果成功返回id，失败返回 None
    """

    value = requests.get(url="https://api.xyfish.cn/api/coco_login/api.php?"+'user='+username+'&pwd='+password,
                          headers=headers).text
    print(value)
    if 'id' in json.loads(value).keys():
        return str(json.loads(value)['id'])

    else:
        return None
