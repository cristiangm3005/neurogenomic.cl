/* =========================================================
   Hélice de ADN en Three.js (se carga solo cuando la sección está cerca).
   Las partículas parten dispersas (las bacterias que se disuelven) y forman
   la doble hélice con el scroll; iones Cu²⁺ turquesa orbitan alrededor.
   ========================================================= */
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.min.js';

export function createHelix(canvas, opts) {
  const pts = opts.points;
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: false, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);
  camera.position.set(0, 0, 15);

  const n = pts.length;
  const start = new Float32Array(n * 3), end = new Float32Array(n * 3), col = new Float32Array(n * 3), size = new Float32Array(n), seed = new Float32Array(n);
  pts.forEach((p, i) => {
    start.set([p.sx, p.sy, p.sz0], i * 3); end.set([p.x, p.y, p.z], i * 3);
    col.set(p.c, i * 3); size[i] = p.sz; seed[i] = p.seed;
  });
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(end, 3));
  geo.setAttribute('aStart', new THREE.BufferAttribute(start, 3));
  geo.setAttribute('aColor', new THREE.BufferAttribute(col, 3));
  geo.setAttribute('aSize', new THREE.BufferAttribute(size, 1));
  geo.setAttribute('aSeed', new THREE.BufferAttribute(seed, 1));

  const uniforms = { uP: { value: 0 }, uTime: { value: 0 }, uPix: { value: renderer.getPixelRatio() } };
  const mat = new THREE.ShaderMaterial({
    uniforms, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    vertexShader: `
      attribute vec3 aStart; attribute vec3 aColor; attribute float aSize; attribute float aSeed;
      uniform float uP; uniform float uTime; uniform float uPix;
      varying vec3 vColor; varying float vA;
      void main(){
        float k = clamp(uP * 1.3 - aSeed * 0.3, 0.0, 1.0); k = k * k * (3.0 - 2.0 * k);
        vec3 drift = vec3(sin(uTime * 0.7 + aSeed * 40.0), cos(uTime * 0.5 + aSeed * 30.0), sin(uTime * 0.6 + aSeed * 20.0)) * 0.35 * (1.0 - k);
        vec3 pos = mix(aStart, position, k) + drift;
        vec4 mv = modelViewMatrix * vec4(pos, 1.0);
        gl_Position = projectionMatrix * mv;
        gl_PointSize = aSize * uPix * 7.0 * (15.0 / -mv.z);
        vColor = aColor; vA = 0.45 + 0.55 * k;
      }`,
    fragmentShader: `
      varying vec3 vColor; varying float vA;
      void main(){
        float d = length(gl_PointCoord - 0.5);
        float a = smoothstep(0.5, 0.0, d);
        gl_FragColor = vec4(vColor * (0.6 + 0.6 * a), a * vA);
      }`
  });
  const group = new THREE.Group();
  group.rotation.x = 0.32; group.rotation.z = -0.18;
  group.add(new THREE.Points(geo, mat));

  // Iones Cu²⁺ orbitando
  const ionN = opts.desk ? 36 : 20, ionPos = new Float32Array(ionN * 3), ions = [];
  for (let i = 0; i < ionN; i++) ions.push({ a: Math.random() * Math.PI * 2, y: Math.random() * 10 - 5, r: 2.5 + Math.random() * 1.1, s: 0.3 + Math.random() * 0.5 });
  const ionGeo = new THREE.BufferGeometry(); ionGeo.setAttribute('position', new THREE.BufferAttribute(ionPos, 3));
  const ionMat = new THREE.PointsMaterial({ color: 0x5cc0b0, size: 0.32, transparent: true, opacity: 0.85, depthWrite: false, blending: THREE.AdditiveBlending, map: dot(), alphaTest: 0.01 });
  group.add(new THREE.Points(ionGeo, ionMat));
  scene.add(group);

  function dot() {
    const c = document.createElement('canvas'); c.width = c.height = 64; const x = c.getContext('2d');
    const g = x.createRadialGradient(32, 32, 0, 32, 32, 32); g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(0.35, 'rgba(255,255,255,.6)'); g.addColorStop(1, 'rgba(255,255,255,0)');
    x.fillStyle = g; x.fillRect(0, 0, 64, 64); const t = new THREE.CanvasTexture(c); return t;
  }
  function resize() {
    const r = canvas.getBoundingClientRect(); if (!r.width) return;
    renderer.setSize(r.width, r.height, false); camera.aspect = r.width / r.height; camera.updateProjectionMatrix();
    camera.position.z = r.width / r.height < 0.8 ? 19 : 15;
  }
  new ResizeObserver(resize).observe(canvas); resize();

  let run = false, raf = 0; const clock = new THREE.Clock();
  function frame() {
    const t = clock.getElapsedTime(), p = opts.getP();
    uniforms.uP.value = Math.min(1, p * 2.2); uniforms.uTime.value = t;
    group.rotation.y = p * Math.PI * 4 + t * 0.12;
    const form = uniforms.uP.value;
    ions.forEach((o, i) => { o.a += 0.01 * o.s; ionPos[i * 3] = Math.cos(o.a) * o.r; ionPos[i * 3 + 1] = o.y + Math.sin(t + i) * 0.15; ionPos[i * 3 + 2] = Math.sin(o.a) * o.r; });
    ionGeo.attributes.position.needsUpdate = true; ionMat.opacity = 0.15 + 0.7 * form;
    renderer.render(scene, camera);
    if (run) raf = requestAnimationFrame(frame);
  }
  return {
    setProgress() {},
    start() { if (run) return; run = true; raf = requestAnimationFrame(frame); },
    stop() { run = false; cancelAnimationFrame(raf); }
  };
}
