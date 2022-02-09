const resultField = document.querySelector("textarea");

function returnPath() {
  eel.path_input(resultField.value);
}

eel.expose(loadNextPage);
function loadNextPage() {
  window.open("tube_diameter.html")
}