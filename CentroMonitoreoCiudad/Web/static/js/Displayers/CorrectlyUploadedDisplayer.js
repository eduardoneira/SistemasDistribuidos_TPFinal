var CorrectlyUploadedDisplayer;
(function(){
  "use strict";
  CorrectlyUploadedDisplayer = function(response){
    this.response = response;
  };
  CorrectlyUploadedDisplayer.prototype.show = function(){
    var answer = document.createTextNode("Correctly uploaded");
    document.getElementById("response").appendChild(answer);
  }
}());
