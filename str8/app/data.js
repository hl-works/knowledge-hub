/* Str8 — données : profil, 25 exercices, 3 séances, routine 5 min, programme 12 sem.
   Aucune promesse de « guérir » une cyphose structurelle. Repère personnel. */

const DEFAULT_PROFILE = {
  prenom: 'Hugo', age: 42, taille: 191,
  niveau: 'Reprise sportive',
  materiel: 'Élastiques de résistance',
  contexte: 'Déplacements fréquents / hôtels',
  dureeIdeale: '15–25 min',
  note: 'Cyphose structurelle · reprise progressive après blessure jambe',
};

/* champs par exo :
   id, name, cat, goal, equipment, level, reps[min,max]|null, sets, holdSec|null,
   restSec, cues[], mistakes[], easier, harder, precaution, media */
const EXERCISES = [
  { id:'band-pull-apart', name:'Band pull-apart', cat:'Renfo dos', goal:'Rétraction des omoplates, haut du dos', equipment:'Élastique', level:'Base', reps:[12,15], sets:3, holdSec:null, restSec:45,
    cues:['Bras tendus, ouvre depuis les omoplates','Ne creuse pas le bas du dos'], mistakes:['Tirer avec les mains','Hausser les épaules'], easier:'Élastique plus souple', harder:'Élastique plus dur / tempo lent', precaution:'', media:'bandOpen' },
  { id:'rowing-horizontal', name:'Rowing horizontal', cat:'Renfo dos', goal:'Milieu du dos, rhomboïdes', equipment:'Élastique', level:'Base', reps:[12,15], sets:3, holdSec:null, restSec:45,
    cues:['Coudes le long du corps, tire vers les hanches','Serre les omoplates en fin de course'], mistakes:['Arrondir le dos','Coudes qui partent trop haut'], easier:'Amplitude réduite', harder:'Pause 2 s en contraction', precaution:'', media:'row' },
  { id:'rowing-unilateral', name:'Rowing unilatéral', cat:'Renfo dos', goal:'Dos, correction des asymétries', equipment:'Élastique', level:'Base', reps:[10,12], sets:3, holdSec:null, restSec:45,
    cues:['Un bras à la fois, buste stable','Ne pivote pas le tronc'], mistakes:['Compenser en tournant','À-coups'], easier:'Appui sur un support', harder:'Tempo lent', precaution:'', media:'row' },
  { id:'face-pull', name:'Face pull', cat:'Renfo dos', goal:'Arrière d’épaule, trapèzes bas', equipment:'Élastique', level:'Base', reps:[12,15], sets:3, holdSec:null, restSec:45,
    cues:['Tire vers le visage, coudes hauts','Écarte les mains en fin de geste'], mistakes:['Coudes qui tombent','Tirer trop bas'], easier:'Élastique plus souple', harder:'Pause en fin d’amplitude', precaution:'', media:'faceHigh' },
  { id:'reverse-fly', name:'Reverse fly', cat:'Renfo dos', goal:'Arrière d’épaule, posture', equipment:'Élastique', level:'Base', reps:[12,15], sets:3, holdSec:null, restSec:45,
    cues:['Ouvre les bras en arc, coudes légers','Contrôle le retour'], mistakes:['Balancer le buste','Bloquer la respiration'], easier:'Amplitude réduite', harder:'Tempo 3 s retour', precaution:'', media:'bandOpen' },
  { id:'rotation-externe', name:'Rotation externe', cat:'Renfo dos', goal:'Coiffe des rotateurs, épaule', equipment:'Élastique', level:'Base', reps:[12,15], sets:3, holdSec:null, restSec:40,
    cues:['Coude collé au corps, ouvre l’avant-bras','Mouvement lent et contrôlé'], mistakes:['Décoller le coude','Aller trop vite'], easier:'Élastique très souple', harder:'Pause 2 s', precaution:'Stop si pincement d’épaule', media:'row' },
  { id:'y-raise', name:'Y raise', cat:'Renfo dos', goal:'Trapèzes bas, épaules', equipment:'Élastique', level:'Intermédiaire', reps:[10,12], sets:3, holdSec:null, restSec:45,
    cues:['Monte les bras en Y, pouces vers le haut','Épaules basses'], mistakes:['Hausser les épaules','Cambrer'], easier:'Sans élastique', harder:'Pause en haut', precaution:'', media:'faceHigh' },
  { id:'pull-apart-diagonal', name:'Pull-apart diagonal', cat:'Renfo dos', goal:'Haut du dos en diagonale', equipment:'Élastique', level:'Intermédiaire', reps:[10,12], sets:3, holdSec:null, restSec:45,
    cues:['Ouvre en diagonale haut/bas','Change de côté chaque série'], mistakes:['Perdre la ligne','À-coups'], easier:'Amplitude réduite', harder:'Tempo lent', precaution:'', media:'faceHigh' },
  { id:'wall-slide', name:'Wall slide', cat:'Mobilité', goal:'Mobilité d’épaule, glissé au mur', equipment:'Mur', level:'Base', reps:[8,10], sets:3, holdSec:null, restSec:40,
    cues:['Dos, bras et poignets au mur','Monte sans décoller'], mistakes:['Cambrer pour tricher','Décoller les poignets'], easier:'Amplitude réduite', harder:'Pause en haut', precaution:'', media:'wallslide' },
  { id:'cat-cow', name:'Cat-cow', cat:'Mobilité', goal:'Mobilité du rachis', equipment:'Sol', level:'Base', reps:[8,10], sets:2, holdSec:null, restSec:30,
    cues:['Alterne arrondi et creux en douceur','Respire avec le mouvement'], mistakes:['Forcer l’amplitude','Bloquer la nuque'], easier:'Amplitude réduite', harder:'Tempo très lent', precaution:'', media:'catcow' },
  { id:'rotation-thoracique', name:'Rotation thoracique', cat:'Mobilité', goal:'Rotation du haut du dos', equipment:'Sol', level:'Base', reps:[8,10], sets:2, holdSec:null, restSec:30,
    cues:['Main derrière la tête, ouvre le coude vers le plafond','Bassin stable'], mistakes:['Tourner depuis le bas du dos','Forcer le cou'], easier:'Amplitude réduite', harder:'Pause en ouverture', precaution:'', media:'rotation' },
  { id:'thread-the-needle', name:'Thread the needle', cat:'Mobilité', goal:'Rotation thoracique, épaule', equipment:'Sol', level:'Base', reps:[8,10], sets:2, holdSec:null, restSec:30,
    cues:['Passe le bras sous le corps puis ouvre','Mouvement lent'], mistakes:['Forcer','Retenir sa respiration'], easier:'Amplitude réduite', harder:'Pause en fin de course', precaution:'', media:'rotation' },
  { id:'extension-thoracique-chaise', name:'Extension thoracique sur chaise', cat:'Mobilité', goal:'Extension du haut du dos', equipment:'Chaise', level:'Base', reps:null, sets:2, holdSec:30, restSec:30,
    cues:['Ouvre depuis le sternum, menton rentré','Ne force pas le bas du dos'], mistakes:['Cambrer les lombaires','Pousser la tête en arrière'], easier:'Amplitude réduite', harder:'Maintien plus long', precaution:'Douceur si gêne cervicale', media:'seatedExt' },
  { id:'etirement-pectoral', name:'Étirement pectoral', cat:'Étirement', goal:'Ouverture de la poitrine', equipment:'Encadrement', level:'Base', reps:null, sets:2, holdSec:30, restSec:20,
    cues:['Avant-bras contre l’appui, avance doucement','Respire lentement'], mistakes:['Étirement brusque','Hausser l’épaule'], easier:'Moins d’amplitude', harder:'Maintien plus long', precaution:'Stop si tiraillement à l’épaule', media:'pec' },
  { id:'bird-dog', name:'Bird dog', cat:'Gainage', goal:'Gainage + extenseurs du dos', equipment:'Sol', level:'Base', reps:[8,10], sets:3, holdSec:null, restSec:40,
    cues:['Bras et jambe opposés, dos neutre','Ne bascule pas le bassin'], mistakes:['Cambrer','Aller trop vite'], easier:'Bras seul puis jambe seule', harder:'Pause 3 s en extension', precaution:'', media:'quad' },
  { id:'dead-bug', name:'Dead bug', cat:'Gainage', goal:'Gainage profond', equipment:'Sol', level:'Base', reps:[8,10], sets:3, holdSec:null, restSec:40,
    cues:['Bas du dos plaqué au sol','Descends bras/jambe opposés lentement'], mistakes:['Décoller les lombaires','Retenir sa respiration'], easier:'Jambes seules', harder:'Amplitude complète, tempo lent', precaution:'', media:'deadbug' },
  { id:'planche-genoux', name:'Planche sur genoux', cat:'Gainage', goal:'Gainage antérieur', equipment:'Sol', level:'Base', reps:null, sets:3, holdSec:20, restSec:45,
    cues:['Ligne épaules-hanches-genoux','Serre les abdos et les fessiers'], mistakes:['Bassin qui tombe','Fesses en l’air'], easier:'Maintien plus court', harder:'Planche classique', precaution:'', media:'plank' },
  { id:'planche-classique', name:'Planche classique', cat:'Gainage', goal:'Gainage antérieur', equipment:'Sol', level:'Intermédiaire', reps:null, sets:3, holdSec:30, restSec:45,
    cues:['Corps aligné, regard au sol','Respiration continue'], mistakes:['Cambrer','Bloquer la respiration'], easier:'Sur les genoux', harder:'Maintien plus long', precaution:'', media:'plank' },
  { id:'side-plank-genoux', name:'Side plank sur genoux', cat:'Gainage', goal:'Obliques, stabilité', equipment:'Sol', level:'Base', reps:null, sets:2, holdSec:20, restSec:40,
    cues:['Appui coude sous l’épaule','Hanches hautes, corps aligné'], mistakes:['Hanches qui tombent','Tête projetée en avant'], easier:'Maintien plus court', harder:'Jambes tendues', precaution:'', media:'sideplank' },
  { id:'side-plank-classique', name:'Side plank classique', cat:'Gainage', goal:'Obliques, stabilité', equipment:'Sol', level:'Intermédiaire', reps:null, sets:2, holdSec:30, restSec:40,
    cues:['Corps en ligne, hanches hautes','Épaule loin de l’oreille'], mistakes:['Bassin bas','Rotation du buste'], easier:'Sur les genoux', harder:'Maintien plus long', precaution:'', media:'sideplank' },
  { id:'hip-hinge', name:'Hip hinge', cat:'Posture', goal:'Charnière de hanche, chaîne postérieure', equipment:'Élastique', level:'Base', reps:[10,12], sets:3, holdSec:null, restSec:45,
    cues:['Pousse les hanches en arrière, dos neutre','Genoux légèrement fléchis'], mistakes:['Arrondir le dos','Plier depuis les lombaires'], easier:'Amplitude réduite', harder:'Élastique plus dur', precaution:'Stop si douleur lombaire', media:'hinge' },
  { id:'good-morning', name:'Good morning léger', cat:'Posture', goal:'Extenseurs du dos, ischios', equipment:'Élastique', level:'Intermédiaire', reps:[10,12], sets:3, holdSec:null, restSec:45,
    cues:['Charnière de hanche, dos gainé','Léger, contrôlé'], mistakes:['Arrondir le dos','Descendre trop bas'], easier:'Sans élastique', harder:'Élastique plus dur', precaution:'Léger — jamais de douleur lombaire', media:'hinge' },
  { id:'cobra-leger', name:'Cobra léger', cat:'Mobilité', goal:'Extension douce du dos', equipment:'Sol', level:'Base', reps:[6,8], sets:2, holdSec:null, restSec:30,
    cues:['Ouvre depuis le haut du dos, coudes souples','Épaules basses'], mistakes:['Forcer les lombaires','Contracter la nuque'], easier:'Sur les avant-bras', harder:'Maintien 3 s en haut', precaution:'Variante douce si gêne lombaire', media:'cobra' },
  { id:'maintien-isometrique', name:'Maintien isométrique', cat:'Gainage', goal:'Endurance posturale', equipment:'Élastique', level:'Base', reps:null, sets:3, holdSec:30, restSec:40,
    cues:['Tiens la position sans bouger','Respiration régulière'], mistakes:['Retenir sa respiration','Perdre la posture'], easier:'Maintien plus court', harder:'Maintien plus long', precaution:'', media:'iso' },
  { id:'respiration-costale', name:'Respiration costale', cat:'Respiration', goal:'Respiration thoracique, détente', equipment:'Aucun', level:'Base', reps:null, sets:1, holdSec:60, restSec:0,
    cues:['Mains sur les côtes, inspire en les écartant','Expire lentement'], mistakes:['Monter les épaules','Respiration trop rapide'], easier:'Assis contre un dossier', harder:'Cycles plus longs', precaution:'', media:'breath' },
];

