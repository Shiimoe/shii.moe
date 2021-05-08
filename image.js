const mascot = document.getElementById("mascot");
const favicon = document.querySelector("link[rel~='icon']");

const randomYui = () => {
	const stem = "/mascots/" + Math.floor(1 + Math.random()*14);
	mascot.setAttribute("src", stem + ".png");
	favicon.setAttribute("href", stem + "-square.png");
}

randomYui();

mascot.addEventListener("click", randomYui)
