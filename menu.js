/* Site menu: hamburger + dropdown on phones and tablets (the desktop nav already shows the links) */
(function(){
  var nav = document.querySelector('.nav-inner');
  if(!nav || document.querySelector('.menu-btn')) return;
  var links = [
    ['Home','/'],['About Ashley','/about'],['Loan Options','/#services'],
    ['Payment Calculator','/calculator'],['Affordability Calculator','/affordability-calculator'],
    ['Free Homebuyer Guide','/#guide'],['Reviews','/#reviews'],['Loan Programs','/loan-programs'],
    ['Service Areas','/service-areas'],['Blog','/blog/'],['Contact','/#contact']
  ];
  var css = document.createElement('style');
  css.textContent =
    '.menu-btn{display:none;background:none;border:1px solid rgba(201,169,106,.55);color:#c9a96a;width:44px;height:40px;cursor:pointer;padding:0;align-items:center;justify-content:center;flex-direction:column;gap:5px;margin-left:8px;flex:0 0 auto}' +
    '.menu-btn span{display:block;width:20px;height:1.5px;background:#c9a96a;transition:transform .25s,opacity .25s}' +
    '.menu-btn.open span:nth-child(1){transform:translateY(6.5px) rotate(45deg)}.menu-btn.open span:nth-child(2){opacity:0}.menu-btn.open span:nth-child(3){transform:translateY(-6.5px) rotate(-45deg)}' +
    '.menu-panel{position:fixed;left:0;right:0;top:var(--menu-top,70px);bottom:0;background:rgba(13,13,15,.98);z-index:60;overflow-y:auto;padding:14px 24px 120px;display:none;border-top:1px solid rgba(201,169,106,.35)}' +
    '.menu-panel.open{display:block}' +
    '.menu-panel a{display:block;padding:15px 2px;border-bottom:1px solid rgba(255,255,255,.07);color:#f2efe9;font-family:"Cormorant Garamond",serif;font-size:24px;font-weight:500;letter-spacing:.3px;text-decoration:none}' +
    '.menu-panel a:hover,.menu-panel a.here{color:#c9a96a}' +
    '.menu-panel .menu-cta{display:flex;gap:10px;margin-top:22px}' +
    '.menu-panel .menu-cta a{flex:1;text-align:center;border:1px solid #c9a96a;font-family:Inter,sans-serif;font-size:12px;letter-spacing:2px;text-transform:uppercase;padding:14px 6px;color:#c9a96a}' +
    '.menu-panel .menu-cta a.solid{background:#c9a96a;color:#0d0d0f}' +
    '@media(max-width:820px){.menu-btn{display:inline-flex}.nav-blog{display:none!important}}' +
    'body.menu-open{overflow:hidden}';
  document.head.appendChild(css);
  var btn = document.createElement('button');
  btn.className = 'menu-btn'; btn.setAttribute('aria-label','Open menu'); btn.setAttribute('aria-expanded','false');
  btn.innerHTML = '<span></span><span></span><span></span>';
  nav.appendChild(btn);
  var panel = document.createElement('div');
  panel.className = 'menu-panel';
  var here = location.pathname.replace(/\.html$/,'').replace(/\/$/,'') || '/';
  panel.innerHTML = links.map(function(l){
    var p = l[1].replace(/\/$/,'') || '/';
    return '<a href="'+l[1]+'"'+(p===here?' class="here"':'')+'>'+l[0]+'</a>';
  }).join('') +
    '<div class="menu-cta"><a class="solid" href="sms:+19255509733">Text Me</a><a href="tel:+19255509733">Call</a>' +
    '<a class="solid" href="https://app.crosscountrymortgage.com/#/signup?referrerId=ashley.gurevich%40ccm.com" target="_blank" rel="noopener">Apply</a></div>';
  document.body.appendChild(panel);
  function setTop(){ var n = nav.closest('nav') || nav; var r = n.getBoundingClientRect(); panel.style.setProperty('--menu-top', Math.max(0, r.bottom) + 'px'); }
  function toggle(open){
    setTop();
    panel.classList.toggle('open', open); btn.classList.toggle('open', open);
    document.body.classList.toggle('menu-open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  btn.addEventListener('click', function(){ toggle(!panel.classList.contains('open')); });
  panel.addEventListener('click', function(e){ if(e.target.tagName === 'A') toggle(false); });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape') toggle(false); });
  window.addEventListener('resize', function(){ if(window.innerWidth > 820) toggle(false); });
})();
