// 获取Cookie
function getCookie(objName) {
    const arrStr = document.cookie.split('; ');
    for (let i = 0; i < arrStr.length; i++) {
        let temp = arrStr[i].split('=');
        if (temp[0] === objName) {
            return decodeURI(temp[1]);
        }
    }
    return '';
}

// 清空Cookie
function delCookie() {
    let cookies;
    cookies = document.cookie.match(/[^ =;]+(?=\=)/g);
    if (cookies != null)
        for (let i = 0; i < cookies.length; i++)
            document.cookie = cookies[i] + "=0;expires=" + new Date().toGMTString() + ";path=/";
}

// 登录：获取Token
function getToken() {
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    const request = new XMLHttpRequest();
    request.open('GET', '/token/?' + 'username=' + username + '&' + 'password=' + encodeURIComponent(password), true);
    request.onreadystatechange = function () {
        if (request.readyState === 4) {
            if (request.status === 200 || request.status === 304) {
                console.log(request.response);
                postLogin();
            }
        }
    }
    request.send();
}

// 登录：发送post
function postLogin() {
    const request = new XMLHttpRequest();
    request.open('POST', '/hall/', true);
    request.onreadystatechange = function () {
        if (request.readyState === 4) {
            if (request.status === 200 || request.status === 304) {
                console.log(request.response);
                if (request.response === 'failed') {
                    delCookie();
                    window.location.href = "/";
                } else {
                    try {
                        reset(request.response);
                        resize();
                    } catch (e) {
                        console.log(e);
                    }
                }
                document.body.style.opacity = '1';
            }
        }
    }
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send('identity=' + getCookie('id') + '&token=' + getCookie('token'));
}

// 发送投票数据
function getDecision(event, name, value) {
    const request = new XMLHttpRequest();
    request.open('GET', '/vote/?' + 'event=' + event + '&' + 'name=' + name + '&' + 'value=' + value, true);
    request.onreadystatechange = function () {
        if (request.readyState === 4) {
            if (request.status === 200 || request.status === 304) {
                location.reload();
            }
        }
    }
    request.send();
}