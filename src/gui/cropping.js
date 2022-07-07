const inputs = document.querySelectorAll("textarea")

function reload() {
  eel.update_bounds(getFields());
  eel.update_cropping_sample();
  window.location.reload(true);
}

window.onload = updateSample;
function updateSample() {
  eel.get_bounds()(updateFields); // Use a callback, since eel returns a promise 
}

function updateFields(val) {
  inputs.forEach((item, index) => {
    item.innerHTML = val[index]
  }
  )
}

function getFields() {
  var val = []
  inputs.forEach((item, _) => {
    val.push(item.value)
  })
  return val
}


function loadNextPage() {
  eel.update_bounds(getFields());
  window.open("set_radius.html", "_self");
}