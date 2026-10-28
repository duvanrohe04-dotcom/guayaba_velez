(function () {
  document.documentElement.classList.add('js');

  // Cabecera compacta al bajar: el logo grande solo se ve arriba del todo
  var header = document.querySelector('.site-header');
  if (header) {
    var ticking = false;
    var actualizar = function () {
      header.classList.toggle('compacta', window.scrollY > 60);
      ticking = false;
    };
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(actualizar); }
    }, { passive: true });
    actualizar();
  }
  var items = document.querySelectorAll(
    '.nutri-card, .quality-card, .timeline-step, .features-list li, ' +
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
