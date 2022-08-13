const resize = () => {
    let container = document.getElementsByClassName('container')[0];
    try {
        container.style.height = window.innerHeight + 'px';
    } catch (e) {
        console.log(e);
    }
};
resize();

window.onresize = resize;