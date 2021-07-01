const YUI_COUNT = 17;
const NOVELTY = [11, 15, 16];

const mascot = document.getElementById("mascot");
const favicon = document.querySelector("link[rel~='icon']");
mascot.style.opacity = 0;

const randomYui = (excludeList=[]) => {
	if (!Array.isArray(excludeList))
		excludeList = [];
	const picks = [...new Array(YUI_COUNT)]
		.map((_, i) => i + 1)
		.filter(e => !excludeList.includes(e));
	const pick = picks[Math.floor(Math.random() * picks.length)];
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
