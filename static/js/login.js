// 动态效果
let login = document.querySelector('.login')
let span
let inTime, outTime
let isIn = true
let isOut

login.addEventListener('mouseenter', function (e) {
    isOut = false
    if (isIn) {
        inTime = new Date().getTime()
        span = document.createElement('span')
        login.appendChild(span)
        span.style.animation = 'in .5s ease-out forwards'
        let top = e.clientY - e.target.offsetTop
        let left = e.clientX - e.target.offsetLeft
        span.style.top = top + 'px'
        span.style.left = left + 'px'
        isIn = false
        isOut = true
    }

})

login.addEventListener('mouseleave', function (e) {
    if (isOut) {
        outTime = new Date().getTime()
        let passTime = outTime - inTime
        if (passTime < 500) {
            setTimeout(mouseleave, 500 - passTime) //已经经过的时间就不要了
        } else {
            mouseleave()
        }
    }

    function mouseleave() {
        span.style.animation = 'out .5s ease-out forwards'
        let top = e.clientY - e.target.offsetTop
        let left = e.clientX - e.target.offsetLeft
        span.style.top = top + 'px'
        span.style.left = left + 'px'
        setTimeout(function () {
            login.removeChild(span)
            isIn = true
        }, 500)
    }
})

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
    cookies = document.cookie.match(/[^ =;]+(?=)/g);
    if (cookies != null)
        for (let i = 0; i < cookies.length; i++)
            document.cookie = cookies[i] + "=0;expires=" + new Date().toGMTString() + ";path=/";
}

// 登录：获取Token
function getToken() {
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    const request = new XMLHttpRequest();
    request.open('GET', '/token/?' + 'username=' + username + '&' + 'password=' + password, true);
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
                } else {
                    document.body.innerHTML = request.response;
                }
            }
        }
    }
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send('identity=' + getCookie('id') + '&token=' + getCookie('token'));
}

// 记住登录状态，自动登录
if (document.cookie !== "") {
    postLogin();
}