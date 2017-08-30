var DoesntExistDisplayer;
(function(){
  "use strict";
  DoesntExistDisplayer = function(response){
    this.response = response;
  };
  DoesntExistDisplayer.prototype.show = function(){
    document.getElementById("outputName").textContent = "Unknown";
    document.getElementById("outputSurname").textContent = "Unknown";
    document.getElementById("outputDni").textContent = "Unknown";
    document.getElementById("outputState").textContent = "Unknown";
  }
}());
