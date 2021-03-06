var countyObjects = [];
var currentData = [];
var cVisualization = 0;
var map = null;

async function onSidebarClicked(e) {
  if (e === 'deathsAtDate') {
    if (cVisualization != 0){
      cVisualization = 0
      //Do things
      await Promise.all([await requestCovidData('deathsAtDate')]);
      drawMap2();

    }
  } else if (e === 'casesAtDate') {
    if (cVisualization != 1){
      cVisualization = 1
      //Do things
      await Promise.all([await requestCovidData('casesAtDate')]);
      drawMap2();
    }
  } else if (e === 'deathsBy100kAtDate') {
    if (cVisualization != 2){
      cVisualization = 2
      //Do things
      await Promise.all([await requestCovidData('deathsBy100kAtDate')]);
      drawMap2();
    }
  } else if (e === 'casesBy100kAtDate') {
    if (cVisualization != 3){
      cVisualization = 3
      //Do things
      await Promise.all([await requestCovidData('casesBy100kAtDate')]);
      drawMap2();
    }
  } else if (e === 'deathsBy100kAtDateVsMOV') {
    if (cVisualization != 4){
      cVisualization = 4
      //Do things
      await Promise.all([await requestCovidData('deathsBy100kAtDateVsMOV')]);
      drawMap2();
    }
  } else if (e === 'casesBy100kAtDateVsMOV') {
    if (cVisualization != 5){
      cVisualization = 5
      await Promise.all([await requestCovidData('casesBy100kAtDateVsMOV')]);
      drawMap2();
      //Do things
    }
  } else {
    console.log("Invalid sidebar option!");
  }
}

async function requestCovidData(type) {
  var covidParams = new URLSearchParams();
  covidParams.append('method', type);
  covidParams.append('granularity', 'county');
  var covidRequest = new Request("http://127.0.0.1:5000/coviddata?"+covidParams.toString());

  const res = await Promise.all([(await fetch(covidRequest)).json()]);
  console.log(res);
  currentData = valsToNormalized(res);
  //console.log(currentData);
}

async function requestGeodata() {
  // TODO: In a live environment, the requests need changed to: http://themememen.com:5000/...
  var countyParams = new URLSearchParams();
  countyParams.append('method', 'countydata');
  var countyRequest = new Request("http://127.0.0.1:5000/geodata?"+countyParams.toString());

  var stateParams = new URLSearchParams();
  stateParams.append('method', 'statedata');
  var stateRequest = new Request("http://127.0.0.1:5000/geodata?"+stateParams.toString());

  await Promise.all([(await requestCovidData('casesatdate'))]);

  const [counties, states] = await Promise.all([
    (await fetch(countyRequest)).json(),
    (await fetch(stateRequest)).json()
  ]);

  return {counties, states};
}

async function drawMap() {
  await requestGeodata().then(({counties, states}) => {
    countyObjects = countyObjects.concat(counties.map((e) => {
      return JSON.parse(e);
    }));
    countyObjects = countyObjects.concat(states.map((e) => {
      return JSON.parse(e);
    }));
    /*
    countyObjects.map((e) => {
      L.geoJson(e, {weight: 1}).addTo(map);
    });
    */
    for(i = 0; i < countyObjects.length; i++){
      L.geoJson(countyObjects[i], {weight: 1, color: currentData[i][1]}).addTo(map);
    }
  });
}

function drawMap2(){
  map.removeLayer(L.geoJson);
  for(i = 0; i < countyObjects.length; i++){
     L.geoJson(countyObjects[i], {weight: 1, color: currentData[i][1]}).addTo(map);
  }
}

$(document).ready(function(){
	map = L.map('map',{center: [31.51, -96.42], minZoom: 4, zoom: 4});
  L.tileLayer( 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',subdomains: ['a','b','c']}).addTo( map );
  drawMap();
});

//Takes a list of (ID, Value) pairs, and returns (ID, color) pairs where color is a value between 0 and 255
function valsToNormalized(dBOutputs) {
  let res = [];
  let min = dBOutputs[0][0][1];
  let max = dBOutputs[0][0][1];
  //Find min and max value
  //console.log(dBOutputs[0]);
  for(i = 0; i < dBOutputs[0].length; i++){
    if(dBOutputs[0][i][1] > max){max = dBOutputs[0][i][1];}
    if(dBOutputs[0][i][1] < min){min = dBOutputs[0][i][1];}
  }
  //Find offset and scale values
  let offset = 0 - min;
  let scale = max - min;
  for(i = 0; i < dBOutputs[0].length; i++){
    console.log((""+parseInt(((dBOutputs[0][i][1] - offset) / scale) * 255)).toString(16).toUpperCase());
    res.push([dBOutputs[0][i][0], (""+parseInt(((dBOutputs[0][i][1] - offset) / scale) * 255)).toString(16).toUpperCase()]);
  }
  console.log(res)
  return res;
}
