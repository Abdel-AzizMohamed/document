let dropDown = document.getElementById("dropDown"),
  dropIcon = document.getElementById("dropIcon"),
  dropMenu = document.getElementById("dropMenu");

dropDown.onclick = function () {
  if (this.classList.contains("active")) {
    this.classList.remove("active");
    dropIcon.classList.remove("fa-caret-up");
    dropIcon.classList.add("fa-caret-down");
    dropMenu.style.display = "none";
  } else {
    this.classList.add("active");
    dropIcon.classList.add("fa-caret-up");
    dropIcon.classList.remove("fa-caret-down");
    dropMenu.style.display = "flex";
  }
};
