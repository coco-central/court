// 动态效果
let login = document.querySelector('.login');
let span;
let inTime, outTime;
let isIn = true;
let isOut;

login.addEventListener('mouseenter', function (e) {
    isOut = false
    if (isIn) {
        inTime = new Date().getTime();
        span = document.createElement('span');
        login.appendChild(span);
        span.style.animation = 'in .5s ease-out forwards';
        let top = 2 * (e.clientY - e.target.offsetTop);
        let left = 2 * (e.clientX - e.target.offsetLeft);
        span.style.top = top + 'px';
        span.style.left = left + 'px';
        isIn = false;
        isOut = true;
    }

})

login.addEventListener('mouseleave', function (e) {
    if (isOut) {
        outTime = new Date().getTime();
        let passTime = outTime - inTime;
        if (passTime < 500) {
            setTimeout(mouseleave, 500 - passTime);
        } else {
            mouseleave();
        }
    }

    function mouseleave() {
        span.style.animation = 'out .5s ease-out forwards';
        let top = e.clientY - e.target.offsetTop;
        let left = e.clientX - e.target.offsetLeft;
        span.style.top = top + 'px';
        span.style.left = left + 'px';
        setTimeout(function () {
            login.removeChild(span);
            isIn = true;
        }, 500);
    }
})

// 回车键登录
document.addEventListener('keyup', function (e) {
    if (e.key === 'Enter') {
        let button = document.getElementById('submit');
        button.focus();
        getToken();
    }
})

// 登录跳转
function reset(text) {
    document.body.innerHTML = text;
}