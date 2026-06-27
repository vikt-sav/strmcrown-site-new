(function () {
  const root = document.documentElement;
  const toggle = document.getElementById("theme-toggle");

  const saved = localStorage.getItem("theme");

  if (saved) {
    root.setAttribute("data-theme", saved);
  } else {
    // system preference fallback
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    root.setAttribute("data-theme", prefersDark ? "dark" : "light");
  }

  toggle?.addEventListener("click", () => {
    const current = root.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";

    root.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
  });
})();

// =========================
// Scroll progress bar
// =========================

(function () {
  const bar = document.getElementById("scroll-progress");
  if (!bar) return;

  function updateProgress() {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (scrollTop / docHeight) * 100;

    bar.style.width = progress + "%";
  }

  window.addEventListener("scroll", updateProgress);
  window.addEventListener("resize", updateProgress);

  updateProgress();
})();