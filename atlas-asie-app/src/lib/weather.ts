// Météo via Open-Meteo (gratuit, sans clé). Appel côté client par lat/lng.
export type WxCat = 'clear' | 'cloud' | 'fog' | 'rain' | 'snow' | 'storm';

export interface Weather {
  temp: number;
  cat: WxCat;
  label: string;
}

// Codes WMO -> catégorie + libellé FR.
function classify(code: number): { cat: WxCat; label: string } {
  if (code === 0) return { cat: 'clear', label: 'Ensoleillé' };
  if (code <= 3) return { cat: 'cloud', label: 'Nuageux' };
  if (code === 45 || code === 48) return { cat: 'fog', label: 'Brouillard' };
  if (code >= 51 && code <= 67) return { cat: 'rain', label: 'Pluie' };
  if (code >= 71 && code <= 77) return { cat: 'snow', label: 'Neige' };
  if (code >= 80 && code <= 82) return { cat: 'rain', label: 'Averses' };
  if (code >= 85 && code <= 86) return { cat: 'snow', label: 'Averses de neige' };
  if (code >= 95) return { cat: 'storm', label: 'Orage' };
  return { cat: 'cloud', label: 'Variable' };
}

export async function fetchWeather(lat: number, lng: number): Promise<Weather | null> {
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lng}&current=temperature_2m,weather_code&timezone=auto`;
  try {
    const res = await fetch(url);
    if (!res.ok) return null;
    const j = await res.json();
    const cur = j.current;
    if (!cur) return null;
    const { cat, label } = classify(Number(cur.weather_code));
    return { temp: Math.round(Number(cur.temperature_2m)), cat, label };
  } catch {
    return null;
  }
}

// Petits pictos SVG (pas d'emoji structurel).
export function weatherIcon(cat: WxCat): string {
  const s = (inner: string) =>
    `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${inner}</svg>`;
  switch (cat) {
    case 'clear':
      return s('<circle cx="12" cy="12" r="4.5"/><path d="M12 2v2M12 20v2M4 12H2M22 12h-2M5 5l1.5 1.5M17.5 17.5 19 19M19 5l-1.5 1.5M6.5 17.5 5 19"/>');
    case 'rain':
      return s('<path d="M17 15a4 4 0 0 0-1-7.9A5 5 0 0 0 6.5 9 3.5 3.5 0 0 0 7 16"/><path d="M8 19l-1 2M12 19l-1 2M16 19l-1 2"/>');
    case 'snow':
      return s('<path d="M17 14a4 4 0 0 0-1-7.9A5 5 0 0 0 6.5 8 3.5 3.5 0 0 0 7 15"/><path d="M9 19h.01M12 20h.01M15 19h.01"/>');
    case 'storm':
      return s('<path d="M17 13a4 4 0 0 0-1-7.9A5 5 0 0 0 6.5 7 3.5 3.5 0 0 0 7 14"/><path d="m12 12-2 4h3l-2 4"/>');
    case 'fog':
      return s('<path d="M4 9h16M6 13h12M4 17h16"/>');
    default:
      return s('<path d="M17 17a4 4 0 0 0-1-7.9A5 5 0 0 0 6.5 11 3.5 3.5 0 0 0 7 18h10Z"/>');
  }
}
