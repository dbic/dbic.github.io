/* Home page slideshow: rotates the pictures shown beside the banner text.
   The pictures are listed by _includes/redesign/home/hero.html from the folder assets/images_for_auto_display/homepage/.
   Without this script the first picture simply stays on show. */
(function () {
  'use strict';
  var fig = document.querySelector('.hero-show'); if (!fig) return;
  var frame = fig.querySelector('.hs-frame'), imgs = [].slice.call(fig.querySelectorAll('.hs-img'));
  if (!frame || imgs.length < 2) return;
  var interval = (+fig.getAttribute('data-interval')) || 8000, i = 0, timer = null, userPaused = false, over = false, ctl = null, loaded = false;
  var reduce = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  if (reduce) userPaused = true;                                        // visitors who asked for less motion get a still picture, and can start it

  function stop() { if (timer) { clearInterval(timer); timer = null; } }
  function play() { stop(); if (userPaused || over || document.hidden || imgs.length < 2) return; timer = setInterval(function () { show(i + 1); }, interval); }
  function show(n) {
    if (!imgs.length) return;
    i = (n % imgs.length + imgs.length) % imgs.length;
    imgs.forEach(function (im, k) { var on = k === i; im.classList.toggle('is-on', on); im.setAttribute('aria-hidden', on ? 'false' : 'true'); });
    if (ctl) [].slice.call(ctl.querySelectorAll('.hs-dot')).forEach(function (d, k) { if (k === i) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current'); });
  }
  function label(btn) { btn.setAttribute('aria-pressed', userPaused ? 'true' : 'false'); btn.setAttribute('aria-label', userPaused ? 'Play slideshow' : 'Pause slideshow'); }
  function controls() {
    if (ctl && ctl.parentNode) ctl.parentNode.removeChild(ctl);
    if (imgs.length < 2) { ctl = null; return; }
    ctl = document.createElement('div'); ctl.className = 'hs-ctl';
    imgs.forEach(function (im, k) {
      var d = document.createElement('button'); d.type = 'button'; d.className = 'hs-dot'; d.setAttribute('aria-label', 'Show photo ' + (k + 1) + ' of ' + imgs.length);
      d.addEventListener('click', function () { loadAll(); show(k); play(); }); ctl.appendChild(d);
    });
    var b = document.createElement('button'); b.type = 'button'; b.className = 'hs-pause'; label(b);
    b.addEventListener('click', function () { userPaused = !userPaused; label(b); play(); }); ctl.appendChild(b);
    frame.appendChild(ctl);
  }
  function drop(im) {                                                    // a picture that cannot be loaded is left out of the rotation
    var k = imgs.indexOf(im); if (k < 0) return;
    imgs.splice(k, 1); if (im.parentNode) im.parentNode.removeChild(im);
    controls(); show(i >= imgs.length ? 0 : i); if (imgs.length < 2) stop();
  }
  function loadAll() {                                                   // the pictures after the first are fetched once the page has loaded
    if (loaded) return; loaded = true;
    imgs.slice().forEach(function (im) { var s = im.getAttribute('data-src'); if (s) { im.removeAttribute('data-src'); im.src = s; } });
  }
  imgs.forEach(function (im) { im.addEventListener('error', function () { if (im.getAttribute('data-src') === null) drop(im); }); });
  fig.addEventListener('mouseenter', function () { over = true; stop(); loadAll(); });
  fig.addEventListener('mouseleave', function () { over = false; play(); });
  fig.addEventListener('focusin', function () { over = true; stop(); loadAll(); });
  fig.addEventListener('focusout', function () { over = false; play(); });
  document.addEventListener('visibilitychange', play);
  controls(); show(0);
  function begin() { loadAll(); play(); }                                // the clock starts once the page has loaded, so the first picture gets its full time
  if (document.readyState === 'complete') begin(); else window.addEventListener('load', begin);
})();
