const resultField = document.querySelector("textarea");

function reload() {
  eel.update_radius(resultField.value); // saves inputted radius
  eel.update_tube_sample();
  // reloads page because browser cached image doesn't automatically update
  window.location.reload(true);
}

window.onload(updateInfo)
function updateInfo() {
  eel.get_radius()(x => resultField.innerHTML = x);
}
// document.addEventListener("DOMContentLoaded", updateInfo);

function loadNextPage() {
  eel.update_radius(resultField.value);
  eel.update_slice_sample();
  window.open("set_parameters.html", "_self", "width=400", "height=800");
}