const mascot = document.getElementById("mascot");
const randomYui = () => 
    mascot.setAttribute("src", "/mascots/" + Math.floor(1 + Math.random()*14) + ".png");

randomYui();

mascot.addEventListener("click", randomYui)