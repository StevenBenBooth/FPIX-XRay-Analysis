const resultField = document.querySelector("textarea");

function returnPath() {
  eel.set_path(resultField.value);
}

eel.expose(loadNextPage);
function loadNextPage() {
  eel.update_tube_sample();
  // Sadly, the window cannot resize itself, so the last argument does nothing
  window.open("tube_diameter.html", "_self", "resizable=true, width=650, height=800");
}