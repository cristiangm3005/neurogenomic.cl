/* =========================================================
   NEUROGENOMIC · main.js (vanilla, sin dependencias)
   1 Utilidades · 2 Navegación · 3 Revelado · 4 Bucle de scroll
   5 Heatmap · 6 Demostración scroll-driven · 7 Caso · 8 Formulario
   Si algo falla, el contenido sigue visible: las animaciones son una capa extra.
   ========================================================= */
(function () {
  'use strict';

  /* ---------- 1 · Utilidades ---------- */
  var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var clamp01 = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
  var hasIO = 'IntersectionObserver' in window;
  var supportsView = !!(window.CSS && CSS.supports && CSS.supports('animation-timeline: view()'));

  /* ---------- 2 · Navegación ---------- */
  var nav = $('#nav'), burger = $('.burger'), menu = $('#menu'), mcta = $('#mcta');
  var setMenu = function (open) {
    menu.hidden = !open; menu.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
    document.documentElement.style.overflow = open ? 'hidden' : '';
    if (open) { var a = menu.querySelector('a'); if (a) a.focus(); }
  };
  burger.addEventListener('click', function () { setMenu(menu.hidden); });
  menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !menu.hidden) { setMenu(false); burger.focus(); }
  });
  addEventListener('resize', function () { if (innerWidth >= 1024 && !menu.hidden) setMenu(false); });

  // Sección activa en el menú
  var links = $$('.nav__links a');
  var ids = ['servicios', 'metodo', 'aplicaciones', 'evidencia', 'etica', 'contacto'];
  if (hasIO) {
    var navIO = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(function (a) {
          if (a.getAttribute('href') === '#' + e.target.id) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    ids.forEach(function (id) { var el = document.getElementById(id); if (el) navIO.observe(el); });
  }

  /* ---------- 3 · Revelado progresivo (respaldo si no hay animation-timeline) ---------- */
  if (!supportsView) {
    if (hasIO && !RM) {
      var rio = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); rio.unobserve(e.target); } });
      }, { rootMargin: '0px 0px -8% 0px' });
      $$('.rv').forEach(function (el) { rio.observe(el); });
    } else { $$('.rv').forEach(function (el) { el.classList.add('in'); }); }
  }

  /* ---------- 4 · Bucle de scroll único (rAF) ---------- */
  var tasks = [], queued = false;
  var frame = function () { queued = false; var y = scrollY, vh = innerHeight; for (var i = 0; i < tasks.length; i++) tasks[i](y, vh); };
  var request = function () { if (!queued) { queued = true; requestAnimationFrame(frame); } };
  addEventListener('scroll', request, { passive: true });
  addEventListener('resize', request);

  var progEl = $('.progress'), hero = $('#inicio'), heroImg = $('.hero__fig img'), contact = $('#contacto');
  tasks.push(function (y, vh) {
    nav.classList.toggle('solid', y > 24);
    var max = document.documentElement.scrollHeight - vh;
    progEl.style.setProperty('--p', max > 0 ? (y / max).toFixed(4) : 0);
    // CTA móvil: aparece tras el hero y se oculta en la sección de contacto
    var c = contact.getBoundingClientRect();
    mcta.classList.toggle('show', y > hero.offsetHeight * .7 && c.top > vh * .9);
    // Parallax sutil de la foto del hero (máx. 40 px)
    if (!RM && heroImg && y < vh * 1.2) heroImg.style.setProperty('--py', (y * .08).toFixed(1) + 'px');
  });

  // Método: la línea se ilumina y las etapas se encienden en orden
  var stepsWrap = $('#steps'), stepEls = $$('.step');
  var setSteps = function (p) {
    stepsWrap.style.setProperty('--m', p.toFixed(4));
    stepEls.forEach(function (s, i) { s.classList.toggle('lit', p >= i / stepEls.length + .02); });
  };
  if (RM) setSteps(1);
  else tasks.push(function (y, vh) {
    var r = stepsWrap.getBoundingClientRect();
    setSteps(clamp01((vh * .82 - r.top) / (r.height + vh * .35)));
  });

  /* ---------- 5 · Heatmap térmico pixelado ---------- */
  var RAMP = [[0, [200, 255, 0, 0]], [.16, [200, 255, 0, .42]], [.4, [200, 255, 0, .8]], [.62, [255, 214, 0, .9]], [.8, [255, 122, 0, .94]], [1, [255, 42, 0, 1]]];
  var thermal = function (v) {
    for (var k = 1; k < RAMP.length; k++) if (v <= RAMP[k][0]) {
      var lo = RAMP[k - 1], hi = RAMP[k], t = (v - lo[0]) / (hi[0] - lo[0]);
      return 'rgba(' + (lo[1][0] + (hi[1][0] - lo[1][0]) * t | 0) + ',' + (lo[1][1] + (hi[1][1] - lo[1][1]) * t | 0) + ',' + (lo[1][2] + (hi[1][2] - lo[1][2]) * t | 0) + ',' + (lo[1][3] + (hi[1][3] - lo[1][3]) * t).toFixed(3) + ')';
    }
    return 'rgba(255,42,0,1)';
  };
  // pts: [x, y, radio (fracción de min(w,h)), peso] en coordenadas 0–1 del rectángulo
  var heat = function (ctx, pts, w, h, gain, alpha) {
    var base = Math.min(w, h), cell = Math.max(5, Math.round(base / 48)), gap = Math.max(1, cell * .18);
    ctx.save(); ctx.globalAlpha = alpha;
    for (var y = 0; y < h; y += cell) for (var x = 0; x < w; x += cell) {
      var cx = x + cell / 2, cy = y + cell / 2, v = 0;
      for (var i = 0; i < pts.length; i++) {
        var p = pts[i], s = p[2] * base, dx = cx - p[0] * w, dy = cy - p[1] * h;
        v += p[3] * Math.exp(-(dx * dx + dy * dy) / (s * s * .9));
      }
      v *= gain; if (v < .08) continue;
      ctx.fillStyle = thermal(Math.min(1, v)); ctx.fillRect(x + gap / 2, y + gap / 2, cell - gap, cell - gap);
    }
    ctx.restore();
  };

  /* =========================================================
     6 · DEMOSTRACIÓN: secuencia de 80 cuadros sincronizada con el scroll
     - El progreso del scroll (0–1) elige el cuadro y la fase.
     - Un suavizado (lerp) en rAF evita saltos con ruedas de mouse "a pasos".
     - Las capas usan la posición del packaging EN CADA CUADRO (NG_SEQ).
     ========================================================= */
  var SEQ = window.NG_SEQ, demo = $('#demo'), cv = $('#demo-cv');
  if (SEQ && demo && cv) (function () {
    var ctx = cv.getContext('2d'), gcv = $('#gsr-cv'), gctx = gcv.getContext('2d');
    var N = SEQ.frames, imgs = [], ok = [], nOk = 0;
    var hudF = $('#hud-f'), hudX = $('#hud-x'), phN = $('#ph-n'), phL = $('#ph-l'), gsrV = $('#gsr-v'), loadEl = $('#demo-load');
    var phaseBars = $$('.phases i'), PH = ['Estímulo', 'Fijaciones', 'Recorrido', 'Mapa de calor', 'Zonas ciegas'];
    var CUT = [0, .16, .36, .56, .78, 1];

    // Carga progresiva: 1 de cada 8 → 4 → 2 → 1 (se puede recorrer desde el inicio)
    var src = function (i) { return 'img/seq/f_' + ('00' + i).slice(-3) + '.webp'; };
    var load = function (i) {
      if (imgs[i]) return;
      var im = new Image(); im.decoding = 'async'; imgs[i] = im;
      im.onload = function () { ok[i] = true; nOk++; loadEl.textContent = nOk < N ? 'Cargando ' + Math.round(nOk / N * 100) + ' %' : ''; dirty = true; kick(); };
      im.src = src(i);
    };
    var started = false;
    var startLoad = function () {
      if (started) return; started = true;
      [8, 4, 2, 1].forEach(function (st, k) { setTimeout(function () { for (var i = 0; i < N; i += st) load(i); }, k * 150); });
      load(N - 1);
    };
    load(0);
    if (hasIO) new IntersectionObserver(function (es) { if (es[0].isIntersecting) startLoad(); }, { rootMargin: '150% 0px' }).observe(demo); else startLoad();
    var nearest = function (i) { for (var d = 0; d < N; d++) { if (ok[i - d]) return i - d; if (ok[i + d]) return i + d; } return -1; };

    // Tamaño de canvas con DPR (máx. 2)
    var W = 0, H = 0, GW = 0, GH = 0, dirty = true;
    var fit = function () {
      var d = Math.min(devicePixelRatio || 1, 2), r = cv.getBoundingClientRect(), g = gcv.getBoundingClientRect();
      W = r.width; H = r.height; cv.width = Math.round(W * d); cv.height = Math.round(H * d); ctx.setTransform(d, 0, 0, d, 0, 0);
      GW = g.width; GH = g.height; gcv.width = Math.round(GW * d); gcv.height = Math.round(GH * d); gctx.setTransform(d, 0, 0, d, 0, 0);
      dirty = true;
    };

    // Fijaciones simuladas en orden de lectura: [zona, desplazamiento x, y, duración ms]
    var FIX = [['origin', 0, 0, 440], ['logo', 0, 0, 300], ['notes', 0, 0, 260], ['valve', 0, 0, 190], ['weight', 0, 0, 340], ['beans', 0, 0, 230], ['logo', .03, .01, 210], ['origin', -.02, .01, 380]];

    // Curva GSR simulada: base lenta + respuestas tras ciertas fijaciones (no son datos reales)
    var GSR = (function () {
      var n = 400, out = [], peaks = [[.24, .9], [.31, .5], [.47, .7], [.63, 1], [.74, .45], [.86, .6]];
      for (var i = 0; i < n; i++) {
        var t = i / (n - 1), v = .22 + .1 * t + .015 * Math.sin(t * 40) + .01 * Math.sin(t * 97);
        peaks.forEach(function (p) { var k = t - p[0]; if (k > 0) v += p[1] * .28 * (1 - Math.exp(-k / .012)) * Math.exp(-k / .06); });
        out.push(v);
      }
      return out;
    })();

    var target = RM ? 1 : 0, shown = RM ? 1 : 0, lastF = -1, typed = '', typeTarget = PH[0], typeT = 0;

    var drawGSR = function (p) {
      gctx.clearRect(0, 0, GW, GH);
      var padT = 26, padB = 8, h = GH - padT - padB, n = Math.max(2, Math.round(p * (GSR.length - 1)));
      gctx.strokeStyle = 'rgba(255,255,255,.06)'; gctx.lineWidth = 1;
      for (var k = 1; k < 4; k++) { var yy = padT + h * k / 4; gctx.beginPath(); gctx.moveTo(0, yy); gctx.lineTo(GW, yy); gctx.stroke(); }
      gctx.beginPath();
      for (var i = 0; i < n; i++) { var x = i / (GSR.length - 1) * GW, y = padT + h * (1 - Math.min(1, GSR[i] / 1.05)); i ? gctx.lineTo(x, y) : gctx.moveTo(x, y); }
      gctx.strokeStyle = '#C8F542'; gctx.lineWidth = 1.6; gctx.stroke();
      var lx = (n - 1) / (GSR.length - 1) * GW, ly = padT + h * (1 - Math.min(1, GSR[n - 1] / 1.05));
      gctx.fillStyle = '#C8FF00'; gctx.beginPath(); gctx.arc(lx, ly, 3.5, 0, 6.2832); gctx.fill();
      gsrV.textContent = (GSR[n - 1] * 5).toFixed(2).replace('.', ',');
    };

    var draw = function () {
      var p = shown, f = Math.round(p * (N - 1)), idx = nearest(f);
      if (idx < 0) return;
      ctx.clearRect(0, 0, W, H);
      // Cuadro en modo "cover"
      var iw = SEQ.size[0], ih = SEQ.size[1], s = Math.max(W / iw, H / ih), dw = iw * s, dh = ih * s, ox = (W - dw) / 2, oy = (H - dh) / 2;
      ctx.drawImage(imgs[idx], ox, oy, dw, dh);
      var at = function (name, dx, dy) { var a = SEQ.anchors[name][f]; return [ox + (a[0] + (dx || 0)) * dw, oy + (a[1] + (dy || 0)) * dh]; };
      var u = Math.max(.55, dw / 1000);

      var pFix = clamp01((p - CUT[1]) / (CUT[2] - CUT[1])), pPath = clamp01((p - CUT[2]) / (CUT[3] - CUT[2]));
      var pHeat = clamp01((p - CUT[3]) / (CUT[4] - CUT[3])), pBlind = clamp01((p - CUT[4]) / (CUT[5] - CUT[4]));
      var phase = 0; for (var q = 1; q < 5; q++) if (p >= CUT[q]) phase = q;

      // Heatmap que se intensifica gradualmente
      if (pHeat > 0) {
        var hp = FIX.map(function (z) { var a = at(z[0], z[1], z[2]); return [a[0] / W, a[1] / H, .028 + z[3] / 12000, .45 + z[3] / 900]; });
        var o = at('origin'); hp.push([o[0] / W, o[1] / H, .055, .9]);
        heat(ctx, hp, W, H, .35 + pHeat * .35, Math.min(.85, pHeat * 1.1));
      }
      // Fijaciones que aparecen una por una
      var pts = FIX.map(function (z) { return at(z[0], z[1], z[2]).concat(z[3]); });
      var nFix = Math.min(FIX.length, Math.ceil(pFix * FIX.length - 1e-6)), dim = 1 - pHeat * .5;
      // Recorrido (scanpath) que se dibuja progresivamente
      if (pPath > 0 && nFix > 1) {
        var segs = (nFix - 1) * pPath;
        ctx.save(); ctx.lineJoin = 'round'; ctx.lineCap = 'round'; ctx.globalAlpha = dim;
        [['rgba(0,0,0,.55)', 4 * u + 1], ['#C8FF00', 1.6 * u + .5]].forEach(function (st) {
          ctx.strokeStyle = st[0]; ctx.lineWidth = st[1]; ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]);
          for (var i = 1; i <= Math.ceil(segs); i++) { var k = Math.min(1, segs - (i - 1)); ctx.lineTo(pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * k, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * k); }
          ctx.stroke();
        });
        ctx.restore();
      }
      for (var i = 0; i < nFix; i++) {
        var pt = pts[i], ap = clamp01(pFix * FIX.length - i), ease = 1 - Math.pow(1 - ap, 3), r = (7 + pt[2] / 24) * u * (.55 + .45 * ease);
        ctx.save(); ctx.globalAlpha = ease * dim;
        ctx.fillStyle = 'rgba(200,255,0,.15)'; ctx.strokeStyle = '#C8FF00'; ctx.lineWidth = Math.max(1.2, 1.8 * u);
        ctx.beginPath(); ctx.arc(pt[0], pt[1], r, 0, 6.2832); ctx.fill(); ctx.stroke();
        var fs = Math.max(10, 12 * u), bw = fs * 2.1, bh = fs * 1.5, bx = pt[0] + r * .7, by = pt[1] - r - bh;
        ctx.fillStyle = '#0A0B0D'; ctx.fillRect(bx, by, bw, bh);
        ctx.fillStyle = '#C8FF00'; ctx.font = '500 ' + fs + 'px "IBM Plex Mono", monospace'; ctx.textBaseline = 'middle';
        ctx.fillText(('0' + (i + 1)).slice(-2), bx + fs * .3, by + bh / 2 + 1);
        ctx.restore();
      }
      // Zonas ciegas (elementos que casi nadie miró en la demostración)
      if (pBlind > 0) ['side', 'fine', 'tear'].forEach(function (b, j) {
        var a = clamp01(pBlind * 3 - j); if (!a) return;
        var poly = SEQ.blind[b][f].map(function (q) { return [ox + q[0] * dw, oy + q[1] * dh]; });
        var bb = poly.reduce(function (m, q) { return [Math.min(m[0], q[0]), Math.min(m[1], q[1]), Math.max(m[2], q[0]), Math.max(m[3], q[1])]; }, [1e9, 1e9, -1e9, -1e9]);
        ctx.save(); ctx.globalAlpha = a;
        ctx.beginPath(); poly.forEach(function (q, k) { k ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); }); ctx.closePath();
        ctx.fillStyle = 'rgba(10,11,13,.55)'; ctx.fill();
        ctx.save(); ctx.clip(); ctx.strokeStyle = 'rgba(242,243,240,.45)'; ctx.lineWidth = 1.2;
        for (var x = bb[0] - (bb[3] - bb[1]); x < bb[2]; x += 7) { ctx.beginPath(); ctx.moveTo(x, bb[3]); ctx.lineTo(x + (bb[3] - bb[1]), bb[1]); ctx.stroke(); }
        ctx.restore();
        ctx.setLineDash([6, 4]); ctx.strokeStyle = '#F2F3F0'; ctx.lineWidth = 1.2; ctx.stroke(); ctx.setLineDash([]);
        var lw = 92, lx = b === 'side' ? bb[0] - lw - 6 : bb[2] + 8, ly = b === 'side' ? bb[1] + 4 : bb[1] - 4;
        lx = Math.max(6, Math.min(W - lw - 6, lx)); ly = Math.max(28, ly);
        ctx.fillStyle = '#F2F3F0'; ctx.fillRect(lx, ly, lw, 18);
        ctx.fillStyle = '#0A0B0D'; ctx.font = '500 10.5px "IBM Plex Mono", monospace'; ctx.textBaseline = 'middle'; ctx.fillText('ZONA CIEGA', lx + 7, ly + 9.5);
        ctx.restore();
      });

      drawGSR(p);
      // HUD e indicadores de fase
      hudF.textContent = ('00' + (f + 1)).slice(-3); hudX.textContent = nFix;
      phaseBars.forEach(function (b, k) { b.style.setProperty('--f', clamp01((p - CUT[k]) / (CUT[k + 1] - CUT[k])).toFixed(3)); });
      phN.textContent = '0' + (phase + 1);
      if (typeTarget !== PH[phase]) { typeTarget = PH[phase]; typed = ''; typeT = 0; }
    };

    // Typewriter corto para el nombre de la fase (solo una palabra o dos)
    var typeStep = function (now) {
      if (typed === typeTarget) return false;
      if (RM) { typed = typeTarget; phL.textContent = typed; return false; }
      if (now - typeT > 28) { typed = typeTarget.slice(0, typed.length + 1); phL.textContent = typed; typeT = now; }
      return true;
    };

    var raf = 0;
    var loop = function (now) {
      raf = 0;
      var d = target - shown;
      shown = Math.abs(d) < .0004 ? target : shown + d * .18;   // suavizado tipo "scrub"
      var f = Math.round(shown * (N - 1));
      if (dirty || f !== lastF || Math.abs(d) > .0001) { draw(); lastF = f; dirty = false; }
      var typing = typeStep(now || 0);
      if (shown !== target || typing) raf = requestAnimationFrame(loop);
    };
    var kick = function () { if (!raf) raf = requestAnimationFrame(loop); };

    if (!RM) tasks.push(function (y, vh) {
      var r = demo.getBoundingClientRect(), total = r.height - vh;
      if (r.bottom < -vh || r.top > vh * 2) return;           // fuera de rango: no hace nada
      var p = clamp01(-r.top / total);
      if (p !== target) { target = p; kick(); }
    });
    if ('ResizeObserver' in window) new ResizeObserver(function () { fit(); kick(); }).observe(cv); else addEventListener('resize', function () { fit(); kick(); });
    fit(); if (RM) startLoad(); kick();
  })();

  /* ---------- 7 · Caso ilustrativo: escaneo + heatmap que se revela con el scroll ---------- */
  var BOX = window.NG_BOX, row = $('#case-row');
  if (BOX && row) (function () {
    var HB = {
      a: [BOX.a.logo.concat([.13, .95]), BOX.a.name.concat([.06, .25]), BOX.a.mid.concat([.08, .18])],
      b: [BOX.b.logo.concat([.17, 1]), BOX.b.leaf.concat([.09, .6]), BOX.b.brand.concat([.1, .85]), BOX.b.name.concat([.07, .45])],
      c: [BOX.c.logo.concat([.09, .42]), BOX.c.name.concat([.07, .3]), BOX.c.low.concat([.08, .15])]
    };
    var cards = $$('.pk', row);
    var paint = function () {
      cards.forEach(function (c) {
        var cvs = $('canvas', c), r = cvs.getBoundingClientRect(), d = Math.min(devicePixelRatio || 1, 2);
        cvs.width = Math.round(r.width * d); cvs.height = Math.round(r.height * d);
        var x = cvs.getContext('2d'); x.setTransform(d, 0, 0, d, 0, 0); heat(x, HB[c.getAttribute('data-v')], r.width, r.height, 1, 1);
      });
    };
    var t; if ('ResizeObserver' in window) new ResizeObserver(function () { clearTimeout(t); t = setTimeout(paint, 120); }).observe(row);
    paint();
    var set = function (p) {
      cards.forEach(function (c, i) { c.style.setProperty('--h', clamp01(p * 3.2 - i * .55).toFixed(3)); });
      cards[1].classList.toggle('win', p > .88);
    };
    if (RM) set(1);
    else tasks.push(function (y, vh) { var r = row.getBoundingClientRect(); set(clamp01((vh * .85 - r.top) / (r.height + vh * .35))); });
  })();

  frame();

  /* ---------- 8 · Formulario ---------- */
  var form = $('#form');
  if (form) (function () {
    var status = $('#form-status'), send = $('#f-send'), consent = form.elements.consentimiento;
    var rules = {
      nombre: function (v) { v = v.trim(); return !v ? 'Escribe tu nombre.' : v.length < 2 ? 'Revisa tu nombre.' : ''; },
      empresa: function (v) { return v.trim().length < 2 ? 'Escribe el nombre de tu empresa.' : ''; },
      email: function (v) { v = v.trim(); return !v ? 'Escribe tu correo.' : /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) ? '' : 'Revisa el formato del correo (ej.: nombre@empresa.cl).'; },
      tipo: function (v) { return v ? '' : 'Elige el tipo de proyecto.'; },
      mensaje: function (v) { v = v.trim(); return !v ? 'Cuéntanos qué necesitas validar.' : v.length < 20 ? 'Agrega un poco más de detalle (mínimo 20 caracteres).' : ''; }
    };
    var errId = { nombre: 'e-nom', empresa: 'e-emp', email: 'e-mail', tipo: 'e-tipo', mensaje: 'e-msg' };
    var check = function (el) {
      var m = rules[el.name](el.value);
      document.getElementById(errId[el.name]).textContent = m;
      el.setAttribute('aria-invalid', m ? 'true' : 'false');
      return !m;
    };
    Object.keys(rules).forEach(function (n) {
      var el = form.elements[n];
      el.addEventListener('blur', function () { if (el.value) check(el); });
      el.addEventListener('input', function () { if (el.getAttribute('aria-invalid') === 'true') check(el); });
      el.addEventListener('change', function () { if (el.tagName === 'SELECT') check(el); });
    });
    consent.addEventListener('change', function () { if (consent.checked) $('#e-ok').textContent = ''; });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var first = null;
      Object.keys(rules).forEach(function (n) { var el = form.elements[n]; if (!check(el) && !first) first = el; });
      if (!consent.checked) { $('#e-ok').textContent = 'Necesitamos tu autorización para contactarte.'; first = first || consent; }
      if (first) { first.focus(); status.textContent = 'Hay campos por revisar.'; return; }
      if (form.elements._honey.value) return; // bot
      var v = function (n) { return form.elements[n].value.trim(); };
      var payload = {
        _subject: 'Solicitud de diagnóstico · ' + v('nombre') + ' (' + v('empresa') + ')', _template: 'table', _captcha: 'false', _replyto: v('email'),
        Nombre: v('nombre'), Empresa: v('empresa'), Correo: v('email'), 'Tipo de proyecto': v('tipo'),
        'Qué necesita validar': v('mensaje'), 'Presupuesto aproximado': v('presupuesto') || '—', 'Autoriza contacto': 'Sí'
      };
      var ep = form.getAttribute('data-endpoint');
      send.disabled = true; send.firstChild.nodeValue = 'Enviando… ';
      (ep ? fetch(ep, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(payload) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok || String(j.success) === 'false') throw new Error(j.message || r.status); }); })
        : new Promise(function (r) { setTimeout(r, 500); }))
        .then(function () {
          $$('.row2,.field,.consent,.form__foot,#e-ok', form).forEach(function (el) { el.style.display = 'none'; });
          var okEl = $('#form-ok'); okEl.classList.add('show'); okEl.focus(); status.textContent = 'Solicitud enviada.';
        })
        .catch(function () {
          send.disabled = false; send.firstChild.nodeValue = 'Solicitar diagnóstico ';
          $('#e-ok').textContent = 'No pudimos enviar la solicitud. Inténtalo de nuevo en unos minutos.';
          status.textContent = 'Error al enviar.';
        });
    });
  })();
})();
