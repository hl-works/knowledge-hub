/* A non-modal invitation after 30 seconds of visible reading. No tracking. */
(() => {
  const panel = document.getElementById('follow-invite');
  if (!panel) return;
  const key = 'kh-follow-dismissed-until';
  const sessionKey = 'kh-follow-shown';
  const read = (storage, name) => { try { return window[storage].getItem(name); } catch (_) { return null; } };
  const write = (storage, name, value) => { try { window[storage].setItem(name, value); } catch (_) {} };
  if (Number(read('localStorage', key)) > Date.now() || read('sessionStorage', sessionKey)) return;
  let remaining = 30000;
  let started = null;
  let timer;
  let finished = false;
  function dismiss() {
    panel.hidden = true;
    finished = true;
    clearTimeout(timer);
    write('localStorage', key, String(Date.now() + 7 * 24 * 60 * 60 * 1000));
  }
  function show() {
    if (document.hidden || finished) return;
    // Let an open search dialog finish before showing another interface.
    if (Array.from(document.querySelectorAll('dialog[open], [role="dialog"][aria-modal="true"]:not([hidden])')).some(dialog => dialog.getClientRects().length && getComputedStyle(dialog).visibility !== 'hidden')) {
      timer = setTimeout(show, 1000);
      return;
    }
    panel.hidden = false;
    finished = true;
    write('sessionStorage', sessionKey, '1');
  }
  function visibility() {
    clearTimeout(timer);
    if (finished) return;
    if (document.hidden) {
      if (started !== null) remaining = Math.max(0, remaining - (Date.now() - started));
      started = null;
    } else {
      started = Date.now();
      timer = setTimeout(show, remaining);
    }
  }
  panel.querySelector('button').addEventListener('click', dismiss);
  panel.querySelectorAll('a').forEach(link => link.addEventListener('click', dismiss));
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && !panel.hidden) dismiss(); });
  document.addEventListener('visibilitychange', visibility);
  visibility();
})();
