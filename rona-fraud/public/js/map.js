var map;

$(document).ready(function(){
  map = L.map('map', {center: [39.83, -98.53], minZoom: 5, zoom: 5});
  L.tileLayer( 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>', subdomains: ['a','b','c']}).addTo( map );
});
