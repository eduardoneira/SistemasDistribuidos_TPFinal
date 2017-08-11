var TrajectoryDisplayer;
(function(){
  "use strict";
  TrajectoryDisplayer = function(response){
    this.response = response;
  };
  TrajectoryDisplayer.prototype.show = function(){
    if (this.response.points.length > 0){
      console.log(this.response.points);
      AgregarPuntos(this.response.points);
      var filepath="/static/images/"+this.response.match;
      console.log("Match: "+filepath);
      //$("#preview_photos").append('<div id="response" class="col-xs-3"  style="width:250px;height:270px;border:1px solid #00F;"><span style="color:blue">Best match will appear here.</span></div>')
      var response= document.getElementById('response');
      var match = document.createElement("img");
      match.src= filepath;
      match.style='height: 100%; width: 100%; object-fit: contain';
      response.appendChild(match);
      //$("#trajectory_map").show();
      $("#preview_photos").show();  
    }
  }
}());
