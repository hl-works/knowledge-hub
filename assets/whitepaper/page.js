'use strict';
(() => {
  const lang = document.documentElement.lang === 'en' ? 'en' : 'fr';
  const text = {
    fr: { preview: 'Aperçu : la collecte n’est pas encore activée. Aucune adresse n’a été envoyée ni enregistrée.', invalid: 'Indique une adresse email valide.', pending: 'Envoi de la confirmation…', error: 'L’accès n’a pas pu être confirmé. Réessaie dans un instant.', success: 'Consulte ta boîte mail et tes indésirables. Ouvre le lien reçu puis confirme ton adresse pour accéder au PDF. Aucun message ? Tu peux réessayer après 2 minutes (3 envois maximum par jour).' },
    en: { preview: 'Preview: contact collection is not active. No email address was sent or saved.', invalid: 'Please enter a valid email address.', pending: 'Sending confirmation…', error: 'We couldn’t confirm access. Please try again shortly.', success: 'Check your inbox and spam folder. Open the email link and confirm your address to access the PDF. No message? Try again after 2 minutes (up to 3 sends per day).' }
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
  let busy = false;
  let pendingRequest = null;
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (busy) return;
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
    const body = { email: email.value.toLowerCase(), language: lang, subscribe: form.elements.subscribe.checked, company_site: form.elements.company_site.value, consent_version: 'whitepaper-2026-10-v3' };
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
      if (response.status === 429) { status.textContent = lang === 'fr' ? 'Patiente 2 minutes entre deux envois. La limite est de 3 emails sur 24 heures.' : 'Wait 2 minutes between sends. The limit is 3 emails per 24 hours.'; pendingRequest = null; return; }
      if (!response.ok) throw new Error('Request failed');
      const data = await response.json();
      if (data.status !== 'confirmation_pending') throw new Error('Invalid confirmation response');
      status.textContent = text.success;
      submit.textContent = lang === 'fr' ? 'Renvoyer un email de confirmation →' : 'Resend confirmation email →';
      pendingRequest = null;
    } catch (_) { status.textContent = text.error; }
    finally { clearTimeout(timeout); busy = false; submit.removeAttribute('aria-disabled'); }
  });
})();
