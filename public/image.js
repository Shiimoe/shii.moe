const YUI_COUNT = 17;

const mascot = document.getElementById("mascot");
const favicon = document.querySelector("link[rel~='icon']");

const randomYui = () => {
	const pick = Math.floor(1 + Math.random() * YUI_COUNT);
	const stem = "/mascots/" + pick;
	mascot.setAttribute("src", stem + ".png");
	favicon.setAttribute("href", stem + "-square.png");

	useColourScheme({
		11: 'pink',
		15: 'green',
		16: 'rainbow'
	}[pick] || 'default');
}

mascot.addEventListener("click", randomYui)
