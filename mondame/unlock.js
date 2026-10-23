// Mondame — déverrouillage d'une collection chiffrée (mêmes primitives que knowledge-hub/coffre).
// La page publique ne contient que la porte d'entrée ; contenu et visuels sont dans
// content.bin et img/*.bin (AES-256-GCM, clé PBKDF2-SHA256), produits par build.py (hors repo).
(function () {
  const store = 'md-key:' + location.pathname;
  const enc = new TextEncoder();
  const b64 = s => Uint8Array.from(atob(s), c => c.charCodeAt(0));
  const toB64 = buf => btoa(String.fromCharCode(...new Uint8Array(buf)));
  const remember = (fn, v) => { try { fn(v); } catch (e) {} };

  async function deriveKey(pass) {
    const v = await (await fetch('vault.json', { cache: 'no-cache' })).json();
    const base = await crypto.subtle.importKey('raw', enc.encode(pass), 'PBKDF2', false, ['deriveKey']);
    return crypto.subtle.deriveKey({ name: 'PBKDF2', salt: b64(v.salt), iterations: v.iter, hash: 'SHA-256' },
      base, { name: 'AES-GCM', length: 256 }, true, ['decrypt']);
  }

  async function open(key, path, bust) {
    const buf = new Uint8Array(await (await fetch(path, { cache: bust ? 'no-cache' : 'default' })).arrayBuffer());
    return crypto.subtle.decrypt({ name: 'AES-GCM', iv: buf.slice(0, 12) }, key, buf.slice(12));
  }

  async function show(key) {
    const html = new TextDecoder().decode(await open(key, 'content.bin', true));
    document.body.innerHTML = html;
    document.documentElement.setAttribute('data-unlocked', '');
    if (location.hash) document.querySelector(location.hash)?.scrollIntoView();

    const load = async img => {
      try {
        const blob = new Blob([await open(key, 'img/' + img.dataset.id + '.bin')], { type: 'image/jpeg' });
        img.src = URL.createObjectURL(blob);
      } catch (e) { img.alt += ' (visuel indisponible)'; }
    };
    const seen = new Map();
    const io = new IntersectionObserver(entries => entries.forEach(en => {
      if (!en.isIntersecting) return;
      io.unobserve(en.target);
      const id = en.target.dataset.id;
      if (!seen.has(id)) seen.set(id, load(en.target));
      else seen.get(id).then(() => { en.target.src = document.querySelector(`img[data-id="${id}"][src]`)?.src || ''; });
    }), { rootMargin: '600px 0px' });
    document.querySelectorAll('img[data-id]').forEach(img => { img.decoding = 'async'; io.observe(img); });

    const lb = document.querySelector('[data-lb]');
    if (lb) {
      const big = lb.querySelector('img');
      document.addEventListener('click', e => {
        const img = e.target.closest('.sh-gal img[src], .sh-duo img[src], .sh-hero-img img[src]');
        if (img) { big.src = img.src; big.alt = img.alt; lb.hidden = false; return; }
        if (!lb.hidden && (e.target === lb || e.target === big || e.target.closest('[data-lb-close]'))) lb.hidden = true;
      });
      document.addEventListener('keydown', e => { if (e.key === 'Escape') lb.hidden = true; });
    }
    document.querySelectorAll('[data-lock]').forEach(b => b.addEventListener('click', () => {
      remember(k => sessionStorage.removeItem(k), store);
      location.replace(location.pathname);
    }));
  }

  const form = document.querySelector('[data-gate]');
  const msg = document.querySelector('[data-gate-msg]');
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const btn = form.querySelector('button');
    btn.disabled = true; msg.textContent = 'Ouverture…'; msg.classList.remove('red');
    try {
      const key = await deriveKey(form.password.value);
      await show(key);
      const raw = await crypto.subtle.exportKey('raw', key);
      remember(v => sessionStorage.setItem(store, v), toB64(raw));
    } catch (err) {
      msg.textContent = 'Mot de passe incorrect.'; msg.classList.add('red');
      form.querySelector('.field').style.borderColor = 'var(--red)';
      btn.disabled = false; form.password.select();
    }
  });

  let saved = null;
  remember(k => { saved = sessionStorage.getItem(k); }, store);
  if (saved) {
    crypto.subtle.importKey('raw', b64(saved), 'AES-GCM', true, ['decrypt'])
      .then(show)
      .catch(() => remember(k => sessionStorage.removeItem(k), store));
  }
})();
