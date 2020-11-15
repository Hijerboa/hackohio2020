async function fetchDataFromDatabase() {
  let response = await fetch("http://themememen.com/mapData");
  console.log(response);
  let result = await response.json();
  return result;
}

$(document).ready(function(){
	console.log("hello there");
	map = L.map('map',{center: [31.51, -96.42], minZoom: 4, zoom: 4});
	L.tileLayer( 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',subdomains: ['a','b','c']}).addTo( map );
  //L.geoJson(statesData).addTo(map);
  var myRequest = new Request("http://127.0.0.1:5000/countydata");
  var countyLines = fetch(myRequest).then(function(response) {
    let json_promise = response.json();
    json_promise.then((data) => { // handle it on success
      for(i=0; i < data.length; i++){
        var first = JSON.parse(data[i]);
        L.geoJson(first).addTo(map);
      }
    }, (err) => { // handle it on error
      throw(err);
    });
  });
  myRequest = new Request("http://127.0.0.1:5000/statedata");
  var stateLines = fetch(myRequest).then(function(response) {
    let json_promise = response.json();
    json_promise.then((data) => { // handle it on success
      for(i=0; i < data.length; i++){
        var first = JSON.parse(data[i]);
        L.geoJson(first).addTo(map);
      }
    }, (err) => { // handle it on error
      throw(err);
    });
  });
});
