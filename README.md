# FamilyTree

Projet de développement full stack — M1 IASI 2026–2027.

FamilyTree permet de gérer les personnes d'une famille, de créer leurs relations
et de visualiser leur arbre généalogique.

## Fonctionnalités

- Ajouter, modifier et supprimer des personnes, avec un identifiant généré automatiquement.
- Créer et supprimer des liens de type **parent** ou **partenaire**.
- Afficher les générations dans un arbre : liens verts pour les parents et pointillés orange pour les partenaires.
- Afficher les erreurs renvoyées par le backend dans les formulaires.

Les personnes et les liens viennent de l'API. Après chaque ajout, modification
ou suppression, l'interface recharge les données depuis le serveur.

## Technologies

| Partie | Technologies |
| --- | --- |
| Interface | React, React Router, Axios, SCSS et SVG |
| Compilation | Webpack |
| Backend | Python, FastAPI et Pydantic |
| Stockage | Fichier JSON |
| Tests | pytest et TestClient |
| Exécution | Docker Compose ou installation locale |

## Lancer avec Docker Compose

Créer un fichier `.env` à la racine pour choisir les ports. Cet exemple laisse
les ports 3000 et 9999 disponibles pour les serveurs lancés sans Docker :

```dotenv
FRONTEND_PORT=13000
BACKEND_PORT=10099
```

Docker Compose lit ce fichier automatiquement. L'adresse de l'API dans React est
configurée avec le port du backend. Le fichier `.env` est ignoré par Git.
Sans ce fichier, les ports utilisés sont 3000 pour React et 9999 pour FastAPI.

Ouvrir Docker Desktop, puis exécuter à la racine du projet :

```bash
docker compose up --build -d
```

| Service | Adresse |
| --- | --- |
| Application | http://localhost:13000 |
| Documentation de l'API | http://127.0.0.1:10099/docs |

Le backend démarre en premier. Le frontend démarre lorsque l'API répond.
Les ports choisis dans `.env` doivent être disponibles. Les adresses ci-dessus
correspondent au fichier `.env` ci-dessus ; adapter leur port si la configuration change.

Pour consulter les journaux et arrêter l'application :

```bash
docker compose logs -f
docker compose down
```

Après une modification du code, relancer `docker compose up --build -d`.

### Conservation des données

Le dossier `back/data/` est partagé avec le conteneur backend. Les modifications
sont enregistrées dans `back/data/data.json` et conservées après l'arrêt ou la
recréation des conteneurs. Ce dossier et son fichier JSON doivent exister.

Cette configuration est prévue pour un lancement sur son ordinateur : le navigateur
contacte l'API à l'adresse `http://127.0.0.1:<BACKEND_PORT>`.

## Lancer sans Docker

Prérequis : **Python 3.12**, **pipenv**, **Node.js 22** et **npm**.
Arrêter les conteneurs avant de réutiliser les mêmes ports.

Dans un premier terminal, depuis la racine :

```bash
cd back
python -m pip install pipenv
python -m pipenv install --dev
python -m pipenv run python main.py
```

Dans un second terminal, depuis la racine :

```bash
cd front
npm ci
npm start
```

Ouvrir http://localhost:3000. Garder les deux terminaux ouverts.

## Tests

Avec Docker :

```bash
docker compose exec backend python -m pytest -q -p no:cacheprovider
```

Sans Docker, depuis la racine :

```bash
cd back
python -m pipenv run python -m pytest -q -p no:cacheprovider
```

Les tests couvrent les modèles, la lecture et l'écriture du JSON, les opérations
sur les personnes et les liens, les règles métier et les routes HTTP.
Ils utilisent des fichiers temporaires et ne modifient pas les données de l'application.

## Règles de l'arbre

Lors de la création ou de la modification d'un lien, le backend vérifie que :

- les deux personnes existent et sont différentes ;
- le lien n'existe pas déjà, y compris dans le sens inverse pour un partenariat ;
- une personne a au plus deux parents et un seul partenaire ;
- un parent et son enfant ne sont pas partenaires ;
- les liens parent/enfant ne créent pas de boucle ;
- le parent est né avant son enfant, lorsque leurs dates de naissance sont connues.

Les personnes acceptent des dates au format `AAAA` ou `AAAA-MM-JJ`. La date de décès
ne peut pas être antérieure à la naissance. Supprimer une personne supprime aussi ses liens.

## Organisation du projet

```text
.
├── docker-compose.yaml      # Lancement des deux services
├── .env                     # Ports locaux (ignoré par Git)
├── back/
│   ├── Dockerfile
│   ├── main.py              # Routes de l'API
│   ├── Pipfile              # Dépendances Python
│   ├── src/
│   │   ├── models.py        # Modèles et validation des champs
│   │   └── persistence.py   # Stockage JSON et règles métier
│   ├── data/data.json       # Personnes et liens enregistrés
│   └── test/                # Tests du backend
└── front/
    ├── Dockerfile
    ├── package.json         # Dépendances et commandes npm
    ├── webpack.config.js
    ├── public/index.html    # Page qui accueille React
    └── src/
        ├── index.js         # Démarrage de React
        ├── App.jsx          # Navigation et routes
        ├── App.scss         # Styles de l'interface
        └── views/
            ├── Home.jsx
            ├── Persons.jsx
            ├── NewPerson.jsx
            └── Tree.jsx
```

Les fichiers `front/index.html`, `front/app.js` et `front/style.css` correspondent
à l'ancienne interface. L'application actuelle utilise les composants React de `front/src/`.

## API

| Méthode | Personnes | Liens |
| --- | --- | --- |
| GET — lister | `/personnes` | `/liens` |
| GET — consulter | `/personnes/{id}` | `/liens/{id}` |
| POST — créer | `/personnes` | `/liens` |
| PUT — modifier | `/personnes/{id}` | `/liens/{id}` |
| DELETE — supprimer | `/personnes/{id}` | `/liens/{id}` |

Pour un lien `parent`, `source` désigne le parent et `destination` désigne l'enfant.
Les erreurs sont renvoyées dans le champ `detail` : **400** pour une règle métier,
**404** pour une ressource inexistante et **422** pour des champs invalides.
Les corps des requêtes sont décrits dans http://127.0.0.1:9999/docs.

## Travail en groupe

Chaque groupe développe sur sa branche, puis propose ses changements vers `master`
par une Merge Request. Les règles métier sont vérifiées par des tests suivant le
cycle TDD : test en échec, implémentation, puis amélioration du code.
