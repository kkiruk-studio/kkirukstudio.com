/* Quote 2048 — playable landing demo (vanilla, no deps).
   Quotes/strings come from the per-locale JSON in #qdata. */
(function () {
  var dataEl = document.getElementById('qdata');
  var board = document.getElementById('pboard');
  if (!dataEl || !board) return;
  var D = JSON.parse(dataEl.textContent);      // {quotes:{"2":"...",...}, tap, hint, toast}
  var N = 4, tiles = [], nextId = 1, started = false, toastShown = false;

  var layer = document.createElement('div'); layer.className = 'tl'; board.appendChild(layer);
  var gate = document.createElement('button'); gate.className = 'gate'; gate.textContent = D.tap;
  board.appendChild(gate);
  var hint = document.getElementById('phint');

  function cellPct(i) { return 'calc(' + (i * 25) + '% + 4px)'; }
  function grade(v) { return D.quotes[String(v)] || D.quotes['2048']; }

  function spawn() {
    var empty = [];
    for (var r = 0; r < N; r++) for (var c = 0; c < N; c++)
      if (!tiles.some(function (t) { return t.r === r && t.c === c; })) empty.push([r, c]);
    if (!empty.length) return;
    var p = empty[Math.floor(Math.random() * empty.length)];
    tiles.push({ id: nextId++, r: p[0], c: p[1], v: Math.random() < 0.9 ? 2 : 4, fresh: true });
  }

  function render() {
    tiles.forEach(function (t) {
      var el = layer.querySelector('[data-id="' + t.id + '"]');
      if (!el) {
        el = document.createElement('div');
        el.className = 'ptile' + (t.fresh ? ' fresh' : '');
        el.dataset.id = t.id;
        el.innerHTML = '<span></span>';
        layer.appendChild(el);
        void el.offsetWidth;
      }
      el.classList.remove('g2','g4','g8','g16','g32','g64','g128','g256','g512','g1024','g2048');
      el.classList.add('g' + Math.min(t.v, 2048));
      if (t.v >= 2048) el.classList.add('crown');
      el.firstChild.textContent = grade(t.v);
      el.style.left = cellPct(t.c); el.style.top = cellPct(t.r);
      if (t.pop) { el.classList.remove('pop'); void el.offsetWidth; el.classList.add('pop'); t.pop = false; }
      t.fresh = false;
    });
    Array.prototype.slice.call(layer.children).forEach(function (el) {
      if (!tiles.some(function (t) { return String(t.id) === el.dataset.id; })) {
        el.classList.add('gone');
        setTimeout(function () { el.remove(); }, 160);
      }
    });
  }

  function move(dr, dc) {
    var moved = false;
    var order = tiles.slice().sort(function (a, b) {
      return (b.r * dr + b.c * dc) - (a.r * dr + a.c * dc);
    });
    var mergedIds = {};
    order.forEach(function (t) {
      var r = t.r, c = t.c;
      while (true) {
        var nr = r + dr, nc = c + dc;
        if (nr < 0 || nr >= N || nc < 0 || nc >= N) break;
        var hit = tiles.find(function (o) { return o !== t && o.r === nr && o.c === nc; });
        if (!hit) { r = nr; c = nc; continue; }
        if (hit.v === t.v && !mergedIds[hit.id] && !mergedIds[t.id]) {
          hit.v *= 2; hit.pop = true; mergedIds[hit.id] = true;
          tiles.splice(tiles.indexOf(t), 1);
          t.r = nr; t.c = nc; t.dead = true; moved = true;
          if (hit.v >= 128 && !toastShown) { toastShown = true; showToast(); }
        }
        break;
      }
      if (!t.dead && (r !== t.r || c !== t.c)) { t.r = r; t.c = c; moved = true; }
    });
    if (moved) { spawn(); render(); }
  }

  function showToast() {
    var el = document.createElement('div');
    el.className = 'ptoast'; el.textContent = D.toast;
    board.parentElement.appendChild(el);
    setTimeout(function () { el.classList.add('on'); }, 30);
    setTimeout(function () { el.classList.remove('on'); }, 6000);
    setTimeout(function () { el.remove(); }, 6600);
  }

  function start() {
    if (started) return;
    started = true;
    gate.classList.add('off');
    setTimeout(function () { gate.remove(); }, 300);
    board.classList.add('live');
    if (hint) hint.classList.add('on');
    spawn(); spawn(); render();
  }
  gate.addEventListener('click', start);

  addEventListener('keydown', function (e) {
    if (!started) return;
    var m = { ArrowUp: [-1, 0], ArrowDown: [1, 0], ArrowLeft: [0, -1], ArrowRight: [0, 1] }[e.key];
    if (!m) return;
    e.preventDefault(); move(m[0], m[1]);
  });

  var sx = 0, sy = 0;
  board.addEventListener('touchstart', function (e) {
    if (!started) return;
    sx = e.touches[0].clientX; sy = e.touches[0].clientY;
  }, { passive: true });
  board.addEventListener('touchend', function (e) {
    if (!started) return;
    var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
    if (Math.abs(dx) < 24 && Math.abs(dy) < 24) return;
    if (Math.abs(dx) > Math.abs(dy)) move(0, dx > 0 ? 1 : -1);
    else move(dy > 0 ? 1 : -1, 0);
  });

  window.__demo = { start: start, move: move, tiles: tiles };
})();
