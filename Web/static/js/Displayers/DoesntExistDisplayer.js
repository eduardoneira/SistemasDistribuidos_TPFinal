var DoesntExistDisplayer;
(function(){
  "use strict";
  DoesntExistDisplayer = function(response){
    this.response = response;
  };
  DoesntExistDisplayer.prototype.show = function(){
    var answer = document.createTextNode("This person doesn 't exist in our databases");
    //$("#preview_photos").append('<div id="response" class="col-xs-3"  style="width:250px;height:270px;border:1px solid #00F;"><span style="color:blue">Best match will appear here.</span></div>')
    document.getElementById("response").appendChild(answer);
    $("#preview_photos").show();
  }
}());
