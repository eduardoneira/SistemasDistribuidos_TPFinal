var AlreadyExistsDisplayer;
(function(){
  "use strict";
  AlreadyExistsDisplayer = function(response){
    this.response = response;
  };
  AlreadyExistsDisplayer.prototype.show = function(){
    var match = document.createElement('img');
    var answer = document.createTextNode("This person already exits in the databse with the following picture");
    var linebreak = document.createElement("br");
    var filepath="/static/images/"+this.response.match;
    console.log("Match: "+filepath);
    match.src= filepath;
    match.style='height: 100%; width: 100%; object-fit: contain';
    document.getElementById("response").appendChild(answer);
    document.getElementById("response").appendChild(linebreak);
    document.getElementById("response").appendChild(match);
  }
}());
