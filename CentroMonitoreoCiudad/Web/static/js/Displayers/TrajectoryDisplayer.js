var mymap;
function initMap() {
  console.log("initMap");
  mymap = new google.maps.Map(document.getElementById('map'), {
  center: new google.maps.LatLng(-34.618696, -58.435593),
  zoom: 11
  });
}
function AgregarPuntos(locations){
  console.log("Agrego puntos: "+locations);
  var points = JSON.parse(locations);
  var marker;
  for (var i = 0; i < points.length; i++) {
    console.log("Agrego Lat:"+points[i].lat+"\tLng: "+points[i].lng);
    marker = new google.maps.Marker({
      position: new google.maps.LatLng(points[i].lat, points[i].lng),
      map: mymap
    });
  }
}
var TrajectoryDisplayer;
(function(){
  "use strict";
  TrajectoryDisplayer = function(response){
    this.response = response;
  };
  TrajectoryDisplayer.prototype.show = function(){
    console.log(this.response.points);
    AgregarPuntos(this.response.points);
    var answer = document.createTextNode("Displaying trajectory");
    document.getElementById("response").appendChild(answer);
  }
}());