const byId = Object.fromEntries(EXERCISES.map(e => [e.id, e]));

const PROGRAM = {
  weeks: 12,
  sessionsPerWeek: 3,
  duration: '15–25 min',
  sessions: {
    A: { id:'A', name:'Haut du dos', focus:'Renforcement du haut du dos', exercises:[
      'respiration-costale','band-pull-apart','rowing-horizontal','face-pull','reverse-fly','rotation-externe','bird-dog','etirement-pectoral' ] },
    B: { id:'B', name:'Extension & gainage', focus:'Extension thoracique et gainage', exercises:[
      'respiration-costale','cat-cow','rotation-thoracique','extension-thoracique-chaise','cobra-leger','hip-hinge','dead-bug','planche-genoux','etirement-pectoral' ] },
    C: { id:'C', name:'Posture globale', focus:'Posture globale', exercises:[
      'wall-slide','rowing-unilateral','face-pull','rotation-externe','y-raise','pull-apart-diagonal','good-morning','maintien-isometrique','side-plank-genoux','respiration-costale' ] },
  },
  // routine rapide 5 min : enchaînement chronométré
  quick: { id:'quick', name:'Routine 5 min', steps:[
    { exId:'respiration-costale', sec:40, label:'Respiration lente' },
    { exId:'band-pull-apart',     sec:40, label:'Band pull-apart' },
    { exId:'rotation-thoracique', sec:40, label:'Rotations thoraciques' },
    { exId:'rowing-horizontal',   sec:40, label:'Rétractions d’omoplates' },
    { exId:'etirement-pectoral',  sec:45, label:'Étirement pectoral' },
    { exId:'maintien-isometrique',sec:30, label:'Menton rentré, posture' },
    { exId:'respiration-costale', sec:35, label:'Posture debout détendue' },
  ] },
  // ordre suggéré de la semaine
  weekOrder: ['A','B','C'],
};

if (typeof window !== 'undefined') {
  window.STR8_DATA = { DEFAULT_PROFILE, EXERCISES, byId, PROGRAM };
}
