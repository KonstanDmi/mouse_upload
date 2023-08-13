Dropzone.autoDiscover = false;

var myDropzone = new Dropzone(".dropzone", {
  addRemoveLinks: true,
  dictCancelUpload: "Cancel",
  parallelUploads: 1,
  uploadMultiple: true,
  autoProcessQueue: false,
  chunking: true,
  parallelChunkUploads: true,
  retryChunks: true,
  maxFilesize: 1,073,741,824
  acceptedFiles:
});

myDropzone.on("drop", function (event) {
  $('.dropzone').animate({
    opacity: 1,
    top: "-5"
  });
});


$("#upload").on('click', function () {
  myDropzone.processQueue();
});



myDropzone.on("success", function (response) {
    setTimeout(
        $(location).attr('href',response.xhr.responseURL)
    , 4000);
});


