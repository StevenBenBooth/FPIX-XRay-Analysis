const label = document.querySelector("label")

eel.expose(update);
function update(s) {
  label.innerHTML = s
}