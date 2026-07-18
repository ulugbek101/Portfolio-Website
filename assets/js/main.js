(function () {
  "use strict";

  // ---- Theme toggle -------------------------------------------------------
  var toggle = document.getElementById("theme-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var isDark = document.documentElement.classList.toggle("dark");
      try {
        localStorage.setItem("theme", isDark ? "dark" : "light");
      } catch (e) {}
    });
  }

  // ---- Mobile menu --------------------------------------------------------
  var menuBtn = document.getElementById("menu-toggle");
  var mobileNav = document.getElementById("mobile-nav");
  if (menuBtn && mobileNav) {
    menuBtn.addEventListener("click", function () {
      mobileNav.classList.toggle("hidden");
    });
  }

  // ---- Toast auto-dismiss + close ----------------------------------------
  document.querySelectorAll(".toast").forEach(function (t) {
    var close = t.querySelector(".toast-close");
    if (close) close.addEventListener("click", function () { t.remove(); });
    setTimeout(function () {
      t.style.transition = "opacity .4s ease";
      t.style.opacity = "0";
      setTimeout(function () { t.remove(); }, 400);
    }, 6000);
  });

  // ---- "Show more replies" (progressive reveal) --------------------------
  document.querySelectorAll("[data-show-more]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var target = document.getElementById(btn.getAttribute("data-show-more"));
      if (target) {
        target.classList.remove("hidden");
        btn.remove();
      }
    });
  });

  // ---- Reply form toggles ------------------------------------------------
  document.querySelectorAll("[data-reply-toggle]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var form = document.getElementById(btn.getAttribute("data-reply-toggle"));
      if (form) {
        form.classList.toggle("hidden");
        var input = form.querySelector("textarea");
        if (input && !form.classList.contains("hidden")) input.focus();
      }
    });
  });
})();
