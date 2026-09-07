// Adopted landing refinements (2026-09-07). RunNote intentionally excluded.
(() => {
const page = location.pathname.split('/')[1] || 'home';
const enabledRoutes = new Set(['/', '/index.html', '/palette2048/ko.html', '/cats-cute/ko.html', '/cats-pop/ko.html', '/genkai-neko/', '/genkai-neko/index.html', '/jixian-mao/', '/jixian-mao/index.html', '/quote2048/ko/', '/quote2048/ko/index.html']);
if (enabledRoutes.has(location.pathname)) {
document.body.dataset.landingPage = page;
const makeLink = (text, href, cls = 'landing-button') => {
  const a = document.createElement('a'); a.textContent = text; a.href = href; a.className = cls; return a;
};
if (page === 'home' || page === 'index.html') {
  document.body.dataset.landingPage = 'home';
  const bar = document.querySelector('header .bar'), nav = bar?.querySelector('nav');
  if (nav) {
    nav.id = 'landing-navigation';
    const toggle = document.createElement('button');
    toggle.className = 'landing-menu'; toggle.textContent = '메뉴';
    toggle.setAttribute('aria-expanded', 'false'); toggle.setAttribute('aria-controls', nav.id);
    toggle.onclick = () => {
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(open)); toggle.textContent = open ? '닫기' : '메뉴';
      bar.classList.toggle('landing-open', open);
    };
    bar.insertBefore(toggle, nav);
    nav.addEventListener('click', e => { if (e.target.closest('a')) { bar.classList.remove('landing-open'); toggle.setAttribute('aria-expanded','false'); toggle.textContent='메뉴'; } });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && bar.classList.contains('landing-open')) { toggle.click(); toggle.focus(); } });
  }
  const hero = document.querySelector('.hero-main');
  if (hero) {
    const actions = document.createElement('div'); actions.className = 'landing-home-actions';
    actions.append(makeLink('게임 둘러보기', '#games'), makeLink('생활에 맞는 앱 찾기', '#apps', 'landing-secondary'));
    hero.querySelector('.hero-sub2')?.after(actions);
  }
}
if (page === 'genkai-neko' || page === 'jixian-mao') {
  const hero = document.querySelector('section.hero'), sets = document.querySelector('#sets');
  if (hero && sets) {
    document.querySelector('.hero-text')?.append(makeLink(page === 'genkai-neko' ? 'LINEスタンプを見る' : '挑選 LINE 貼圖', '#sets'));
    hero.after(sets);
  }
}
if (page === 'quote2048') {
  const cta = document.querySelector('.cta');
  const intro = document.querySelector('main .sub');
  if (cta && intro) { const copy = cta.cloneNode(true); copy.classList.add('landing-quote-cta'); intro.after(copy); }
}
}

})();
