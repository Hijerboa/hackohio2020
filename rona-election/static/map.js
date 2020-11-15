var countyObjects = [];
var map = null;

async function requestGeodata() {
  var countyParams = new URLSearchParams();
  countyParams.append('method', 'countydata');
  var countyRequest = new Request("http://127.0.0.1:5000/geodata?"+countyParams.toString());

  var stateParams = new URLSearchParams();
  stateParams.append('method', 'statedata');
  var stateRequest = new Request("http://127.0.0.1:5000/geodata?"+stateParams.toString());
  
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
    for(i=0; i<countyObjects.length; i++){
      L.geoJson(countyObjects[i]).addTo(map);
    }
  });
}

$(document).ready(function(){
	map = L.map('map',{center: [31.51, -96.42], minZoom: 4, zoom: 4});
  L.tileLayer( 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',subdomains: ['a','b','c']}).addTo( map );
  drawMap();
});

//Takes a list of (ID, Value) pairs, and returns (ID, color) pairs where color is a value between 0 and 255
function valsToNormalized(dBOutputs) {
  let res = [];
  let min = dBOutputs[0][1];
  let max = dBOutputs[0][1];
  //Find min and max value
  for(i = 0; i < dBOutputs.length; i++){
    if(dBOutputs[i][1] > max){max = dBOutputs[i][1];}
    if(dBOutputs[i][1] < min){min = dBOutputs[i][1];}
  }
  //Find offset and scale values
  let offset = 0 - min;
  let scale = max - min;
  for(i = 0; i < dBOutputs.length; i++){
    res.push([dBOutputs[i][0], int(((dBOutputs[i][1] - offset) / scale) * 255)]);
  }
  return res;
}
