var TrajectoryDisplayer;
(function(){
  "use strict";
  TrajectoryDisplayer = function(response){
    this.response = response;
  };
  TrajectoryDisplayer.prototype.show = function(){
    var answer = document.createTextNode("Displaying trajectory");
    document.getElementById("response").appendChild(answer);
  }
}());
