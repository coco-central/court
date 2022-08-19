// 不跳回主页
function reset(text) {
    return text;
}

// 自适应
function resize() {
    let container = document.getElementsByClassName('container')[0];
    container.style.height = window.innerHeight + 'px';
};
resize();

window.onresize = resize;