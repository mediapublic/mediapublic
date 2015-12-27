javascript:(function(){
  var MEDIAPUBLIC_URL = "http://localhost:8080"; /*https?*/
  var RECORDING_PATH = "/#recordings/new";
  var mediapublicWindow = window.open(MEDIAPUBLIC_URL + RECORDING_PATH + "?title=" + document.title + "&url=" + document.location.href);
})();
