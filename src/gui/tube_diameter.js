const resultField = document.querySelector("textarea");

function updateImage() {
  eel.update_tube_sample(resultField.value)
  // reloads page because browser cached image doesn't automatically update
  window.location.reload(true);
}

// function returnRadius() {
//   eel.update_radius()
// }

// eel.expose(loadNextPage);
function loadNextPage() {
  window.open("set_parameters.html", "_self")
}