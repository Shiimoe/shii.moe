const YUI_COUNT = 17;

const mascot = document.getElementById("mascot");
const favicon = document.querySelector("link[rel~='icon']");

const randomYui = () => {
	const pick = Math.floor(1 + Math.random() * YUI_COUNT);
	const stem = "/mascots/" + pick;
	mascot.setAttribute("src", stem + ".png");
	favicon.setAttribute("href", stem + "-square.png");

	if      (pick === 11) useColourScheme('pink');
	if      (pick === 15) useColourScheme('green');
	else if (pick === 16) useColourScheme('rainbow');
	else                  useColourScheme('default');
}

mascot.addEventListener("click", randomYui)
