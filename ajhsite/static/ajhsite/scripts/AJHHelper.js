// *************************************************
// The helper script contains data and functions
// for the AJHDotcom website.
// *************************************************
function showHideSection(id) {
  var x = document.getElementById(id);
  if (x.className.indexOf("w3-show") == -1) {
      x.className += " w3-show";
  } else { 
      x.className = x.className.replace(" w3-show", "");
  }
};

function showHideRespMenu() {
  var x = document.getElementById("responsiveNav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}