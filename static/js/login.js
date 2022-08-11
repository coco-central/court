//获取 login
let login = document.querySelector('.login')

let span
let inTime, outTime
let isIn = true //默认开关 打开
let isOut

//鼠标进入事件
login.addEventListener('mouseenter', function (e) {
    isOut = false //预先关闭，若不进入if语句，则不能进入鼠标离开事件里的 if
    if (isIn) {
        inTime = new Date().getTime()

        //生成 span 元素并添加进 login 的末尾
        span = document.createElement('span')
        login.appendChild(span)

        //span 去使用 in动画
        span.style.animation = 'in .5s ease-out forwards'

        //计算 top 和 left 值，跟踪鼠标位置
        let top = e.clientY - e.target.offsetTop
        let left = e.clientX - e.target.offsetLeft

        span.style.top = top + 'px'
        span.style.left = left + 'px'

        isIn = false //当我们执行完程序后，关闭
        isOut = true //当我们执行完里面的程序，再打开
    }

})
//鼠标离开事件
login.addEventListener('mouseleave', function (e) {
    if (isOut) {
        outTime = new Date().getTime()
        let passTime = outTime - inTime

        if (passTime < 500) {
            setTimeout(mouseleave, 500 - passTime) //已经经过的时间就不要了
        }
        else {
            mouseleave()
        }
    }

    function mouseleave() {
        span.style.animation = 'out .5s ease-out forwards'

        //计算 top 和 left 值，跟踪鼠标位置
        let top = e.clientY - e.target.offsetTop
        let left = e.clientX - e.target.offsetLeft

        span.style.top = top + 'px'
        span.style.left = left + 'px'

        //注意：因为要等到动画结束，所以要给个定时器
        setTimeout(function () {
            login.removeChild(span)
            isIn = true //当我们执行完鼠标离开事件里的程序，才再次打开
        }, 500)
    }
})

function getToken() {
    username = document.getElementById('username').value;
    password = document.getElementById('password').value;
    var request = new XMLHttpRequest();
    request.open('GET', '/token/?' + 'username=' + username + '&' + 'password=' + password, true);
    request.send();

    setTimeout(Login,999);
}

function getCookie(objName) {
    var arrStr = document.cookie.split('; ');
    for (var i = 0; i < arrStr.length; i++) {
        var temp = arrStr[i].split('=');
        if (temp[0] == objName) {
            return unescape(temp[1]);
        }
    }
    return '';
}

function Login() {
    // 创建一个 form
    var form1 = document.createElement("form");
    // 添加到 body 中
    document.body.appendChild(form1);
    // 创建一个输入
    var input1 = document.createElement("input");
    input1.type = "text";
    input1.name = "identity";
    input1.value = getCookie('id');
    console.log(input1.value);
    form1.appendChild(input1);
    // 创建一个输入
    var input2 = document.createElement("input");
    input2.type = "text";
    input2.name = "token";
    input2.value = getCookie('token');
    // 将该输入框插入到 form 中
    form1.appendChild(input2);
    // form 的提交方式
    form1.method = "POST";
    form1.action = "/login/";
    form1.enctype = 'multipart/form-data';
    // 对该 form 执行提交
    form1.submit();
    // 删除该 form
    document.body.removeChild(form1);
}

console.log(document.cookie);

if (document.cookie != "") {
    setTimeout(Login, 500);
}