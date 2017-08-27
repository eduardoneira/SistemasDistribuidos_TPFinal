var CorrectlyUploadedDisplayer;
(function(){
  "use strict";
  CorrectlyUploadedDisplayer = function(response){
    this.response = response;
  };
  CorrectlyUploadedDisplayer.prototype.show = function(){
    var answer = document.createTextNode("Correctly uploaded");
    //$("#preview_photos").append('<div id="response" class="col-xs-3"  style="width:250px;height:270px;border:1px solid #00F;"><span style="color:blue">Best match will appear here.</span></div>')
    //document.getElementById("response").appendChild(answer);
  }
}());
