# Arbre généalogique — M1 IASI 2026-27 (Full Stack Dev)

Application web pour gérer un arbre généalogique : des **personnes** et des **liens**
entre elles (`parent` ou `partenaire`).

- **Back** : API REST en Python ([FastAPI](https://fastapi.tiangolo.com/)), données stockées dans un fichier JSON.
- **Front** : page web en HTML, CSS et JavaScript, sans framework.

## Structure

```text
.
├── back/
│   ├── main.py              # API FastAPI : les routes HTTP
│   ├── src/
│   │   ├── models.py        # modèles Pydantic : Personne, Lien, ArbreGenealogique
│   │   └── persistence.py   # MoteurPersistence : lecture/écriture du JSON, CRUD, règles
│   ├── data/
│   │   ├── data.json        # données de l'application
│   │   └── example.json     # jeu de données d'exemple
│   ├── test/                # tests pytest
│   ├── Pipfile              # dépendances
│   └── pytest.ini
└── front/
    ├── index.html           # la page
    ├── style.css            # la mise en forme
    └── app.js               # les appels à l'API
```

## Installation

Prérequis : **Python 3.12** et **pipenv**.

```bash
cd back
python -m pip install pipenv
python -m pipenv install --dev
```

## Lancer l'application

**1. Le serveur** (dans un terminal, à laisser ouvert) :

```bash
cd back
python -m pipenv run python main.py
```

L'API répond sur <http://127.0.0.1:9999>. Sa documentation interactive est sur
<http://127.0.0.1:9999/docs> : on peut y tester chaque route avec « Try it out ».

**2. La page** (dans un autre terminal, depuis la racine du projet) :

```bash
open front/index.html
```

Sous Windows : double-cliquer sur `front/index.html`.

> Le serveur doit tourner pour que la page fonctionne. Après une modification de
> `main.py` ou de `src/`, il faut le redémarrer (`Ctrl + C`, puis relancer).

## Lancer les tests

```bash
cd back
python -m pipenv run python -m pytest -v
```

| Fichier | Ce qui est testé |
| --- | --- |
| `test_models.py` | les modèles Pydantic (champs obligatoires, format des dates, types de lien) |
| `test_persistence.py` | `load` / `dump` et le chemin du fichier de données |
| `test_personne_crud.py` | le CRUD des personnes dans le fichier JSON |
| `test_lien_crud.py` | le CRUD des liens dans le fichier JSON |
| `test_regles.py` | les règles de cohérence de l'arbre |
| `test_api.py` | toutes les routes HTTP et le CORS |

Les tests travaillent sur des **fichiers JSON temporaires** : ils ne modifient jamais
`data/data.json`.

## Données

Une **personne** :

```json
{
  "id": "p_001",
  "prenom": "Jean",
  "nom_famille": "Dupont",
  "date_naissance": "1990-05-15",
  "lieu_naissance": "Paris",
  "date_mort": "2020",
  "lieu_mort": "Lyon",
  "nationalite": "Française"
}
```

Seul `id` est obligatoire (et non vide). Les dates sont au format `AAAA` ou `AAAA-MM-JJ`.

Un **lien** (tous les champs sont obligatoires) :

```json
{ "id": "l_001", "source": "p_001", "destination": "p_002", "type": "parent" }
```

`type` vaut `parent` (la source est parent de la destination) ou `partenaire`.

## Routes de l'API

| Méthode | Route | Rôle | Codes de retour |
| --- | --- | --- | --- |
| GET | `/personnes` | liste des personnes | 200 |
| GET | `/personnes/{id}` | une personne | 200, 404 |
| POST | `/personnes` | créer une personne | 200, 400 (id déjà utilisé), 422 |
| PUT | `/personnes/{id}` | modifier une personne (champs à changer dans le corps) | 200, 404, 422 |
| DELETE | `/personnes/{id}` | supprimer une personne **et ses liens** | 200, 404 |
| GET | `/liens` | liste des liens | 200 |
| GET | `/liens/{id}` | un lien | 200, 404 |
| POST | `/liens` | créer un lien | 200, 400 (id déjà utilisé ou règle non respectée), 422 |
| PUT | `/liens/{id}` | modifier un lien | 200, 400 (règle non respectée), 404, 422 |
| DELETE | `/liens/{id}` | supprimer un lien | 200, 404 |

- **400** : la demande n'a pas de sens (id déjà utilisé, règle de l'arbre non respectée).
  Le champ `detail` contient le message en clair.
- **404** : l'id demandé n'existe pas.
- **422** : les données n'ont pas le bon format (date invalide, type inconnu, champ manquant…).

## Règles de cohérence

En plus du format, l'application refuse les données qui n'ont pas de sens :

1. la source et la destination d'un lien doivent être des personnes existantes ;
2. une personne ne peut pas être liée à elle-même ;
3. un même lien ne peut pas exister deux fois (un partenariat compte dans les deux sens) ;
4. une personne a au plus deux parents ;
5. une personne ne peut pas devenir son propre ancêtre (pas de boucle dans l'arbre) ;
6. un parent doit être né avant son enfant (si les deux dates sont connues) ;
7. la date de décès doit être après la date de naissance ;
8. supprimer une personne supprime aussi ses liens.

Les règles 1 à 6 sont dans `MoteurPersistence._verifier_lien` (`back/src/persistence.py`),
la règle 7 dans le modèle `Personne` (`back/src/models.py`).

## Méthode de travail

Le projet est développé en **TDD** (*Test-Driven Development*) :

1. 🔴 **Red** : écrire un test qui échoue ;
2. 🟢 **Green** : écrire le minimum de code pour le faire passer ;
3. 🔵 **Refactor** : améliorer le code sans changer son comportement, les tests restant verts.

Chaque groupe travaille sur sa propre branche, puis propose son travail sur `master`
par une Merge Request.
