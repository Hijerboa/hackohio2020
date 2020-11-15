var map;

$(document).ready(function(){
	console.log("hello there");
	map = L.map('map',{center: [20.0, 5.0], minZoom: 2, zoom: 2});
	L.tileLayer( 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',subdomains: ['a','b','c']}).addTo( map ); 
	/*$.getJSON("http://themememen.com/mapData", function(data){
		console.log("data retrieved");
	});*/
	/*const response = await fetch('http://themememen.com/mapData');
	const json = await response.json();*/
	let fetchDataFromDatabase = async ("http://themememen.com/mapData")=>{
		let response = await fetch("http://themememen.com/mapData");
		let result = await response.json();
	}
	console.log("Data should be retrieved");
});
