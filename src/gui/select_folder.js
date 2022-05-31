const resultField = document.querySelector("textarea");

function returnPath() {
  eel.path_input(resultField.value);
}

eel.expose(loadNextPage);
function loadNextPage() {
  eel.update_tube_sample();
  window.open("tube_diameter.html", "_self", "width=400, height=400");
}