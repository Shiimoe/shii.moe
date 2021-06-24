const YUI_COUNT = 17;

const mascot = document.getElementById("mascot");
const favicon = document.querySelector("link[rel~='icon']");
mascot.style.opacity = 0;

const randomYui = () => {
	const pick = Math.floor(1 + Math.random() * YUI_COUNT);
	const stem = "/mascots/" + pick;
	mascot.style.opacity = 0;
	mascot.setAttribute("src", stem + ".png");
	favicon.setAttribute("href", stem + "-square.png");

	const loaded = () => { mascot.style.opacity = .85 };
	if (mascot.complete) loaded();
	else mascot.addEventListener('load', loaded);

	useColourScheme({
		11: 'pink',
		15: 'green',
		16: 'rainbow'
	}[pick] || 'default');
}

mascot.addEventListener("click", randomYui)
