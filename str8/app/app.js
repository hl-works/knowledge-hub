/* Str8 — logique applicative (SPA vanilla, routeur par hash). */
(function () {
  const S = window.Store, D = window.STR8_DATA, M = window.MEDIA;
  const EX = D.byId, PR = D.PROGRAM;
  const view = () => document.getElementById('view');
  const nav  = () => document.getElementById('nav');
  const esc = (s) => String(s).replace(/[&<>"]/g, c => ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;' }[c]));
  const fmt = (t) => { t = Math.max(0, Math.round(t)); const m = Math.floor(t/60), s = t%60; return (m<10?'0':'')+m+':'+(s<10?'0':'')+s; };
  const media = (k) => M[k] || M.iso;

  /* ---------- semaine / stats ---------- */
  function isoWeek(d) { d = new Date(d); d.setHours(0,0,0,0); d.setDate(d.getDate() + 3 - ((d.getDay()+6)%7));
    const w1 = new Date(d.getFullYear(),0,4); return d.getFullYear()+'-'+String(1+Math.round(((d-w1)/864e5 - 3 + ((w1.getDay()+6)%7))/7)).padStart(2,'0'); }
  function thisWeekSessions() { const wk = isoWeek(new Date()); return S.getSessions().filter(s => isoWeek(s.date) === wk); }
  function streakWeeks() {
    const weeks = new Set(S.getSessions().map(s => isoWeek(s.date)));
    let n = 0, d = new Date();
    while (weeks.has(isoWeek(d))) { n++; d.setDate(d.getDate() - 7); }
    return n;
  }
  function recommendedSession() { const n = S.getSessions().filter(s => s.kind === 'session').length; return PR.weekOrder[n % PR.weekOrder.length]; }

  /* ---------- valeurs éditables par exo ---------- */
  const getSets = (ex) => S.getExPref(ex.id).sets ?? ex.sets;
  const getHold = (ex) => S.getExPref(ex.id).holdSec ?? ex.holdSec;
  const getRest = (ex) => S.getExPref(ex.id).restSec ?? ex.restSec;
  const getReps = (ex) => S.getExPref(ex.id).repsChosen ?? (ex.reps ? ex.reps[1] : null);

  /* ============================================================= ACCUEIL */
  function home() {
    const p = S.getProfile();
    const rec = PR.sessions[recommendedSession()];
    const nExo = rec.exercises.length;
    const last = S.getSessions()[0];
    const wk = thisWeekSessions().length;
    setView(`
      <header class="hd">
        <div class="hd-l">STR8 <span class="dim mono">/ ${esc(p.prenom)}</span></div>
        <div class="mono dim">${new Date().toLocaleDateString('fr-FR',{weekday:'short',day:'numeric',month:'short'})}</div>
      </header>
      <section class="load">
        <div class="load-h"><span>PROGRAMME CHARGÉ</span><span>SÉANCE ${rec.id}</span></div>
        <div class="load-name">${esc(rec.name)}</div>
        <div class="load-spec">
          <div><b>${esc(PR.duration)}</b><i>Durée</i></div>
          <div><b>${String(nExo).padStart(2,'0')}</b><i>Exos</i></div>
          <div><b>${esc(p.materiel.split(' ')[0])}</b><i>Matériel</i></div>
        </div>
      </section>
      <div class="row2">
        <div class="stat"><div class="stat-v">${wk}</div><div class="stat-l">séances cette semaine</div></div>
        <div class="stat"><div class="stat-v">${streakWeeks()}</div><div class="stat-l">semaines de suite</div></div>
      </div>
      ${last ? `<div class="last mono">Dernière : <b>${esc(last.name)}</b> · ${new Date(last.date).toLocaleDateString('fr-FR')}</div>` : ''}
      <button class="btn-go" onclick="App.start('${rec.id}')">DÉMARRER <span class="mono">▶ ${String(nExo).padStart(2,'0')} EXOS</span></button>
      <div class="row2 mt">
        <button class="btn-line" onclick="location.hash='#/quick'">◱ ROUTINE 5 MIN</button>
        <button class="btn-line" onclick="App.logCardio()">◐ COURSE / MARCHE</button>
      </div>
    `);
    setNav('home');
  }

  /* ============================================================= SÉANCE */
  let run = null;
  function buildQueue(sessionId) {
    const sess = PR.sessions[sessionId];
    return sess.exercises.map(id => EX[id]).filter(Boolean);
  }
  App_start = function (sessionId) {
    const q = buildQueue(sessionId);
    run = { kind:'session', sessionId, name: PR.sessions[sessionId].name, q, i:0, set:0, mode:'exercise',
            startTs: Date.now(), log:[], pain:[], variant:false, tid:null, remain:0, paused:false };
    renderRun();
  };
  function stopTimer() { if (run && run.tid) { clearInterval(run.tid); run.tid = null; } }
  function tickTo(el, ring, total) {
    const c = document.getElementById(el); if (c) c.textContent = fmt(run.remain);
    const r = document.getElementById(ring); if (r) r.style.strokeDashoffset = 596 - 596 * Math.max(0, run.remain) / total;
  }

  function renderRun() {
    stopTimer();
    if (run.mode === 'done') return renderDone();
    if (run.mode === 'rest') return renderRest();
    const ex = run.q[run.i];
    const sets = getSets(ex), hold = getHold(ex), reps = getReps(ex);
    const dots = Array.from({length:sets}, (_,k) => `<i class="${k<run.set?'done':k===run.set?'cur':''}"></i>`).join('');
    const counter = hold ? timerBlock(hold) : repBlock(ex, reps);
    setView(`
      <div class="sess">
        <div class="sess-top mono"><span>${String(run.i+1).padStart(2,'0')} / ${String(run.q.length).padStart(2,'0')}</span>
          <span>SÉANCE ${run.sessionId} · ${esc(run.name)}</span></div>
        <div class="sess-name">${esc(ex.name)}</div>
        <div class="sess-tag mono">${esc(ex.cat)} · ${esc(ex.goal)}</div>
        <div class="media">${media(ex.media)}<span class="media-lbl mono">SVG · REPÈRE</span></div>
        <div class="seg">${dots}</div>
        ${run.variant ? `<div class="cue warn"><b>Variante plus simple</b> ${esc(ex.easier||'Réduis l’amplitude et l’intensité.')}</div>`
                      : `<div class="cue"><b>Consigne</b> ${esc(ex.cues[0])}</div><div class="cue sub"><b>À éviter</b> ${esc(ex.mistakes[0])}</div>`}
        ${counter}
        <div class="ctrl">
          <button class="c-sec" onclick="App.prevEx()">◁</button>
          <button class="c-go" onclick="App.validateSet()">${hold ? 'SÉRIE FAITE ▷' : 'VALIDER SÉRIE ▷'}</button>
          <button class="c-sec" onclick="App.nextEx()">▷</button>
        </div>
        <div class="sub-actions">
          <button onclick="App.pain()">⚠ Douleur</button>
          <button onclick="App.toggleVariant()">↔ Variante</button>
          <button onclick="App.quit()">✕ Quitter</button>
        </div>
      </div>`);
    setNav(null);
    if (hold) startHold(hold);
  }

  function repBlock(ex, reps) {
    return `<div class="counter">
      <div class="c-lab mono">RÉPÉTITIONS<b>reco ${ex.reps ? ex.reps[0]+'–'+ex.reps[1] : '—'}</b></div>
      <div class="stepper">
        <button onclick="App.repDelta(-1)">−</button>
        <input class="c-val mono" id="repv" inputmode="numeric" value="${reps}" onchange="App.setReps(this.value)">
        <button onclick="App.repDelta(1)">+</button>
      </div></div>`;
  }
  function timerBlock(hold) {
    return `<div class="dial">
      <svg viewBox="0 0 210 210"><circle class="ring-bg" cx="105" cy="105" r="95"/><circle class="ring-fg" id="ring" cx="105" cy="105" r="95"/></svg>
      <div class="dial-c"><div class="dial-big mono" id="clock">${fmt(hold)}</div><div class="dial-l mono">MAINTIEN</div></div>
      </div>
      <div class="tadj">
        <button onclick="App.timerAdj(-10)">−10s</button>
        <button class="tgo" id="tgo" onclick="App.toggleTimer()">DÉMARRER</button>
        <button onclick="App.timerAdj(10)">+10s</button>
      </div>`;
  }
  function startHold(hold) { run.remain = hold; run.paused = true; run.holdTotal = hold; } // démarre en pause
  App_toggleTimer = function () {
    const b = document.getElementById('tgo'); if (!b) return;
    if (!run.tid) { run.paused = false; b.textContent = 'PAUSE';
      run.tid = setInterval(() => { if (run.paused) return; run.remain--; tickTo('clock','ring',run.holdTotal);
        if (run.remain <= 0) { stopTimer(); b.textContent = 'TERMINÉ'; if (S.getPrefs().vibration && navigator.vibrate) navigator.vibrate(120); } }, 1000);
    } else { run.paused = !run.paused; b.textContent = run.paused ? 'REPRENDRE' : 'PAUSE'; }
  };
  App_timerAdj = function (d) { run.remain = Math.max(0, run.remain + d); tickTo('clock','ring',run.holdTotal); };

  App_repDelta = function (d) { const el = document.getElementById('repv'); const v = Math.max(0, (parseInt(el.value,10)||0) + d); el.value = v; saveReps(run.q[run.i].id, v); };
  App_setReps = function (v) { const n = Math.max(0, parseInt(v,10)||0); saveReps(run.q[run.i].id, n); const el = document.getElementById('repv'); if (el) el.value = n; };
  function saveReps(id, v) { S.saveExPref(id, { repsChosen: v }); }

  App_validateSet = function () {
    const ex = run.q[run.i], hold = getHold(ex);
    run.log.push({ exId: ex.id, name: ex.name, set: run.set+1, reps: hold ? null : getReps(ex), holdSec: hold || null, ts: Date.now() });
    const sets = getSets(ex);
    run.set++;
    const lastSet = run.set >= sets;
    const lastEx = run.i >= run.q.length - 1;
    if (lastSet && lastEx) { return finishSession(); }
    if (!lastSet && S.getPrefs().autoRepos && getRest(ex) > 0) { return renderRest(); }
    if (lastSet) { run.i++; run.set = 0; run.variant = false; }
    renderRun();
  };
  App_nextEx = function () { stopTimer(); if (run.i < run.q.length-1) { run.i++; run.set = 0; run.variant = false; renderRun(); } };
  App_prevEx = function () { stopTimer(); if (run.i > 0) { run.i--; run.set = 0; run.variant = false; renderRun(); } };
  App_toggleVariant = function () { run.variant = !run.variant; renderRun(); };
  App_pain = function () { const ex = run.q[run.i]; if (!run.pain.includes(ex.id)) run.pain.push(ex.id); run.variant = true; renderRun(); };
  App_quit = function () { if (confirm('Quitter la séance ? La progression en cours ne sera pas enregistrée.')) { stopTimer(); run = null; location.hash = '#/'; } };

  function renderRest() {
    run.mode = 'rest';
    const ex = run.q[run.i]; const rest = getRest(ex);
    setView(`
      <div class="rest">
        <div class="mono dim">REPOS</div>
        <div class="dial big">
          <svg viewBox="0 0 210 210"><circle class="ring-bg" cx="105" cy="105" r="95"/><circle class="ring-fg" id="ring" cx="105" cy="105" r="95"/></svg>
          <div class="dial-c"><div class="dial-big mono" id="clock">${fmt(rest)}</div><div class="dial-l mono">PROCHAINE : SÉRIE ${run.set+1}</div></div>
        </div>
        <div class="tadj">
          <button onclick="App.timerAdj(-10)">−10s</button>
          <button class="tgo" onclick="App.skipRest()">PASSER ▷</button>
          <button onclick="App.timerAdj(10)">+10s</button>
        </div>
        <div class="mono dim mt">Ensuite : ${esc(ex.name)}</div>
      </div>`);
    setNav(null);
    run.remain = rest; run.holdTotal = rest; run.paused = false; stopTimer();
    run.tid = setInterval(() => { run.remain--; tickTo('clock','ring',rest); if (run.remain <= 0) App_skipRest(); }, 1000);
  }
  App_skipRest = function () { stopTimer(); run.mode = 'exercise'; renderRun(); };

  function finishSession() {
    stopTimer();
    const durationSec = Math.round((Date.now() - run.startTs)/1000);
    S.saveWorkoutSession({ id:'w'+run.startTs, date:new Date().toISOString(), kind:run.kind, sessionId:run.sessionId,
      name:run.name, durationSec, sets:run.log, pain:run.pain });
    run.mode = 'done'; run._dur = durationSec; renderDone();
  }
  function renderDone() {
    const totalSets = run.log.length, painN = run.pain.length;
    setView(`
      <div class="done">
        <div class="done-mark">✓</div>
        <div class="done-h">Séance terminée</div>
        <div class="done-name mono">${esc(run.name)}</div>
        <div class="done-grid">
          <div><b>${fmt(run._dur)}</b><i>durée</i></div>
          <div><b>${totalSets}</b><i>séries</i></div>
          <div><b>${painN}</b><i>gênes</i></div>
        </div>
        ${painN ? `<div class="cue warn">Gêne notée. Reste sur la variante douce la prochaine fois — jamais forcer la douleur.</div>` : ''}
        <button class="btn-go" onclick="App.done()">RETOUR ACCUEIL</button>
      </div>`);
    setNav(null);
  }
  App_done = function () { run = null; location.hash = '#/'; };

  /* ---- routine rapide (enchaînement chronométré) ---- */
  App_quick = function () {
    const steps = PR.quick.steps;
    run = { kind:'quick', sessionId:'quick', name:'Routine 5 min', steps, i:0, mode:'quick', startTs:Date.now(), log:[], pain:[], tid:null, remain:0 };
    renderQuick();
  };
  function renderQuick() {
    stopTimer();
    if (run.i >= run.steps.length) { finishSession(); return; }
    const st = run.steps[run.i], ex = EX[st.exId];
    setView(`
      <div class="sess">
        <div class="sess-top mono"><span>${String(run.i+1).padStart(2,'0')} / ${String(run.steps.length).padStart(2,'0')}</span><span>ROUTINE 5 MIN</span></div>
        <div class="sess-name">${esc(st.label)}</div>
        <div class="sess-tag mono">${esc(ex.cat)}</div>
        <div class="media">${media(ex.media)}<span class="media-lbl mono">SVG · REPÈRE</span></div>
        <div class="dial"><svg viewBox="0 0 210 210"><circle class="ring-bg" cx="105" cy="105" r="95"/><circle class="ring-fg" id="ring" cx="105" cy="105" r="95"/></svg>
          <div class="dial-c"><div class="dial-big mono" id="clock">${fmt(st.sec)}</div><div class="dial-l mono">ÉTAPE</div></div></div>
        <div class="cue"><b>Consigne</b> ${esc(ex.cues[0])}</div>
        <div class="ctrl"><button class="c-sec" onclick="App.quitQuick()">✕</button><button class="c-go" onclick="App.nextQuick()">ÉTAPE SUIVANTE ▷</button></div>
      </div>`);
    setNav(null);
    run.remain = st.sec; run.holdTotal = st.sec;
    run.tid = setInterval(() => { run.remain--; tickTo('clock','ring',st.sec); if (run.remain <= 0) App_nextQuick(); }, 1000);
  }
  App_nextQuick = function () { stopTimer(); run.log.push({ exId:run.steps[run.i].exId, name:run.steps[run.i].label, set:1, reps:null, holdSec:run.steps[run.i].sec, ts:Date.now() }); run.i++; renderQuick(); };
  App_quitQuick = function () { stopTimer(); run = null; location.hash = '#/'; };

  App_logCardio = function () {
    const type = prompt('Course ou marche ? (course / marche)', 'marche'); if (!type) return;
    const min = parseInt(prompt('Durée en minutes ?', '30'), 10); if (!min) return;
    S.saveWorkoutSession({ id:'c'+Date.now(), date:new Date().toISOString(), kind:'cardio', sessionId:null,
      name: (type.toLowerCase().startsWith('c')?'Course':'Marche')+' '+min+' min', durationSec:min*60, sets:[], pain:[] });
    location.hash = '#/progress';
  };

  /* ============================================================= EXERCICES */
  function exercisesView() {
    const cats = [...new Set(D.EXERCISES.map(e => e.cat))];
    const list = cats.map(c => `
      <div class="ex-cat mono">${esc(c)}</div>
      ${D.EXERCISES.filter(e => e.cat === c).map(e => `
        <a class="ex-item" href="#/exercise/${e.id}">
          <div class="ex-thumb">${media(e.media)}</div>
          <div><div class="ex-n">${esc(e.name)}</div><div class="ex-m mono dim">${e.reps?e.reps[0]+'–'+e.reps[1]+' reps':getHold(e)+'s'} · ${e.sets} séries</div></div>
          <span class="dim">›</span>
        </a>`).join('')}`).join('');
    setView(`<header class="hd"><div class="hd-l">Exercices <span class="dim mono">/ ${D.EXERCISES.length}</span></div></header>${list}`);
    setNav('exercises');
  }
  function exerciseDetail(id) {
    const e = EX[id]; if (!e) return home();
    const p = S.getExPref(id);
    setView(`
      <header class="hd"><a class="back mono" href="#/exercises">← Exercices</a></header>
      <div class="media lg">${media(e.media)}</div>
      <div class="ex-title">${esc(e.name)}</div>
      <div class="sess-tag mono">${esc(e.cat)} · ${esc(e.level)} · ${esc(e.equipment)}</div>
      <div class="cue"><b>Objectif</b> ${esc(e.goal)}</div>
      <div class="cue"><b>Consignes</b> ${e.cues.map(esc).join(' · ')}</div>
      <div class="cue sub"><b>À éviter</b> ${e.mistakes.map(esc).join(' · ')}</div>
      <div class="cue"><b>Plus facile</b> ${esc(e.easier)}</div>
      <div class="cue"><b>Plus difficile</b> ${esc(e.harder)}</div>
      ${e.precaution ? `<div class="cue warn"><b>Précaution</b> ${esc(e.precaution)}</div>` : ''}
      <div class="ex-cat mono">RÉGLAGES (mémorisés)</div>
      ${e.reps ? adjRow('Répétitions', 'reps', getReps(e)) : ''}
      ${e.holdSec ? adjRow('Maintien (s)', 'hold', getHold(e)) : ''}
      ${adjRow('Séries', 'sets', getSets(e))}
      ${adjRow('Repos (s)', 'rest', getRest(e))}
      <label class="field"><span>Résistance élastique</span>
        <input class="inp" value="${esc(p.resistance||'')}" placeholder="ex. moyen / rouge" onchange="App.saveField('${id}','resistance',this.value)"></label>
    `);
    setNav('exercises');
  }
  function adjRow(label, key, val) {
    return `<div class="adj"><span>${label}</span><div class="stepper sm">
      <button onclick="App.adj('${key}',-1)">−</button><span class="mono adj-v" id="adj-${key}">${val}</span><button onclick="App.adj('${key}',1)">+</button>
    </div></div>`;
  }
  App_adj = function (key, d) {
    const id = location.hash.split('/')[2]; const e = EX[id];
    const map = { reps:getReps(e), hold:getHold(e), sets:getSets(e), rest:getRest(e) };
    const step = (key==='rest'||key==='hold') ? 5 : 1;
    let v = Math.max(0, (map[key]||0) + d*step);
    const patch = { reps:'repsChosen', hold:'holdSec', sets:'sets', rest:'restSec' }[key];
    S.saveExPref(id, { [patch]: v }); document.getElementById('adj-'+key).textContent = v;
  };
  App_saveField = function (id, key, val) { S.saveExPref(id, { [key]: val }); };

  /* ============================================================= PROGRÈS */
  function progress() {
    const all = S.getSessions();
    const wk = thisWeekSessions();
    const totalSec = all.reduce((a,s) => a + (s.durationSec||0), 0);
    // 6 dernières semaines
    const weeks = [];
    for (let i=5;i>=0;i--){ const d=new Date(); d.setDate(d.getDate()-i*7); weeks.push(isoWeek(d)); }
    const counts = weeks.map(w => all.filter(s => isoWeek(s.date)===w).length);
    const maxc = Math.max(1, ...counts);
    const bars = counts.map((c,i)=>`<div class="bar"><div class="bar-f" style="height:${Math.round(c/maxc*100)}%"></div><span class="mono">${c}</span></div>`).join('');
    const pains = all.flatMap(s => (s.pain||[]).map(id => EX[id]?.name)).filter(Boolean);
    setView(`
      <header class="hd"><div class="hd-l">Progrès</div></header>
      <div class="row2">
        <div class="stat"><div class="stat-v">${wk.length}</div><div class="stat-l">séances cette semaine</div></div>
        <div class="stat"><div class="stat-v">${Math.round(totalSec/60)}</div><div class="stat-l">minutes au total</div></div>
      </div>
      <div class="row2 mt">
        <div class="stat"><div class="stat-v">${streakWeeks()}</div><div class="stat-l">semaines de suite</div></div>
        <div class="stat"><div class="stat-v">${all.length}</div><div class="stat-l">séances enregistrées</div></div>
      </div>
      <div class="ex-cat mono">6 DERNIÈRES SEMAINES</div>
      <div class="bars">${bars}</div>
      ${pains.length ? `<div class="cue warn"><b>Gênes signalées</b> ${[...new Set(pains)].map(esc).join(' · ')}</div>` : ''}
      <div class="ex-cat mono">HISTORIQUE</div>
      ${all.length ? all.slice(0,20).map(s => `<div class="hist"><div><b>${esc(s.name)}</b><div class="mono dim">${new Date(s.date).toLocaleDateString('fr-FR')} · ${s.kind}</div></div><div class="mono">${fmt(s.durationSec||0)}</div></div>`).join('')
                   : `<div class="dim">Aucune séance pour l’instant.</div>`}
    `);
    setNav('progress');
  }

  /* ============================================================= RÉGLAGES */
  function settings() {
    const p = S.getProfile(), pr = S.getPrefs();
    setView(`
      <header class="hd"><div class="hd-l">Réglages</div></header>
      <div class="ex-cat mono">PROFIL</div>
      ${pf('Prénom','prenom',p.prenom)}${pf('Âge','age',p.age)}${pf('Taille (cm)','taille',p.taille)}
      ${pf('Niveau','niveau',p.niveau)}${pf('Matériel','materiel',p.materiel)}${pf('Contexte','contexte',p.contexte)}
      <div class="ex-cat mono">PRÉFÉRENCES</div>
      ${tg('Repos auto entre séries','autoRepos',pr.autoRepos)}
      ${tg('Vibration','vibration',pr.vibration)}
      ${tg('Son','son',pr.son)}
      <div class="ex-cat mono">MÉDIAS DES EXERCICES</div>
      <div class="note-box">Les démonstrations sont des repères SVG. Pour tes vraies vidéos : dépose des .mp4/.webm dans
        <code>str8/app/media-video/</code> puis mappe-les (voir README « Ajouter mes vidéos »). Import direct depuis l’appareil : à venir.</div>
      <div class="ex-cat mono">SAUVEGARDE</div>
      <div class="note-box">Les données sont enregistrées <b>sur cet appareil</b>. Pense à exporter une sauvegarde régulièrement.</div>
      <div class="row2">
        <button class="btn-line" onclick="App.exportJSON()">⭳ Export JSON</button>
        <button class="btn-line" onclick="document.getElementById('imp').click()">⭱ Import JSON</button>
      </div>
      <div class="row2 mt">
        <button class="btn-line" onclick="App.exportCSV()">⭳ Export CSV</button>
        <button class="btn-line danger" onclick="App.reset()">⟲ Réinitialiser</button>
      </div>
      <input type="file" id="imp" accept="application/json" style="display:none" onchange="App.importJSON(this.files[0])">
      <div class="ex-cat mono">SÉCURITÉ</div>
      <div class="note-box">Str8 propose une routine personnelle de mobilité et de renforcement. Elle ne remplace pas un suivi médical ou kinésithérapique. N’effectue pas un mouvement qui déclenche une douleur importante ou inhabituelle.</div>
      <div class="ver mono dim">Str8 v0.1 · PWA hors-ligne · aucune donnée envoyée</div>
    `);
    setNav('settings');
  }
  const pf = (label, key, val) => `<label class="field"><span>${label}</span><input class="inp" value="${esc(val)}" onchange="App.saveProfile('${key}',this.value)"></label>`;
  const tg = (label, key, on) => `<label class="field row"><span>${label}</span><input type="checkbox" ${on?'checked':''} onchange="App.savePref('${key}',this.checked)"></label>`;
  App_saveProfile = function (k, v) { const p = S.getProfile(); p[k] = v; S.saveProfile(p); };
  App_savePref = function (k, v) { const p = S.getPrefs(); p[k] = v; S.savePrefs(p); };

  App_exportJSON = function () { download('str8-sauvegarde.json', JSON.stringify(S.exportAll(), null, 2), 'application/json'); };
  App_exportCSV = function () {
    const rows = [['date','type','séance','durée_s','exercice','série','reps','maintien_s']];
    S.getSessions().forEach(s => { if (!s.sets.length) rows.push([s.date,s.kind,s.name,s.durationSec,'','','','']);
      s.sets.forEach(x => rows.push([s.date,s.kind,s.name,s.durationSec,x.name,x.set,x.reps??'',x.holdSec??''])); });
    download('str8-historique.csv', rows.map(r => r.map(c => `"${String(c).replace(/"/g,'""')}"`).join(',')).join('\n'), 'text/csv');
  };
  App_importJSON = function (file) { if (!file) return; const r = new FileReader();
    r.onload = () => { try { S.importAll(JSON.parse(r.result)); alert('Sauvegarde importée.'); location.hash = '#/'; route(); } catch (e) { alert('Import impossible : ' + e.message); } };
    r.readAsText(file); };
  App_reset = function () { if (confirm('Tout réinitialiser ? Cette action est irréversible. Pense à exporter d’abord.')) { S.reset(); location.hash = '#/'; route(); } };
  function download(name, content, type) {
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([content], { type })); a.download = name; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  }

  /* ============================================================= disclaimer */
  function maybeDisclaimer() {
    if (S.getFlags().disclaimerVu) return;
    const o = document.getElementById('overlay');
    o.innerHTML = `<div class="modal">
      <div class="modal-h">Avant de commencer</div>
      <p>Str8 propose une routine personnelle de mobilité et de renforcement. Elle ne remplace pas un suivi médical ou kinésithérapique. N’effectue pas un mouvement qui déclenche une douleur importante ou inhabituelle.</p>
      <p class="dim">L’app ne promet pas de corriger une cyphose structurelle : elle vise l’apparence, la fonction et la régularité.</p>
      <button class="btn-go" onclick="App.acceptDisclaimer()">J’ai compris</button></div>`;
    o.classList.add('on');
  }
  App_acceptDisclaimer = function () { S.setFlag('disclaimerVu', true); document.getElementById('overlay').classList.remove('on'); document.getElementById('overlay').innerHTML = ''; };

  /* ============================================================= shell */
  function setView(html) { view().innerHTML = html; view().scrollTop = 0; window.scrollTo(0,0); }
  function setNav(active) {
    const items = [['','Accueil','◠'],['exercises','Exos','☰'],['progress','Progrès','◔'],['settings','Réglages','○']];
    if (active === null) { nav().style.display = 'none'; return; }
    nav().style.display = 'flex';
    nav().innerHTML = items.map(([r,l,ic]) => `<a class="${active===(r||'home')||(active==='home'&&r==='')?'on':''}${(r===''&&active==='home')?' on':''}" href="#/${r}"><span class="ic">${ic}</span>${l}</a>`).join('');
  }

  function route() {
    if (run && ['session','quick'].includes(run.kind) && run.mode !== 'done' && location.hash.startsWith('#/session')) { renderRun(); return; }
    const parts = location.hash.replace(/^#\//,'').split('/');
    const r = parts[0] || '';
    if (r === 'exercise' && parts[1]) return exerciseDetail(parts[1]);
    if (r === 'quick') return App_quick();
    switch (r) {
      case '': return home();
      case 'exercises': return exercisesView();
      case 'progress': return progress();
      case 'settings': return settings();
      default: return home();
    }
  }

  // API publique (inline handlers)
  window.App = {
    start:App_start, quick:App_quick, prevEx:App_prevEx, nextEx:App_nextEx, validateSet:App_validateSet,
    repDelta:App_repDelta, setReps:App_setReps, toggleTimer:App_toggleTimer, timerAdj:App_timerAdj,
    skipRest:App_skipRest, pain:App_pain, toggleVariant:App_toggleVariant, quit:App_quit, done:App_done,
    nextQuick:App_nextQuick, quitQuick:App_quitQuick, logCardio:App_logCardio,
    adj:App_adj, saveField:App_saveField, saveProfile:App_saveProfile, savePref:App_savePref,
    exportJSON:App_exportJSON, exportCSV:App_exportCSV, importJSON:App_importJSON, reset:App_reset,
    acceptDisclaimer:App_acceptDisclaimer,
  };
  // hoisting des fonctions nommées ci-dessus
  var App_start, App_quick, App_prevEx, App_nextEx, App_validateSet, App_repDelta, App_setReps, App_toggleTimer,
      App_timerAdj, App_skipRest, App_pain, App_toggleVariant, App_quit, App_done, App_nextQuick, App_quitQuick,
      App_logCardio, App_adj, App_saveField, App_saveProfile, App_savePref, App_exportJSON, App_exportCSV,
      App_importJSON, App_reset, App_acceptDisclaimer;

  window.addEventListener('hashchange', route);
  window.addEventListener('DOMContentLoaded', () => { maybeDisclaimer(); route();
    if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js').catch(()=>{}); });
})();
