# Carrière Territoriale

Web app iPhone (installable sur l'écran d'accueil) de suivi de carrière pour les agents de la fonction publique territoriale.

- **Accueil** : grade, échelon, indice majoré, net estimé, compte à rebours jusqu'au prochain échelon, échéances.
- **Carrière** : déroulé des échelons avec dates et gains, grille modifiable (modèles C1, C2, B), historique des arrêtés.
- **Salaire** : estimation façon bulletin de paie (traitement, NBI, résidence, SFT, RIFSEEP, CNRACL, RAFP, CSG/CRDS, PAS).
- **Congés** : droits annuels, jours de fractionnement, RTT, CET ; jours ouvrés calculés hors week-ends et jours fériés.
- **Suivi** : échéances, formations, CPF, export/import de sauvegarde.

Les données restent sur l'appareil (localStorage). Valeurs et durées indicatives : l'arrêté et le bulletin de paie font foi.

## Fichiers
- `app.html` : source de l'app (contenu de la page).
- `build.py` : génère `index.html` (ajoute l'en-tête iOS, le manifeste et le service worker). Lancer `python3 build.py` après modification.
- `index.html`, `manifest.webmanifest`, `sw.js`, `icon-*.png` : à héberger tels quels (ex. GitHub Pages) pour installer l'app sur iPhone.
