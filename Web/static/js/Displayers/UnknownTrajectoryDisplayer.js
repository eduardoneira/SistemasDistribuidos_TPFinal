var UnknownTrajectoryDisplayer;
(function(){
  "use strict";
  UnknownTrajectoryDisplayer = function(response){
    this.response = response;
  };
  UnknownTrajectoryDisplayer.prototype.show = function(){
    alert("Unknown trajetory");
  }
}());
