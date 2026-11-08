---
title: "03 - Auditer les dépendances sans bloquer"
description: "npm audit, allow_failure et un rapport en artefact"
---

Les dépendances peuvent contenir des failles connues. Le `package.json` de ce projet utilise volontairement une ancienne version de `lodash` pour en montrer une. `npm audit` les compare à une base de vulnérabilités, un contrôle appelé **SCA** (*software composition analysis*).

## 03.1 - Ajouter un job d'audit

`allow_failure: true` signale l'échec sans arrêter le pipeline, ce qui convient pour commencer à traiter un existant. `--audit-level=high` n'échoue qu'à partir des failles graves, `--json` donne le format, et `>` l'écrit dans un fichier conservé en artefact :

```exec
cd ~/layers-git/ci-quality/calculatrice && git switch main && git pull
cat > ~/layers-git/ci-quality/calculatrice/.gitlab-ci.yml <<'EOF'
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

stages:
  - test

default:
  image: node:24-bookworm-slim

tests:
  stage: test
  script:
    - npm install
    - npm test

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
    expire_in: 7 days
EOF
```

Pour aller vite, vous poussez directement en tant que Maintainer. En équipe, ce changement passerait par une merge request :

```exec
cd ~/layers-git/ci-quality/calculatrice && git add .gitlab-ci.yml && git commit -m "Ajoute un audit des dépendances" && git push
```

Sur la page du pipeline, le job `audit` affiche un point d'exclamation orange : il a trouvé des failles, et le pipeline reste vert. Téléchargez `audit.json` depuis la page du job.

```verify
C=$(cat ~/layers-git/ci-quality/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/layers-git/ci-quality/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
Y=$(curl -fsS "$A/repository/files/.gitlab-ci.yml/raw?ref=main" 2>/dev/null)
if ! echo "$Y" | grep -q 'npm audit' || ! echo "$Y" | grep -q 'allow_failure: true'; then
  echo "Le pipeline publié ne contient pas d'audit avec allow_failure."
  exit 1
fi
if ! curl -fsS "$A/pipelines?ref=main&per_page=1" 2>/dev/null | grep -q '"status":"success"'; then
  echo "Le dernier pipeline de main n'a pas réussi, ou il est encore en cours."
  exit 1
fi
echo "L'audit signale sans bloquer."
```

## 03.2 - Ranger le dossier de ce lab

Vous pouvez aussi supprimer le projet sur GitLab, depuis **Settings**, **General**, **Advanced**, **Delete project**.

```exec
cd ~ && rm -rf ~/layers-git/ci-quality
```

```verify
if [ -e ~/layers-git/ci-quality ]; then
  echo "Le dossier ~/layers-git/ci-quality existe encore."
  exit 1
fi
echo "Le dossier est supprimé."
```

## Récap

- `workflow: rules:` choisit quand un pipeline est créé.
- **Pipelines must succeed** interdit de fusionner une merge request en échec.
- `allow_failure: true` signale un problème sans arrêter le pipeline.

Pour vous tester sans guide, faites le challenge [Écrire un pipeline complet, sans guide](https://byte-layers.com/fr/challenges/gitlab-ci-challenge).

> 📖 [`allow_failure`](https://docs.gitlab.com/ci/yaml/#allow_failure) · [`npm audit`](https://docs.npmjs.com/cli/commands/npm-audit)
