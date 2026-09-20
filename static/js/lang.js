/* Язык сайта: ручной выбор через переключатель (запоминается навсегда),
   иначе одноразовое определение страны по IP (get.geojs.io):
   RU-адрес — русская версия, любой другой — английская.
   Если API недоступен, ориентируемся на язык браузера. */
(function () {
  function store(key, value) {
    try { localStorage.setItem(key, value); } catch (e) {}
  }
  function read(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }

  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest("a.lang-switch") : null;
    if (a && a.dataset.prefLang) {
      store("lang-pref", a.dataset.prefLang);
    }
  });

  var el = document.documentElement;
  var enURL = el.getAttribute("data-en-url");
  if (!enURL) return;

  var path = location.pathname;
  if (path === "/en" || path.slice(0, 4) === "/en/") return;

  if (read("lang-pref")) return;
  try { if (sessionStorage.getItem("geo-checked")) return; } catch (e) {}
  try { sessionStorage.setItem("geo-checked", "1"); } catch (e) {}

  function go() { location.replace(enURL); }

  fetch("https://get.geojs.io/v1/ip/country.json", { cache: "no-store" })
    .then(function (r) { return r.json(); })
    .then(function (d) {
      if (d && d.country && d.country !== "RU") go();
    })
    .catch(function () {
      var lang = (navigator.language || "en").toLowerCase();
      if (lang.indexOf("ru") !== 0) go();
    });
})();
