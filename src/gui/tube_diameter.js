const resultField = document.querySelector("textarea");

function reload() {
  eel.update_radius(resultField.value) // saves inputted radius
  // reloads page because browser cached image doesn't automatically update
  window.location.reload(true);
}

window.onload = updateInfo;
function updateInfo() {
  eel.update_tube_sample();
  eel.get_radius()(x => resultField.innerHTML = x);
}

function loadNextPage() {
  window.open("set_parameters.html", "_self")
}