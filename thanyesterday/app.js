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
