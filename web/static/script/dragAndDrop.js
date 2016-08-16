var dropZone = document.getElementById("dropzone");
var body = document.body;
body.ondragover = function () { dropZone.style.visibility = "visible"; return false; };
body.ondragend = function () { dropZone.style.visibility = "hidden"; return false; };
body.ondragleave = function () { dropZone.style.visibility = "hidden"; return false; };
body.ondrop = function () { dropZone.style.visibility = "hidden"; return false; };
