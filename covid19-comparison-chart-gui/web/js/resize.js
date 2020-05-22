










onresize = function() {
    let div = document.getElementById("right");
    let div_width = div.clientWidth;
    let div_height = div.clientHeight;

    var win_w = window.innerWidth;
    var win_h = window.innerHeight;

    desired_width = win_w - 312;
    div.style = "width:" + desired_width + "px;";
}