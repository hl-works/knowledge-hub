// Prononciations pré-générées (TTS, MP3 joués au clic), résolues par
// scripts/gen_audio.py dans public/fixtures/audio.json :
//   { "<tl>|<mot_local>": "id-01.mp3" }   (fichiers sous fixtures/audio/)
// Qualité homogène sur tous les appareils ; le site retombe sur la voix native
// du navigateur si un mot n'a pas de fichier (cas du mongol).

let map: Record<string, string> = {};
let dir = '';

export async function loadAudio(): Promise<void> {
  try {
    const base = import.meta.env.BASE_URL.replace(/\/$/, '');
    dir = `${base}/fixtures/audio/`;
    const res = await fetch(`${base}/fixtures/audio.json`);
    if (res.ok) map = await res.json();
  } catch {
    map = {};
  }
}

/** URL du MP3 pour (code TTS, mot local), ou undefined si non pré-généré. */
export function audioUrl(tl: string, text: string): string | undefined {
  const f = tl ? map[`${tl}|${text}`] : undefined;
  return f ? dir + f : undefined;
}
