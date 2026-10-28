(function () {
  document.documentElement.classList.add('js');

  // La cabecera ya NO cambia de tamaño al deslizar: antes se encogía a mitad
  // del scroll, el contenido "saltaba" bajo el dedo y el navegador corregía la
  // posición (parpadeo). Ahora mide siempre lo mismo.

  // Ahorro de batería/GPU: las animaciones decorativas (destellos de títulos,
  // resplandores) solo corren mientras el elemento está en pantalla.
  var animados = document.querySelectorAll(
    '.section-title, .section-label, .photo-hero-title, .quote-text, .quote-mark, ' +
    '.regional-title, .rstat-value, .cta-title, .cta-tag, .footer-logo, ' +
    '.hero h2 span, .hero-copy .hero-sub'
  );
  if ('IntersectionObserver' in window) {
    var pausador = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        e.target.classList.toggle('pausa', !e.isIntersecting);
      });
    }, { rootMargin: '80px 0px' });
    animados.forEach(function (el) { pausador.observe(el); });
  }
  var items = document.querySelectorAll(
    '.producto-card, .nutri-card, .quality-card, .timeline-step, .features-list li, ' +
    '.regional-phrase-item, .info-block, .rstat, .quote-inner, .cta-inner'
  );
  items.forEach(function (el) { el.classList.add('reveal'); });

  if (!('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('visible'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  items.forEach(function (el) { io.observe(el); });

  // Marca el enlace activo de la barra inferior según la sección visible
  var links = document.querySelectorAll('.bottom-nav a[href^="#"]');
  var map = {};
  links.forEach(function (a) { map[a.getAttribute('href')] = a; });
  var spy = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      links.forEach(function (a) { a.classList.remove('active'); });
      var a = map['#' + e.target.id];
      if (a) a.classList.add('active');
    });
  }, { threshold: 0.4 });
  document.querySelectorAll('section[id]').forEach(function (s) { spy.observe(s); });
})();
