// Deep links also reveal archived content inside native disclosures.
function revealDossierTarget() {
  let id;
  try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
  const target = document.getElementById(id);
  if (!target) return;
  let parent = target.parentElement;
  let revealed = false;
  while (parent) {
    if (parent.tagName === 'DETAILS' && !parent.open) { parent.open = true; revealed = true; }
    parent = parent.parentElement;
  }
  if (revealed) requestAnimationFrame(() => target.scrollIntoView({block:'start', behavior:'instant'}));
}
window.addEventListener('hashchange', revealDossierTarget);
revealDossierTarget();
