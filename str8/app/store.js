/* Str8 — couche de stockage abstraite.
   Aujourd'hui : LocalStorageAdapter. Demain on peut brancher une base distante
   sans réécrire l'app (même interface). */

const K = {
  profile:  'str8:profile',
  prefs:    'str8:prefs',      // { son, vibration, autoRepos }
  exPrefs:  'str8:exPrefs',    // overrides par exo : { [id]: {reps,sets,holdSec,restSec,resistance} }
  sessions: 'str8:sessions',   // historique [{...WorkoutSession}]
  flags:    'str8:flags',      // { disclaimerVu:true }
};

class LocalStorageAdapter {
  _get(k, def) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : def; } catch { return def; } }
  _set(k, v)   { localStorage.setItem(k, JSON.stringify(v)); }

  getProfile()      { return this._get(K.profile, { ...window.STR8_DATA.DEFAULT_PROFILE }); }
  saveProfile(p)    { this._set(K.profile, p); }

  getPrefs()        { return this._get(K.prefs, { son:true, vibration:true, autoRepos:true }); }
  savePrefs(p)      { this._set(K.prefs, p); }

  getExPrefs()      { return this._get(K.exPrefs, {}); }
  getExPref(id)     { return this.getExPrefs()[id] || {}; }
  saveExPref(id, patch) { const all = this.getExPrefs(); all[id] = { ...all[id], ...patch }; this._set(K.exPrefs, all); }

  getSessions()     { return this._get(K.sessions, []); }
  saveWorkoutSession(s) { const all = this.getSessions(); all.unshift(s); this._set(K.sessions, all); }

  getFlags()        { return this._get(K.flags, {}); }
  setFlag(k, v)     { const f = this.getFlags(); f[k] = v; this._set(K.flags, f); }

  // export / import / reset
  exportAll() {
    return {
      _app:'str8', _version:1, _exported:new Date().toISOString(),
      profile:this.getProfile(), prefs:this.getPrefs(),
      exPrefs:this.getExPrefs(), sessions:this.getSessions(), flags:this.getFlags(),
    };
  }
  importAll(obj) {
    if (!obj || obj._app !== 'str8') throw new Error('Fichier Str8 invalide');
    if (obj.profile)  this._set(K.profile, obj.profile);
    if (obj.prefs)    this._set(K.prefs, obj.prefs);
    if (obj.exPrefs)  this._set(K.exPrefs, obj.exPrefs);
    if (obj.sessions) this._set(K.sessions, obj.sessions);
    if (obj.flags)    this._set(K.flags, obj.flags);
  }
  reset() { Object.values(K).forEach(k => localStorage.removeItem(k)); }
}

if (typeof window !== 'undefined') window.Store = new LocalStorageAdapter();
