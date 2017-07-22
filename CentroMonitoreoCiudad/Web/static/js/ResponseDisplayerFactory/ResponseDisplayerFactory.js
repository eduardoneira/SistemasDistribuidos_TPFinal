/*global  AlreadyExistsDisplayer, CorrectlyUploadedDisplayer */
/*global DoesntExistDisplayer, TrajectoryDisplayer*/
var ResponseDisplayerFactory;
const RESPONSEALREADYEXISTS=0;
const RESPONSECORRECTLYUPLOADED=1;
const RESPONSEDOESNTEXIST=2;
const RESPONSETRAJECTORY=3;
(function(){
  "use strict";
  ResponseDisplayerFactory = function(response){
    this.response = response;
    this.type = response.operation;
  };
  ResponseDisplayerFactory.prototype.createDisplayer= function(){
    if (this.type == RESPONSEALREADYEXISTS){
      return new AlreadyExistsDisplayer(this.response);
    }
    if (this.type == RESPONSECORRECTLYUPLOADED) {
      return new CorrectlyUploadedDisplayer(this.response);
    }
    if (this.type == RESPONSEDOESNTEXIST){
      return new DoesntExistDisplayer(this.response);
    }
    if (this.type == RESPONSETRAJECTORY) {
      return new TrajectoryDisplayer(this.response);
    }
    return NULL;
  };
}());
