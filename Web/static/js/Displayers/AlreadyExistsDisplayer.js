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
    //$("#preview_photos").append('<div id="response" class="col-xs-3"  style="width:250px;height:270px;border:1px solid #00F;"><span style="color:blue">Best match will appear here.</span></div>')
    document.getElementById("response").appendChild(answer);
    document.getElementById("response").appendChild(linebreak);
    document.getElementById("response").appendChild(match);
    $("#preview_photos").show();
  }
}());
