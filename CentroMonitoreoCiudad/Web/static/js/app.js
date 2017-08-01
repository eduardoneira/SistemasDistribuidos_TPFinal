/*global ResponseDisplayerFactory */
const REQUESTEXISTANCE = 4;
const REQUESTUPLOAD = 5;
const REQUESTTRAJECTORY=6;
const STATELEGALPROBLEMS= 7;
const STATEMISSING=8;
function setOperation(){
  if ((document.getElementById("RadioInsertFace").checked == true)){
    return REQUESTUPLOAD;
  }
  if ((document.getElementById("RadiosCheckExistance").checked == true)){
    return REQUESTEXISTANCE;
  }
  return REQUESTTRAJECTORY;
}
function setState(){
  if ((document.getElementById("RadiosCheckLegalProblems").checked == true)){
    return STATELEGALPROBLEMS;
  }
  return STATEMISSING;
}
function setDefaultRadioButtonSelection(radioButtonsName){
  var ele = document.getElementsByName(radioButtonsName);
   for(var i=0;i<ele.length;i++)
      ele[i].checked = (i==0)?(true):(false);
}
function disableButtonsAndRadio(setDisable){
  document.querySelector(".start").disabled = setDisable;
  document.querySelector(".home").disabled = setDisable;
  document.getElementById("RadioInsertFace").disabled = setDisable;
  document.getElementById("RadiosCheckExistance").disabled = setDisable;
  document.getElementById("RadiosGetTrajectory").disabled = setDisable;
  document.getElementById("RadiosCheckLegalProblems").disabled = setDisable;
  document.getElementById("RadiosCheckMissing").disabled = setDisable;
}
Dropzone.autoDiscover= false;
$(function() {
var myDropzone = new Dropzone("div#droparea", {
    url: "/uploadajax",
    method: "POST", // can be changed to "put" if necessary
    maxFilesize: 2, // in MB
    paramName: "file", // The name that will be used to transfer the file
    uploadMultiple: true, // This option will also trigger additional events (like processingmultiple).
    previewsContainer: "#previewsContainer",
    createImageThumbnails: true,
    maxThumbnailFilesize: 2, // in MB
    thumbnailWidth: 300,
    thumbnailHeight: 300,
    maxFiles: 1,
    acceptedFiles: "image/png, image/jpeg, image/gif", //This is a comma separated list of mime types or file extensions.Eg.: image/*,application/pdf,.psd.
    autoProcessQueue: false, // When set to false you have to call myDropzone.processQueue() yourself in order to upload the dropped files.
    forceFallback: false,
    init: function(){
      disableButtonsAndRadio(true);
      setDefaultRadioButtonSelection("Choose")
      setDefaultRadioButtonSelection("ChooseState")
    },
    accept: function(file, done) {
      console.log("accept");
      done();
    },
    fallback: function() {
      console.log("fallback");
    },
    resize: function(file) {
        var resizeInfo = {
            srcX: 0,
            srcY: 0,
            trgX: 0,
            trgY: 0,
            srcWidth: file.width,
            srcHeight: file.height,
            trgWidth: this.options.thumbnailWidth,
            trgHeight: this.options.thumbnailHeight
        };
        return resizeInfo;
    }
  });

  /*
   * Custom preview template here.
   * ex) myDropzone.options.previewTemplate = '';
   */
  myDropzone.options.previewTemplate = '\
    <div class="dz-preview dz-file-preview">\
    <img data-dz-thumbnail />\
    </div>\
    <div class="dz-progress"><span class="dz-upload" data-dz-uploadprogress></span></div>\
    <div class="dz-error-message"><span data-dz-errormessage></span></div>\
    </div>';


  /*
   * Available Events
   */

  /* receive the "event" as first parameter */
  myDropzone.on("drop", function(event){
    console.log(event.type);
    console.log(event)
  });
  myDropzone.on("dragstart", function(event){ console.log(event.type); });
  myDropzone.on("dragend", function(event){ console.log(event.type); });
  myDropzone.on("dragenter", function(event){ console.log(event.type); });
  myDropzone.on("dragover", function(event){ console.log(event.type); });
  myDropzone.on("dragremove", function(event){ console.log(event.type); });

  /* receive the "file" as first parameter */
  myDropzone.on("addedfile", function(file) {
    console.log("addedfile");
    if (this.files[1]!=null){
        this.removeFile(this.files[0]);
      }
    disableButtonsAndRadio(false);
    $('.start').click(function(){
        myDropzone.processQueue(); //processes the queue
        disableButtonsAndRadio(true);
    });
    $('.home').click(function(){
      //myDropzone.removeAllFiles(true);
      window.location.reload();
    });
  });
  myDropzone.on("removedfile", function(file) {
    console.log("removedfile");
    disableButtonsAndRadio(true);
    setDefaultRadioButtonSelection("Choose")
    setDefaultRadioButtonSelection("ChooseState")
    var response = document.getElementById("response");
    while (response.firstChild) {
        response.removeChild(response.firstChild);
    }
    var spanInfo = document.createElement("SPAN");
    spanInfo.setAttribute('style', 'color: blue');
    var text = document.createTextNode("Best match will appear here.");
    spanInfo.appendChild(text);
    response.appendChild(spanInfo);
  });
  myDropzone.on('sending', function(file, xhr, formData){
    var operation = setOperation();
    var state = setState();
    formData.append('operation',operation);
    formData.append('state', state)
  });
  myDropzone.on("success", function(file, response) {
    displayerFactory = new ResponseDisplayerFactory(response);
    displayer = displayerFactory.createDisplayer();
    displayer.show();
  });
});
