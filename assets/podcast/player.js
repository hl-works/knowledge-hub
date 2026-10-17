(() => {
  const panel = document.getElementById('daily-podcast');
  if (!panel) return;
  const players = ['short', 'full'].map(name => document.getElementById(`podcast-${name}`));
  const fallback = document.getElementById('podcast-fallback');
  let episode;
  function renderDate() {
    if (!episode) return;
    const lang = document.documentElement.dataset.lang === 'en' ? 'en-GB' : 'fr-FR';
    const date = document.getElementById('podcast-date');
    date.dateTime = episode.date;
    date.textContent = new Intl.DateTimeFormat(lang, {day:'numeric', month:'long', year:'numeric', timeZone:'UTC'}).format(new Date(`${episode.date}T12:00:00Z`));
  }
  players.forEach(player => {
    player.addEventListener('play', () => players.forEach(other => { if (other !== player) other.pause(); }));
    player.addEventListener('error', () => { fallback.hidden = false; });
  });
  fetch('/assets/podcast/latest.json', {cache: 'no-cache'})
    .then(response => { if (!response.ok) throw new Error('Unavailable'); return response.json(); })
    .then(data => {
      if (!/^\d{4}-\d{2}-\d{2}$/.test(data.date) || !Number.isFinite(Date.parse(`${data.date}T12:00:00Z`))) throw new Error('Invalid date');
      ['short', 'full'].forEach(name => {
        const track = data[name];
        if (!track || !Number.isFinite(track.seconds) || track.seconds <= 0 || track.src !== `/assets/podcast/${name}.mp3`) throw new Error('Invalid audio');
      });
      episode = data;
      renderDate();
      ['short', 'full'].forEach((name, index) => {
        const track = data[name];
        players[index].src = `${track.src}?v=${encodeURIComponent(data.version || data.date)}`;
        document.getElementById(`podcast-${name}-duration`).textContent = `${Math.floor(track.seconds / 60)} min ${String(track.seconds % 60).padStart(2, '0')}`;
        const cover = document.querySelector(`[data-radio-cover="${name}"]`);
        if (cover) {
          const timing = `${Math.floor(track.seconds / 60)}:${String(track.seconds % 60).padStart(2, '0')}`;
          cover.querySelector('.duration-minutes').textContent = Math.floor(track.seconds / 60);
          cover.querySelector('.duration-seconds').textContent = String(track.seconds % 60).padStart(2, '0');
          cover.querySelector('.cover-date strong').textContent = data.date.split('-').reverse().join('.');
          cover.querySelector('.podcast-cover').setAttribute('aria-label', `Le Podcast iA, ${name === 'short' ? 'Le Flash' : 'Le Débrief'}, ${data.date}, ${timing}`);
          const portrait = cover.querySelector('.cover-portrait');
          portrait.onload = () => { portrait.hidden = false; };
          portrait.onerror = () => { portrait.hidden = true; };
          portrait.src = `/assets/podcast/art/iastro-${data.date.slice(5, 7)}-v1.png`;
        }
      });
      document.getElementById('podcast-tracks').hidden = false;
      fallback.hidden = true;
    }).catch(() => { fallback.hidden = false; });
  new MutationObserver(renderDate).observe(document.documentElement, {attributes:true, attributeFilter:['data-lang']});
})();
