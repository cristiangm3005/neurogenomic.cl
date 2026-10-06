/* =========================================================
   MetalGenomic · escenas y microinteracciones
   GSAP + ScrollTrigger + Lenis (CDN). Three.js solo para la hélice (carga diferida).
   ========================================================= */
(function () {
  'use strict';

  var d = document, W = window, root = d.documentElement;
  var reduce = W.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasGsap = !!(W.gsap && W.ScrollTrigger);
  if (!hasGsap) root.classList.remove('motion');
  var motion = root.classList.contains('motion');
  var fine = W.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var $ = function (s, c) { return (c || d).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || d).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
  var isDesk = function () { return W.innerWidth >= 768; };

  /* ---------------------------------------------------------
     Renders reales: cuando existan, escribe aquí la ruta y la
     ilustración SVG se reemplaza sola (ver ASSETS.md).
     --------------------------------------------------------- */
  var RENDERS = {
    truckSide: '',   // 'assets/img/render/truck-side.webp'  (PNG/WebP con alfa, 1600×900)
    truckTop: ''     // 'assets/img/render/truck-top.webp'   (vista cenital con alfa, 1200×660)
  };
  function useRender(imgId, url, svg) {
    if (!url) return;
    var probe = new Image();
    probe.onload = function () { var img = $('#' + imgId); img.src = url; img.hidden = false; svg.style.visibility = 'hidden'; };
    probe.src = url;
  }

  /* ---------- Detalle generado: tacos, pernos y roca ---------- */
  function rng(seed) { return function () { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }; }
  var NS = 'http://www.w3.org/2000/svg';
  function el(tag, attrs) { var e = d.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); return e; }
  function decorateTruck(svg) {
    $$('.wheel', svg).forEach(function (w) {
      var cx = +w.dataset.cx, cy = +w.dataset.cy, lugs = $('.lugs', w), bolts = $('.bolts', w);
      for (var i = 0; i < 30; i++) lugs.appendChild(el('rect', { x: cx - 5, y: cy - 92, width: 10, height: 13, rx: 2, fill: '#2A2926', transform: 'rotate(' + (i * 12) + ' ' + cx + ' ' + cy + ')' }));
      for (var j = 0; j < 10; j++) { var a = j / 10 * Math.PI * 2; bolts.appendChild(el('circle', { cx: (cx + Math.cos(a) * 26).toFixed(1), cy: (cy + Math.sin(a) * 26).toFixed(1), r: 3.6, fill: '#4A4843' })); }
    });
    var rocks = $('.t-rocks', svg), r = rng(7);
    if (rocks) for (var k = 0; k < 46; k++) {
      var x = 40 + r() * 410, top = 70 - (x - 22) * 0.058, h = 34 * Math.sin(Math.PI * (x - 30) / 432);
      rocks.appendChild(el('ellipse', { cx: x.toFixed(1), cy: (top - r() * h).toFixed(1), rx: (4 + r() * 7).toFixed(1), ry: (3.5 + r() * 5).toFixed(1), fill: r() < 0.18 ? 'url(#gRockT)' : 'url(#gRock)' }));
    }
  }
  decorateTruck($('#truckHero'));
  (function () {
    var g = $('#oreTop'), r = rng(19);
    for (var i = 0; i < 80; i++) {
      var a = r() * Math.PI * 2, rr = Math.sqrt(r());
      g.appendChild(el('ellipse', { cx: (164 + Math.cos(a) * 118 * rr).toFixed(1), cy: (114 + Math.sin(a) * 62 * rr).toFixed(1), rx: (4 + r() * 8).toFixed(1), ry: (4 + r() * 6).toFixed(1), fill: r() < 0.16 ? 'url(#gRockT)' : 'url(#gRock)' }));
    }
  })();
  // Segundo camión (Soluciones): misma ilustración, ruedas independientes
  var solTruck = $('#truckHero').cloneNode(true);
  solTruck.id = 'truckSol';
  $('#solTruckSlot').appendChild(solTruck);
  useRender('renderTruckSide', RENDERS.truckSide, $('#truckHero'));
  useRender('renderTruckTop', RENDERS.truckTop, $('#truckTop'));

  /* ---------- Pala: pose por ángulos (brazo, balancín, compuerta) ---------- */
  var boom = $('#boom'), stick = $('#stick'), clam = $('#clam'), bLoad = $('#bLoad');
  var pose = { b: 0, s: 0, c: 0 };
  function setPose() {
    boom.setAttribute('transform', 'rotate(' + pose.b.toFixed(2) + ' 250 210)');
    stick.setAttribute('transform', 'rotate(' + pose.s.toFixed(2) + ' 380 -10)');
    clam.setAttribute('transform', 'rotate(' + pose.c.toFixed(2) + ' 527 13)');
  }
  setPose();

  /* ---------- Medición (dataLayer / GA4 / GTM) ---------- */
  W.dataLayer = W.dataLayer || [];
  function track(ev, data) { var o = { event: ev }; for (var k in data) o[k] = data[k]; W.dataLayer.push(o); }
  $$('[data-cta]').forEach(function (a) { a.addEventListener('click', function () { track('cta_click', { cta_location: a.dataset.cta }); }); });
  var utm = (function () { var q = new URLSearchParams(location.search), o = []; ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid'].forEach(function (k) { if (q.get(k)) o.push(k + '=' + q.get(k)); }); return o.join(' · '); })();

  /* ---------- Contador ---------- */
  function countUp(node, to, dur) {
    if (!node) return;
    if (!motion) { node.textContent = to; return; }
    var t0 = performance.now(); dur = dur || 1200;
    (function f(t) { var p = clamp((t - t0) / dur, 0, 1), e = 1 - Math.pow(1 - p, 3); node.textContent = Math.round(to * e); if (p < 1) requestAnimationFrame(f); })(t0);
  }

  /* ---------- Revelados por intersección (ambos modos) ---------- */
  var revealIO = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('is-in');
      $$('[data-count]', e.target).forEach(function (n) { if (!n._done) { n._done = 1; countUp(n, +n.dataset.count, 1400); } });
      revealIO.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -12% 0px' });
  $$('[data-reveal]').forEach(function (n) { if (motion) $$('[data-count]', n).forEach(function (c) { c.textContent = '0'; }); revealIO.observe(n); });

  /* ---------- Diagnóstico express ---------- */
  (function () {
    var R = {
      mnt: { img: 'assets/img/mill-800.webp', alt: 'Molino SAG en una planta concentradora.', k: 'Empezaríamos por · Equipo', t: 'Mantenimiento predictivo con IA', r: 'Vibración, temperatura, acústica y datos de operación de tus equipos críticos.', p: 'Un equipo crítico, por ejemplo un molino o una correa.', g: 'Planificar las intervenciones en vez de reaccionar ante ellas.', topic: 'Mantenimiento predictivo' },
      bio: { img: 'assets/img/mineral-800.webp', alt: 'Mineral de cobre con oxidación turquesa.', k: 'Empezaríamos por · Microbio', t: 'Biolixiviación genómica', r: 'Tu mineral, tus soluciones y su comunidad microbiana, para diseñar consorcios nativos.', p: 'Un circuito o un sector de la pila.', g: 'Más recuperación en mineral de baja ley, con menos ácido.', topic: 'Biolixiviación genómica' },
      geo: { img: 'assets/img/geo-800.webp', alt: 'Imagen satelital de quebradas del desierto.', k: 'Empezaríamos por · Territorio', t: 'Exploración geoespacial predictiva', r: 'Imágenes satelitales y datos geológicos disponibles, cruzados con machine learning.', p: 'Un sector de exploración o un talud a vigilar.', g: 'Decidir dónde intervenir con menos riesgo.', topic: 'Exploración geoespacial' },
      twin: { img: 'assets/img/pit-800.webp', alt: 'Rajo abierto de cobre al atardecer.', k: 'Empezaríamos por · Planta', t: 'Gemelo digital y BIM', r: 'Planos, modelos existentes y datos de operación de la planta o del circuito.', p: 'Un circuito o un área de la planta.', g: 'Probar cambios sin riesgo antes de ejecutarlos en terreno.', topic: 'Gemelo digital' }
    };
    var btns = $$('.pain'), A = $('#recImgA'), B = $('#recImgB'), front = A;
    var GL = 'abcdefghijklmnopqrstuvwxyz0123456789';
    function scramble(node, text) {
      if (!motion) { node.textContent = text; return; }
      var t0 = performance.now(), dur = 380;
      (function f(t) {
        var p = clamp((t - t0) / dur, 0, 1), n = Math.floor(text.length * p), s = text.slice(0, n);
        for (var i = n; i < text.length; i++) s += text[i] === ' ' ? ' ' : GL[(Math.random() * GL.length) | 0];
        node.textContent = s; if (p < 1) requestAnimationFrame(f); else node.textContent = text;
      })(t0);
    }
    function pick(b, focus) {
      var o = R[b.dataset.pain];
      btns.forEach(function (x) { x.setAttribute('aria-checked', String(x === b)); x.tabIndex = x === b ? 0 : -1; });
      if (focus) b.focus();
      var back = front === A ? B : A;
      back.src = o.img; back.alt = o.alt; front.alt = '';
      back.classList.remove('is-out'); front.classList.add('is-out'); front = back;
      scramble($('#recKicker'), o.k); scramble($('#recTitle'), o.t);
      $('#recReview').textContent = o.r; $('#recPilot').textContent = o.p; $('#recGain').textContent = o.g;
      $('#recBtn').dataset.topic = o.topic;
      track('finder_select', { challenge: o.topic });
    }
    btns.forEach(function (b, i) {
      b.tabIndex = i === 0 ? 0 : -1;
      b.addEventListener('click', function () { pick(b); });
      b.addEventListener('keydown', function (e) {
        var n = e.key === 'ArrowDown' || e.key === 'ArrowRight' ? 1 : e.key === 'ArrowUp' || e.key === 'ArrowLeft' ? -1 : 0;
        if (!n) return; e.preventDefault(); pick(btns[(i + n + btns.length) % btns.length], true);
      });
    });
  })();

  /* ---------- Formulario en dos pasos → correo ---------- */
  (function () {
    var f = $('#leadForm'), msg = $('#formMsg'), msg1 = $('#formMsg1'), s1 = $('[data-step="1"]', f), s2 = $('[data-step="2"]', f), done = $('#formDone'), lbl = $('#stepLbl'), bar = $('#stepBar'), started = false;
    function go(n) {
      s1.hidden = n !== 1; s2.hidden = n !== 2; done.hidden = n !== 3;
      lbl.textContent = n === 3 ? 'Listo' : 'Paso ' + n + ' de 2';
      bar.style.transform = 'scaleX(' + (n === 1 ? 0.5 : 1) + ')';
      done.classList.toggle('is-shown', n === 3);
      if (n === 2) { $('#f-name').focus({ preventScroll: true }); track('form_step', { step: 2 }); }
      if (n === 3) done.focus({ preventScroll: true });
    }
    f.addEventListener('input', function () { if (!started) { started = true; track('form_start', {}); } });
    $$('[data-topic]').forEach(function (a) { a.addEventListener('click', function () { var v = a.dataset.topic; $$('input[name=interes]', f).forEach(function (c) { if (c.value === v) c.checked = true; }); go(1); }); });
    $('#toStep2').addEventListener('click', function () {
      if (!$$('input[name=interes]:checked', f).length) { msg1.textContent = 'Elige al menos una opción (o «Aún no lo sé»).'; msg1.className = 'form__msg is-err'; return; }
      msg1.textContent = ''; go(2);
    });
    $('#toStep1').addEventListener('click', function () { go(1); });
    $('#formAgain').addEventListener('click', function () { go(2); });
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!s1.hidden) { $('#toStep2').click(); return; }
      var ok = true;
      ['f-name', 'f-company', 'f-email'].forEach(function (id) {
        var x = $('#' + id), fd = x.closest('.field'), bad = !x.value.trim() || (x.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(x.value));
        fd.classList.toggle('is-err', bad); x.setAttribute('aria-invalid', bad ? 'true' : 'false'); if (bad && ok) { x.focus(); ok = false; }
      });
      if (!ok) { msg.textContent = 'Revisa los campos marcados: nombre, empresa y un correo válido.'; msg.className = 'form__msg is-err'; return; }
      var ints = $$('input[name=interes]:checked', f).map(function (c) { return c.value; }).join(', ');
      var et = (($('input[name=etapa]:checked', f) || {}).value) || '—';
      var v = function (id) { return $('#' + id).value.trim() || '—'; };
      var body = 'Nombre: ' + v('f-name') + '\nCargo: ' + v('f-role') + '\nEmpresa / faena: ' + v('f-company') + '\nCorreo: ' + v('f-email') + '\nTeléfono: ' + v('f-phone') + '\n\nInterés: ' + ints + '\nEtapa: ' + et + '\n\nDesafío:\n' + v('f-msg') + (utm ? '\n\nOrigen: ' + utm : '');
      track('generate_lead', { interest: ints, stage: et });
      W.location.href = 'mailto:contacto@metalgenomic.cl?subject=' + encodeURIComponent('Diagnóstico operativo · ' + v('f-company')) + '&body=' + encodeURIComponent(body);
      go(3);
    });
  })();

  /* ---------- Preguntas: acordeón accesible ---------- */
  $$('.qa').forEach(function (q, i, all) {
    var b = $('button', q);
    b.addEventListener('click', function () {
      var open = b.getAttribute('aria-expanded') !== 'true';
      all.forEach(function (o) { var ob = $('button', o); if (o !== q) { o.classList.remove('is-open'); ob.setAttribute('aria-expanded', 'false'); } });
      q.classList.toggle('is-open', open); b.setAttribute('aria-expanded', String(open));
      if (open) track('faq_open', { question: b.textContent });
    });
  });

  /* ---------- Navegación: ocultar al bajar, tono según sección, sección activa, progreso ---------- */
  var heroDark = false;
  (function () {
    var nav = $('#nav'), prog = $('#progress'), dock = $('#dock'), darks = $$('.on-ink'), last = W.scrollY, ticking = false;
    var links = $$('.nav__links a'), secs = links.map(function (a) { return d.querySelector(a.getAttribute('href')); });
    var formIn = false;
    var io = new IntersectionObserver(function (es) { es.forEach(function (x) { x.target._in = x.isIntersecting; }); formIn = !!($('#agendar')._in || $('#pie')._in); upd(); });
    io.observe($('#agendar')); io.observe($('#pie'));
    function upd() {
      ticking = false;
      var y = W.scrollY, max = root.scrollHeight - W.innerHeight, probe = 38;
      nav.classList.toggle('is-solid', y > 40);
      if (y > last + 4 && y > 240) nav.classList.add('is-hidden'); else if (y < last - 4 || y < 240) nav.classList.remove('is-hidden');
      last = y;
      var dark = heroDark || darks.some(function (s) { var r = s.getBoundingClientRect(); return r.top <= probe && r.bottom > probe; });
      nav.classList.toggle('is-dark', dark);
      prog.style.transform = 'scaleX(' + (max > 0 ? y / max : 0).toFixed(4) + ')';
      var mid = W.innerHeight * 0.45, act = -1;
      secs.forEach(function (s, i) { if (!s) return; var r = s.getBoundingClientRect(); if (r.top <= mid && r.bottom > mid) act = i; });
      links.forEach(function (a, i) { a.classList.toggle('is-active', i === act); if (i === act) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
      var heroEnd = $('#inicio').getBoundingClientRect().bottom < W.innerHeight * 0.5;
      var pinned = ['#solPin', '#scalesPin'].some(function (q) { var r = $(q).getBoundingClientRect(); return r.top < W.innerHeight * .5 && r.bottom > W.innerHeight * .5; });
      var on = heroEnd && !formIn && !pinned;
      dock.classList.toggle('is-on', on); dock.setAttribute('aria-hidden', String(!on)); $('a', dock).tabIndex = on ? 0 : -1;
    }
    W.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(upd); } }, { passive: true });
    W.addEventListener('resize', upd);
    W.__navUpd = upd;
    upd();
  })();

  /* ---------- Método: carretera generada y camión cenital ---------- */
  var method = $('#metodo'), roadSvg = $('#road'), roadPath = $('#roadPath'), roadEdge = $('#roadEdge'), roadDash = $('#roadDash'), roadCp = $('#roadCp');
  var tTop = $('#truckTop'), steps = $$('.step'), railSpans = $$('.rail span'), railFill = $('#railFill');
  var RD = { L: 0, yA: 0, sA: 0, cps: [] };
  function buildRoad() {
    var w = method.clientWidth, h = method.clientHeight; if (!w) return;
    var mr = method.getBoundingClientRect(), lane = $('.step__lane', steps[0]).getBoundingClientRect(), head = $('.method__head').getBoundingClientRect();
    var x = Math.round(lane.left - mr.left + lane.width / 2), desk = isDesk(), rw = desk ? 96 : 52, dstr;
    var y0 = Math.round(head.bottom - mr.top + (desk ? 70 : 40));
    if (desk) { var r = 150; dstr = 'M -260 ' + y0 + ' H ' + (x - r) + ' A ' + r + ' ' + r + ' 0 0 1 ' + x + ' ' + (y0 + r) + ' V ' + (h + 300); RD.yA = y0 + r; RD.sA = (x - r + 260) + Math.PI * r / 2; }
    else { dstr = 'M ' + x + ' ' + (y0 - 300) + ' V ' + (h + 300); RD.yA = y0; RD.sA = 300; }
    roadSvg.setAttribute('width', w); roadSvg.setAttribute('height', h); roadSvg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
    [roadPath, roadEdge, roadDash].forEach(function (p) { p.setAttribute('d', dstr); });
    roadPath.setAttribute('stroke-width', rw); roadEdge.setAttribute('stroke-width', rw + 12);
    RD.L = roadPath.getTotalLength(); RD.rw = rw;
    var html = '';
    RD.cps = steps.map(function (s) { var r = s.getBoundingClientRect(); var cy = Math.round(r.top - mr.top + (desk ? 96 : 56)); html += '<circle cx="' + x + '" cy="' + cy + '" r="' + (desk ? 13 : 9) + '"/>'; return cy; });
    roadCp.innerHTML = html;
    tTop.style.width = Math.round(rw * 1.72) + 'px';
    var rt = $('#renderTruckTop'); rt.style.width = tTop.style.width;
  }
  var stepDone = [];
  function placeTruck() {
    if (!RD.L) return;
    var mr = method.getBoundingClientRect();
    var y = motion ? W.innerHeight * 0.56 - mr.top : RD.cps[0];
    var s = clamp(RD.sA + (y - RD.yA), 0, RD.L);
    var p = roadPath.getPointAtLength(s), a;
    if (s + 2 <= RD.L) { var q = roadPath.getPointAtLength(s + 2); a = Math.atan2(q.y - p.y, q.x - p.x); } else { var o = roadPath.getPointAtLength(s - 2); a = Math.atan2(p.y - o.y, p.x - o.x); }
    var tf = 'translate(' + p.x.toFixed(1) + 'px,' + p.y.toFixed(1) + 'px) translate(-50%,-50%) rotate(' + (a * 180 / Math.PI).toFixed(2) + 'deg)';
    tTop.style.transform = tf; $('#renderTruckTop').style.transform = tf;
    // El asfalto se dibuja por delante del camión
    var ahead = motion ? s + W.innerHeight * 0.55 : RD.L;
    [roadPath, roadEdge].forEach(function (pth) { pth.style.strokeDasharray = RD.L + ' ' + RD.L; pth.style.strokeDashoffset = RD.L - ahead; });
    dashClip(ahead);
    var dots = roadCp.children, n = 0;
    RD.cps.forEach(function (cy, i) {
      var on = !motion || p.y >= cy - 2; if (on) n = i + 1;
      steps[i].classList.toggle('is-on', on); if (dots[i]) dots[i].classList.toggle('is-on', on);
      if (on && !stepDone[i]) { stepDone[i] = 1; var c = $('[data-step-count]', steps[i]); if (c) countUp(c, +c.dataset.stepCount, 900); }
      if (railSpans[i]) railSpans[i].classList.toggle('is-on', on);
    });
    if (railFill) railFill.style.transform = 'scaleY(' + clamp((s - RD.sA) / Math.max(1, (RD.cps[RD.cps.length - 1] - RD.yA)), 0, 1).toFixed(3) + ')';
  }
  // La línea central discontinua se recorta al tramo ya dibujado con una máscara de trazo
  var dashMaskPath = null;
  function dashClip(ahead) {
    if (!dashMaskPath) {
      var defs = el('defs', {}), m = el('mask', { id: 'dashMask', maskUnits: 'userSpaceOnUse' });
      dashMaskPath = el('path', { fill: 'none', stroke: '#fff' });
      m.appendChild(dashMaskPath); defs.appendChild(m); roadSvg.insertBefore(defs, roadSvg.firstChild);
      roadDash.setAttribute('mask', 'url(#dashMask)');
    }
    dashMaskPath.setAttribute('d', roadPath.getAttribute('d'));
    dashMaskPath.setAttribute('stroke-width', (RD.rw || 96) + 20);
    dashMaskPath.setAttribute('stroke-dasharray', RD.L + ' ' + RD.L);
    dashMaskPath.setAttribute('stroke-dashoffset', RD.L - ahead);
  }

  /* ---------- Escala 03: gráfico de vibración con detección de anomalía ---------- */
  function makeVib() {
    var cv = $('#vibCanvas'), ctx = cv.getContext('2d'), st = $('#vibStatus'), alert = $('#sensorAlert'), Wd, H, buf = [], t = 0, run = false, raf, stage = -1;
    function size() { var r = cv.getBoundingClientRect(), dpr = Math.min(2, W.devicePixelRatio || 1); Wd = r.width; H = r.height; cv.width = Wd * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); buf = new Array(Math.ceil(Wd / 2)).fill(0); }
    function setStage(s) { if (s === stage) return; stage = s; st.textContent = s === 0 ? 'Normal' : s === 1 ? 'Anomalía detectada' : 'Intervención planificada'; st.classList.toggle('is-warn', s === 1); alert.style.visibility = s === 1 ? 'visible' : 'hidden'; }
    function sample() { var cyc = (t % 720) / 60, a = cyc < 4 ? 0 : cyc < 8.5 ? Math.pow((cyc - 4) / 4.5, 1.6) * .62 : Math.max(0, .62 - (cyc - 8.5) * .4); setStage(cyc < 5.2 ? 0 : cyc < 8.5 ? 1 : (a > .02 ? 2 : 0)); return Math.sin(t * .35) * .18 + Math.sin(t * .9) * .08 + (Math.random() - .5) * .14 + Math.sin(t * 1.7) * a; }
    function draw() {
      t++; buf.push(sample()); buf.shift(); ctx.clearRect(0, 0, Wd, H);
      var mid = H / 2, sc = H * .42;
      ctx.fillStyle = 'rgba(92,192,176,.1)'; ctx.fillRect(0, mid - sc * .42, Wd, sc * .84);
      ctx.strokeStyle = 'rgba(232,128,106,.75)'; ctx.setLineDash([4, 4]); ctx.beginPath(); ctx.moveTo(0, mid - sc * .95); ctx.lineTo(Wd, mid - sc * .95); ctx.moveTo(0, mid + sc * .95); ctx.lineTo(Wd, mid + sc * .95); ctx.stroke(); ctx.setLineDash([]);
      ctx.font = '500 10px "JetBrains Mono", monospace'; ctx.fillStyle = 'rgba(242,160,142,.95)'; ctx.fillText('UMBRAL DE FALLA', 6, mid - sc * .95 - 5);
      ctx.lineWidth = 1.6;
      for (var i = 1; i < buf.length; i++) { var v = buf[i]; ctx.strokeStyle = Math.abs(v) > .42 ? '#F0A877' : 'rgba(242,239,233,.9)'; ctx.beginPath(); ctx.moveTo((i - 1) * 2, mid - buf[i - 1] * sc); ctx.lineTo(i * 2, mid - v * sc); ctx.stroke(); }
      if (run) raf = requestAnimationFrame(draw);
    }
    size(); W.addEventListener('resize', size);
    return { start: function () { if (run) return; run = true; draw(); }, stop: function () { run = false; cancelAnimationFrame(raf); }, once: function () { for (var i = 0; i < buf.length + 300; i++) { run = false; draw(); } } };
  }

  /* ---------- Escala 04: bacterias sobre el grano (canvas con ruido suave) ---------- */
  function makeMicro() {
    var cv = $('#microCanvas'), ctx = cv.getContext('2d'), Wd, H, bugs = [], run = false, raf, t = 0;
    function size() {
      var r = cv.getBoundingClientRect(), dpr = Math.min(2, W.devicePixelRatio || 1); Wd = r.width; H = r.height; cv.width = Wd * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Wd < 700 ? 26 : 54, R = rng(11); bugs = [];
      for (var i = 0; i < n; i++) bugs.push({ x: R() * Wd, y: H * .25 + R() * H * .7, a: R() * 6.28, l: 18 + R() * 22, w: 6 + R() * 3, ph: R() * 100, sp: .25 + R() * .45, c: R() < .62 ? 0 : 1 });
    }
    function draw() {
      t += 1 / 60; ctx.clearRect(0, 0, Wd, H);
      bugs.forEach(function (b) {
        var na = Math.sin(t * .6 + b.ph) * .9 + Math.sin(t * .23 + b.ph * 2) * .6;
        b.a += na * .012; b.x += Math.cos(b.a) * b.sp; b.y += Math.sin(b.a) * b.sp;
        if (b.x < -40) b.x = Wd + 40; if (b.x > Wd + 40) b.x = -40; if (b.y < H * .2) b.a = Math.abs(b.a); if (b.y > H + 30) b.y = H * .2;
        ctx.save(); ctx.translate(b.x, b.y); ctx.rotate(b.a);
        var g = ctx.createLinearGradient(0, -b.w, 0, b.w);
        if (b.c === 0) { g.addColorStop(0, 'rgba(180,245,232,.95)'); g.addColorStop(1, 'rgba(47,143,130,.85)'); ctx.shadowColor = 'rgba(92,192,176,.9)'; }
        else { g.addColorStop(0, 'rgba(255,214,180,.95)'); g.addColorStop(1, 'rgba(212,130,79,.85)'); ctx.shadowColor = 'rgba(240,168,119,.9)'; }
        ctx.shadowBlur = 12; ctx.fillStyle = g;
        var l = b.l, w = b.w; ctx.beginPath(); ctx.moveTo(-l / 2 + w / 2, -w / 2); ctx.lineTo(l / 2 - w / 2, -w / 2); ctx.arc(l / 2 - w / 2, 0, w / 2, -Math.PI / 2, Math.PI / 2); ctx.lineTo(-l / 2 + w / 2, w / 2); ctx.arc(-l / 2 + w / 2, 0, w / 2, Math.PI / 2, -Math.PI / 2); ctx.fill();
        ctx.shadowBlur = 0; ctx.strokeStyle = 'rgba(220,250,240,.45)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(-l / 2, 0);
        for (var k = 1; k <= 8; k++) ctx.lineTo(-l / 2 - k * 3, Math.sin(t * 8 + b.ph + k) * 3); ctx.stroke();
        ctx.restore();
      });
      if (run) raf = requestAnimationFrame(draw);
    }
    size(); W.addEventListener('resize', size);
    return { start: function () { if (run) return; run = true; draw(); }, stop: function () { run = false; cancelAnimationFrame(raf); }, once: function () { run = false; for (var i = 0; i < 30; i++) draw(); } };
  }
  var vib = makeVib(), micro = makeMicro();
  if (!motion) { vib.once(); micro.once(); }
  else new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { vib.start(); micro.start(); } else { vib.stop(); micro.stop(); } }); }, { rootMargin: '100px' }).observe($('#escalas'));

  /* ---------- Escena 5: hélice de ADN (Three.js diferido, canvas 2D como respaldo) ---------- */
  var helix = null, helixP = 0;
  function helixPoints(desk) {
    var pts = [], turns = 3.2, n = desk ? 300 : 170, len = 10, R = 1.7, rr = rng(5);
    for (var s = 0; s < 2; s++) for (var i = 0; i < n; i++) { var t = i / (n - 1), a = t * turns * Math.PI * 2 + s * Math.PI; pts.push({ x: Math.cos(a) * R, y: (t - .5) * len, z: Math.sin(a) * R, c: s ? [0.94, 0.66, 0.47] : [0.83, 0.51, 0.31], sz: 1.0 }); }
    var pairs = desk ? 40 : 26;
    for (var p = 0; p < pairs; p++) { var tp = (p + .5) / pairs, ap = tp * turns * Math.PI * 2; for (var k = 1; k < 10; k++) { var f = k / 10, a1 = ap, a2 = ap + Math.PI; pts.push({ x: Math.cos(a1) * R * (1 - f) + Math.cos(a2) * R * f, y: (tp - .5) * len, z: Math.sin(a1) * R * (1 - f) + Math.sin(a2) * R * f, c: k < 5 ? [0.36, 0.75, 0.69] : [0.91, 0.64, 0.23], sz: .7 }); } }
    pts.forEach(function (q) { var u = rr() * 2 - 1, th = rr() * 6.283, rad = 4 + rr() * 5, sq = Math.sqrt(1 - u * u); q.sx = sq * Math.cos(th) * rad; q.sy = u * rad; q.sz0 = sq * Math.sin(th) * rad; q.seed = rr(); });
    return pts;
  }
  function makeHelix2D(cv) {
    var ctx = cv.getContext('2d'), Wd, H, pts = helixPoints(isDesk()), t0 = performance.now(), run = false, raf, ions = [];
    for (var i = 0; i < 26; i++) ions.push({ a: Math.random() * 6.28, y: Math.random() * 10 - 5, r: 2.4 + Math.random() * .9, s: .4 + Math.random() * .5 });
    function size() { var r = cv.getBoundingClientRect(), dpr = Math.min(2, W.devicePixelRatio || 1); Wd = r.width; H = r.height; cv.width = Wd * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); }
    function frame(now) {
      var time = (now - t0) / 1000, form = clamp(helixP * 2.2, 0, 1), rot = helixP * Math.PI * 4 + (motion ? time * .12 : .6), sc = Math.min(Wd, H) / 13;
      ctx.clearRect(0, 0, Wd, H); ctx.globalCompositeOperation = 'lighter';
      var cr = Math.cos(rot), sr = Math.sin(rot);
      pts.forEach(function (q) {
        var k = clamp(form * 1.3 - q.seed * .3, 0, 1); k = k * k * (3 - 2 * k);
        var x = q.sx + (q.x - q.sx) * k, y = q.sy + (q.y - q.sy) * k, z = q.sz0 + (q.z - q.sz0) * k;
        var X = x * cr - z * sr, Z = x * sr + z * cr, persp = 12 / (12 - Z), px = Wd / 2 + X * sc * persp, py = H / 2 + y * sc * .82 * persp, a = .35 + .5 * (Z + 3) / 6;
        ctx.fillStyle = 'rgba(' + (q.c[0] * 255 | 0) + ',' + (q.c[1] * 255 | 0) + ',' + (q.c[2] * 255 | 0) + ',' + a.toFixed(2) + ')';
        ctx.beginPath(); ctx.arc(px, py, q.sz * 2.2 * persp, 0, 6.283); ctx.fill();
      });
      ions.forEach(function (o) { o.a += motion ? .01 * o.s : 0; var x = Math.cos(o.a + rot) * o.r, z = Math.sin(o.a + rot) * o.r, persp = 12 / (12 - z); ctx.fillStyle = 'rgba(92,192,176,' + (.5 * form + .1).toFixed(2) + ')'; ctx.beginPath(); ctx.arc(Wd / 2 + x * sc * persp, H / 2 + o.y * sc * .82 * persp, 3.4 * persp, 0, 6.283); ctx.fill(); });
      ctx.globalCompositeOperation = 'source-over';
      if (run) raf = requestAnimationFrame(frame);
    }
    size(); W.addEventListener('resize', size);
    return { setProgress: function (p) { helixP = p; }, start: function () { if (run) return; run = true; raf = requestAnimationFrame(frame); }, stop: function () { run = false; cancelAnimationFrame(raf); }, once: function () { helixP = 1; frame(performance.now()); } };
  }
  (function () {
    var cv = $('#helix'), started = false;
    if (!motion) { helix = makeHelix2D(cv); helix.once(); return; }
    var vis = new IntersectionObserver(function (es) { es.forEach(function (e) { if (!helix) return; e.isIntersecting ? helix.start() : helix.stop(); }); });
    var near = new IntersectionObserver(function (es) {
      if (!es[0].isIntersecting || started) return; started = true; near.disconnect();
      import('./helix.js').then(function (m) { helix = m.createHelix(cv, { desk: isDesk(), points: helixPoints(isDesk()), getP: function () { return helixP; } }); })
        .catch(function () { helix = makeHelix2D(cv); })
        .then(function () { vis.observe(cv); });
    }, { rootMargin: '900px 0px' });
    near.observe(cv);
  })();

  /* ---------- Partículas del hero: roca y polvo ---------- */
  var FX = (function () {
    var cv = $('#fx'), ctx = cv.getContext('2d'), Wd = 0, H = 0, ps = [], run = false;
    function size() { var r = cv.getBoundingClientRect(), dpr = Math.min(2, W.devicePixelRatio || 1); Wd = r.width; H = r.height; cv.width = Wd * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); }
    function loop() {
      ctx.clearRect(0, 0, Wd, H);
      for (var i = ps.length - 1; i >= 0; i--) {
        var p = ps[i]; p.life -= 1 / 60;
        if (p.k === 'rock') { p.vy += 0.42; p.x += p.vx; p.y += p.vy; if (p.y >= p.floor) { ps.splice(i, 1); dust(p.x, p.floor, 2, .6); continue; } ctx.fillStyle = p.c; ctx.beginPath(); ctx.ellipse(p.x, p.y, p.r, p.r * .8, p.rot += .1, 0, 6.283); ctx.fill(); }
        else { p.x += p.vx; p.y += p.vy; p.r += p.g; var a = clamp(p.life / p.l0, 0, 1) * p.a; if (p.life <= 0) { ps.splice(i, 1); continue; } ctx.fillStyle = 'rgba(176,140,104,' + a.toFixed(3) + ')'; ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.283); ctx.fill(); }
      }
      if (ps.length) requestAnimationFrame(loop); else run = false;
    }
    function kick() { if (!run) { run = true; requestAnimationFrame(loop); } }
    function dust(x, y, n, s) { for (var i = 0; i < n; i++) ps.push({ k: 'dust', x: x + (Math.random() - .5) * 20, y: y - Math.random() * 8, vx: (Math.random() - .5) * 1.2 * s - .3, vy: -Math.random() * .7 * s, r: 4 + Math.random() * 8, g: .35 + Math.random() * .4, life: 1 + Math.random() * .8, l0: 1.6, a: .22 + Math.random() * .16 }); kick(); }
    function rocks(x0, x1, y, floor, n) { var cs = ['#7A4528', '#A8613A', '#5A3522', '#2F8F82', '#C77B4A']; for (var i = 0; i < n; i++) ps.push({ k: 'rock', x: x0 + Math.random() * (x1 - x0), y: y + Math.random() * 6, vx: (Math.random() - .5) * .8, vy: Math.random() * 1.5, r: 2.5 + Math.random() * 4, c: cs[(Math.random() * cs.length) | 0], rot: 0, floor: floor + Math.random() * 10 }); kick(); }
    size(); W.addEventListener('resize', size);
    return { dust: dust, rocks: rocks, size: size };
  })();

  /* ---------- Cursor, botones magnéticos y tarjetas con inclinación (solo escritorio) ---------- */
  if (fine && motion) {
    var cur = $('#cursor'), cx = 0, cy = 0, tx = 0, ty = 0;
    W.addEventListener('pointermove', function (e) { tx = e.clientX; ty = e.clientY; cur.classList.add('is-on'); }, { passive: true });
    d.addEventListener('pointerleave', function () { cur.classList.remove('is-on'); });
    d.addEventListener('pointerover', function (e) { cur.classList.toggle('is-hover', !!e.target.closest('a,button,label,[role=radio]')); });
    (function f() { cx += (tx - cx) * .22; cy += (ty - cy) * .22; cur.style.transform = 'translate(' + cx.toFixed(1) + 'px,' + cy.toFixed(1) + 'px)'; requestAnimationFrame(f); })();
    $$('[data-magnet]').forEach(function (b) {
      b.addEventListener('pointermove', function (e) { var r = b.getBoundingClientRect(); b.style.translate = ((e.clientX - r.left - r.width / 2) * .22).toFixed(1) + 'px ' + ((e.clientY - r.top - r.height / 2) * .3).toFixed(1) + 'px'; });
      b.addEventListener('pointerleave', function () { b.style.translate = '0 0'; });
      b.style.transition += ',translate .35s cubic-bezier(.23,1,.32,1)';
    });
    $$('[data-tilt]').forEach(function (c) {
      var g = $('.card__glare', c);
      c.addEventListener('pointermove', function (e) { var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height; c.style.transform = 'perspective(900px) rotateY(' + ((x - .5) * 12).toFixed(2) + 'deg) rotateX(' + ((.5 - y) * 12).toFixed(2) + 'deg)'; g.style.setProperty('--gx', (x * 100).toFixed(1) + '%'); g.style.setProperty('--gy', (y * 100).toFixed(1) + '%'); });
      c.addEventListener('pointerleave', function () { c.style.transform = ''; });
      c.style.transition = 'border-color .3s ease, transform .4s cubic-bezier(.23,1,.32,1)';
    });
  }

  /* =========================================================
     Sin movimiento: estado final estático y legible
     ========================================================= */
  if (!motion) {
    $$('.cap').forEach(function (c) { $('[data-layer="' + c.dataset.cap + '"]').appendChild(c); });
    $$('[data-count]').forEach(function (n) { n.textContent = n.dataset.count; });
    var stat = function () { buildRoad(); placeTruck(); };
    stat(); W.addEventListener('resize', stat); W.addEventListener('load', stat);
    if (d.fonts && d.fonts.ready) d.fonts.ready.then(stat);
    return;
  }

  /* =========================================================
     Con movimiento: GSAP + ScrollTrigger + Lenis
     ========================================================= */
  gsap.registerPlugin(ScrollTrigger);
  var lenis = null;
  if (W.Lenis) {
    lenis = new Lenis({ duration: 1.15, easing: function (t) { return 1 - Math.pow(1 - t, 4); } });
    root.classList.add('lenis'); lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); }); gsap.ticker.lagSmoothing(0);
  }
  function goTo(y) { if (lenis) lenis.scrollTo(y, { duration: 1.6 }); else W.scrollTo({ top: y, behavior: 'smooth' }); }
  var solST = null;
  $$('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href'); if (id.length < 2) return;
      var tg = d.querySelector(id); if (!tg) return; e.preventDefault();
      if (id === '#soluciones' && solST) { goTo(solST.start + 2); return; }
      if (lenis) lenis.scrollTo(tg, { duration: 1.6, offset: id === '#inicio' ? 0 : -8 }); else tg.scrollIntoView({ behavior: 'smooth' });
      if (tg.matches('section,footer')) { tg.setAttribute('tabindex', '-1'); tg.focus({ preventScroll: true }); }
    });
  });

  /* ---------- Escena 0: precarga ---------- */
  var heroCount = $$('#heroCopy [data-count]');
  heroCount.forEach(function (n) { n.textContent = '0'; });
  var loadN = { v: 0 };
  var intro = gsap.timeline({ defaults: { ease: 'power3.out' } });
  intro.to('#loader svg rect, #loader svg path', { strokeDashoffset: 0, duration: .9, ease: 'power2.inOut', stagger: .08 }, 0)
    .to(loadN, { v: 100, duration: .95, ease: 'power2.inOut', onUpdate: function () { $('#loaderN').textContent = String(Math.round(loadN.v)).padStart(3, '0'); } }, 0)
    .to('#loader', { yPercent: -100, duration: .7, ease: 'expo.inOut' }, 1.0)
    .set('#loader', { display: 'none' })
  /* ---------- Escena 1: entrada del hero (ciclo de carga) ---------- */
    .to('#heroCopy .h1 .ln > span', { y: 0, duration: 1.1, stagger: .08 }, 1.25)
    .fromTo('[data-hero-fade]', { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .9, stagger: .07 }, 1.45)
    .add(function () { heroCount.forEach(function (n) { countUp(n, +n.dataset.count, 1100); }); }, 1.7)
    .fromTo('#rig', { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 1, ease: 'expo.out' }, 1.15)
    .fromTo('#truckHero .t-load', { scaleY: .45, transformOrigin: '50% 100%' }, { scaleY: .45, duration: .01 }, 1.15)
    .to(pose, { c: 58, duration: .35, ease: 'power2.inOut', onUpdate: setPose }, 1.9)
    .add(function () { dumpRocks(); }, 2.0)
    .to(bLoad, { opacity: 0, y: 30, duration: .3, ease: 'power2.in' }, 2.0)
    .to('#truckHero .t-load', { scaleY: 1, duration: .55, ease: 'power2.out' }, 2.1)
    .to('#truckHero', { y: function () { return heroTruckW() * .012; }, duration: .12, ease: 'power2.out' }, 2.2)
    .to('#truckHero', { y: 0, duration: .9, ease: 'elastic.out(1, .35)' }, 2.32)
    .to(pose, { c: 0, b: 7, s: 12, duration: 1.1, ease: 'power2.inOut', onUpdate: setPose }, 2.55);

  function heroTruckW() { return $('#truckHero').getBoundingClientRect().width; }
  function dumpRocks() {
    var rig = $('#rig'), sc = $('#scene'), rr = rig.getBoundingClientRect(), sr = sc.getBoundingClientRect(), u = rr.height / 460;
    var ox = rr.left - sr.left, oy = rr.top - sr.top;
    FX.size();
    FX.rocks(ox + 532 * u, ox + 600 * u, oy + 116 * u, oy + 150 * u, 46);
    FX.dust(ox + 566 * u, oy + 150 * u, 10, 1);
  }

  var mm = gsap.matchMedia();
  mm.add({ desk: '(min-width: 768px)', mob: '(max-width: 767px)' }, function (ctx) {
    var desk = ctx.conditions.desk;

    /* ---------- Hero fijado: el camión arranca y el fondo pasa a negro ---------- */
    var truck = $('#truckHero'), wheels = $$('#truckHero .wheel');
    gsap.set(wheels, { transformOrigin: '50% 50%' });
    var tLeft = function () { return truck.getBoundingClientRect().left - (gsap.getProperty(truck, 'x') || 0); };
    var offR = function () { return W.innerWidth - tLeft() + 60; };
    var deg = function (px, w) { return px / (2 * Math.PI * (92 / 640) * w) * 360; };
    var lastDust = 0;
    var htl = gsap.timeline({ defaults: { ease: 'none' }, scrollTrigger: {
      trigger: '#heroPin', start: 'top top', end: desk ? '+=150%' : '+=110%', pin: true, scrub: 1, invalidateOnRefresh: true,
      onUpdate: function (st) {
        heroDark = st.progress > .45; if (W.__navUpd) W.__navUpd();
        var v = Math.abs(st.getVelocity()), now = performance.now();
        if (st.progress > .08 && st.progress < .95 && v > 60 && now - lastDust > 70) {
          lastDust = now; var r = truck.getBoundingClientRect(), s = $('#scene').getBoundingClientRect();
          FX.size(); FX.dust(r.left - s.left + r.width * .2, r.bottom - s.top - 4, 2 + Math.min(4, v / 600 | 0), 1.4);
        }
      } } });
    htl.to('#heroCopy', { y: -70, opacity: 0, duration: .4, ease: 'power2.in' }, 0)
      .to('#sweep', { scaleX: 1, duration: .55, ease: 'power2.inOut' }, .1)
      .to('#shovel', { x: function () { return -W.innerWidth * .25; }, opacity: 0, duration: .5, ease: 'power2.in' }, .15)
      .to(truck, { x: offR, duration: .85, ease: 'power2.in' }, .15)
      .to(wheels, { rotation: function () { return deg(offR(), truck.getBoundingClientRect().width); }, duration: .85, ease: 'power2.in' }, .15)
      .to('#lane', { xPercent: -40, duration: .85, ease: 'power2.in' }, .15)
      .to({}, { duration: .05 });

    /* ---------- Soluciones ---------- */
    var cards = $$('.card'), solW = $$('#truckSol .wheel');
    gsap.set(solW, { transformOrigin: '50% 50%' });
    cards.forEach(function (c) {
      gsap.set(c, { clipPath: 'inset(0% 0% 0% 100% round 18px)' });
      gsap.set($('.card__img img', c), { scale: 1.15 });
      $$('.card__top svg path, .card__top svg circle', c).forEach(function (p) { p.style.strokeDasharray = '1'; p.style.strokeDashoffset = '1'; });
    });
    function revealCard(c) {
      if (c._in) return; c._in = 1;
      gsap.to(c, { clipPath: 'inset(0% 0% 0% 0% round 18px)', duration: 1.1, ease: 'expo.out' });
      gsap.to($('.card__img img', c), { scale: 1, duration: 1.6, ease: 'power3.out' });
      gsap.to($$('.card__top svg path, .card__top svg circle', c), { strokeDashoffset: 0, duration: 1, delay: .3, ease: 'power2.out' });
    }
    function checkCards() { cards.forEach(function (c) { var r = c.getBoundingClientRect(); if (r.left < W.innerWidth * .96 && r.top < W.innerHeight * .95) revealCard(c); }); }

    if (desk) {
      var view = $('.cards-view'), trackEl = $('#cards'), mq = $('#marquee'), solTruckEl = $('#truckSol');
      var dist = function () { return Math.max(0, trackEl.scrollWidth - view.clientWidth + 40); };
      var sdeg = function (px) { return deg(px, solTruckEl.getBoundingClientRect().width); };
      var stl = gsap.timeline({ defaults: { ease: 'none' }, scrollTrigger: {
        trigger: '#solPin', start: 'top top', end: function () { return '+=' + Math.round(dist() + W.innerHeight * 1.1); },
        pin: true, scrub: 1, invalidateOnRefresh: true, onUpdate: checkCards, onEnter: checkCards } });
      solST = stl.scrollTrigger;
      stl.fromTo(solTruckEl, { x: function () { return -W.innerWidth * .7; } }, { x: 0, duration: .25, ease: 'power2.out' }, 0)
        .fromTo(solW, { rotation: 0 }, { rotation: function () { return sdeg(W.innerWidth * .7); }, duration: .25, ease: 'power2.out' }, 0)
        .fromTo(mq, { xPercent: -50 }, { xPercent: -12, duration: 1.25 }, 0)
        .to(trackEl, { x: function () { return -dist(); }, duration: 1 }, .15)
        .to(solW, { rotation: function () { return sdeg(W.innerWidth * .7) + sdeg(dist() * .5); }, duration: 1 }, .15)
        .to(solTruckEl, { x: function () { return W.innerWidth * .8; }, duration: .2, ease: 'power2.in' }, 1.15)
        .to(solW, { rotation: function () { return sdeg(W.innerWidth * .7) + sdeg(dist() * .5) + sdeg(W.innerWidth * .8); }, duration: .2, ease: 'power2.in' }, 1.15);
      ScrollTrigger.create({ trigger: '#soluciones', start: 'top 70%', onEnter: checkCards });
    } else {
      ScrollTrigger.create({ trigger: '#soluciones', start: 'top bottom', end: 'bottom top', scrub: true, animation: gsap.fromTo('#marquee', { xPercent: -45 }, { xPercent: -5, ease: 'none' }) });
      ScrollTrigger.create({ trigger: '#soluciones', start: 'top bottom', end: 'bottom top', scrub: true, animation: gsap.fromTo(solW, { rotation: 0 }, { rotation: 900, ease: 'none' }) });
      var cio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) revealCard(e.target); }); }, { threshold: .25 });
      cards.forEach(function (c) { cio.observe(c); });
    }

    /* ---------- Método ---------- */
    ScrollTrigger.create({ trigger: method, start: 'top bottom', end: 'bottom top', onUpdate: placeTruck, onRefresh: function () { buildRoad(); placeTruck(); } });

    /* ---------- Escalas: zoom continuo por cuatro escalas ---------- */
    var layers = $$('.layer'), caps = $$('.cap'), lis = $$('.scale-list li'), ruler = $('#rulerV');
    gsap.set(layers.slice(1), { opacity: 0 }); gsap.set(caps, { opacity: 0, y: 24 });
    $$('#contours .contour').forEach(function (p) { p.style.strokeDasharray = '1'; p.style.strokeDashoffset = '1'; });
    gsap.set('[data-layer="0"] .anom, [data-layer="0"] .pin-l', { opacity: 0 });
    var R = { l: Math.log10(400000) };
    function fmt(m) { if (m >= 1000) { var k = m / 1000; return (k >= 10 ? Math.round(k) : k.toFixed(1).replace('.', ',')) + ' km'; } if (m >= 1) return (m >= 10 ? Math.round(m) : m.toFixed(1).replace('.', ',')) + ' m'; if (m >= 1e-3) return Math.round(m * 1000) + ' mm'; return Math.max(1, Math.round(m * 1e6)) + ' µm'; }
    function onRuler() { var m = Math.pow(10, R.l); ruler.textContent = fmt(m); var i = R.l > 4.3 ? 0 : R.l > 2 ? 1 : R.l > -2.5 ? 2 : 3; lis.forEach(function (x, k) { x.classList.toggle('is-on', k === i); }); }
    var blur = desk ? 'blur(6px)' : 'blur(0px)';
    var ztl = gsap.timeline({ defaults: { ease: 'none' }, scrollTrigger: { trigger: '#scalesPin', start: 'top top', end: desk ? '+=400%' : '+=260%', pin: true, scrub: 1 } });
    ztl.to('#contours .contour', { strokeDashoffset: 0, duration: .5, stagger: .05, ease: 'power1.inOut' }, .05)
      .to('[data-layer="0"] .anom', { opacity: 1, duration: .2, stagger: .1 }, .4)
      .to('[data-layer="0"] .pin-l', { opacity: 1, duration: .2, stagger: .1 }, .5);
    var marks = [Math.log10(400000), Math.log10(2000), 1, -6];
    [0, 1, 2].forEach(function (i) {
      var t = 1.1 + i * 1.6, a = layers[i], b = layers[i + 1];
      ztl.to(a, { scale: 2.5, filter: blur, duration: .6, ease: 'power2.in' }, t)
        .to(a, { opacity: 0, duration: .3 }, t + .3)
        .fromTo(b, { opacity: 0, scale: 1.2, filter: blur }, { opacity: 1, scale: 1, filter: 'blur(0px)', duration: .45, ease: 'power2.out' }, t + .3)
        .to(R, { l: marks[i + 1], duration: .6, ease: 'power1.inOut', onUpdate: onRuler }, t)
        .to(i === 0 ? '#scalesCopy' : caps[i - 1], { opacity: 0, y: -20, duration: .25 }, t)
        .to(caps[i], { opacity: 1, y: 0, duration: .3 }, t + .45);
    });
    ztl.to({}, { duration: .6 });

    /* ---------- Genómica ---------- */
    ScrollTrigger.create({ trigger: '#genomica', start: 'top 85%', end: 'bottom 30%', onUpdate: function (st) { helixP = st.progress; if (helix && helix.setProgress) helix.setProgress(st.progress); } });

    /* ---------- Cátodo: barrido especular y frase palabra por palabra ---------- */
    var words = splitWords($('#quote'));
    gsap.fromTo(words, { color: '#5E5A53' }, { color: '#F2EFE9', stagger: .1, ease: 'none', scrollTrigger: { trigger: '#catodo', start: 'top 65%', end: 'center 40%', scrub: true } });
    gsap.fromTo('#spec', { xPercent: -70 }, { xPercent: 70, ease: 'none', scrollTrigger: { trigger: '#catodo', start: 'top bottom', end: 'bottom top', scrub: true } });
    gsap.fromTo('#cathodeMedia', { yPercent: -6, scale: 1.1 }, { yPercent: 6, scale: 1, ease: 'none', scrollTrigger: { trigger: '#catodo', start: 'top bottom', end: 'bottom top', scrub: true } });

    return function () { solST = null; };
  });

  function splitWords(node) {
    if (!node) return [];
    var txt = node.textContent.trim(); node.setAttribute('aria-label', txt); node.textContent = '';
    txt.split(/\s+/).forEach(function (w, i) { if (i) node.appendChild(d.createTextNode(' ')); var s = d.createElement('span'); s.className = 'w'; s.setAttribute('aria-hidden', 'true'); s.textContent = w; node.appendChild(s); });
    return $$('.w', node);
  }

  var refresh = function () { ScrollTrigger.refresh(); };
  if (d.fonts && d.fonts.ready) d.fonts.ready.then(refresh);
  W.addEventListener('load', refresh);
})();
