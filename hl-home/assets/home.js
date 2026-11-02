document.documentElement.classList.add('js');
const toggle = document.querySelector('.menu-toggle');
const menu = document.querySelector('#site-menu');
if (toggle && menu) {
  const closeMenu = (returnFocus = false) => {
    menu.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Ouvrir le menu');
    if (returnFocus) toggle.focus();
  };
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    menu.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
  });
  menu.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && menu.classList.contains('is-open')) closeMenu(true); });
  document.addEventListener('click', event => { if (!event.target.closest('.site-header')) closeMenu(); });
  document.addEventListener('focusin', event => { if (!event.target.closest('.site-header')) closeMenu(); });
  matchMedia('(min-width: 851px)').addEventListener('change', event => { if (event.matches) closeMenu(); });
}
// Arithmetic only: the installer supplies all dimensions, including manufacturer clearances.
const measureForm = document.querySelector('#measure-form');
if (measureForm) {
  const result = document.querySelector('#measure-result');
  const fields = [...measureForm.querySelectorAll('input')];
  const display = value => value.toLocaleString('fr-FR', { maximumFractionDigits: 2 });
  const update = () => {
    const values = fields.map(field => field.value.trim() === '' ? NaN : Number(field.value));
    if (values.some(value => !Number.isFinite(value) || value < 0) || values.slice(0,2).some(value => value <= 0) || values[2] <= 0) {
      result.textContent = 'Renseigne les cinq cotes relevées et les dégagements de la notice pour calculer la largeur résiduelle. Aucune valeur de sécurité n’est présupposée.';
      return;
    }
    const [width, depth, rear, front, maintenance] = values;
    const residual = width - rear - depth - Math.max(front, maintenance);
    result.textContent = residual < 0
      ? `Il manque ${display(-residual)} m : cette configuration ne tient pas dans la largeur saisie. Revoir le matériel ou l’emplacement ; ne pas réduire les dégagements.`
      : `Largeur résiduelle théorique : ${display(residual)} m après réservations. Ce résultat vérifie seulement la largeur ; il ne valide ni la ventilation réelle, ni le passage, ni les zones de protection, ni la longueur du mur.`;
  };
  measureForm.addEventListener('input', update);
  measureForm.addEventListener('submit', event => event.preventDefault());
  update();
}

// The standalone drawings share a millimetre-based geometry; controls only choose the variant.
const batterySize = document.querySelector('#battery-size');
if (batterySize) {
  const screenToggle = document.querySelector('#screen-toggle');
  const drawing = document.querySelector('#elevation-image');
  const fullDrawing = document.querySelector('#elevation-link');
  const caption = document.querySelector('#simulation-caption');
  const variants = {11: ['11,04',4,1228,842], 13: ['13,80',5,1461,609], 16: ['16,56',6,1694,376]};
  function renderSimulation() {
    const key = batterySize.value;
    const screened = screenToggle.getAttribute('aria-pressed') === 'true';
    const [capacity,modules,height,space] = variants[key];
    const src = '../../assets/mur-nord-elevation' + (key === '13' ? '' : '-' + key) + (screened ? '-habillage' : '') + '.svg?v=20261102-5';
    drawing.src = src;
    fullDrawing.href = src;
    drawing.alt = `Simulation cotée : batterie de ${capacity} kWh et onduleur à gauche ; trois Daikin et groupe Calypso à droite. ${screened ? 'Habillage vert visible.' : 'Équipements visibles.'}`;
    caption.textContent = `${capacity} kWh : ${modules} modules, batterie haute de ${height.toLocaleString('fr-FR')} mm. Espace entre le haut de l’onduleur et la réserve haute : ${space} mm. Simulation non validée pour exécution.`;
    screenToggle.textContent = screened ? 'Voir les équipements' : 'Afficher l’habillage vert';
  }
  batterySize.addEventListener('change', renderSimulation);
  screenToggle.addEventListener('click', () => {screenToggle.setAttribute('aria-pressed', screenToggle.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');renderSimulation();});
}
