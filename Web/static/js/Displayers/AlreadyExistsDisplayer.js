var AlreadyExistsDisplayer;
(function(){
  "use strict";
  AlreadyExistsDisplayer = function(response){
    this.response = response;
  };
  AlreadyExistsDisplayer.prototype.show = function(){
    var image = document.createElement('img');
    var answer = document.createTextNode("This person already exits in the databse with the following picture");
    var linebreak = document.createElement("br");
    image.src = "data:image/jpg;base64," + this.response.img;
    document.getElementById("response").appendChild(answer);
    document.getElementById("response").appendChild(linebreak);
    document.getElementById("response").appendChild(image);
  }
}());
