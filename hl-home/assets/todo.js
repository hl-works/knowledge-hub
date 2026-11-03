(() => {
  'use strict';
  const key = 'hl-home-actions-v1';
  const legacyKey = 'hl-home-v0-todo';
  const rows = [...document.querySelectorAll('[data-task]')];
  const ids = new Set(rows.map(row => row.dataset.task));
  const status = document.querySelector('#save-status');
  const transfer = document.querySelector('#transfer-status');
  const normalMessage = 'Coches et notes enregistrées dans ce navigateur uniquement. Exporte ton suivi pour le sauvegarder ou le reprendre ailleurs. Rien n’est envoyé au site.';
  let state = {}, filter = 'pending', importState = null, printDetails = [];
  // Only accept known task IDs and plain values, including on import.
  function validate(data) {
    if (!data || data.format !== key || !data.tasks || typeof data.tasks !== 'object' || Array.isArray(data.tasks)) throw new Error('format');
    const clean = {};
    for (const id of ids) {
      const item = data.tasks[id];
      if (item === undefined) continue;
      if (!item || typeof item.done !== 'boolean' || typeof item.note !== 'string' || item.note.length > 4000) throw new Error('task');
      clean[id] = {done:item.done, note:item.note};
    }
    if (!Object.keys(clean).length) throw new Error('empty');
    return clean;
  }
  function readLegacy() {
    const data = JSON.parse(localStorage.getItem(legacyKey) || '{}');
    return data && typeof data === 'object' && !Array.isArray(data) ? data : {};
  }
  let loadError = false;
  try {
    const saved = localStorage.getItem(key);
    if (saved) state = validate(JSON.parse(saved));
    const legacy = readLegacy();
    for (const id of ids) if (/^t\d+$/.test(id) && typeof legacy[id] === 'boolean') state[id] = {...state[id], done:legacy[id]};
  } catch (_) { loadError = true; }
  for (const id of ids) state[id] = {done:!!state[id]?.done, note:state[id]?.note || ''};
  status.textContent = loadError ? 'L’ancien suivi n’a pas pu être lu entièrement. Vérifie les coches affichées avant de modifier une action. Tu peux toujours exporter ton suivi.' : normalMessage;
  function persist() {
    try {
      localStorage.setItem(key, JSON.stringify({format:key, tasks:state}));
      let legacy = {};
      try { legacy = readLegacy(); } catch (_) {}
      for (const id of ids) if (/^t\d+$/.test(id)) legacy[id] = state[id].done;
      localStorage.setItem(legacyKey, JSON.stringify(legacy));
      status.textContent = normalMessage;
    } catch (_) {
      status.textContent = 'Le navigateur ne permet pas d’enregistrer ton suivi. Tes modifications restent visibles tant que cette page est ouverte : exporte-les avant de la quitter.';
    }
  }
  function draw() {
    let completed = 0, visible = 0;
    for (const row of rows) {
      const item = state[row.dataset.task];
      row.querySelector('input').checked = item.done;
      row.classList.toggle('is-done', item.done);
      row.querySelector('.action-status').textContent = item.done ? 'Terminé' : 'À faire';
      row.hidden = filter === 'done' ? !item.done : filter === 'pending' && item.done;
      if (item.done) completed++;
      if (!row.hidden) visible++;
    }
    document.querySelector('#todo-progress').textContent = `${completed} / ${rows.length} actions terminées`;
    document.querySelector('#todo-meter').value = completed;
    document.querySelector('#todo-meter').textContent = `${completed} / ${rows.length}`;
    document.querySelector('#filter-count').textContent = `${visible} action${visible > 1 ? 's' : ''} affichée${visible > 1 ? 's' : ''}`;
    for (const group of document.querySelectorAll('.task-group')) {
      const items = [...group.querySelectorAll('[data-task]')];
      const done = items.filter(row => state[row.dataset.task].done).length;
      group.querySelector('.group-count').textContent = `${done} / ${items.length} terminées`;
      group.querySelector('.empty-group').hidden = items.some(row => !row.hidden);
    }
    const next = rows.filter(row => !state[row.dataset.task].done && (row.dataset.requires || '').split(' ').filter(Boolean).every(id => state[id]?.done)).sort((a,b) => Number(a.dataset.priority)-Number(b.dataset.priority)).slice(0,3);
    const list = document.querySelector('#next-actions');
    list.replaceChildren();
    for (const row of next) {
      const li = document.createElement('li'), a = document.createElement('a'), text = document.createElement('span'), small = document.createElement('small');
      a.href = `#${row.id}`;
      text.append(document.createTextNode(row.querySelector('label').textContent));
      small.textContent = row.querySelector('.action-who').textContent;
      text.append(small); a.append(text); li.append(a); list.append(li);
    }
    if (!next.length) { const li = document.createElement('li'); li.textContent = completed === rows.length ? 'Toutes les actions sont cochées. Tu peux retrouver tes notes avec le filtre « Tout ».' : 'Consulte les prérequis des actions restantes dans la liste ci-dessous.'; list.append(li); }
  }
  function setFilter(value) {
    filter = value;
    for (const button of document.querySelectorAll('[data-filter]')) button.setAttribute('aria-pressed', String(button.dataset.filter === filter));
    draw();
  }
  function showAnchor() {
    let id;
    try {id = decodeURIComponent(location.hash.slice(1));} catch (_) {return;}
    const row = document.getElementById(id);
    if (!row?.matches('[data-task]')) return;
    if (row.hidden) setFilter('all');
    row.querySelector('details').open = true;
    row.scrollIntoView({block:'start'});
  }
  for (const row of rows) {
    const id = row.dataset.task, input = row.querySelector('input'), note = row.querySelector('textarea');
    input.disabled = false; note.disabled = false; note.value = state[id].note;
    input.addEventListener('change', () => {
      state[id].done = input.checked;
      persist(); draw();
      // A filtered-out checkbox must not leave keyboard focus on an invisible element.
      if (row.hidden) document.querySelector(`[data-filter="${filter}"]`).focus({preventScroll:true});
    });
    note.addEventListener('input', () => {state[id].note = note.value; persist();});
  }
  for (const button of document.querySelectorAll('[data-filter]')) {button.disabled = false; button.addEventListener('click', () => setFilter(button.dataset.filter));}
  const exportButton = document.querySelector('#export-todo'); exportButton.disabled = false;
  exportButton.addEventListener('click', () => {
    const blob = new Blob([JSON.stringify({format:key, exportedAt:new Date().toISOString(), tasks:state}, null, 2)], {type:'application/json'});
    const url = URL.createObjectURL(blob), a = document.createElement('a');
    a.href = url; a.download = 'hl-home-mon-suivi.json'; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    transfer.textContent = 'Export préparé : conserve ce fichier avec tes documents privés. Il contient tes coches et tes notes.';
  });
  const importButton = document.querySelector('#import-todo'), file = document.querySelector('#import-file'), review = document.querySelector('#import-review');
  importButton.disabled = false; importButton.addEventListener('click', () => file.click());
  file.addEventListener('change', async () => {
    const selected = file.files[0]; if (!selected) return;
    importState = null; review.hidden = true;
    try {
      if (selected.size > 1000000) throw new Error('size');
      importState = validate(JSON.parse(await selected.text()));
      const items = Object.values(importState);
      document.querySelector('#import-summary').textContent = `Ce fichier contient ${items.filter(x=>x.done).length} actions terminées et ${items.filter(x=>x.note).length} notes. Remplacer ton suivi actuel ? Les actions absentes du fichier seront conservées.`;
      review.hidden = false;
      document.querySelector('#confirm-import').focus();
      transfer.textContent = 'Fichier lu. Rien n’a encore été remplacé.';
    } catch (_) {transfer.textContent = 'Ce fichier n’est pas un export HL Home valide. Ton suivi est conservé.';}
    file.value = '';
  });
  document.querySelector('#confirm-import').addEventListener('click', () => {
    if (!importState) return;
    state = {...state,...importState};
    for (const row of rows) row.querySelector('textarea').value = state[row.dataset.task].note;
    persist(); draw(); review.hidden = true; importState = null;
    transfer.textContent = 'Suivi importé. Les coches et les notes ont été mises à jour.'; importButton.focus();
  });
  document.querySelector('#cancel-import').addEventListener('click', () => {importState = null; review.hidden = true; transfer.textContent = 'Import annulé. Ton suivi est conservé.'; importButton.focus();});
  const printButton = document.querySelector('#print-todo'); printButton.disabled = false; printButton.addEventListener('click', () => window.print());
  window.addEventListener('beforeprint', () => {printDetails = [...document.querySelectorAll('.action-row details')].map(el=>[el,el.open]); for(const [el] of printDetails)el.open=true;});
  window.addEventListener('afterprint', () => {for(const [el,open] of printDetails)el.open=open;});
  window.addEventListener('hashchange', showAnchor);
  draw(); showAnchor();
})();
