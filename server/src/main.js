const PDFJS = require("pdfjs-dist");

PDFJS.workerSrc = "pdf.worker.js";

var checksum = "";
var scrollX = 0;
var scrollY = 0;

function renderErr() {
  document.getElementById("err-container").style.display = "block";
}

function renderPage(page) {
  var scale = 0.7;
  var viewport = page.getViewport({ scale: scale });
  var canvas = document.createElement("canvas");
  var ctx = canvas.getContext("2d");
  var renderContext = {
    canvasContext: ctx,
    viewport: viewport
  };
  canvas.height = viewport.height;
  canvas.width = viewport.width;
  canvas.style.borderWidth = "1px";
  canvas.style.borderColor = "#000000";
  canvas.style.borderStyle = "solid";

  document.getElementById("pdf-container").appendChild(canvas);

  page.render(renderContext);
}

function renderPDF() {
  PDFJS.getDocument("pdf")
    .promise.then(function(pdf) {
      scrollX = window.pageXOffset;
      srcollY = window.pageYOffset;
      document.getElementById("err-container").style.display = "none";
      document.getElementById("pdf-container").innerHTML = "";
      for (var num = 1; num <= pdf.numPages; num++)
        pdf.getPage(num).then(renderPage);
    })
    .catch(_ => renderErr());
}

function regularExec() {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onload = function() {
    if (xmlHttp.status == 200) {
      if (xmlHttp.responseText != checksum) {
        checksum = xmlHttp.responseText;
        renderPDF();
      }
    } else {
      renderErr();
    }
  };
  xmlHttp.open("GET", "md5", true);
  xmlHttp.send();
  setTimeout(regularExec, 3000);
}

if (
  document.readyState === "complete" ||
  document.readyState === "interactive"
) {
  setTimeout(regularExec, 1);
} else {
  document.addEventListener("DOMContentLoaded", regularExec);
}
