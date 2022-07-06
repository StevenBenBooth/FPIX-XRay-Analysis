const resultField = document.querySelector("textarea");

function returnPath() {
  eel.set_path(resultField.value);
}

eel.expose(loadNextPage);
function loadNextPage() {
  eel.update_cropping_sample();
  // Sadly, the window cannot resize itself, so we can't use height/width arguments
  window.open("cropping.html", "_self");
}