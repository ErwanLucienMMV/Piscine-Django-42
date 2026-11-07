# Base Django

Chaque dossier `ex00` à `ex03` contient une version autonome du projet `d04`.
Les exercices sont cumulatifs : la version `ex03` contient les quatre applications.
Aucun import ne dépend d’un autre dossier de rendu.

Depuis le dossier de l’exercice choisi, avec Python 3.10 ou supérieur :

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py check
python manage.py runserver
```

Sous PowerShell, activer l’environnement avec `.\.venv\Scripts\Activate.ps1`.
Le projet utilise Django 5.2 LTS, SQLite dans sa configuration et le serveur de
développement Django. Aucun modèle ni migration de données n’est nécessaire.
La clé et `DEBUG = True` sont destinés au développement local.

Pages disponibles selon la version choisie, avec ou sans slash final :

| Application | URL |
| --- | --- |
| ex00 | `/ex00` |
| ex01 | `/ex01/django`, `/ex01/affichage`, `/ex01/templates` |
| ex02 | `/ex02` |
| ex03 | `/ex03` |

Les autres chemins répondent 404. Les liens de navigation utilisent la variante
sans slash. Pour collecter les feuilles CSS dans `staticfiles/` :

```sh
python manage.py collectstatic --noinput
```

`runserver` sert les ressources statiques des applications pendant le développement.

Le formulaire d’`ex02` sauvegarde chaque entrée dans un fichier UTF-8 au format
JSON Lines. `EX02_LOG_FILE`, dans `d04/settings.py`, définit son chemin complet :
`ex02/entries.log`. Ce fichier est créé à la première soumission valide et reste
présent après un redémarrage du serveur. Chaque ligne contient d’abord un horodatage
ISO 8601 avec fuseau, puis le texte soumis. La page relit ce fichier pour afficher
l’historique dans l’ordre des entrées ; une actualisation après soumission ne
duplique pas l’entrée. Le fichier n’est pas versionné. Le supprimer réinitialise
l’historique.

La vue d’`ex03` calcule 50 nuances par colonne et les transmet au template.
Les 200 couleurs sont distinctes ; chaque cellule mesure 80 × 40 pixels.
