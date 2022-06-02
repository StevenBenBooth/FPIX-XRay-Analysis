const label = document.querySelector("label")

eel.expose(update);
function update(a, b) {
  label.innerHTML = "{a}/{b} slices processed"
}