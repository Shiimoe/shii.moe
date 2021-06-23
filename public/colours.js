const ROOT = window.document.documentElement;

const COLOUR_SCHEMES = {
	default: {
		'bg-colour': '#badaff',
		'hue': '0deg'
	},
	pink: {
		'bg-colour': '#ffcdef',
		'hue': '75deg'
	},
	green: {
		'bg-colour': '#91ffeb',
		'hue': '300deg'
	}
}

const CSS = new Proxy({}, {
	get(_, variable) {
		const styles = window.getComputedStyles(ROOT);
		return styles.getPropertyValue(`--${variable}`).trim();
	},
	set(_, variable, value) {
		return ROOT.style.setProperty(`--${variable}`, value);
	}
});

let currentScheme = 'default';
let rainbowInterval = null;
let hueOffs = 0;

function useColourScheme(scheme) {
	if (scheme === currentScheme) return;
	currentScheme = scheme;

	clearInterval(rainbowInterval);
	if (scheme === 'rainbow') {
		hueOffs = 0;
		rainbowInterval = setInterval(() => {
			CSS['bg-colour'] = `hsl(${hueOffs + 212}deg, 100%, 86%)`;
			CSS['hue'] = `${hueOffs}deg`;
			hueOffs = (hueOffs + 2) % 360;
		}, 40)
		return;
	}

	const variables = COLOUR_SCHEMES[scheme];
	for (const variable in variables)
		CSS[variable] = variables[variable];
}

