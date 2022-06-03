const resultField = document.querySelector("textarea");

function returnPath() {
  eel.set_path(resultField.value);
}

eel.expose(loadNextPage);
function loadNextPage() {
  eel.update_tube_sample();
  window.open("tube_diameter.html", "_self", "width=650, height=800");
}