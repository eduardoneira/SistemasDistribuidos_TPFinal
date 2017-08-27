/*global ResponseDisplayerFactory */
//const REQUESTEXISTANCE = 4;
const REQUESTUPLOAD = 5;
//const REQUESTTRAJECTORY=6;
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
function getState(){
  console.log("get state");
  if ((document.getElementById("gridRadios1").checked == true)){
    console.log("Legal problems");
    return STATELEGALPROBLEMS;
  }
  console.log("missing");
  return STATEMISSING;
}
function setDefaultRadioButtonSelection(){
  document.getElementById("gridRadios1").disabled = false;
  document.getElementById("gridRadios2").disabled = true;
}
function disableButtonsAndRadio(setDisable){
  document.getElementById("startAddPerson").disabled = setDisable;
  document.getElementById("cancelAddPerson").disabled = setDisable;
  document.getElementById("gridRadios1").disabled = setDisable;
  document.getElementById("gridRadios2").disabled = setDisable;
  document.getElementById("inputNameAddPerson").disabled = setDisable;
  document.getElementById("inputSurnameAddPerson").disabled = setDisable;
  document.getElementById("inputDniAddPerson").disabled = setDisable;
}

Dropzone.autoDiscover= false;
$(function() {
var dropzoneAddPerson = new Dropzone("div#dropareaAddPerson", {
    url: "/uploadajax",
    method: "POST", // can be changed to "put" if necessary
    maxFilesize: 2, // in MB
    paramName: "file", // The name that will be used to transfer the file
    uploadMultiple: true, // This option will also trigger additional events (like processingmultiple).
    parallelUploads: 100,
    previewsContainer: "#previewsContainerAddPerson",
    createImageThumbnails: true,
    maxThumbnailFilesize: 2, // in MB
    maxFiles: 100,
    addRemoveLinks : true,
    hiddenInputContainer: "#previewsContainerAddPerson .addfile",
    dictResponseError: 'Server not responding',
    renderMethod: "prepend",
    dictDefaultMessage: "Add Photo",
    clickable : "#previewsContainerAddPerson .addfile",
    acceptedFiles: ".jpg, .jpeg, .JPG, .JPEG", //This is a comma separated list of mime types or file extensions.Eg.: image/*,application/pdf,.psd.
    autoProcessQueue: false, // When set to false you have to call myDropzone.processQueue() yourself in order to upload the dropped files.
    forceFallback: false,
    init: function(){
      disableButtonsAndRadio(true);
      setDefaultRadioButtonSelection();
    },
    accept: function(file, done) {
      console.log("accept");
      done();
    }
  });

  dropzoneAddPerson.options.previewTemplate = '\
    <div class= pic dz-preview dz-file-preview>\
      <div class="dz-image">\
        <img data-dz-thumbnail />\
        </div>\
      <div class="dz-details">\
          <div class="dz-size">\
            <span data-dz-size></span>\
          </div>\
          <div class="dz-filename">\
            <span data-dz-name></span>\
          </div>\
      </div>\
      <div class="dz-progress">\
        <span class="dz-upload" data-dz-uploadprogress></span>\
      </div>\
      <div class="dz-error-message">\
        <span data-dz-errormessage></span>\
      </div>\
      <div class="dz-success-mark">\
        <svg width="30px" height="30px" viewBox="0 0 30 30" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:sketch="http://www.bohemiancoding.com/sketch/ns">\
          <title>Check</title>\
          <defs></defs>\
          <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" sketch:type="MSPage">\
            <path d="M23.5,31.8431458 L17.5852419,25.9283877 C16.0248253,24.3679711 13.4910294,24.366835 11.9289322,25.9289322 C10.3700136,27.4878508 10.3665912,30.0234455 11.9283877,31.5852419 L20.4147581,40.0716123 C20.5133999,40.1702541 20.6159315,40.2626649 20.7218615,40.3488435 C22.2835669,41.8725651 24.794234,41.8626202 26.3461564,40.3106978 L43.3106978,23.3461564 C44.8771021,21.7797521 44.8758057,19.2483887 43.3137085,17.6862915 C41.7547899,16.1273729 39.2176035,16.1255422 37.6538436,17.6893022 L23.5,31.8431458 Z M27,53 C41.3594035,53 53,41.3594035 53,27 C53,12.6405965 41.3594035,1 27,1 C12.6405965,1 1,12.6405965 1,27 C1,41.3594035 12.6405965,53 27,53 Z" id="Oval-2" stroke-opacity="0.198794158" stroke="#FFFFFF" fill-opacity="0.816519475" fill="#32A336" sketch:type="MSShapeGroup"></path>\
          </g>\
        </svg>\
      </div>\
      <div class="dz-error-mark">\
        <svg width="30px" height="30px" viewBox="0 0 30 30" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:sketch="http://www.bohemiancoding.com/sketch/ns">\
          <title>Error</title>\
          <defs></defs>\
          <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" sketch:type="MSPage">\
            <g id="Check-+-Oval-2" sketch:type="MSLayerGroup" stroke="#FFFFFF" stroke-opacity="0.198794158" fill="#ff0000" fill-opacity="0.816519475">\
              <path d="M32.6568542,29 L38.3106978,23.3461564 C39.8771021,21.7797521 39.8758057,19.2483887 38.3137085,17.6862915 C36.7547899,16.1273729 34.2176035,16.1255422 32.6538436,17.6893022 L27,23.3431458 L21.3461564,17.6893022 C19.7823965,16.1255422 17.2452101,16.1273729 15.6862915,17.6862915 C14.1241943,19.2483887 14.1228979,21.7797521 15.6893022,23.3461564 L21.3431458,29 L15.6893022,34.6538436 C14.1228979,36.2202479 14.1241943,38.7516113 15.6862915,40.3137085 C17.2452101,41.8726271 19.7823965,41.8744578 21.3461564,40.3106978 L27,34.6568542 L32.6538436,40.3106978 C34.2176035,41.8744578 36.7547899,41.8726271 38.3137085,40.3137085 C39.8758057,38.7516113 39.8771021,36.2202479 38.3106978,34.6538436 L32.6568542,29 Z M27,53 C41.3594035,53 53,41.3594035 53,27 C53,12.6405965 41.3594035,1 27,1 C12.6405965,1 1,12.6405965 1,27 C1,41.3594035 12.6405965,53 27,53 Z" id="Oval-2" sketch:type="MSShapeGroup">\
              </path>\
            </g>\
          </g>\
        </svg>\
      </div>\
    </div>';

  dropzoneAddPerson.options.dictRemoveFile  = '\
    <div class="remove" data-dz-remove>\
      <i class="glyphicon glyphicon-remove"></i>\
    </div>';
  /* receive the "file" as first parameter */
  dropzoneAddPerson.on("addedfile", function(file) {
    console.log("addedfile");
    disableButtonsAndRadio(false);
    $('#startAddPerson').click(function(){
        console.log("start add person");
        dropzoneAddPerson.processQueue(); //processes the queue
        disableButtonsAndRadio(true);
        document.getElementById("cancelAddPerson").disabled = false;
    });
    $('#cancelAddPerson').click(function(){
      console.log("cancel add person");
      dropzoneAddPerson.removeAllFiles(true);
      document.getElementById("inputNameAddPerson").value = "";
      document.getElementById("inputSurnameAddPerson").value = "";
      document.getElementById("inputDniAddPerson").value = "";
    });
  });
  dropzoneAddPerson.on("removedfile", function(file) {
    console.log("removedfile");
    disableButtonsAndRadio(true);
    setDefaultRadioButtonSelection();
  });
  dropzoneAddPerson.on('sending', function(file, xhr, formData){
    /*console.log("sending single");
    var operation = REQUESTUPLOAD;
    var state = getState();
    formData.append('operation',operation);
    formData.append('state', state);
    formData.append('name', getElementById("inputNameAddPerson").value);
    formData.append('surname', getElementById("inputSurnameAddPerson").value);
    formData.append('dni', getElementById("inputDniAddPerson").value);
    $('.meter').show();*/
  });
  dropzoneAddPerson.on("error", function(file) { console.log("error"); });
  dropzoneAddPerson.on("maxfilesreached", function(file) { console.log("maxfilesreached"); });
  dropzoneAddPerson.on("maxfilesexceeded", function(file) { console.log("maxfilesexceeded"); });
  dropzoneAddPerson.on('sendingmultiple', function(file, xhr, formData){
    console.log("dropzone on sendingmultiple");
    var operation = REQUESTUPLOAD;
    var state = getState();
    formData.append('operation',REQUESTUPLOAD);
    formData.append('state', state);
    console.log("input name person");
    formData.append('name', $('#inputNameAddPerson').val());
    console.log("input surname");
    formData.append('surname', $('#inputSurnameAddPerson').val());
    console.log("input dni");
    formData.append('dni', $('#inputDniAddPerson').val());
    //$('.meter').show();
  });
  dropzoneAddPerson.on("success", function(file, response) {
    //TODO: ver aca
    // disableButtonsAndRadio(false);
    console.console.log("on success");
    displayerFactory = new ResponseDisplayerFactory(response);
    displayer = displayerFactory.createDisplayer();
    displayer.show();

  });
  dropzoneAddPerson.on("totaluploadprogress", function (progress) {
    console.log("progress ", progress);
    $('.roller').width(progress + '%');
  });

  dropzoneAddPerson.on("queuecomplete", function (progress) {
    console.log("queuecomplete");
    $('.meter').delay(999).slideUp(999);
  });
});
