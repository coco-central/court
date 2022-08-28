import json
from typing import Optional

import requests


def login(username: str, password: str) -> Optional[str]:
    """
    编程猫登录
    :param username: 向服务器请求的用户名
    :param password: 向服务器请求的密码
    :return: 如果成功返回id，失败返回 None
    """
    data = {
        'user': username,
        'pwd': password
    }
    value = requests.post(url="https://api.bcmcreator.cn/login/user_bcmlogin.php",
                          data=data).text
    print(username, password, value)
    if 'id' in json.loads(value).keys():
        return str(json.loads(value)['id'])
    else:
        return None
