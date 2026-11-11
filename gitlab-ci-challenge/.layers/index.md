---
title: "Écrire un pipeline complet, sans guide"
description: "Construire un pipeline à plusieurs stages, avec cache, audit et livraison manuelle, à partir d'un cahier des charges."
tags:
  - challenge
  - gitlab
  - ci
difficulty: intermediate
duration: 30
introTitle: "Le défi"
requires: "0.4.0"
options:
  allowManualProgress: false
  autoCompleteOnNext: unverifiable
---

Ce challenge prouve que vous savez écrire un pipeline GitLab complet. Il n'y a **aucune commande de pipeline à recopier** : chaque tâche donne un objectif et des critères, puis un bouton vérifie l'état réel du projet.

Si vous êtes bloqué, les **indices** se dévoilent un par un, et la **solution** reste en dernier recours. Les utiliser ne coûte rien : seule la vérification compte.

## Avant de commencer

- **Ce qu'il faut savoir** : ce qu'enseignent [Les essentiels de GitLab CI](https://byte-layers.com/fr/skills/gitlab-ci-essentials) et [Bloquer une merge request qui casse les tests](https://byte-layers.com/fr/labs/gitlab-ci-quality-gate).
- **Ce qu'il faut avoir** : un compte gratuit sur [gitlab.com](https://gitlab.com/) et Git. Les vérifications utilisent `curl`, livré avec Git Bash sous Windows.
- **Un dossier de travail** : `~/byte-layers/git/ci-challenge` est créé pour vous, et la dernière tâche le supprime.
- **L'ordre compte** : chaque tâche reprend l'état laissé par la précédente.

# Tâche 1 : le projet à tester

## Créer le projet et y publier le code

```setup
mkdir -p ~/byte-layers/git/ci-challenge
```

Créez un projet public nommé `calculatrice-challenge`, avec un README. Écrivez son adresse de clonage dans `~/byte-layers/git/ci-challenge/url`, clonez-le dans `~/byte-layers/git/ci-challenge/calculatrice`, puis publiez-y le code de départ, avec cette commande :

```bash
cd ~/byte-layers/git/ci-challenge/calculatrice
cat > package.json <<'EOF'
{
  "name": "calculatrice",
  "version": "1.0.0",
  "scripts": { "test": "mocha test.js" },
  "dependencies": { "lodash": "4.17.4" },
  "devDependencies": { "mocha": "5.2.0" }
}
EOF
cat > operations.js <<'EOF'
const add = (x, y) => (+x) + (+y);
module.exports = { add };
EOF
cat > test.js <<'EOF'
const assert = require('assert');
const operations = require('./operations.js');
describe('operations', () => {
  it('additionne 20 et 20', () => assert.equal(operations.add(20, 20), 40));
});
EOF
echo node_modules > .gitignore
git add . && git commit -m "Ajoute la calculatrice et ses tests" && git push
```

**Critère :** `test.js` est sur la branche `main` du projet.

```verify
C=$(cat ~/byte-layers/git/ci-challenge/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/byte-layers/git/ci-challenge/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
if ! curl -fsS "$A/repository/files/test.js?ref=main" >/dev/null 2>&1; then
  echo "test.js n'est pas sur main."
  exit 1
fi
echo "Le code est sur GitLab."
```

# Tâche 2 : un pipeline à deux stages

## Écrire un pipeline build puis test

Écrivez un `.gitlab-ci.yml` avec les stages `build` et `test`, dans l'image `node:24-bookworm-slim`. Un job du stage `build` installe les dépendances, et un job du stage `test` lance `npm test`. Les dépendances sont mises en cache, et le job de tests doit fonctionner même si le cache est absent.

**Critères :**

- le fichier déclare les stages `build` et `test`, sous forme de liste à tirets ;
- il contient un `cache:` sur `node_modules/` ;
- le dernier pipeline de `main` réussit.

```hint
Chaque job démarre dans un environnement neuf : le job de tests doit aussi installer ce qui manque.
```

```verify
C=$(cat ~/byte-layers/git/ci-challenge/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/byte-layers/git/ci-challenge/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
Y=$(curl -fsS "$A/repository/files/.gitlab-ci.yml/raw?ref=main" 2>/dev/null)
for T in '- build' '- test' 'cache:' 'node_modules' 'npm test'; do
  if ! echo "$Y" | grep -q -- "$T"; then
    echo "Le pipeline ne contient pas : $T"
    exit 1
  fi
done
if ! curl -fsS "$A/pipelines?ref=main&per_page=1" 2>/dev/null | grep -qE '"status":"(success|manual)"'; then
  echo "Le dernier pipeline de main n'a pas réussi, ou il est encore en cours."
  exit 1
fi
echo "Le pipeline à deux stages réussit."
```

````solution
```yaml
stages:
  - build
  - test

default:
  image: node:24-bookworm-slim
  cache:
    key: $CI_COMMIT_REF_SLUG
    paths:
      - node_modules/

installation:
  stage: build
  script:
    - npm install

tests:
  stage: test
  script:
    - npm install
    - npm test
```
````

# Tâche 3 : un audit qui signale sans bloquer

## Ajouter un job d'audit avec son rapport

Ajoutez, dans le stage `test`, un job `audit` qui lance `npm audit`, garde son résultat dans un fichier `audit.json` conservé en artefact même en cas d'échec, et n'empêche pas le pipeline de réussir.

**Critères :**

- le fichier contient `npm audit` et `audit.json` ;
- l'artefact est conservé en cas d'échec ;
- le dernier pipeline de `main` réussit.

```hint
Un mot-clé autorise un job à échouer, et un autre, sous `artifacts`, précise quand conserver les fichiers.
```

```verify
C=$(cat ~/byte-layers/git/ci-challenge/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/byte-layers/git/ci-challenge/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
Y=$(curl -fsS "$A/repository/files/.gitlab-ci.yml/raw?ref=main" 2>/dev/null)
for T in 'npm audit' 'audit.json' 'allow_failure: true' 'when: always'; do
  if ! echo "$Y" | grep -q -- "$T"; then
    echo "Le pipeline ne contient pas : $T"
    exit 1
  fi
done
if ! curl -fsS "$A/pipelines?ref=main&per_page=1" 2>/dev/null | grep -qE '"status":"(success|manual)"'; then
  echo "Le dernier pipeline de main n'a pas réussi, ou il est encore en cours."
  exit 1
fi
echo "L'audit signale sans bloquer."
```

````solution
```yaml
audit:
  stage: test
  script:
    - npm install
    - npm audit --audit-level=high --json > audit.json
  allow_failure: true
  artifacts:
    when: always
    paths:
      - audit.json
```
````

# Tâche 4 : une livraison sur décision humaine

## Ajouter un job manuel réservé à la branche par défaut

Ajoutez un stage `livraison` à la liste de `stages`, et un job `livrer`, qui affiche un message. Il ne doit exister que sur la branche par défaut, et attendre un lancement manuel.

**Critères :**

- le fichier contient un stage `livraison` et un job `livrer` ;
- le job utilise `rules` avec `CI_DEFAULT_BRANCH` et `when: manual` ;
- le dernier pipeline de `main` aboutit.

```hint
Sans `allow_failure: true`, un job manuel défini dans `rules` laisse le pipeline en attente.
```

```verify
C=$(cat ~/byte-layers/git/ci-challenge/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/byte-layers/git/ci-challenge/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
Y=$(curl -fsS "$A/repository/files/.gitlab-ci.yml/raw?ref=main" 2>/dev/null)
for T in '- livraison' 'livrer:' 'rules:' 'CI_DEFAULT_BRANCH' 'when: manual'; do
  if ! echo "$Y" | grep -q -- "$T"; then
    echo "Le pipeline ne contient pas : $T"
    exit 1
  fi
done
if ! curl -fsS "$A/pipelines?ref=main&per_page=1" 2>/dev/null | grep -qE '"status":"(success|manual)"'; then
  echo "Le dernier pipeline de main n'a pas abouti, ou il est encore en cours."
  exit 1
fi
echo "La livraison attend une décision humaine."
```

````solution
```yaml
stages:
  - build
  - test
  - livraison
```

```yaml
livrer:
  stage: livraison
  script:
    - echo "Livraison"
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
      allow_failure: true
```
````

# Tâche 5 : ne rien laisser derrière soi

## Supprimer le dossier du challenge

Supprimez le dossier `~/byte-layers/git/ci-challenge`. Vous pouvez aussi supprimer le projet sur GitLab.

**Critère :** le dossier `~/byte-layers/git/ci-challenge` n'existe plus.

```verify
if [ -e ~/byte-layers/git/ci-challenge ]; then
  echo "Le dossier ~/byte-layers/git/ci-challenge existe encore."
  exit 1
fi
echo "Le dossier est supprimé. Challenge terminé."
```

````solution
```bash
cd ~ && rm -rf ~/byte-layers/git/ci-challenge
```
````
