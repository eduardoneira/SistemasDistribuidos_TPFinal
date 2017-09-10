const REQUESTUPLOAD = 5;
const STATELEGALPROBLEMS= 7;
const STATEMISSING=8;

function getState(){
  if ((document.getElementById("gridRadios1").checked == true)){
    return STATELEGALPROBLEMS;
  }
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
$("#compose-photo").dropzone({
    maxFilesize: 2, // in MB
    paramName: "file",
    uploadMultiple: true,
    parallelUploads: 100,
    previewsContainer: "#file-uploader",
    createImageThumbnails: true,
    maxThumbnailFilesize: 2, // in MB
    maxFiles: 100,
    addRemoveLinks : true,
    hiddenInputContainer: "#file-uploader .addfile",
    dictResponseError: 'Server not responding',
    renderMethod: "prepend",
    dictDefaultMessage: "Add Photo",
    clickable : "#file-uploader .addfile",
    acceptedFiles: ".jpg, .jpeg, .JPG, .JPEG",
    autoProcessQueue: false,
    forceFallback: false,
    previewTemplate: "<div class=\"pic dz-preview dz-file-preview\">\n  <div class=\"dz-image\"><img data-dz-thumbnail /></div>\n  <div class=\"dz-details\">\n    <div class=\"dz-size\"><span data-dz-size></span></div>\n    <div class=\"dz-filename\"><span data-dz-name></span></div>\n  </div>\n  <div class=\"dz-progress\"><span class=\"dz-upload\" data-dz-uploadprogress></span></div>\n  <div class=\"dz-error-message\"><span data-dz-errormessage></span></div>\n  <div class=\"dz-success-mark\">\n    <svg width=\"54px\" height=\"54px\" viewBox=\"0 0 54 54\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xmlns:sketch=\"http://www.bohemiancoding.com/sketch/ns\">\n      <title>Check</title>\n      <defs></defs>\n      <g id=\"Page-1\" stroke=\"none\" stroke-width=\"1\" fill=\"none\" fill-rule=\"evenodd\" sketch:type=\"MSPage\">\n<path d=\"M23.5,31.8431458 L17.5852419,25.9283877 C16.0248253,24.3679711 13.4910294,24.366835 11.9289322,25.9289322 C10.3700136,27.4878508 10.3665912,30.0234455 11.9283877,31.5852419 L20.4147581,40.0716123 C20.5133999,40.1702541 20.6159315,40.2626649 20.7218615,40.3488435 C22.2835669,41.8725651 24.794234,41.8626202 26.3461564,40.3106978 L43.3106978,23.3461564 C44.8771021,21.7797521 44.8758057,19.2483887 43.3137085,17.6862915 C41.7547899,16.1273729 39.2176035,16.1255422 37.6538436,17.6893022 L23.5,31.8431458 Z M27,53 C41.3594035,53 53,41.3594035 53,27 C53,12.6405965 41.3594035,1 27,1 C12.6405965,1 1,12.6405965 1,27 C1,41.3594035 12.6405965,53 27,53 Z\" id=\"Oval-2\" stroke-opacity=\"0.198794158\" stroke=\"#FFFFFF\" fill-opacity=\"0.816519475\" fill=\"#32A336\" sketch:type=\"MSShapeGroup\"></path>\n      </g>\n    </svg>\n  </div>\n  <div class=\"dz-error-mark\">\n    <svg width=\"54px\" height=\"54px\" viewBox=\"0 0 54 54\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xmlns:sketch=\"http://www.bohemiancoding.com/sketch/ns\">\n      <title>Error</title>\n      <defs></defs>\n      <g id=\"Page-1\" stroke=\"none\" stroke-width=\"1\" fill=\"none\" fill-rule=\"evenodd\" sketch:type=\"MSPage\">\n<g id=\"Check-+-Oval-2\" sketch:type=\"MSLayerGroup\" stroke=\"#FFFFFF\" stroke-opacity=\"0.198794158\" fill=\"#ff0000\" fill-opacity=\"0.816519475\">\n  <path d=\"M32.6568542,29 L38.3106978,23.3461564 C39.8771021,21.7797521 39.8758057,19.2483887 38.3137085,17.6862915 C36.7547899,16.1273729 34.2176035,16.1255422 32.6538436,17.6893022 L27,23.3431458 L21.3461564,17.6893022 C19.7823965,16.1255422 17.2452101,16.1273729 15.6862915,17.6862915 C14.1241943,19.2483887 14.1228979,21.7797521 15.6893022,23.3461564 L21.3431458,29 L15.6893022,34.6538436 C14.1228979,36.2202479 14.1241943,38.7516113 15.6862915,40.3137085 C17.2452101,41.8726271 19.7823965,41.8744578 21.3461564,40.3106978 L27,34.6568542 L32.6538436,40.3106978 C34.2176035,41.8744578 36.7547899,41.8726271 38.3137085,40.3137085 C39.8758057,38.7516113 39.8771021,36.2202479 38.3106978,34.6538436 L32.6568542,29 Z M27,53 C41.3594035,53 53,41.3594035 53,27 C53,12.6405965 41.3594035,1 27,1 C12.6405965,1 1,12.6405965 1,27 C1,41.3594035 12.6405965,53 27,53 Z\" id=\"Oval-2\" sketch:type=\"MSShapeGroup\"></path>\n</g>\n      </g>\n    </svg>\n  </div>\n</div>",
    dictRemoveFile: "<div class=\"remove\" data-dz-remove><i class=\"glyphicon glyphicon-remove\"></i></div>",
    init: function(){
      disableButtonsAndRadio(true);
      setDefaultRadioButtonSelection();
      var dropzoneAddPerson = this;
      this.on("addedfile", function(file) {
        disableButtonsAndRadio(false);
        $('#startAddPerson').click(function(e){
            disableButtonsAndRadio(true);
            document.getElementById("cancelAddPerson").disabled = false;
            e.preventDefault();
            e.stopPropagation();
            dropzoneAddPerson.processQueue();
        });
        $('#cancelAddPerson').click(function(){
          dropzoneAddPerson.removeAllFiles(true);
          document.getElementById("inputNameAddPerson").value = "";
          document.getElementById("inputSurnameAddPerson").value = "";
          document.getElementById("inputDniAddPerson").value = "";
        });
      });
      this.on("removedfile", function(file) {
        disableButtonsAndRadio(true);
        setDefaultRadioButtonSelection();
      });
      this.on('sendingmultiple', function(file, xhr, formData){
        var state = getState();
        formData.append('operation',REQUESTUPLOAD);
        formData.append('state', state);
        formData.append('name', $('#inputNameAddPerson').val());
        formData.append('surname', $('#inputSurnameAddPerson').val());
        formData.append('dni', $('#inputDniAddPerson').val());
      });
      this.on("success", function(file, response) {
        $(".loading").remove();
      });
      this.on("uploadprogress", function(file, progress, bytesSent) {
        if (progress >= 100){
          $(".dz-preview").append('<div class="loading" id="loading"><img src="../static/loader.gif" style="max-width: 100%; max-height: 100%"/></div>')
        }
      });
      this.on("error", function(file, message, xhr) {
        $(".loading").remove();
      });
    },
    accept: function(file, done) {
      done();
    }
});
