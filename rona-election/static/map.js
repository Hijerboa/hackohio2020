var countyObjects = [];
var json_promise, json_promise2;

$(document).ready(function(){
	console.log("hello there");
	map = L.map('map',{center: [31.51, -96.42], minZoom: 4, zoom: 4});
	L.tileLayer( 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',subdomains: ['a','b','c']}).addTo( map );
  var params = new URLSearchParams();
  params.append('method', 'countydata');
  var myRequest = new Request("http://127.0.0.1:5000/geodata?"+params.toString());
  myRequest.body = params;
  var countyLines = fetch(myRequest).then(function(response) {
    json_promise = response.json();
    json_promise.then((data) => { // handle it on success
      for(i=0; i < data.length; i++){
        var first = JSON.parse(data[i]);
        countyObjects.push(first);
        //L.geoJson(first).addTo(map);
      }
    }, (err) => { // handle it on error
      throw(err);
    });
  });
  console.log("got county data");
  var params = new URLSearchParams();
  params.append('method', 'statedata');
  var myRequest = new Request("http://127.0.0.1:5000/geodata?"+params.toString());
  myRequest.body = params;
  var stateLines = fetch(myRequest).then(function(response) {
    json_promise2 = response.json();
    json_promise2.then((data) => { // handle it on success
      for(i=0; i < data.length; i++){
        var first = JSON.parse(data[i]);
        countyObjects.push(first);
        //L.geoJson(first).addTo(map);
      }
    }, (err) => { // handle it on error
      throw(err);
    });
  });
  console.log("got state data");
  Promise.all([json_promise, json_promise2]).then((values)=>{
    console.log(countyObjects.length);
  });

  for(i=0; i<countyObjects.length; i++){
    console.log(i);
    L.geoJson(countyObjects[i]).addTo(map);
  }
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
