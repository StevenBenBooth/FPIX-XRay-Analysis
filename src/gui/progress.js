const label = document.querySelector("label")

window.onload = start;
function start() {
  eel.process();
}

eel.expose(update);
function update(s) {
  label.innerHTML = s
}