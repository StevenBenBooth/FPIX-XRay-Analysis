const resultField = document.querySelector("textarea");

function updateImage() {
  eel.update_tube_sample(resultField.value)
  // reloads page because browser cached image doesn't automatically update
  window.location.reload(true);
}

window.onload = updateRadius;
function updateRadius() {
  eel.get_radius()(changeField);
}

function changeField(x) {
  resultField.innerHTML = x;
}

function loadNextPage() {
  window.open("set_parameters.html", "_self")
}