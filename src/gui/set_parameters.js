const inputs = document.querySelectorAll("textarea")

function reload() {
  eel.update_params(getFields());
  eel.update_slice_sample();
  window.location.reload(true);
}

window.onload = updateSample;
function updateSample() {
  eel.get_parameters()(updateFields); // Use a callback, since eel returns a promise 
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


function beginProcessing() {
  eel.update_params(getFields());
  window.open("progress.html", "_self");
}