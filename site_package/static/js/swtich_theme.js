let switchButton = document.getElementById("theme-switch"),
  buttonIcon = document.querySelector("#theme-switch i"),
  darkTheme = document.getElementById("theme");

function switchTheme() {
  if (buttonIcon.classList.contains("fa-sun")) {
    buttonIcon.classList.remove("fa-sun");
    buttonIcon.classList.add("fa-moon");
    darkTheme.disabled = false;
  } else {
    buttonIcon.classList.add("fa-sun");
    buttonIcon.classList.remove("fa-moon");
    darkTheme.disabled = true;
  }
}

if (buttonIcon.classList.contains("fa-sun")) darkTheme.disabled = true;

switchButton.onclick = switchTheme;
