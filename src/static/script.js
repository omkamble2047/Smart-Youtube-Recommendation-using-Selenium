// script.js

document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.getElementById("togglePassword");
  const password = document.getElementById("password");

  if (toggle && password) {
    toggle.addEventListener("click", () => {
      const type = password.getAttribute("type") === "password" ? "text" : "password";
      password.setAttribute("type", type);
      toggle.textContent = type === "password" ? "👁️" : "🙈";
    });
  }
});
