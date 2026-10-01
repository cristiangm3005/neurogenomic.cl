/* ==========================================================
   NEUROGENOMIC · Núcleo JS compartido (window.NG)
   Idempotente: puede venir repetido en varios bloques Elementor.
   Carga GSAP + ScrollTrigger (cdnjs) y Lenis (jsDelivr) una sola vez.
   ========================================================== */
(function () {
  if (window.NG) return;
  var NG = (window.NG = {});
  var d = document, de = d.documentElement;
  de.classList.add('ng-js');

  var mq = function (q) { return window.matchMedia ? window.matchMedia(q).matches : false; };
  NG.rm = mq('(prefers-reduced-motion: reduce)');
  NG.fine = mq('(hover: hover) and (pointer: fine)');
  NG.edit = function () { return d.body && d.body.classList.contains('elementor-editor-active'); };
  NG.lerp = function (a, b, t) { return a + (b - a) * t; };
  NG.clamp = function (v, a, b) { return Math.min(b, Math.max(a, v)); };

  var CDN = {
    gsap: 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js',
    st: 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js',
    lenis: 'https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js'
  };
  function load(src) {
    return new Promise(function (res, rej) {
      var ex = d.querySelector('script[src="' + src + '"]');
      if (ex) {
        if (ex.getAttribute('data-ng-loaded')) return res();
        ex.addEventListener('load', function () { res(); });
        ex.addEventListener('error', rej);
        return;
      }
      var s = d.createElement('script');
      s.src = src; s.async = true; s.crossOrigin = 'anonymous';
      s.onload = function () { s.setAttribute('data-ng-loaded', '1'); res(); };
      s.onerror = rej;
      d.head.appendChild(s);
    });
  }

  /* --- Carga de librerías + Lenis ------------------------------------ */
  var readyP = null;
  NG.ready = function () {
    if (readyP) return readyP;
    readyP = (window.gsap ? Promise.resolve() : load(CDN.gsap))
      .then(function () { return window.ScrollTrigger ? null : load(CDN.st); })
      .then(function () {
        gsap.registerPlugin(ScrollTrigger);
        gsap.defaults({ ease: 'power3.out', duration: 0.9 });
        if (NG.rm || NG.edit()) return;
        return (window.Lenis ? Promise.resolve() : load(CDN.lenis)).then(initLenis, function () {});
      })
      .then(function () { return window.gsap; })
      .catch(function () { de.classList.add('ng-nolib'); return null; });
    return readyP;
  };
  function initLenis() {
    if (NG.lenis || !window.Lenis) return;
    var lenis = (NG.lenis = new Lenis({ duration: 1.15, easing: function (t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); }, smoothWheel: true }));
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
  }
  NG.scrollTo = function (target) {
    var el = typeof target === 'string' ? d.querySelector(target) : target;
    if (!el) return;
    if (NG.lenis) NG.lenis.scrollTo(el, { offset: 0, duration: 1.4 });
    else el.scrollIntoView({ behavior: NG.rm ? 'auto' : 'smooth' });
  };

  /* --- Arranque con guardas data-init y múltiples entradas ----------- */
  NG.boot = function (selector, init) {
    var run = function () {
      var els = d.querySelectorAll(selector);
      for (var i = 0; i < els.length; i++) {
        var el = els[i];
        if (el.getAttribute('data-init')) continue;
        el.setAttribute('data-init', '1');
        try { init(el); } catch (e) { if (window.console) console.error('[NG]', selector, e); }
      }
    };
    if (d.readyState !== 'loading') run(); else d.addEventListener('DOMContentLoaded', run);
    window.addEventListener('load', run);
    var hook = function () {
      if (window.elementorFrontend && elementorFrontend.hooks) elementorFrontend.hooks.addAction('frontend/element_ready/global', run);
    };
    if (window.elementorFrontend && window.elementorFrontend.hooks) hook();
    else window.addEventListener('elementor/frontend/init', hook);
  };

  /* --- Preloader → secciones esperan este evento --------------------- */
  NG.afterPreload = function (cb) {
    if (!de.classList.contains('ng-pre-on') || de.classList.contains('ng-pre-done')) return cb();
    window.addEventListener('ng:preloaded', function f() { window.removeEventListener('ng:preloaded', f); cb(); });
  };

  /* --- Split de texto accesible (copia sr + spans aria-hidden) ------- */
  NG.split = function (el, mode) {
    if (el._ngSplit) return el._ngSplit;
    var text = el.textContent.replace(/\s+/g, ' ').trim();
    var out = [];
    el.setAttribute('aria-label', text);
    var frag = d.createDocumentFragment();
    var sr = d.createElement('span'); sr.className = 'ng-sr'; sr.textContent = text; frag.appendChild(sr);
    var vis = d.createElement('span'); vis.setAttribute('aria-hidden', 'true');
    // conserva <br> y <em> simples: trabajamos sobre los nodos hijos
    var walk = function (node, parent) {
      [].slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var parts = n.textContent.split(/(\s+)/);
          parts.forEach(function (p) {
            if (!p) return;
            if (/^\s+$/.test(p)) { parent.appendChild(d.createTextNode(' ')); return; }
            if (mode === 'chars') {
              var w = d.createElement('span'); w.style.display = 'inline-block'; w.style.whiteSpace = 'nowrap';
              p.split('').forEach(function (c) { var s = d.createElement('span'); s.textContent = c; s.style.display = 'inline-block'; w.appendChild(s); out.push(s); });
              parent.appendChild(w);
            } else {
              var m = d.createElement('span'); m.className = 'ng-w';
              var i = d.createElement('span'); i.textContent = p; m.appendChild(i); parent.appendChild(m); out.push(i);
            }
          });
        } else if (n.nodeType === 1) {
          if (n.tagName === 'BR') { parent.appendChild(d.createElement('br')); return; }
          var c = n.cloneNode(false); c.removeAttribute('id'); parent.appendChild(c); walk(n, c);
        }
      });
    };
    walk(el, vis);
    frag.appendChild(vis);
    el.textContent = ''; el.appendChild(frag);
    el.removeAttribute('aria-label');
    el._ngSplit = out;
    return out;
  };

  /* --- Visibilidad + bucles rAF que se pausan fuera de viewport ------ */
  NG.vis = function (el, onIn, onOut, margin) {
    if (!('IntersectionObserver' in window)) { onIn && onIn(); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) onIn && onIn(e); else onOut && onOut(e); });
    }, { rootMargin: margin || '0px' });
    io.observe(el);
    return io;
  };
  NG.loop = function (el, fn) {
    var on = false, raf = 0, last = 0, docVis = !d.hidden;
    var tick = function (t) {
      raf = 0;
      if (!on || !docVis) return;
      var dt = last ? Math.min(64, t - last) : 16; last = t;
      fn(t, dt);
      raf = requestAnimationFrame(tick);
    };
    var start = function () { if (!raf && on && docVis) { last = 0; raf = requestAnimationFrame(tick); } };
    NG.vis(el, function () { on = true; start(); }, function () { on = false; }, '80px');
    d.addEventListener('visibilitychange', function () { docVis = !d.hidden; start(); });
    return { kick: start };
  };

  /* --- Canvas con DPR y ResizeObserver ------------------------------ */
  NG.canvas = function (cv, onResize) {
    var ctx = cv.getContext('2d');
    var o = { cv: cv, ctx: ctx, w: 0, h: 0, dpr: 1 };
    var fit = function () {
      var r = cv.getBoundingClientRect();
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = Math.max(1, Math.round(r.width)), h = Math.max(1, Math.round(r.height));
      if (w === o.w && h === o.h && dpr === o.dpr) return;
      o.w = w; o.h = h; o.dpr = dpr;
      cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      onResize && onResize(o);
    };
    fit();
    if ('ResizeObserver' in window) new ResizeObserver(fit).observe(cv); else window.addEventListener('resize', fit);
    return o;
  };

  /* --- Heatmap monocromático dentro de la paleta (volt → lima → blanco) */
  NG.heat = function (cv, pts, opts) {
    opts = opts || {};
    var r = cv.getBoundingClientRect();
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var W = Math.max(1, Math.round(r.width * dpr)), H = Math.max(1, Math.round(r.height * dpr));
    cv.width = W; cv.height = H;
    var ctx = cv.getContext('2d', { willReadFrequently: true });
    var base = Math.min(W, H);
    ctx.clearRect(0, 0, W, H);
    pts.forEach(function (p) {
      var rad = (p[2] || 0.12) * base, x = p[0] * W, y = p[1] * H, w = p[3] == null ? 1 : p[3];
      var g = ctx.createRadialGradient(x, y, 0, x, y, rad);
      g.addColorStop(0, 'rgba(0,0,0,' + 0.55 * w + ')'); g.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = g; ctx.fillRect(x - rad, y - rad, rad * 2, rad * 2);
    });
    var img = ctx.getImageData(0, 0, W, H), px = img.data;
    var ramp = [[0, [200, 245, 66, 0]], [0.18, [200, 245, 66, 70]], [0.55, [200, 255, 0, 170]], [1, [242, 243, 240, 225]]];
    for (var i = 0; i < px.length; i += 4) {
      var a = px[i + 3] / 255; if (!a) continue;
      a = Math.min(1, a * (opts.gain || 1.25));
      for (var k = 1; k < ramp.length; k++) {
        if (a <= ramp[k][0]) {
          var lo = ramp[k - 1], hi = ramp[k], t = (a - lo[0]) / (hi[0] - lo[0]);
          px[i] = lo[1][0] + (hi[1][0] - lo[1][0]) * t; px[i + 1] = lo[1][1] + (hi[1][1] - lo[1][1]) * t;
          px[i + 2] = lo[1][2] + (hi[1][2] - lo[1][2]) * t; px[i + 3] = lo[1][3] + (hi[1][3] - lo[1][3]) * t;
          break;
        }
      }
    }
    ctx.putImageData(img, 0, 0);
  };

  /* --- Contador ----------------------------------------------------- */
  NG.count = function (el, to, o) {
    o = o || {};
    var dec = o.dec || 0, fmt = function (v) { return (o.pre || '') + v.toFixed(dec) + (o.suf || ''); };
    if (NG.rm || !window.gsap) { el.textContent = fmt(to); o.done && o.done(); return; }
    var st = { v: o.from || 0 };
    el.textContent = fmt(st.v);
    return gsap.to(st, { v: to, duration: o.dur || 1.8, ease: o.ease || 'expo.out', delay: o.delay || 0,
      onUpdate: function () { el.textContent = fmt(st.v); o.update && o.update(st.v / to); },
      onComplete: function () { el.textContent = fmt(to); o.done && o.done(); } });
  };

  /* --- Reveals genéricos dentro de una sección ----------------------- */
  NG.reveals = function (root) {
    if (!window.gsap || NG.rm) return;
    root.querySelectorAll('[data-ng-split]').forEach(function (el) {
      var w = NG.split(el);
      gsap.from(w, { yPercent: 110, duration: 1.1, ease: 'expo.out', stagger: 0.05,
        scrollTrigger: { trigger: el, start: 'top 88%', once: true } });
    });
    root.querySelectorAll('[data-ng-reveal]').forEach(function (el) {
      gsap.from(el, { autoAlpha: 0, y: 28, duration: 1, ease: 'power3.out', delay: parseFloat(el.getAttribute('data-ng-reveal')) || 0,
        scrollTrigger: { trigger: el, start: 'top 90%', once: true } });
    });
    if (root.hasAttribute('data-ng-bg')) {
      gsap.timeline({ scrollTrigger: { trigger: root, start: 'top 75%', end: 'bottom 25%', scrub: true } })
        .fromTo(root, { '--ng-bgo': 0 }, { '--ng-bgo': 1, ease: 'none', duration: 0.25 })
        .to(root, { '--ng-bgo': 1, duration: 0.5 })
        .to(root, { '--ng-bgo': 0, ease: 'none', duration: 0.25 });
    }
  };

  /* --- Botones magnéticos ------------------------------------------- */
  NG.magnet = function (el, k) {
    if (!NG.fine || NG.rm || el._ngMag) return;
    el._ngMag = 1; k = k || 0.3;
    var inner = el.querySelector('.ng-btn__t') || el;
    el.addEventListener('pointermove', function (e) {
      var r = el.getBoundingClientRect();
      var x = (e.clientX - r.left - r.width / 2) * k, y = (e.clientY - r.top - r.height / 2) * k;
      el.style.transform = 'translate(' + x + 'px,' + y + 'px)';
      if (inner !== el) inner.style.transform = 'translate(' + x * 0.35 + 'px,' + y * 0.35 + 'px)';
    });
    el.addEventListener('pointerleave', function () {
      el.style.transition = 'transform .6s cubic-bezier(.16,1,.3,1)';
      el.style.transform = ''; if (inner !== el) { inner.style.transition = el.style.transition; inner.style.transform = ''; }
      setTimeout(function () { el.style.transition = ''; inner.style.transition = ''; }, 600);
    });
  };

  /* --- Anclas internas con Lenis ------------------------------------ */
  d.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href*="#"]');
    if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey) return;
    var url = new URL(a.href, location.href);
    if (url.pathname !== location.pathname || !url.hash || url.hash.length < 2) return;
    var t = d.getElementById(decodeURIComponent(url.hash.slice(1)));
    if (!t) return;
    e.preventDefault();
    NG.scrollTo(t);
    if (t.tabIndex < 0 && !/^(A|BUTTON|INPUT|SELECT|TEXTAREA)$/.test(t.tagName)) t.setAttribute('tabindex', '-1');
    t.focus({ preventScroll: true });
    history.replaceState(null, '', url.hash);
  });
})();
