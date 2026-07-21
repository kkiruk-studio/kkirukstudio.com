/* GA4 — kkirukstudio.com 공용 (G-8SGXCRLT1P) · localhost/파일 열람은 집계 제외 */
(function () {
  var h = location.hostname;
  if (h === 'localhost' || h === '127.0.0.1' || h === '' || location.protocol === 'file:') return;
  window.dataLayer = window.dataLayer || [];
  window.gtag = function(){dataLayer.push(arguments);};
  gtag('js', new Date());
  gtag('config', 'G-8SGXCRLT1P');
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=G-8SGXCRLT1P';
  document.head.appendChild(s);
})();
