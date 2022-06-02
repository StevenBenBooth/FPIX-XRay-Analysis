const label = document.querySelector("label")

window.onload = start;
function start() {
  eel.start_processing();
}

eel.expose(update);
function update(s) {
  label.innerHTML = s
}