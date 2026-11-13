// FOLLOW THE GREEN — réception des événements et des participations dans Google Sheets.
// À coller dans Extensions > Apps Script depuis le Google Sheet qui doit stocker les données.

const SHEET_EVENTS = 'events';
const SHEET_ENTRIES = 'participations';

function doPost(e) {
  const p = (e && e.parameter) || {};
  const lock = LockService.getScriptLock();
  try {
    lock.waitLock(10000);
  } catch (err) {
    return text_('occupé');
  }
  try {
    if (p.type === 'entry') return text_(handleEntry_(p));
    handleEvent_(p);
    return text_('ok');
  } catch (err) {
    return text_('error');
  } finally {
    lock.releaseLock();
  }
}

function doGet() { return text_('FOLLOW THE GREEN endpoint OK'); }
function text_(s) { return ContentService.createTextOutput(s); }
function safe_(v) { const s = String(v == null ? '' : v); return /^[=+\-@]/.test(s) ? "'" + s : s; }

function handleEvent_(p) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(SHEET_EVENTS) || initEvents_(ss);
  const known = ['game', 'sessionId', 'event', 't', 'place', 'route', 'type'];
  const rest = {};
  Object.keys(p).forEach(function (k) { if (known.indexOf(k) < 0) rest[k] = p[k]; });
  sheet.appendRow([new Date(), p.sessionId || '', p.event || '', Number(p.t) || 0, p.place || '', p.route || '', JSON.stringify(rest)]);
}

// Les contacts sont stockés à part, sans identifiant de session : on ne relie pas comportement et identité.
function handleEntry_(p) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(SHEET_ENTRIES) || initEntries_(ss);
  const contact = String(p.contact || '').trim().toLowerCase().slice(0, 120);
  const name = String(p.name || '').trim().slice(0, 80);
  if (!contact || !name) return 'invalide';
  const existing = sheet.getLastRow() > 1
    ? sheet.getRange(2, 3, sheet.getLastRow() - 1, 1).getValues().map(function (r) { return String(r[0]).toLowerCase(); })
    : [];
  const status = existing.indexOf(contact) >= 0 ? 'doublon' : (hasEnded_(ss, p.sessionId) ? 'ok' : 'à vérifier');
  sheet.appendRow([new Date(), safe_(name), safe_(contact), p.contactType || '', p.profile || '', Number(p.posters) || 0, status]);
  return status;
}

function hasEnded_(ss, sessionId) {
  const sh = ss.getSheetByName(SHEET_EVENTS);
  if (!sh || !sessionId || sh.getLastRow() < 2) return false;
  return sh.getRange(2, 2, sh.getLastRow() - 1, 2).getValues().some(function (r) { return r[0] === sessionId && r[1] === 'end'; });
}

function initEvents_(ss) {
  const sheet = ss.insertSheet(SHEET_EVENTS);
  sheet.appendRow(['Reçu le', 'Session', 'Événement', 'Temps (s)', 'Lieu', 'Chemin', 'Détails (JSON)']);
  sheet.setFrozenRows(1);
  return sheet;
}

function initEntries_(ss) {
  const sheet = ss.insertSheet(SHEET_ENTRIES);
  sheet.appendRow(['Reçu le', 'Prénom / nom / pseudo', 'Contact', 'Type', 'Profil', 'Affiches', 'Statut']);
  sheet.setFrozenRows(1);
  return sheet;
}

// À lancer à la main le jour du tirage : 2 gagnant·es + 2 suppléant·es parmi les participations "ok".
function tirer() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(SHEET_ENTRIES);
  if (!sheet) return;
  const rows = sheet.getDataRange().getValues().slice(1).filter(function (r) { return r[6] === 'ok'; });
  for (let i = rows.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const tmp = rows[i]; rows[i] = rows[j]; rows[j] = tmp;
  }
  const out = ss.getSheetByName('tirage') || ss.insertSheet('tirage');
  out.clear();
  out.appendRow(['Rang', 'Prénom / nom / pseudo', 'Contact', 'Type']);
  rows.slice(0, 4).forEach(function (r, i) {
    out.appendRow([i < 2 ? 'GAGNANT·E ' + (i + 1) : 'SUPPLÉANT·E ' + (i - 1), r[1], r[2], r[3]]);
  });
}

// À lancer après le tirage : supprime tous les contacts de l'onglet "participations".
function purgerContacts() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_ENTRIES);
  if (sheet && sheet.getLastRow() > 1) sheet.deleteRows(2, sheet.getLastRow() - 1);
}

function count_(event, place, route) {
  let cond = 'events!C2:C="' + event + '"';
  if (place) cond += ',events!E2:E="' + place + '"';
  if (route) cond += ',events!F2:F="' + route + '"';
  return '=IFERROR(COUNTUNIQUE(FILTER(events!B2:B,' + cond + ')),0)';
}

// À lancer une fois à la main : crée l'onglet "stats" avec l'entonnoir (joueurs uniques par étape).
function setupStats() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  if (!ss.getSheetByName(SHEET_EVENTS)) initEvents_(ss);
  const sheet = ss.getSheetByName('stats') || ss.insertSheet('stats');
  sheet.clear();
  const steps = [
    ['Démarrage', count_('start')],
    ['Cour (après intro)', count_('location', 'courtyard')],
    ['Premier objet', count_('first_item')],
    ['Van', count_('location', 'alcove')],
    ['Régie', count_('location', 'local')],
    ['Tram', count_('location', 'tram')],
    ['Serre', count_('location', 'greenhouse')],
    ['Chemin passage de service', count_('route', null, 'vines')],
    ['Chemin voix de DRIIA', count_('route', null, 'signal')],
    ['Chemin marques sous les rails', count_('route', null, 'sewer')],
    ['Karmen Camina', count_('location', 'karmen')],
    ['Salle (scène finale)', count_('location', 'final')],
    ['Fin (profil affiché)', count_('end')],
    ['A lu une affiche', count_('poster')],
    ['A vu un indice automatique', count_('auto_hint')],
    ['A utilisé le ?', count_('hint')],
    ['S\'est heurté·e à un blocage', count_('blocked')],
    ['Clic billetterie', count_('ticket_click')],
    ['Inscrit·e au tirage', count_('entry_submit')]
  ];
  sheet.appendRow(['ÉTAPE', 'JOUEUR·EUSES UNIQUES', '% DES DÉMARRAGES']);
  steps.forEach(function (s, i) { sheet.appendRow([s[0], s[1], '=IFERROR(B' + (i + 2) + '/$B$2,0)']); });
  sheet.getRange(2, 3, steps.length, 1).setNumberFormat('0%');
  sheet.setFrozenRows(1);
  sheet.autoResizeColumns(1, 3);
}
