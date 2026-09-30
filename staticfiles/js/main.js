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

  // ---- Live password requirements ----------------------------------------
  // Each rule hides itself once satisfied. The "not too similar" rule mirrors
  // Django's UserAttributeSimilarityValidator (SequenceMatcher.quick_ratio at
  // the 0.7 threshold) against the account's personal info — supplied via
  // data-* attributes (reset page) or read live from the form (register page).
  function quickRatio(a, b) {
    if (!a.length && !b.length) return 1;
    var avail = {}, i, matches = 0, c;
    for (i = 0; i < b.length; i++) avail[b[i]] = (avail[b[i]] || 0) + 1;
    for (i = 0; i < a.length; i++) {
      c = a[i];
      if (avail[c] > 0) { matches++; avail[c]--; }
    }
    return (2 * matches) / (a.length + b.length);
  }

  document.querySelectorAll("[data-password-rules]").forEach(function (box) {
    var form = box.closest("form");
    var pw = document.getElementById(box.getAttribute("data-password-input"));
    if (!pw) return;
    var rules = Array.prototype.slice.call(box.querySelectorAll("[data-rule]"));

    function personalParts() {
      var raw = [];
      ["username", "email", "first", "last"].forEach(function (k) {
        raw.push(box.getAttribute("data-" + k));
      });
      if (form) {
        ["username", "email", "first_name", "last_name"].forEach(function (n) {
          var el = form.querySelector('[name="' + n + '"]');
          if (el) raw.push(el.value);
        });
      }
      var parts = [];
      raw.forEach(function (v) {
        if (!v) return;
        v = v.toLowerCase();
        parts.push(v);
        v.split(/\W+/).forEach(function (p) { if (p) parts.push(p); });
      });
      return parts;
    }

    function tooSimilar(lower) {
      return personalParts().some(function (p) {
        return p.length && quickRatio(lower, p) >= 0.7;
      });
    }

    function evaluate() {
      var v = pw.value, lower = v.toLowerCase();
      rules.forEach(function (li) {
        var rule = li.getAttribute("data-rule"), ok = false;
        if (v) {
          if (rule === "length") ok = v.length >= 8;
          else if (rule === "numeric") ok = !/^\d+$/.test(v);
          else if (rule === "similar") ok = !tooSimilar(lower);
        }
        li.classList.toggle("hidden", ok && v.length > 0);
      });
    }

    pw.addEventListener("input", evaluate);
    if (form) form.addEventListener("input", function (e) { if (e.target !== pw) evaluate(); });
    evaluate();
  });
})();
