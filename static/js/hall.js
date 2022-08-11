const resize = () => {
    let container = document.getElementsByClassName('container')[0];
    container.style.height = window.innerHeight + 'px';
};
resize();

window.onresize = resize;