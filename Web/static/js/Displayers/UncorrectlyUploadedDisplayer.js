var UncorrectlyUploadedDisplayer;
(function(){
  "use strict";
  UncorrectlyUploadedDisplayer = function(response){
    this.response = response;
  };
  UncorrectlyUploadedDisplayer.prototype.show = function(){
    alert("Uncorrectly uploaded");
  }
}());
