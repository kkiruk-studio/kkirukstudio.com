/* 어제보다 랜딩 — 방문자 시각에 따라 페이지가 앱처럼 물든다 */
(function () {
  // 앱 DS.bgForHour 와 동일한 경계
  function timeClass(h) {
    if (h < 5)  return "t-midnight";
    if (h < 7)  return "t-dawn";
    if (h < 10) return "t-morning";
    if (h < 17) return "t-day";
    if (h < 19) return "t-sunset";
    if (h < 21) return "t-evening";
    return "t-midnight";
  }

  var h = new Date().getHours();
  var root = document.documentElement;
  root.classList.add(timeClass(h));
  if (h < 7 || h >= 19) root.classList.add("is-night");

  // 폰 목업 상단 시계 (현지 시각)
  function tick() {
    var els = document.querySelectorAll("[data-clock]");
    var now = new Date();
    var hh = String(now.getHours()).padStart(2, "0");
    var mm = String(now.getMinutes()).padStart(2, "0");
    els.forEach(function (el) { el.textContent = hh + ":" + mm; });
  }
  tick();
  setInterval(tick, 30000);

  // 홈: 스크롤 리빌 + 스탯 카운트업 (요소 있을 때만 동작)
  root.classList.add("js");
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function countUp(el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    if (!target || reduce) { el.textContent = target.toLocaleString("en-US"); return; }
    var t0 = null, dur = 1300;
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased).toLocaleString("en-US");
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  var reveals = document.querySelectorAll(".reveal");
  var counts = document.querySelectorAll("[data-count]");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        if (e.target.classList.contains("reveal")) e.target.classList.add("on");
        if (e.target.hasAttribute("data-count")) countUp(e.target);
        io.unobserve(e.target);
      });
    }, { threshold: 0.15 });
    reveals.forEach(function (el) { io.observe(el); });
    counts.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("on"); });
    counts.forEach(countUp);
  }

  // 히어로 메시지 순환 (페이지의 data-messages JSON 사용)
  var msgEl = document.querySelector("[data-cycle]");
  if (msgEl) {
    var messages = JSON.parse(msgEl.getAttribute("data-cycle"));
    var i = 0;
    setInterval(function () {
      msgEl.classList.add("fade");
      setTimeout(function () {
        i = (i + 1) % messages.length;
        msgEl.textContent = messages[i];
        msgEl.classList.remove("fade");
      }, 450);
    }, 3800);
  }
})();
