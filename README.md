# FOLLOW THE GREEN

Jeu point-and-click non linéaire conçu pour **SPECTR × KEEP HUSH** au **Karmen Camina**, le **20 novembre 2026**.

Le jeu fonctionne uniquement avec HTML, CSS et JavaScript : aucune installation et aucun build ne sont nécessaires.

## Mettre le jeu sur GitHub Pages

1. Crée un nouveau dépôt GitHub public.
2. Dans le dépôt, clique sur **Add file**, puis **Upload files**.
3. Dépose directement le contenu de ce dossier. `index.html` doit être à la racine du dépôt, pas dans un sous-dossier.
4. Clique sur **Commit changes**.
5. Ouvre **Settings**, puis **Pages**.
6. Dans **Build and deployment**, choisis **Deploy from a branch**.
7. Sélectionne la branche **main**, le dossier **/(root)**, puis clique sur **Save**.
8. GitHub affichera ensuite l'adresse publique du jeu, généralement sous cette forme :
   `https://TON-PSEUDO.github.io/NOM-DU-DEPOT/`

## Organisation des fichiers

- `index.html` : structure des trois écrans du jeu.
- `styles.css` : esthétique, responsive et mise en page.
- `game.js` : histoire, objets, déplacements, profils et export Story.
- `assets/` : `scenes/` (décors), `sprites/` (objets et personnages), `audio/` (extraits MP3 du morceau), logos Keep Hush et SPECTR × KEEP HUSH.
- `tools/` : scripts Python qui génèrent les décors et les sprites.
- `apps-script/Code.gs` : script Google Sheets qui reçoit les événements (à coller dans Apps Script, le site ne l'utilise pas).
- `PROMPT_IA.md` : résumé complet à transmettre à une IA pour continuer le projet.

## Connecter le jeu à Google Sheets

Dans `game.js`, remplace la valeur vide située au début du fichier :

```js
const RESULT_ENDPOINT = "";
```

par l'URL de ton déploiement Google Apps Script :

```js
const RESULT_ENDPOINT = "https://script.google.com/macros/s/TON-ID/exec";
```

Le jeu enverra alors le profil, le score, le chemin, les objets, les découvertes et le temps de jeu à ton script.

## Modifier les informations de la soirée

- La ligne visible en bas du résultat se trouve dans `index.html`.
- Les informations inscrites sur l'image Story se trouvent vers la fin de `game.js`.
- Les textes, objets et chemins sont principalement regroupés dans `game.js`.

## Important

Conserve les noms des dossiers et les chemins relatifs des images. GitHub distingue les majuscules et les minuscules : `Image.png` et `image.png` sont deux noms différents.

## Mesurer les abandons (événements Google Sheets)

Le jeu envoie des événements anonymes (identifiant de session aléatoire, aucune donnée personnelle) : `start`, `location`, `first_item`, `route`, `blocked`, `hint`, `leave` et `end`.

1. Crée un Google Sheet, puis **Extensions > Apps Script**.
2. Colle le contenu de `apps-script/Code.gs`, enregistre, puis lance une fois la fonction `setupStats` (autorise l'accès).
3. **Déployer > Nouveau déploiement > Application Web** : exécuter en tant que **toi**, accès **Tout le monde**.
4. Copie l'URL `/exec` dans `RESULT_ENDPOINT` au début de `game.js`.
5. Joue une partie : l'onglet `events` se remplit et l'onglet `stats` affiche l'entonnoir.

Pour modifier le script plus tard sans changer l'URL : **Gérer les déploiements > modifier > Nouvelle version**.

## Modifier les infos de la soirée (V3)

- **Carte « Rendez-vous »** et **lien de billetterie** : dans `index.html` (cherche `rdv-card` et `ticketButton`).
- **Textes des 7 affiches** : dans `game.js`, constante `POSTERS`.
- **Dialogues** de Noli, DRIIA et de la régie : dans `game.js`, fonctions `talkMusician`, `talkDriia` et `talkRegie`.
- **Musique** : trois extraits dans `assets/audio/` (`explore`, `riser`, `drop`), joués selon l'avancée. Le son démarre uniquement après un tap.

## Mobile et participation (V3.2)

- **Mobile d'abord** : l'inventaire est affiché au-dessus du texte (masqué tant qu'il est vide), il ne cache plus le décor. Les objets sont posés à des endroits logiques du décor, sans lueur permanente. Après **8 secondes** sans toucher l'écran, un seul élément utile scintille brièvement.
- Les positions des objets sont exprimées en % de l'image du décor et recalculées selon la taille de l'écran : ils restent posés au bon endroit sur tous les téléphones.
- **Personnages** : Noli, DRIIA, la régie et le personnage mystère viennent de ta planche, recolorés en vert et pixelisés (`assets/sprites/*-1.png` et `*-2.png`, deux poses qui alternent). Pour les refaire : `python3 tools/process_characters.py tools/personnages-source 52`.
- **Tram et serre** : `python3 tools/generate_tram_serre.py`.
- **Tirage au sort** : le formulaire de fin envoie un prénom/pseudo et un contact (@Instagram ou e-mail) à Google Sheets, dans l'onglet `participations`. Il faut avoir renseigné `RESULT_ENDPOINT` dans `game.js`.
- **Mettre à jour le script Google** : colle le nouveau `apps-script/Code.gs`, puis **Déployer > Gérer les déploiements > modifier > Nouvelle version** (l'URL ne change pas).
- **Le jour du tirage** : lance `tirer` dans Apps Script (onglet `tirage` : 2 gagnant·es + 2 suppléant·es parmi les participations au statut `ok`). Ensuite, lance `purgerContacts` pour supprimer tous les contacts.
- Statuts : `ok` (a terminé le jeu), `à vérifier` (aucun événement de fin trouvé), `doublon` (même contact déjà inscrit).

## Accessibilité (V3.5)

Sur l'écran d'accueil, le panneau **ACCESSIBILITÉ** propose quatre réglages, modifiables à tout moment pendant la partie avec le bouton **Aa** :
- **Mode daltonisme** : tout ce qui guide (flèches, objets, indices, jauge) passe en blanc et bleu, avec des contours, au lieu de reposer sur le vert.
- **Texte agrandi** : dialogues, boutons, affiches et écran de fin plus grands.
- **Liste des actions** : sous le texte, la liste de tout ce qu'on peut faire dans le lieu, sous forme de boutons. Le jeu se termine entièrement ainsi, avec un lecteur d'écran (VoiceOver, TalkBack) ou en cas de malvoyance. Les animations sont coupées dans ce mode.
- **Sans flash ni animation** : pour les personnes photosensibles ou sensibles au mouvement.

Les choix sont mémorisés sur l'appareil. Le jeu reste jouable entièrement au clavier sur ordinateur (Tab, Entrée, Échap).
