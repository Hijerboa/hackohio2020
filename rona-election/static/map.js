var map;

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
	/*$.getJSON("http://themememen.com/mapData", function(data){
		console.log("data retrieved");
	});*/
	/*const response = await fetch('http://themememen.com/mapData');
	const json = await response.json();*/
	fetchDataFromDatabase().then(result => console.log(result));
	console.log("Data should be retrieved");
});
