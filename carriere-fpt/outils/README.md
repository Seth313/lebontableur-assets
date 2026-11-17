# Mise à jour du référentiel des grilles

1. Télécharger https://www.fpt-pratique.fr/grilles-indiciaires.html dans un dossier temporaire.
2. `python3 -I outils/parse.py page.html grilles-brutes.json`
3. `python3 -I outils/toref.py grilles-brutes.json data/grilles.json AAAA-MM-JJ`
   (attention : régénère tout le fichier ; pour une revalorisation future, ajouter plutôt une nouvelle version datée dans `versions`).
4. `python3 build.py`
