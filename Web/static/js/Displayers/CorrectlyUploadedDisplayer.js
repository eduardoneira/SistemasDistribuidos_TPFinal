var CorrectlyUploadedDisplayer;
(function(){
  "use strict";
  CorrectlyUploadedDisplayer = function(response){
    this.response = response;
  };
  CorrectlyUploadedDisplayer.prototype.show = function(){
    alert("Correctly uploaded");
  }
}());
