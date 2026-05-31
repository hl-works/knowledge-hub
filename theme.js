/* Thème clair/sombre — Knowledge Hub. Zéro dépendance.
   3 états : auto (préférence système) / light / dark. Persisté en localStorage.
   L'anti-FOUC est géré par un petit script inline dans le <head> de chaque page. */
(function(){
  var KEY = "kh-theme";
  var mq = window.matchMedia ? matchMedia("(prefers-color-scheme:dark)") : null;

  function get(){ try { return localStorage.getItem(KEY) || "auto"; } catch(e){ return "auto"; } }
  function resolvedDark(t){ return t === "dark" || (t !== "light" && mq && mq.matches); }

  function apply(t){
    var root = document.documentElement;
    if (t === "dark" || t === "light") root.setAttribute("data-theme", t);
    else root.removeAttribute("data-theme");
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", resolvedDark(t) ? "#1A1813" : "#FFFCF8");
  }

  function label(t){ return t === "auto" ? "Thème : automatique" : t === "light" ? "Thème : clair" : "Thème : sombre"; }

  document.addEventListener("DOMContentLoaded", function(){
    var btns = [].slice.call(document.querySelectorAll("[data-theme-toggle]"));
    function refresh(){
      var t = get();
      btns.forEach(function(b){ b.dataset.state = t; b.setAttribute("aria-label", label(t)); b.title = label(t); });
    }
    btns.forEach(function(b){
      b.addEventListener("click", function(){
        var order = ["auto", "light", "dark"];
        var t = order[(order.indexOf(get()) + 1) % 3];
        try { localStorage.setItem(KEY, t); } catch(e){}
        apply(t); refresh();
      });
    });
    refresh();
    if (mq && mq.addEventListener) mq.addEventListener("change", function(){ if (get() === "auto") apply("auto"); });
  });
})();
