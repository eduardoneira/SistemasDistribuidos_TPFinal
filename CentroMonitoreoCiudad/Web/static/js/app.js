function setOperation(){
  if ((document.getElementById("RadioInsertFace").checked == true)){
    return 0;
  }
  if ((document.getElementById("RadiosCheckExistance").checked == true)){
    return 1;
  }
  return 2;
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
      document.querySelector("#actions .start").disabled = true;
      document.querySelector("#actions .refresh").disabled = true;
      document.getElementById("RadioInsertFace").disabled = true;
      document.getElementById("RadiosCheckExistance").disabled = true;
      document.getElementById("RadiosGetTrajectory").disabled = true;
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
    console.log(file);
    document.querySelector("#actions .start").disabled = false;
    document.querySelector("#actions .refresh").disabled = false;
    document.getElementById("RadioInsertFace").disabled = false;
    document.getElementById("RadiosCheckExistance").disabled = false;
    document.getElementById("RadiosGetTrajectory").disabled = false;
    $('#actions .start').click(function(){
        myDropzone.processQueue(); //processes the queue
    });
    $('#actions .refresh').click(function(){
      myDropzone.removeAllFiles(true);
    });
  });
  myDropzone.on("removedfile", function(file) {
    console.log("removedfile");
    document.querySelector("#actions .start").disabled = true;
    document.querySelector("#actions .refresh").disabled = true;
    document.getElementById("RadioInsertFace").disabled = true;
    document.getElementById("RadiosCheckExistance").disabled = true;
    document.getElementById("RadiosGetTrajectory").disabled = true;
    var ele = document.getElementsByName("Choose");
     for(var i=0;i<ele.length;i++)
        ele[i].checked = (i==0)?(true):(false);
    var response = document.getElementById("response");
    while (response.firstChild) {
        response.removeChild(response.firstChild);
    }
  });
  myDropzone.on("selectedfiles", function(file) { console.log("selectedfiles"); });
  myDropzone.on("thumbnail", function(file) { console.log("thumbnail"); });
  myDropzone.on("error", function(file) { console.log("error"); });
  myDropzone.on("processing ", function(file) { console.log("processing "); });
  myDropzone.on("uploadprogress", function(file) { console.log("uploadprogress"); });
  myDropzone.on('sending', function(file, xhr, formData){
    var operation = setOperation();
    formData.append('operation',operation);
  });
  myDropzone.on("success", function(file, response) {
    console.log("success");
    console.log(file);
    console.log(response);
    var image = document.createElement('img');
    var answer = document.createTextNode(response.answer);
    linebreak = document.createElement("br");
    image.src = "data:image/jpg;base64," + response.img;
    document.getElementById("response").appendChild(answer);
    document.getElementById("response").appendChild(linebreak);
    document.getElementById("response").appendChild(image);
  });
  myDropzone.on("complete", function(file) { console.log("complete"); });
  myDropzone.on("canceled", function(file) { console.log("canceled"); });
  myDropzone.on("maxfilesreached", function(file) { console.log("maxfilesreached"); });
  myDropzone.on("maxfilesexceeded", function(file) {
    console.log("maxfilesexceeded");
    myDropzone.removeAllFiles();
    myDropzone.addFile(file);
  });

  /* receive a "list of files" as first parameter
   * only called if the uploadMultiple option is true:
   */
  myDropzone.on("processingmultiple", function(files) { console.log("processingmultiple") });
  myDropzone.on("sendingmultiple", function(files) { console.log("sendingmultiple") });
  myDropzone.on("successmultiple", function(files) { console.log("successmultiple") });
  myDropzone.on("completemultiple", function(files) { console.log("completemultiple") });
  myDropzone.on("canceledmultiple", function(files) { console.log("canceledmultiple") });

  /* Special events */
  myDropzone.on("totaluploadprogress", function() { console.log("totaluploadprogress") });
  myDropzone.on("reset", function() { console.log("reset") });
});
