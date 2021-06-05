function clone_row () {
  let wordsec=document.getElementById ("word-section")
  let row=document.getElementsByClassName ("data-row")[0];
  let clone=row.cloneNode (true);
  wordsec.appendChild (clone);

  let word=document.getElementsByName ("word");
  let freq=document.getElementsByName ("frequency");
  word [word.length -1].value="";
  freq [freq.length -1].value="";
}

function show_colormaps () {
  let div=document.getElementById ("colormaps");
  if (div.style.display!="block") {
    div.style.display="block";
  }
  else {
    div.style.display="none";
  }
}

function show_help () {
  let div=document.getElementById ("help");
  if (div.style.display!="block") {
    div.style.display="block";
  }
  else {
    div.style.display="none";
  }
}

document.addEventListener ("keydown", function (event) {
  if (event.key == "+") {
    clone_row ();
  }
})
