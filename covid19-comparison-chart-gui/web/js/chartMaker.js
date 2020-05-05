/*** After clicking button, show up the chart
 *
 * on button click
 *	 get values from inputs
 *
 *   async:
 *   	call python to receive:
 *   	   - number of days
 *   	   - data for each country
 *
 *   	make a chart
 *	 	display it
 *
 *
 */

////////////
//// Variables declaration

let button = document.getElementById("generate");
var ctx = document.getElementById("chart").getContext("2d");
let currentChart = new Chart(ctx, {type:'line'});

let COLORS = [
	'#96BFFF',
	'#FFAFA3',
	'#8AF5FF',
	'#FFD070',
	'#7DFFC1',
	'#3e95cd'
];

////////////
//// Function Definitions

async function makeChart(type, countries, align, per_million, start_from, days_limit) {

    let data = await eel.getData(type, countries, align, per_million, start_from, days_limit)();
    let labels = data.labels;
	let countriesData = data.data;

    let datasets = [];
	for(let i = 0; i < countries.length; ++i) {
		datasets.push({
			label: countries[i],
			data: countriesData[i],
			borderColor: COLORS[i],
  			fill: false
		});
	}

	currentChart.data.labels = labels;
	currentChart.data.datasets = datasets;
	currentChart.update();
}

function onButtonClick(e) {
    let type = document.getElementById('type').value; 
	let countries = getCountries();
	let per_million = document.getElementById('per-million').checked;
	let align = document.getElementById('align').checked;

	let start_from = '';
	let days_limit = '';
	if (align) {
		start_from = document.getElementById('start-from').value; 
		days_limit = document.getElementById('days-limit').value;
	}

	if (start_from == '' || start_from == null)
		start_from = 100;
	else start_from = parseInt(start_from);

	if (days_limit == '' || days_limit == null)
		days_limit = 0;
	else days_limit = parseInt(days_limit);

    makeChart(type, countries, align, per_million, start_from, days_limit);
}

eel.expose(signalizeState);
function signalizeState(message) {
	div = document.getElementById('state');
	div.innerHTML = message;
}

////////////
//// Script


button.onclick = onButtonClick;
