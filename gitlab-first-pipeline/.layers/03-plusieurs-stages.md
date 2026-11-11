---
title: "03 - Découper le pipeline en deux stages"
description: "Séparer l'installation et les tests, et constater que les jobs sont isolés"
---

Séparer les étapes rend un échec plus lisible. Vous allez isoler l'installation des dépendances dans son propre job, et voir ce que cela change.

## 03.1 - Séparer l'installation et les tests

Remplacez le contenu du pipeline par ces deux stages :

```exec
cat > ~/byte-layers/git/ci-first/calculatrice/.gitlab-ci.yml <<'EOF'
stages:
  - build
  - test

default:
  image: node:24-bookworm-slim

installation:
  stage: build
  script:
    - npm install

tests:
  stage: test
  script:
    - npm test
EOF
cd ~/byte-layers/git/ci-first/calculatrice && git add .gitlab-ci.yml && git commit -m "Sépare installation et tests" && git push
```

Le mot-clé `default` applique ici la même image à tous les jobs. Sur GitLab, le job `installation` réussit, et le job `tests` échoue :

```text
sh: 1: mocha: not found
```

Chaque job démarre dans un environnement neuf : les paquets installés par le premier ont disparu.

## 03.2 - Transmettre node_modules avec un artefact

Un **artefact** est un fichier produit par un job et conservé par GitLab. Les jobs des stages suivants le reçoivent automatiquement. Complétez le job `installation` :

```exec
cat > ~/byte-layers/git/ci-first/calculatrice/.gitlab-ci.yml <<'EOF'
stages:
  - build
  - test

default:
  image: node:24-bookworm-slim

installation:
  stage: build
  script:
    - npm install
  artifacts:
    paths:
      - node_modules/
    expire_in: 1 hour

tests:
  stage: test
  script:
    - npm test
EOF
cd ~/byte-layers/git/ci-first/calculatrice && git add .gitlab-ci.yml && git commit -m "Transmet les dépendances au job de tests" && git push
```

`expire_in` limite la durée de conservation sur GitLab. Le pipeline réussit cette fois, avec ses deux stages.

> 💡 **Remarque.** Ce transfert sert à montrer l'isolation des jobs. Pour des dépendances, on préfère le cache.

```verify
C=$(cat ~/byte-layers/git/ci-first/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/byte-layers/git/ci-first/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
if ! curl -fsS "$A/repository/files/.gitlab-ci.yml/raw?ref=main" 2>/dev/null | grep -q 'artifacts:'; then
  echo "Le pipeline publié ne contient pas d'artefact."
  exit 1
fi
L=$(curl -fsS "$A/pipelines?ref=main&per_page=1" 2>/dev/null)
if ! echo "$L" | grep -q '"status":"success"'; then
  echo "Le dernier pipeline de main n'a pas réussi, ou il est encore en cours."
  exit 1
fi
echo "Le pipeline à deux stages réussit."
```

## 03.3 - Ranger le dossier de ce lab

Vous pouvez aussi supprimer le projet sur GitLab, depuis **Settings**, **General**, **Advanced**, **Delete project**.

```exec
cd ~ && rm -rf ~/byte-layers/git/ci-first
```

```verify
if [ -e ~/byte-layers/git/ci-first ]; then
  echo "Le dossier ~/byte-layers/git/ci-first existe encore."
  exit 1
fi
echo "Le dossier est supprimé."
```

## Récap

- `.gitlab-ci.yml`, à la racine du dépôt, décrit le pipeline.
- Les stages s'enchaînent, l'un après l'autre.
- Chaque job part d'un environnement neuf, et un artefact transmet des fichiers aux stages suivants.

Le bit [Cache ou artefacts](https://byte-layers.com/fr/bits/cache-vs-artifacts) explique quand utiliser l'un ou l'autre.

> 📖 [Stages et jobs](https://docs.gitlab.com/ci/jobs/) · [Artefacts](https://docs.gitlab.com/ci/jobs/job_artifacts/)
