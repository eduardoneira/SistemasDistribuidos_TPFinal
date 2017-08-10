var TrajectoryDisplayer;
(function(){
  "use strict";
  TrajectoryDisplayer = function(response){
    this.response = response;
  };
  TrajectoryDisplayer.prototype.show = function(){
    console.log(this.response.points);
    AgregarPuntos(this.response.points);
    var filepath="/static/images/"+this.response.match;
    console.log("Match: "+filepath);
    var response= document.getElementById('response');
    var match = document.createElement("img");
    match.src= filepath;
    match.style='height: 100%; width: 100%; object-fit: contain';
    response.appendChild(match);
    $("#trajectory_map").show();
    $("#preview_photos").show();
  }
}());
