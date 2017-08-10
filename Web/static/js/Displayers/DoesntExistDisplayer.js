var DoesntExistDisplayer;
(function(){
  "use strict";
  DoesntExistDisplayer = function(response){
    this.response = response;
  };
  DoesntExistDisplayer.prototype.show = function(){
    var answer = document.createTextNode("This person doesn 't exist in our databases");
    document.getElementById("response").appendChild(answer);
    $("#preview_photos").show();
  }
}());
