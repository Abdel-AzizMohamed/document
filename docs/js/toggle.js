let toggleButton = document.getElementById("toggle"),
  toggleMenu = document.getElementById("toggle-item"),
  toggleIcon = document.getElementById("toggle-icon");

toggleButton.onclick = function () {
  if (toggleMenu.classList.contains("hid-xe")) {
    toggleMenu.classList.remove("hid-xe");

    toggleIcon.classList.remove("fa-plus");
    toggleIcon.classList.add("fa-minus");

    toggleButton.style.backgroundColor = toggleButton.dataset.active;
  } else {
    toggleMenu.classList.add("hid-xe");

    toggleIcon.classList.remove("fa-minus");
    toggleIcon.classList.add("fa-plus");

    toggleButton.style.backgroundColor = "";
  }
};
