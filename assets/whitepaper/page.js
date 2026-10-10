'use strict';
(() => {
  const lang = document.documentElement.lang === 'en' ? 'en' : 'fr';
  const text = {
    fr: { preview: 'Aperçu : la collecte n’est pas encore activée. Aucune adresse n’a été envoyée ni enregistrée.', invalid: 'Indique une adresse email valide.', pending: 'Préparation de ton accès…', error: 'L’accès n’a pas pu être confirmé. Réessaie dans un instant.', success: 'Ton PDF est prêt. Clique ci-dessous pour le télécharger.' },
    en: { preview: 'Preview: contact collection is not active. No email address was sent or saved.', invalid: 'Please enter a valid email address.', pending: 'Preparing your access…', error: 'We couldn’t confirm access. Please try again shortly.', success: 'Your PDF is ready. Use the link below to download it.' }
  }[lang];
  document.querySelector('.theme').addEventListener('click', () => {
    const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = theme;
    document.querySelector('meta[name="theme-color"]').content = theme === 'dark' ? '#0A0A0A' : '#FF8C7A';
    try { localStorage.setItem('hl-theme', theme); } catch (_) {}
  });
  const form = document.querySelector('#download-form');
  const email = form.elements.email;
  const status = document.querySelector('#form-status');
  const submit = form.querySelector('[type=submit]');
  const link = document.querySelector('#download-link');
  let busy = false;
  let pendingRequest = null;
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (busy) return;
    link.hidden = true;
    email.value = email.value.trim();
    email.removeAttribute('aria-invalid');
    if (!email.checkValidity()) {
      email.setAttribute('aria-invalid', 'true');
      status.textContent = text.invalid;
      email.focus();
      return;
    }
    // Fail closed until the actual provider, privacy notice and protected storage are configured.
    if (!form.dataset.endpoint) { status.textContent = text.preview; return; }
    let endpoint;
    try { endpoint = new URL(form.dataset.endpoint); if (endpoint.protocol !== 'https:') throw new Error(); }
    catch (_) { status.textContent = text.error; return; }
    const body = { email: email.value.toLowerCase(), language: lang, subscribe: form.elements.subscribe.checked, company_site: form.elements.company_site.value, consent_version: 'whitepaper-2026-10-v2' };
    const fingerprint = JSON.stringify(body);
    // Conserver le même identifiant après une réponse perdue, sans stockage du courriel.
    if (!pendingRequest || pendingRequest.fingerprint !== fingerprint) pendingRequest = { fingerprint, id: crypto.randomUUID() };
    body.request_id = pendingRequest.id;
    busy = true;
    submit.setAttribute('aria-disabled', 'true');
    status.textContent = text.pending;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000);
    try {
      const response = await fetch(endpoint, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        credentials: 'omit', signal: controller.signal, referrerPolicy: 'no-referrer',
        body: JSON.stringify(body)
      });
      if (!response.ok) throw new Error('Request failed');
      const data = await response.json();
      const download = new URL(data.download_url);
      if (download.protocol !== 'https:' || download.origin !== endpoint.origin) throw new Error('Invalid download origin');
      link.href = download.href;
      link.rel = 'noreferrer';
      link.hidden = false;
      status.textContent = text.success;
      email.value = '';
      pendingRequest = null;
      link.focus();
    } catch (_) { status.textContent = text.error; }
    finally { clearTimeout(timeout); busy = false; submit.removeAttribute('aria-disabled'); }
  });
})();
