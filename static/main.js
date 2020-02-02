var imageDisplay = document.getElementById("image-display");
var predResult = document.getElementById("pred-result");

function predictImage() {
  fetch("/predict", {
    method: "GET",
    })
    .then(resp => {
      if (resp.ok)
        resp.json().then(data => {
          displayImage(data.img, imageDisplay),
          displayResult(data);
        });
    })
    .catch(err => {
      console.log("An error occured", err.message);
      window.alert("Oops! Something went wrong.");
    });
}

function displayImage(image, id) {
  let display = document.getElementById(id);
  display.src = image;
  show(display);
}

function displayResult(data) {
  predResult.innerHTML = data.result;
  show(predResult);
}

function hide(el) {
  // hide an element
  el.classList.add("hidden");
}

function show(el) {
  // show an element
  el.classList.remove("hidden");
}
predictImage()