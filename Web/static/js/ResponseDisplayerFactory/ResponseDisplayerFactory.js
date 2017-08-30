/*global  AlreadyExistsDisplayer, CorrectlyUploadedDisplayer, UncorrectlyUploadedDisplayer */
/*global DoesntExistDisplayer, TrajectoryDisplayer, UnknownTrajectoryDisplayer*/
var ResponseDisplayerFactory;
const RESPONSEALREADYEXISTS=0;
const RESPONSECORRECTLYUPLOADED=1;
const RESPONSEDOESNTEXIST=2;
const RESPONSETRAJECTORY=3;
(function(){
  "use strict";
  ResponseDisplayerFactory = function(file, response){
    this.response = response;
    this.answer = response.answer;
    this.type = response.operation;
    this.file = file;
  };
  ResponseDisplayerFactory.prototype.createRequestUploadDisplayer= function() {
    if (this.answer == RESPONSECORRECTLYUPLOADED){
      return new CorrectlyUploadedDisplayer(this.response);
    }
    return new UncorrectlyUploadedDisplayer(this.file, this.response);
  }
  ResponseDisplayerFactory.prototype.createRequestExistanceDisplayer = function (){
    if (this.answer == RESPONSEALREADYEXISTS){
      return new AlreadyExistsDisplayer(this.response);
    }
    return new DoesntExistDisplayer(this.file, this.response);
  }
  ResponseDisplayerFactory.prototype.createRequestTrajectoryDisplayer = function (){
    if (this.answer == RESPONSETRAJECTORY){
      return new TrajectoryDisplayer(this.response);
    }
    return new UnknownTrajectoryDisplayer(this.response);
  }
  ResponseDisplayerFactory.prototype.createDisplayer= function(){
    if (this.type == REQUESTUPLOAD) {
      return this.createRequestUploadDisplayer();
    }
    if (this.type == REQUESTEXISTANCE) {
      return this.createRequestExistanceDisplayer();
    }
    if (this.type == REQUESTTRAJECTORY){
      return createRequestTrajectoryDisplayer();
    }

  };
}());
