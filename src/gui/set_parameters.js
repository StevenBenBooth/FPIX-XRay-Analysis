// const numwedges = document.getElementById("num-wedges");
// const highlightcutoff = document.getElementById("highlight-cutoff");
// const epoxlowbound = document.getElementById("epox-low-bound");
// const cftopbound = document.getElementById("cf-top-bound");
// const cfbottombound = document.getElementById("cf-bottom-bound");
// const cfthickness = document.getElementById("cf-thickness");
// const highlightthickness = document.getElementById("highlight-thickness");
// const interpolationthresh = document.getElementById("interpolation-thresh");
// const epoxyinterpthresh = document.getElementById("epoxy-interp-thresh");


// var numwedges_val;
// var highlightcutoff_val;
// var epoxlowbound_val;
// var cftopbound_val;
// var cfbottombound_val;
// var cfthickness_val;
// var highlightthickness_val;
// var interpolationthresh_val;
// var epoxyinterpthresh_val;

// numwedges.onRelease = function () {
//   numwedges_val = this.value; updateSample(); window.location.reload(true);
// }
// highlightcutoff.onRelease = function () {
//   highlightcutoff_val = this.value; updateSample(); window.location.reload(true);
// }
// epoxlowbound.onRelease = function () {
//   epoxlowbound_val = this.value; updateSample(); window.location.reload(true);
// }
// cftopbound.onRelease = function () {
//   cftopbound_val = this.value; updateSample(); window.location.reload(true);
// }
// cfbottombound.onRelease = function () {
//   cfbottombound_val = this.value; updateSample(); window.location.reload(true);
// }
// cfthickness.onRelease = function () {
//   cfthickness_val = this.value; updateSample(); window.location.reload(true);
// }
// highlightthickness.onRelease = function () {
//   highlightthickness_val = this.value; updateSample(); window.location.reload(true);
// }
// interpolationthresh.onRelease = function () {
//   interpolationthresh_val = this.value; updateSample(); window.location.reload(true);
// }
// epoxyinterpthresh.onRelease = function () {
//   epoxyinterpthresh_val = this.value; updateSample(); window.location.reload(true);
// }
// function returnParameters() {
//   return [numwedges_val,
//     highlightcutoff_val,
//     epoxlowbound_val,
//     cftopbound_val,
//     cfbottombound_val,
//     cfthickness_val,
//     highlightthickness_val,
//     interpolationthresh_val,
//     epoxyinterpthresh_val]
// }


// //It would be better to do something like this:
// const sliders = document.querySelectorAll("slidecontainer.slider")
// const displays = document.querySelectorAll("span")
// var values = []
// values.length = 9

// sliders.forEach((item, index) => {
//   item.onRelease = function () {
//     values[index] = this.value;
//     displays[index].innerHTML = "hi";
//     eel.updated_slider(item)
//     window.location.reload(true);
//   };
// });


// inputs.forEach((item) => {
//   item.onchange = function () {
//     values[index] = this.value;
//     eel.log("hello");
//     window.location.reload(true);
//     eel.updateSample(values);
//   };
// }
// )

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
  window.open("progress.html", "_self", "resizable=true, width=650, height=800");
}