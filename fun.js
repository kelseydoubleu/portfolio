/* kelsey wang: interactions. no build step, no dependencies except assets/matter.min.js on the home page. */
(function () {
  'use strict';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const coarse = matchMedia('(pointer: coarse)').matches;
  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  const mouse = { x: -9999, y: -9999 };
  addEventListener('pointermove', e => { mouse.x = e.clientX; mouse.y = e.clientY; }, { passive: true });
  addEventListener('pointerleave', () => { mouse.x = mouse.y = -9999; });

  /* ---------------- scatter letters ---------------- */
  const letters = [];
  function split(el) {
    const text = el.textContent; el.textContent = '';
    el.setAttribute('aria-label', text);
    text.split(/(\s+)/).forEach(part => {
      if (/^\s+$/.test(part)) { el.appendChild(document.createTextNode(' ')); return; }
      const w = document.createElement('span'); w.className = 'w'; w.setAttribute('aria-hidden', 'true');
      for (const c of part) {
        const s = document.createElement('span'); s.className = 'ch'; s.textContent = c; w.appendChild(s);
        letters.push({ el: s, host: el, ax: 0, ay: 0, x: 0, y: 0, r: 0, vx: 0, vy: 0, vr: 0, bx: 0, by: 0, size: 0 });
      }
      el.appendChild(w);
    });
  }
  $$('[data-scatter]').forEach(split);
  // (measure runs before entrance offsets are applied)
  function measure() {
    const sy = scrollY, sx = scrollX;
    for (const L of letters) {
      const r = L.el.getBoundingClientRect();
      L.bx = r.left + r.width / 2 - L.ax + sx; L.by = r.top + r.height / 2 - L.ay + sy;
      L.size = Math.max(10, r.height);
    }
  }
  measure();
  // entrance: big titles fall in from scattered positions
  if (!reduce) letters.forEach(L => { if (L.host.matches('.big, .ptitle')) { L.x = (Math.random() - .5) * 600; L.y = -300 - Math.random() * 500; L.r = (Math.random() - .5) * 180; } });
  $$('[data-explode]').forEach(h => h.addEventListener('click', () => {
    letters.forEach(L => { if (L.host === h) { L.vx += (Math.random() - .5) * 90; L.vy += (Math.random() - .8) * 90; L.vr += (Math.random() - .5) * 60; } });
  }));
  function stepLetters() {
    const sy = scrollY, sx = scrollX, vh = innerHeight;
    for (const L of letters) {
      const cx = L.bx - sx, cy = L.by - sy;
      if (cy < -400 || cy > vh + 400) continue;
      const R = L.size * 1.9;
      const dx = cx + L.x - mouse.x, dy = cy + L.y - mouse.y, d = Math.hypot(dx, dy);
      if (d < R && d > 0.1) { const f = (1 - d / R) * 3.2; L.vx += dx / d * f; L.vy += dy / d * f; L.vr += (dx > 0 ? 1 : -1) * f * .6; }
      L.vx += -L.x * .045; L.vy += -L.y * .045; L.vr += -L.r * .045;
      L.vx *= .84; L.vy *= .84; L.vr *= .84;
      L.x += L.vx; L.y += L.vy; L.r += L.vr;
      if (Math.abs(L.x) + Math.abs(L.y) + Math.abs(L.r) > .05) { L.el.style.transform = `translate(${L.x.toFixed(1)}px,${L.y.toFixed(1)}px) rotate(${L.r.toFixed(1)}deg)`; L.ax = L.x; L.ay = L.y; }
      else if (L.el.style.transform) { L.el.style.transform = ''; L.x = L.y = L.r = L.ax = L.ay = 0; }
      L.el.style.color = (Math.abs(L.x) + Math.abs(L.y) > 6 && !L.host.matches('.big,.ptitle,.logo span')) ? 'var(--o)' : '';
    }
  }

  /* ---------------- bounding-box cursor ---------------- */
  const box = document.createElement('div'); box.className = 'bbox'; box.innerHTML = '<i></i>';
  document.body.appendChild(box);
  const tagEl = box.firstChild;
  const WRONG = ['chair', 'person', 'dog', 'umbrella', 'potted plant', 'toilet', 'kite', 'bench', 'cake', 'surfboard', 'clock'];
  const hash = s => { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; };
  let target = null;
  function labelFor(el) {
    const key = (el.getAttribute('src') || el.dataset.title || el.textContent || '').slice(0, 80);
    const h = hash(key + el.tagName), conf = (0.5 + (h % 49) / 100).toFixed(2);
    if (el.dataset.title) return el.dataset.title + ' ' + conf;
    if (h % 7 === 0) return WRONG[h % WRONG.length] + ' ' + (0.12 + (h % 30) / 100).toFixed(2);
    if (el.tagName === 'IMG') return 'image ' + conf;
    if (/^H[1-3]$/.test(el.tagName)) return 'heading ' + conf;
    if (el.matches('a, button')) return 'link ' + conf;
    if (el.matches('.row')) return 'row ' + conf;
    return 'text ' + conf;
  }
  const PICK = '.card, .cube, .row, img, h1, h2, a, button, p, dd, li';
  if (!coarse) addEventListener('pointermove', e => {
    const el = document.elementFromPoint(e.clientX, e.clientY);
    const t = el && el.closest(PICK);
    if (t && t.closest('.bbox, .lb')) return;
    if (t !== target) { target = t; if (t) tagEl.textContent = labelFor(t); }
  }, { passive: true });
  function stepBox() {
    if (!target || !target.isConnected) { box.classList.remove('on'); return; }
    let r = target.getBoundingClientRect();
    if (target.classList.contains('cube')) { const top = target.querySelector('.top'); if (top) r = top.getBoundingClientRect(); }
    if (r.width > innerWidth * .96 && r.height > innerHeight * .9) { box.classList.remove('on'); return; }
    const p = 5;
    box.style.transform = `translate(${r.left - p}px,${r.top - p}px)`;
    box.style.width = (r.width + p * 2) + 'px'; box.style.height = (r.height + p * 2) + 'px';
    box.classList.toggle('below', r.top < 40);
    box.classList.add('on');
  }

  /* ---------------- figures reveal + lightbox ---------------- */
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px' });
  $$('figure').forEach(f => { f.style.setProperty('--rot', ((Math.random() - .5) * 8).toFixed(1) + 'deg'); io.observe(f); });
  const lb = $('#lb');
  if (lb) {
    const li = lb.querySelector('img');
    $$('figure img, .hero-img img').forEach(i => i.addEventListener('click', () => { li.src = i.src; lb.hidden = false; }));
    lb.addEventListener('click', () => lb.hidden = true);
    addEventListener('keydown', e => { if (e.key === 'Escape') lb.hidden = true; });
  }

  /* ---------------- home ---------------- */
  const W = window.WORKS;
  let pileStep = null, axonPar = null;
  if (W) {
    const views = { pile: $('#pile'), axon: $('#axon'), index: $('#index') };
    const hints = { pile: coarse ? 'tap to open' : 'drag, throw, click to open, click the white to drop things', axon: 'drag the blocks around, click to enter', index: 'all of it, in order' };
    let mode = 'pile';
    try { mode = sessionStorage.getItem('kw-mode') || (reduce ? 'index' : 'pile'); } catch (e) {}
    function setMode(m) {
      mode = m;
      document.body.classList.remove('m-pile', 'm-axon', 'm-index'); document.body.classList.add('m-' + m);
      $$('.modes button').forEach(b => b.classList.toggle('on', b.dataset.mode === m));
      Object.entries(views).forEach(([k, v]) => v.classList.toggle('on', k === m));
      $('#hint').textContent = hints[m];
      try { sessionStorage.setItem('kw-mode', m); } catch (e) {}
      if (m === 'pile') startPile();
      if (m === 'axon') buildAxon();
    }
    $$('.modes button').forEach(b => b.addEventListener('click', () => setMode(b.dataset.mode)));

    /* ----- pile (matter.js) ----- */
    let pileStarted = false;
    function startPile() {
      if (pileStarted || !window.Matter || reduce) return; pileStarted = true;
      const { Engine, Bodies, Body, Composite, Mouse, MouseConstraint, Events } = Matter;
      const el = views.pile;
      const engine = Engine.create(); engine.gravity.y = 1.1;
      let Wd = el.clientWidth, Hd = el.clientHeight;
      const walls = [];
      function makeWalls() {
        walls.forEach(w => Composite.remove(engine.world, w)); walls.length = 0;
        const t = 200;
        walls.push(Bodies.rectangle(Wd / 2, Hd + t / 2, Wd * 3, t, { isStatic: true }));
        walls.push(Bodies.rectangle(-t / 2, Hd / 2 - 1000, t, Hd * 4, { isStatic: true }));
        walls.push(Bodies.rectangle(Wd + t / 2, Hd / 2 - 1000, t, Hd * 4, { isStatic: true }));
        Composite.add(engine.world, walls);
      }
      makeWalls();
      const items = [];
      const scale = Math.max(.36, Math.min(1, Math.sqrt(Wd * Hd / (1300 * 820))) * .7);
      function add(node, w, h, opts, delay) {
        node.style.width = w + 'px'; node.style.height = h + 'px';
        node.style.transform = `translate(-999px,-999px)`;
        el.appendChild(node);
        setTimeout(() => {
          const b = Bodies.rectangle(80 + Math.random() * (Wd - 160), -h - Math.random() * 300, w, h, Object.assign({ restitution: .25, friction: .6, frictionAir: .012, angle: (Math.random() - .5) * .8, chamfer: { radius: 2 } }, opts));
          Body.setAngularVelocity(b, (Math.random() - .5) * .08);
          Composite.add(engine.world, b); items.push({ b, node, w, h });
        }, delay);
      }
      W.forEach((it, i) => {
        const d = document.createElement('a'); d.className = 'card'; d.href = it.href; if (it.ext) { d.target = '_blank'; d.rel = 'noopener'; }
        d.dataset.title = it.title.toLowerCase();
        d.draggable = false;
        const [iw, ih] = it.size; const ar = ih / iw;
        let w = (it.section === 'studio' ? 230 + (i % 3) * 45 : 170 + (i % 2) * 30) * scale;
        let h = w * ar; if (h > 330 * scale) { h = 330 * scale; w = h / ar; }
        d.innerHTML = it.cover ? `<img src="img/${it.cover}.jpg" alt="${it.title}" draggable="false">` : `<span>${it.title.toLowerCase()}</span>`;
        if (!it.cover) { d.classList.add('note', 'sq'); w = 200 * scale; h = 120 * scale; }
        add(d, Math.round(w), Math.round(h), {}, 250 + i * 160);
      });
      ['studio', 'research', 'games + tools', 'drag me', 'hi :)'].forEach((t, i) => {
        const d = document.createElement('div'); d.className = 'card note'; d.textContent = t; d.dataset.title = 'note ' + (0.4 + i / 10).toFixed(2);
        const w = Math.max(90, t.length * 10 + 40) * scale;
        add(d, Math.round(w), Math.round(34 * Math.max(scale, .8)), { chamfer: { radius: 16 } }, 400 + i * 450);
      });
      // drag + throw
      const m = Mouse.create(el);
      m.element.removeEventListener('mousewheel', m.mousewheel); m.element.removeEventListener('DOMMouseScroll', m.mousewheel); m.element.removeEventListener('wheel', m.mousewheel);
      if (coarse) { m.element.removeEventListener('touchmove', m.mousemove); m.element.removeEventListener('touchstart', m.mousedown); m.element.removeEventListener('touchend', m.mouseup); }
      const mc = MouseConstraint.create(engine, { mouse: m, constraint: { stiffness: .2, render: { visible: false } } });
      Composite.add(engine.world, mc);
      let down = null;
      Events.on(mc, 'startdrag', e => { const it = items.find(x => x.b === e.body); if (it) it.node.classList.add('grab'); });
      Events.on(mc, 'enddrag', e => { const it = items.find(x => x.b === e.body); if (it) it.node.classList.remove('grab'); });
      el.addEventListener('pointerdown', e => { down = { x: e.clientX, y: e.clientY, t: Date.now() }; });
      el.addEventListener('click', e => {
        const moved = down && (Math.hypot(e.clientX - down.x, e.clientY - down.y) > 6 || Date.now() - down.t > 350);
        const card = e.target.closest('a.card');
        if (card) { if (moved && !coarse) e.preventDefault(); return; }
        if (!moved && !coarse) { // drop a little orange thing where you clicked
          const r = el.getBoundingClientRect();
          const s = 18 + Math.random() * 26, d = document.createElement('div');
          d.className = 'card note sq'; d.style.borderRadius = Math.random() < .5 ? '50%' : '0'; d.style.padding = '0';
          el.appendChild(d); d.style.width = d.style.height = s + 'px';
          const b = (d.style.borderRadius === '50%' ? Bodies.circle(e.clientX - r.left, e.clientY - r.top, s / 2, { restitution: .6 }) : Bodies.rectangle(e.clientX - r.left, e.clientY - r.top, s, s, { restitution: .5 }));
          Composite.add(engine.world, b); items.push({ b, node: d, w: s, h: s });
          if (items.length > 90) { const old = items.find(x => x.node.classList.contains('sq') && !x.node.textContent); if (old) { Composite.remove(engine.world, old.b); old.node.remove(); items.splice(items.indexOf(old), 1); } }
        }
      });
      addEventListener('resize', () => { Wd = el.clientWidth; Hd = el.clientHeight; makeWalls(); });
      let last = performance.now();
      pileStep = now => {
        if (!views.pile.classList.contains('on')) { last = now; return; }
        Engine.update(engine, Math.min(32, now - last)); last = now;
        for (const it of items) {
          const { x, y } = it.b.position;
          if (y > Hd + 400) { Body.setPosition(it.b, { x: Wd / 2, y: -200 }); Body.setVelocity(it.b, { x: 0, y: 0 }); }
          it.node.style.transform = `translate(${(x - it.w / 2).toFixed(1)}px,${(y - it.h / 2).toFixed(1)}px) rotate(${it.b.angle.toFixed(3)}rad)`;
        }
      };
    }

    /* ----- axon: floating isometric blocks (2d affine faces, js-driven drift) ----- */
    let axonBuilt = false;
    function buildAxon() {
      if (axonBuilt) return; axonBuilt = true;
      const iso = $('#iso'), stage = views.axon;
      const C = Math.cos(Math.PI / 6), Sn = Math.sin(Math.PI / 6);
      const P = (x, y, z) => [(x - y) * C, (x + y) * Sn - z];
      const toWorld = (sx, sy) => [(sx / C + sy / Sn) / 2, (sy / Sn - sx / C) / 2];
      const bg = n => n ? `url(img/${n}.jpg)` : 'none';
      let SW = stage.clientWidth, SH = stage.clientHeight;
      const k = Math.max(.55, Math.min(1, Math.sqrt(SW * SH / (1400 * 800))));
      const rnd = (a, b) => a + Math.random() * (b - a);
      const blocks = [];
      W.forEach((it, i) => {
        const S = Math.round(rnd(70, 150) * k), h = Math.round(rnd(.25, 1.5) * S);
        const c = document.createElement('a'); c.className = 'cube'; c.href = it.href; if (it.ext) { c.target = '_blank'; c.rel = 'noopener'; }
        c.dataset.title = it.title.toLowerCase(); c.draggable = false;
        const imgs = it.imgs.length ? it.imgs : [null];
        const top = P(0, 0, h), south = P(0, S, h), east = P(S, 0, h);
        c.innerHTML = `<div class="lift">` +
          `<div class="f s" style="width:${S}px;height:${h}px;transform:matrix(${C},${Sn},0,1,${south[0]},${south[1]});background-image:${bg(imgs[1 % imgs.length])}"></div>` +
          `<div class="f e" style="width:${S}px;height:${h}px;transform:matrix(${-C},${Sn},0,1,${east[0]},${east[1]})"><div style="position:absolute;inset:0;background-image:${bg(imgs[2 % imgs.length])};background-size:cover;background-position:center;transform:scaleX(-1)"></div></div>` +
          `<div class="f top" style="width:${S}px;height:${S}px;transform:matrix(${C},${Sn},${-C},${Sn},${top[0]},${top[1]});background-image:${bg(imgs[0])}${it.cover ? '' : ';background-color:var(--o)'}"></div></div>`;
        iso.appendChild(c);
        blocks.push({ c, S, h, x: 0, y: 0, vx: 0, vy: 0, ph: Math.random() * 6.28, sp: rnd(.5, 1.1), amp: rnd(6, 18), drag: false });
      });
      // scatter in screen space with rejection sampling, then convert to world coords
      const margin = 60 * k, topPad = 90;
      blocks.forEach((b, i) => {
        let best = null, bestD = -1;
        for (let t = 0; t < 40; t++) {
          const sx = rnd(margin + b.S * C, SW - margin - b.S * C), sy = rnd(topPad + b.h + b.S * .5, SH - margin - b.S * Sn);
          let d = Infinity; blocks.slice(0, i).forEach(o => { const p = P(o.x + o.S / 2, o.y + o.S / 2, 0); d = Math.min(d, Math.hypot(p[0] - sx, p[1] - sy) - (o.S + b.S) * .6); });
          if (d > bestD) { bestD = d; best = [sx, sy]; }
        }
        const w = toWorld(best[0], best[1]); b.x = w[0] - b.S / 2; b.y = w[1] - b.S / 2;
        const ang = Math.random() * 6.28; b.vx = Math.cos(ang) * rnd(4, 10); b.vy = Math.sin(ang) * rnd(4, 10);
      });
      // drag in the ground plane; click without moving opens
      let dragB = null, start = null;
      blocks.forEach(b => {
        b.c.addEventListener('pointerdown', e => { dragB = b; b.drag = true; start = { x: e.clientX, y: e.clientY, bx: b.x, by: b.y, moved: false }; b.c.setPointerCapture(e.pointerId); e.preventDefault(); });
        b.c.addEventListener('pointermove', e => {
          if (dragB !== b) return;
          const dx = e.clientX - start.x, dy = e.clientY - start.y;
          if (Math.hypot(dx, dy) > 5) start.moved = true;
          const w = toWorld(dx, dy); b.x = start.bx + w[0]; b.y = start.by + w[1];
        });
        b.c.addEventListener('pointerup', () => { if (dragB === b) { b.drag = false; dragB = null; } });
        b.c.addEventListener('click', e => { if (start && start.moved) e.preventDefault(); });
      });
      addEventListener('resize', () => { SW = stage.clientWidth; SH = stage.clientHeight; });
      let last = performance.now();
      axonPar = now => {
        if (!stage.classList.contains('on')) { last = now; return; }
        const dt = Math.min(.05, (now - last) / 1000); last = now; const t = now / 1000;
        for (const b of blocks) {
          if (!b.drag) {
            // soft separation in screen space
            for (const o of blocks) if (o !== b) {
              const pb = P(b.x + b.S / 2, b.y + b.S / 2, 0), po = P(o.x + o.S / 2, o.y + o.S / 2, 0);
              const dx = pb[0] - po[0], dy = (pb[1] - b.h / 2) - (po[1] - o.h / 2), d = Math.hypot(dx, dy), min = (b.S + o.S) * .62 + (b.h + o.h) * .15;
              if (d < min && d > .1) { const w = toWorld(dx / d, dy / d); const f = (min - d) * .9; b.vx += w[0] * f * dt; b.vy += w[1] * f * dt; }
            }
            // keep on screen
            const p = P(b.x + b.S / 2, b.y + b.S / 2, 0);
            const L = margin + b.S * C, R = SW - margin - b.S * C, T = topPad + b.h + b.S * .5, B = SH - margin - b.S * Sn;
            let fx = 0, fy = 0;
            if (p[0] < L) fx = L - p[0]; if (p[0] > R) fx = R - p[0]; if (p[1] < T) fy = T - p[1]; if (p[1] > B) fy = B - p[1];
            if (fx || fy) { const w = toWorld(fx, fy); b.vx += w[0] * 2 * dt; b.vy += w[1] * 2 * dt; }
            // wander
            b.vx += Math.sin(t * .3 + b.ph) * 2 * dt; b.vy += Math.cos(t * .27 + b.ph * 1.3) * 2 * dt;
            const v = Math.hypot(b.vx, b.vy), vmax = 14; if (v > vmax) { b.vx *= vmax / v; b.vy *= vmax / v; }
            b.vx *= .995; b.vy *= .995;
            b.x += b.vx * dt; b.y += b.vy * dt;
          }
          const z = Math.sin(t * b.sp + b.ph) * b.amp + (b.drag ? 30 : 0);
          const s = P(b.x, b.y, z);
          b.c.style.transform = `translate(${s[0].toFixed(1)}px,${s[1].toFixed(1)}px)`;
          b.c.style.zIndex = Math.round(b.x + b.y + b.S) + 2000;
        }
      };
    }

    /* ----- index peek ----- */
    const peek = $('#peek');
    $$('.row').forEach(r => {
      r.addEventListener('mouseenter', () => { if (r.dataset.img) { peek.src = r.dataset.img; peek.classList.add('on'); } });
      r.addEventListener('mouseleave', () => peek.classList.remove('on'));
    });
    addEventListener('pointermove', e => { if (peek.classList.contains('on')) peek.style.transform = `translate(${e.clientX + 24}px,${e.clientY - 80}px) rotate(${((e.clientX % 40) - 20) / 10}deg)`; }, { passive: true });

    // start the pile when the stage scrolls into view
    setMode(mode);
    $$('.modes button').forEach(b => b.classList.toggle('on', b.dataset.mode === mode));
  }

  /* ---------------- loop ---------------- */
  function measureSoon() { requestAnimationFrame(measure); }
  addEventListener('resize', measureSoon);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(measureSoon);
  addEventListener('load', measureSoon);
  measure();
  function frame(now) {
    if (!reduce) stepLetters();
    if (pileStep) pileStep(now);
    if (axonPar) axonPar(now);
    if (!coarse) stepBox();
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
