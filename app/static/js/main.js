(function () {
  document.documentElement.classList.add('js');

  // La cabecera ya NO cambia de tamaño al deslizar: antes se encogía a mitad
  // del scroll, el contenido "saltaba" bajo el dedo y el navegador corregía la
  // posición (parpadeo). Ahora mide siempre lo mismo.

  // Reserva de agroturismo: arma el mensaje y abre WhatsApp (no se guarda nada en el servidor)
  var formAgro = document.querySelector('.agro-form');
  if (formAgro) {
    var fecha = formAgro.querySelector('[name=fecha]');
    var hoy = new Date();
    var yyyy = hoy.getFullYear(), mm = ('0' + (hoy.getMonth() + 1)).slice(-2), dd = ('0' + hoy.getDate()).slice(-2);
    fecha.min = yyyy + '-' + mm + '-' + dd;
    var aviso = formAgro.querySelector('.agro-error');

    formAgro.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var nombre = formAgro.nombre.value.trim();
      var personas = parseInt(formAgro.personas.value, 10);
      var valor = fecha.value;                      // yyyy-mm-dd
      var mensaje = formAgro.mensaje.value.trim();
      var errores = [];
      [formAgro.nombre, formAgro.personas, fecha].forEach(function (c) { c.classList.remove('invalido'); });

      if (nombre.length < 2) { errores.push('Escribe tu nombre.'); formAgro.nombre.classList.add('invalido'); }
      if (!(personas >= 1 && personas <= 60)) { errores.push('Indica cuántas personas (1 a 60).'); formAgro.personas.classList.add('invalido'); }
      if (!valor || valor < fecha.min) { errores.push('Elige una fecha desde hoy en adelante.'); fecha.classList.add('invalido'); }

      if (errores.length) { aviso.textContent = errores.join(' '); aviso.hidden = false; return; }
      aviso.hidden = true;

      var partes = valor.split('-');
      var legible = new Date(+partes[0], +partes[1] - 1, +partes[2]).toLocaleDateString('es-CO',
        { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
      var texto = 'Hola, quiero reservar una visita de agroturismo.\n' +
        'Nombre: ' + nombre + '\n' +
        'Personas: ' + personas + '\n' +
        'Fecha deseada: ' + legible +
        (mensaje ? '\nMensaje: ' + mensaje : '') +
        '\n¿Tienen disponibilidad?';
      var url = formAgro.getAttribute('data-wa') + '?text=' + encodeURIComponent(texto);
      var ventana = window.open(url, '_blank', 'noopener');
      if (!ventana) { window.location.href = url; }   // si el navegador bloquea la ventana, se abre en la misma pestaña
    });
  }

  // Ahorro de batería/GPU: las animaciones decorativas (destellos de títulos,
  // resplandores) solo corren mientras el elemento está en pantalla.
  var animados = document.querySelectorAll(
    '.section-title, .section-label, .photo-hero-title, .quote-text, .quote-mark, ' +
    '.regional-title, .rstat-value, .cta-title, .cta-tag, .footer-logo, ' +
    '.hero h2 span, .hero-copy .hero-sub, .cj-title'
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
    '.agro-info, .agro-form-card, .cj-pilar, .producto-card, .nutri-card, .quality-card, .timeline-step, .features-list li, ' +
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
