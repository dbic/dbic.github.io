/* DBIC redesign: behavior for every page that uses the "redesign" layout.
   Each feature switches itself on only if its elements are on the page.
   Content comes from the data files (_data/*.csv, *.yml), passed in as JSON blocks by the layouts. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var mqReduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  function reduced() { return mqReduce.matches; }
  var DBIC = window.DBIC || {};
  var BASE = DBIC.base || '';
  function href(u) { return (u && u.charAt(0) === '/') ? BASE + u : u; }
  function J(id) { var el = document.getElementById(id); if (!el) return null; try { return JSON.parse(el.textContent); } catch (e) { return null; } }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  function fmt(d, o) { return d.toLocaleDateString('en-US', o || { weekday: 'short', month: 'short', day: 'numeric' }); }
  function parseISO(s) { var m = s ? String(s).match(/^(\d{4})-(\d{2})-(\d{2})/) : null; return m ? new Date(+m[1], +m[2] - 1, +m[3]) : null; }
  function endOfDay(d) { return new Date(d.getFullYear(), d.getMonth(), d.getDate(), 23, 59, 59); }
  function at(d, h) { return new Date(d.getFullYear(), d.getMonth(), d.getDate(), h, 0, 0); }

  /* ---------- links to other sites (and sibling project sites) open in a new tab ---------- */
  function markExternal(scope) {
    var paths = DBIC.newTabPaths || [];
    $$('a[href]', scope).forEach(function (a) {
      if (a.getAttribute('target') || !/^https?:$/.test(a.protocol)) return;
      var other = a.hostname !== window.location.hostname || paths.some(function (p) { return a.pathname.indexOf(p) === 0; });
      if (other) { a.target = '_blank'; a.rel = 'noopener noreferrer'; }
    });
  }
  markExternal(document);

  /* ---------- color mode ---------- */
  var themeBtn = $('#theme');
  function currentTheme() {
    var t = document.documentElement.getAttribute('data-theme');
    return t || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  }
  function syncTheme() {
    var dark = currentTheme() === 'dark';
    themeBtn.setAttribute('aria-pressed', String(dark));
    themeBtn.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
    $('.ico', themeBtn).textContent = dark ? '☀' : '☾';
  }
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = currentTheme() === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      store.set('dbic-theme', next);
      syncTheme();
    });
    syncTheme();
  }

  /* ---------- header menus ---------- */
  var nav = $('#nav'), burger = $('#burger'), menus = $$('.menu');
  function closeMenus(except) {
    menus.forEach(function (m) {
      if (m !== except) { m.classList.remove('open'); $('.menu-btn', m).setAttribute('aria-expanded', 'false'); }
    });
  }
  menus.forEach(function (m) {
    var b = $('.menu-btn', m);
    b.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = !m.classList.contains('open');
      closeMenus(m);
      m.classList.toggle('open', open);
      b.setAttribute('aria-expanded', String(open));
    });
  });
  document.addEventListener('click', function (e) { if (!e.target.closest('.menu')) closeMenus(); });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var open = menus.filter(function (m) { return m.classList.contains('open'); })[0];
    if (open) { $('.menu-btn', open).focus(); closeMenus(); }
    else if (nav && nav.classList.contains('open')) { nav.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); burger.focus(); }
  });
  if (nav) {
    nav.addEventListener('focusout', function (e) { if (e.relatedTarget && !nav.contains(e.relatedTarget)) closeMenus(); });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('.menu-panel a')) { closeMenus(); nav.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); }
    });
    burger.addEventListener('click', function () {
      var o = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', String(o));
    });
  }

  /* ---------- quick find (built from the same menu data as the header and footer) ---------- */
  (function () {
    var qf = $('#qf'); if (!qf) return;
    var qfIn = $('#qf-input'), qfList = $('#qf-list'), active = 0, QF = [];
    (J('menu-data') || []).forEach(function (g) {
      (g.items || []).forEach(function (it) { QF.push({ t: it.title, u: it.url, g: g.title, k: it.keywords || '', p: it.popular ? 1 : 0 }); });
    });
    function render() {
      var tokens = qfIn.value.toLowerCase().split(/\s+/).filter(Boolean), rows;
      if (!tokens.length) rows = QF.filter(function (x) { return x.p; });
      else rows = QF.map(function (x, i) {
        var t = x.t.toLowerCase(), k = String(x.k).toLowerCase(), g = x.g.toLowerCase(), s = 0;
        for (var j = 0; j < tokens.length; j++) {
          var w = tokens[j], hit = 0;
          if (t.indexOf(w) === 0) hit = 5; else if (t.indexOf(w) > -1) hit = 3; else if (k.indexOf(w) > -1) hit = 2; else if (g.indexOf(w) > -1) hit = 1;
          if (!hit) return null;
          s += hit;
        }
        return { x: x, s: s, i: i };
      }).filter(Boolean).sort(function (a, b) { return b.s - a.s || a.i - b.i; }).map(function (r) { return r.x; });
      active = 0;
      qfList.innerHTML = rows.length ? rows.map(function (x, i) {
        return '<li><a href="' + esc(href(x.u)) + '"' + (i === 0 ? ' class="on"' : '') + '><span>' + esc(x.t) + '</span><small>' + esc(x.g) + '</small></a></li>';
      }).join('') : '<li><a href="mailto:courtney.rogers@dartmouth.edu?subject=DBIC%20question"><span>No match. Ask the DBIC team</span><small>email</small></a></li>';
      markExternal(qfList);
    }
    function move(d) {
      var items = $$('a', qfList); if (!items.length) return;
      items[active].classList.remove('on');
      active = (active + d + items.length) % items.length;
      items[active].classList.add('on');
      items[active].scrollIntoView({ block: 'nearest' });
    }
    function close() { if (qf.close) qf.close(); else qf.removeAttribute('open'); }
    function open() {
      if (typeof qf.showModal === 'function') { if (!qf.open) qf.showModal(); } else qf.setAttribute('open', '');
      qfIn.value = ''; render(); qfIn.focus();
    }
    $('#qf-open').addEventListener('click', open);
    $('#qf-close').addEventListener('click', close);
    qfIn.addEventListener('input', render);
    qfIn.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.preventDefault(); close(); }
      else if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
      else if (e.key === 'Enter') { var a = $$('a', qfList)[active]; if (a) { e.preventDefault(); a.click(); } }
    });
    qfList.addEventListener('click', function (e) { if (e.target.closest('a')) close(); });
    qf.addEventListener('click', function (e) { if (e.target === qf) close(); });
    document.addEventListener('keydown', function (e) {
      var typing = /^(input|textarea|select)$/i.test(e.target.tagName) || e.target.isContentEditable;
      if ((e.key === '/' && !typing) || ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k')) { e.preventDefault(); open(); }
    });
  })();

  /* ---------- home hero: changing words + network animation ---------- */
  var rot = $('#rot');
  if (rot) {
    var words = []; try { words = JSON.parse(rot.getAttribute('data-words')) || []; } catch (e) {}
    var wi = 0;
    if (reduced() || words.length < 2) { rot.textContent = rot.getAttribute('data-static') || (words[0] || ''); }
    else {
      setInterval(function () {
        if (document.hidden) return;
        rot.classList.add('swap');
        setTimeout(function () { wi = (wi + 1) % words.length; rot.textContent = words[wi]; rot.classList.remove('swap'); }, 280);
      }, 2600);
    }
  }
  (function () {
    var cv = $('#neural'); if (!cv) return;
    var ctx = cv.getContext('2d'), w = 0, h = 0, nodes = [], raf = 0, onscreen = true, mouse = { x: -999, y: -999 };
    function size() {
      var dpr = Math.min(window.devicePixelRatio || 1, 2), r = cv.getBoundingClientRect();
      w = r.width; h = r.height; cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.round(Math.min(95, Math.max(26, w * h / 15000)));
      nodes = [];
      for (var i = 0; i < n; i++) nodes.push({ x: Math.random() * w, y: Math.random() * h, vx: (Math.random() - .5) * .28, vy: (Math.random() - .5) * .28, r: Math.random() * 1.6 + .8 });
    }
    function frame(move) {
      ctx.clearRect(0, 0, w, h);
      var L = Math.min(150, Math.max(90, w / 7)), i, j, a, b, dx, dy, d;
      for (i = 0; i < nodes.length; i++) {
        a = nodes[i];
        if (move) {
          dx = a.x - mouse.x; dy = a.y - mouse.y; d = Math.sqrt(dx * dx + dy * dy);
          if (d < 120 && d > 0) { a.x += dx / d * .9; a.y += dy / d * .9; }
          a.x += a.vx; a.y += a.vy;
          if (a.x < -10) a.x = w + 10; else if (a.x > w + 10) a.x = -10;
          if (a.y < -10) a.y = h + 10; else if (a.y > h + 10) a.y = -10;
        }
      }
      for (i = 0; i < nodes.length; i++) {
        a = nodes[i];
        for (j = i + 1; j < nodes.length; j++) {
          b = nodes[j]; dx = a.x - b.x; dy = a.y - b.y; d = Math.sqrt(dx * dx + dy * dy);
          if (d < L) { ctx.strokeStyle = 'rgba(190,255,225,' + (0.22 * (1 - d / L)).toFixed(3) + ')'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); }
        }
      }
      ctx.fillStyle = 'rgba(210,255,235,.75)';
      for (i = 0; i < nodes.length; i++) { a = nodes[i]; ctx.beginPath(); ctx.arc(a.x, a.y, a.r, 0, 6.2832); ctx.fill(); }
    }
    function loop() { frame(true); raf = onscreen && !document.hidden && !reduced() ? requestAnimationFrame(loop) : 0; }
    function start() { if (!raf && !reduced()) loop(); }
    size(); frame(false);
    window.addEventListener('resize', function () { size(); frame(false); });
    cv.parentNode.addEventListener('pointermove', function (e) { var r = cv.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; });
    cv.parentNode.addEventListener('pointerleave', function () { mouse.x = mouse.y = -999; });
    document.addEventListener('visibilitychange', start);
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { onscreen = en[0].isIntersecting; if (onscreen) start(); }).observe(cv.parentNode);
    start();
  })();

  /* ---------- events: "Coming up" tabs and the status cards (data: events.csv, scan_windows.csv) ---------- */
  var EV = J('events-data') || [], WIN = J('windows-data') || [], HOME = J('home-data') || {};
  var SCAN = 'Scan requests';
  function allEvents() {
    var out = [];
    EV.forEach(function (r) {
      var d = parseISO(r.date); if (!d) return;
      out.push({ at: d, until: endOfDay(d), label: r.date_label || '', time: r.time || '', category: r.category || '', title: r.title || '', detail: r.detail || '', deadline: parseISO(r.deadline), url: r.url || '' });
    });
    WIN.forEach(function (w) {
      var o1 = parseISO(w.tier1_open), c1 = parseISO(w.tier1_close), o2 = parseISO(w.tier2_open), c2 = parseISO(w.tier2_close), o3 = parseISO(w.tier3_open);
      function add(d, hour, text) { if (d) { var t = at(d, hour); out.push({ at: t, until: t, label: '', time: '', category: SCAN, title: text, detail: '', deadline: null, url: '', win: true }); } }
      add(o1, 0, 'Tier 1 requests open for ' + w.month);
      add(c1, 16, 'Tier 1 requests close for ' + w.month + ' at 4 p.m.');
      add(o2, 0, 'Tier 2 requests open for ' + w.month);
      add(c2, 16, 'Tier 2 requests close for ' + w.month + ' at 4 p.m.');
      add(o3, 0, 'Tier 3 (rolling, first come first served) opens for ' + w.month);
    });
    return out;
  }
  function upcoming(list, now) { return list.filter(function (e) { return e.until >= now; }).sort(function (a, b) { return a.at - b.at; }); }
  function openWindows(now) {
    var out = [];
    WIN.forEach(function (w) {
      [['Tier 1', w.tier1_open, w.tier1_close], ['Tier 2', w.tier2_open, w.tier2_close]].forEach(function (t) {
        var o = parseISO(t[1]), c = parseISO(t[2]);
        if (o && c && at(o, 0) <= now && now < at(c, 16)) out.push(t[0] + ' for ' + w.month + ' (until ' + fmt(c) + ')');
      });
    });
    return out;
  }

  var cp = $('#cp'), tabs = $$('#ev-tabs .tab');
  function renderTab(tab) {
    var cat = tab.getAttribute('data-category'), show = (HOME.events && HOME.events.show) || 4, now = new Date();
    var mine = allEvents().filter(function (e) { return e.category === cat; });
    var up = upcoming(mine, now);
    var past = mine.filter(function (e) { return e.until < now; }).sort(function (a, b) { return b.at - a.at; });
    var list = (up.length ? up : past).slice(0, show), note = '';
    if (!up.length && past.length) note = 'No upcoming dates are listed. The most recent are shown.';
    if (!list.length) note = 'Nothing is scheduled yet. Check back soon.';
    var year = now.getFullYear();
    var rows = list.map(function (e) {
      var date = e.label || fmt(e.at, e.at.getFullYear() !== year || e.until < now ? { month: 'short', day: 'numeric', year: 'numeric' } : undefined);
      var meta = [e.time, e.detail, e.deadline ? 'Register by ' + fmt(e.deadline) : ''].filter(Boolean).join(' · ');
      var title = e.url ? '<a href="' + esc(href(e.url)) + '">' + esc(e.title) + '</a>' : esc(e.title);
      return '<li><time>' + esc(date) + '</time><span>' + title + (meta ? '<small>' + esc(meta) + '</small>' : '') + '</span></li>';
    }).join('');
    var more = tab.getAttribute('data-more-url');
    cp.innerHTML = (note ? '<p class="up-note">' + esc(note) + '</p>' : '') + (rows ? '<ul class="up">' + rows + '</ul>' : '') +
      (more ? '<a class="up-more" href="' + esc(href(more)) + '">' + esc(tab.getAttribute('data-more-text') || 'More') + '</a>' : '');
    cp.setAttribute('aria-labelledby', tab.id);
    markExternal(cp);
  }
  if (cp && tabs.length) {
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () {
        tabs.forEach(function (o) { o.setAttribute('aria-selected', String(o === t)); o.tabIndex = o === t ? 0 : -1; });
        renderTab(t);
      });
      t.addEventListener('keydown', function (e) {
        var n = null;
        if (e.key === 'ArrowRight') n = (i + 1) % tabs.length; else if (e.key === 'ArrowLeft') n = (i - 1 + tabs.length) % tabs.length;
        if (n !== null) { e.preventDefault(); tabs[n].focus(); tabs[n].click(); }
      });
    });
    renderTab(tabs[0]);
  }

  $$('#status .chip-card').forEach(function (card) {
    var kind = card.getAttribute('data-kind'), label = card.getAttribute('data-label') || '', box = $('div', card), now = new Date();
    if (kind === 'next_event') {
      var cat = card.getAttribute('data-category'), next = upcoming(allEvents().filter(function (e) { return e.category === cat; }), now)[0];
      if (next) {
        var sub = next.deadline ? 'Register by ' + fmt(next.deadline) : next.detail;
        box.innerHTML = '<small>' + esc(label) + '</small><b>' + esc(fmt(next.at) + (next.time ? ', ' + next.time : '')) + '</b>' + (sub ? '<span class="s">' + esc(sub) + '</span>' : '');
      } else {
        box.innerHTML = '<small>' + esc(label) + '</small><b>See the schedule</b><span class="s">New dates are posted each term</span>';
      }
    } else if (kind === 'scan_windows') {
      var open = openWindows(now), nxt = upcoming(allEvents().filter(function (e) { return e.win; }), now).filter(function (e) { return /open/.test(e.title); })[0];
      if (open.length) box.innerHTML = '<small>' + esc(label + ' · open now') + '</small><b>' + esc(open[0]) + '</b>' + (open[1] ? '<span class="s">Also: ' + esc(open[1]) + '</span>' : '<span class="s">Email Courtney Rogers to request time</span>');
      else if (nxt) box.innerHTML = '<small>Next scan-request window</small><b>' + esc(fmt(nxt.at)) + '</b><span class="s">' + esc(nxt.title) + '</span>';
      else box.innerHTML = '<small>' + esc(label) + '</small><b>See the scheduling page</b>';
    }
  });

  /* ---------- tables built from events.csv: hide rows whose date has passed (works between site rebuilds) ---------- */
  $$('.events-table').forEach(function (box) {
    var now = new Date();
    $$('tr[data-date]', box).forEach(function (tr) { var d = parseISO(tr.getAttribute('data-date')); if (d && endOfDay(d) < now) tr.hidden = true; });
    var anyYear = false;
    $$('.et-year', box).forEach(function (sec) {
      var any = $$('tr[data-date]', sec).some(function (tr) { return !tr.hidden; });
      sec.hidden = !any; if (any) anyYear = true;
    });
    var empty = $('.et-empty', box); if (empty) empty.hidden = anyYear;
  });

  /* ---------- "how a study works" steps ---------- */
  var steps = $$('#steps [role=tab]'), panels = $$('#steps-panels [role=tabpanel]');
  function selectStep(i, focus) {
    steps.forEach(function (t, j) { var on = i === j; t.setAttribute('aria-selected', String(on)); t.tabIndex = on ? 0 : -1; panels[j].hidden = !on; });
    if (focus) steps[i].focus();
  }
  steps.forEach(function (t, i) {
    t.addEventListener('click', function () { selectStep(i); });
    t.addEventListener('keydown', function (e) {
      var n = null, k = e.key;
      if (k === 'ArrowDown' || k === 'ArrowRight') n = (i + 1) % steps.length;
      else if (k === 'ArrowUp' || k === 'ArrowLeft') n = (i - 1 + steps.length) % steps.length;
      else if (k === 'Home') n = 0; else if (k === 'End') n = steps.length - 1;
      if (n !== null) { e.preventDefault(); selectStep(n, true); }
    });
  });
  $$('[data-next-step]').forEach(function (b) { b.addEventListener('click', function () { selectStep(+b.getAttribute('data-next-step'), true); }); });

  /* ---------- research slideshow (cards come from research_highlights.yml) ---------- */
  (function () {
    var track = $('#track'); if (!track) return;
    var slides = $$('.slide', track), dots = $('#dots'), pauseBtn = $('#slide-pause'), timer = 0, paused = false, hover = false, visible = true;
    slides.forEach(function (s, i) {
      var b = document.createElement('button'); b.type = 'button'; b.setAttribute('aria-label', 'Go to example ' + (i + 1));
      b.addEventListener('click', function () { go(i); }); dots.appendChild(b);
    });
    function idx() { var best = 0, d = 1e9; slides.forEach(function (s, i) { var x = Math.abs(s.offsetLeft - track.scrollLeft); if (x < d) { d = x; best = i; } }); return best; }
    function go(i) { i = (i + slides.length) % slides.length; track.scrollTo({ left: slides[i].offsetLeft, behavior: reduced() ? 'auto' : 'smooth' }); }
    function mark() { var c = idx(); $$('button', dots).forEach(function (b, i) { b.setAttribute('aria-current', String(i === c)); }); }
    var ticking = false;
    track.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(function () { mark(); ticking = false; }); } });
    $('#prev').addEventListener('click', function () { go(idx() - 1); });
    $('#next').addEventListener('click', function () { go(idx() + 1); });
    track.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { e.preventDefault(); go(idx() + 1); } else if (e.key === 'ArrowLeft') { e.preventDefault(); go(idx() - 1); } });
    function play() { clearInterval(timer); timer = 0; if (!paused && !hover && visible && !reduced() && slides.length > 1) timer = setInterval(function () { go(idx() + 1); }, 7000); }
    pauseBtn.addEventListener('click', function () { paused = !paused; pauseBtn.setAttribute('aria-pressed', String(paused)); pauseBtn.textContent = paused ? '▶' : '❚❚'; pauseBtn.setAttribute('aria-label', paused ? 'Resume automatic scrolling' : 'Pause automatic scrolling'); play(); });
    ['mouseenter', 'focusin', 'touchstart'].forEach(function (ev) { track.addEventListener(ev, function () { hover = true; play(); }, { passive: true }); });
    ['mouseleave', 'focusout'].forEach(function (ev) { track.addEventListener(ev, function () { hover = false; play(); }); });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; play(); }, { threshold: .3 }).observe(track);
    mark(); play();
  })();

  /* ---------- dataset browser (cards come from datasets.csv) ---------- */
  (function () {
    var q = $('#ds-q'); if (!q) return;
    var cards = $$('.ds'), chips = $$('button[data-filter]'), filter = 'all';
    function apply() {
      var term = q.value.trim().toLowerCase(), n = 0;
      cards.forEach(function (c) {
        var show = (filter === 'all' || c.getAttribute('data-access') === filter) && (!term || (c.textContent + ' ' + (c.getAttribute('data-kw') || '')).toLowerCase().indexOf(term) > -1);
        c.hidden = !show; if (show) n++;
      });
      $('#ds-count').textContent = n + ' of ' + cards.length + ' datasets';
      $('#ds-empty').hidden = n !== 0;
    }
    q.addEventListener('input', apply);
    chips.forEach(function (c) { c.addEventListener('click', function () { filter = c.getAttribute('data-filter'); chips.forEach(function (o) { o.setAttribute('aria-pressed', String(o === c)); }); apply(); }); });
    apply();
  })();

  /* ---------- count-up numbers and scroll reveal ---------- */
  $$('[data-since]').forEach(function (el) {
    var y = +el.getAttribute('data-since'), m = +(el.getAttribute('data-since-month') || 1);
    var yrs = Math.floor((Date.now() - new Date(y, m - 1, 1).getTime()) / 31557600000);
    el.setAttribute('data-count', yrs); el.textContent = yrs;
  });
  function countUp(el) {
    var to = +el.getAttribute('data-count');
    if (reduced()) { el.textContent = to; return; }
    var t0 = performance.now(), dur = 1100;
    el.textContent = '0';
    (function step(t) { var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(to * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); })(t0);
  }
  if ('IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (en) { en.forEach(function (x) { if (x.isIntersecting) { countUp(x.target); cio.unobserve(x.target); } }); }, { threshold: .5 });
    $$('[data-count]').forEach(function (el) { cio.observe(el); });
    var rio = new IntersectionObserver(function (en) { en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); rio.unobserve(x.target); } }); }, { threshold: .12, rootMargin: '0px 0px -6% 0px' });
    $$('.reveal').forEach(function (el) { rio.observe(el); });
  } else { $$('.reveal').forEach(function (el) { el.classList.add('in'); }); }
})();
