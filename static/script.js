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

function show_accordion (id) {
  let div=document.getElementById (id);
  if (div.style.display!="block") {
    div.style.display="block";
  }
  else {
    div.style.display="none";
  }
}

function activate_gen_freq () {
  document.getElementById ("tab-gen-freq").className = "tab-active"
  document.getElementById ("tab-gen-text").className = "tab-inactive"
  document.getElementById ("btn-gen-freq").className = "tab-btn-active"
  document.getElementById ("btn-gen-text").className = "tab-btn-inactive"
}

function activate_gen_text () {
  document.getElementById ("tab-gen-freq").className = "tab-inactive"
  document.getElementById ("tab-gen-text").className = "tab-active"
  document.getElementById ("btn-gen-freq").className = "tab-btn-inactive"
  document.getElementById ("btn-gen-text").className = "tab-btn-active"
}

document.addEventListener ("keydown", function (event) {
  if (event.key == "+") {
    clone_row ();
  }
})
