/* Les liens sortants s'ouvrent dans un nouvel onglet : la documentation renvoie
   vers PayPal et PrestaShop Addons, et on ne veut pas que le lecteur perde sa page.
   rel="noopener" est indispensable avec target="_blank" (la page ouverte peut
   sinon manipuler celle d'origine via window.opener). */
(function () {
  function marquerLiensExternes() {
    document.querySelectorAll(".md-content a[href^='http']").forEach(function (a) {
      if (a.hostname === window.location.hostname) return;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      if (!a.querySelector(".lien-externe-note")) {
        var note = document.createElement("span");
        note.className = "lien-externe-note";
        note.textContent = " (nouvel onglet)";   // masqué visuellement, lu par les lecteurs d'écran
        a.appendChild(note);
      }
    });
  }
  // document$ est l'observable de Material : rejoue à chaque navigation
  if (typeof document$ !== "undefined") {
    document$.subscribe(marquerLiensExternes);
  } else {
    document.addEventListener("DOMContentLoaded", marquerLiensExternes);
  }
})();
