const MASCOT_COUNT = 17;
const MASCOTS = [...new Array(MASCOT_COUNT)].map((_, i) => i + 1)
const NOVELTY = [11, 15, 16];  //< Novelty/special mascots.

const mascot = document.getElementById("mascot");
const favicon = document.querySelector("link[rel~='icon']");

const setMascot = (pick) => {
	const stem = `/mascots/${pick}`;
	mascot.style.opacity = 0;
	mascot.setAttribute('src', `${stem}.png`);
	favicon.setAttribute('href', `${stem}-square.png`);

	const loaded = () => { mascot.style.opacity = .85 };
	if (mascot.complete) loaded();
	else mascot.addEventListener('load', loaded);
}

const randomMascot = (excludeList=[]) => {
	if (!Array.isArray(excludeList)) excludeList = [];

	const picks = MASCOTS.filter(e => !excludeList.includes(e));
	const pick = picks[Math.floor(Math.random() * picks.length)];
	setMascot(pick);

	useColourScheme({
		11: 'pink',
		15: 'green',
		16: 'rainbow'
	}[pick] || 'default');
}

mascot.addEventListener('click', randomMascot)
