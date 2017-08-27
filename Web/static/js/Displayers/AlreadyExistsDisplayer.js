var AlreadyExistsDisplayer;
(function(){
  "use strict";
  AlreadyExistsDisplayer = function(response){
    this.response = response;
  };
  AlreadyExistsDisplayer.prototype.show = function(){
    console.log("Already exists");
    console.log(this.response);
    document.getElementById("outputName").textContent = this.response['name'];
    document.getElementById("outputSurname").textContent = this.response['surname'];
    document.getElementById("outputDni").textContent = this.response['dni'];
    document.getElementById("outputState").textContent = this.response['state'];
  }
}());
