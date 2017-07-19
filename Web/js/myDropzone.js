Dropzone.autoDiscover= false;
function setOperation(){
  if ((document.getElementById("RadioInsertFace").checked == true)){
    return 0;
  }
  if ((document.getElementById("RadiosCheckExistance").checked == true)){
    return 1;
  }
  return 2;
}
var myDropzone = new Dropzone("div#dropzone",{
  url: "http://localhost:3000/", // Set the url
  autoQueue: false, // Make sure the files aren't queued until manually added,
  init: function(){
    document.querySelector("#actions .start").disabled = true;
    document.querySelector("#actions .cancel").disabled = true;
    document.getElementById("RadioInsertFace").disabled = true;
    document.getElementById("RadiosCheckExistance").disabled = true;
    document.getElementById("RadiosGetTrajectory").disabled = true;
  }
});
myDropzone.on('sending', function(file, xhr, formData){
  var operation = setOperation();
  formData.append('operation',operation);
});
myDropzone.on("addedfile", function(file) {
  document.querySelector("#actions .start").disabled = false;
  document.querySelector("#actions .cancel").disabled = false;
  document.getElementById("RadioInsertFace").disabled = false;
  document.getElementById("RadiosCheckExistance").disabled = false;
  document.getElementById("RadiosGetTrajectory").disabled = false;
});

// Setup the buttons for all transfers
// The "add files" button doesn't need to be setup because the config
// `clickable` has already been specified.
document.querySelector("#actions .start").onclick = function() {
  console.log(myDropzone.getFilesWithStatus(Dropzone.ADDED));
  myDropzone.enqueueFiles(myDropzone.getFilesWithStatus(Dropzone.ADDED));
};
document.querySelector("#actions .cancel").onclick = function() {
  myDropzone.removeAllFiles(true);
  document.querySelector("#actions .start").disabled = true;
  document.querySelector("#actions .cancel").disabled = true;
  document.getElementById("RadioInsertFace").disabled = true;
  document.getElementById("RadiosCheckExistance").disabled = true;
  document.getElementById("RadiosGetTrajectory").disabled = true;
  var ele = document.getElementsByName("Choose");
   for(var i=0;i<ele.length;i++)
      ele[i].checked = (i==0)?(true):(false);
};
