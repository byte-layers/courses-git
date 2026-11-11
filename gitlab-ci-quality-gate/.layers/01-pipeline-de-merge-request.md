---
title: "01 - Lancer le pipeline sur les merge requests"
description: "Préparer le projet, le pipeline et la règle de fusion"
---

Pour qu'une merge request soit contrôlée, le pipeline doit tourner sur elle, et GitLab doit tenir compte de son résultat.

## 01.1 - Créer le projet et publier le code

Créez un projet public nommé `calculatrice-qualite`, avec un README, puis enregistrez son adresse en remplaçant l'exemple :

```bash
mkdir -p ~/byte-layers/git/ci-quality
echo 'git@gitlab.com:demo-votre-nom/calculatrice-qualite.git' > ~/byte-layers/git/ci-quality/url
```

Clonez-le :

```exec
cd ~/byte-layers/git/ci-quality && git clone "$(cat url)" calculatrice
```

Cette commande crée le code à tester, puis le publie :

```exec
cd ~/byte-layers/git/ci-quality/calculatrice
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

## 01.2 - Déclencher le pipeline sur les merge requests

Le bloc `workflow: rules:` choisit quand un pipeline est créé : ici sur les merge requests, et sur la branche par défaut, ce qui évite un pipeline en double à chaque envoi :

```exec
cat > ~/byte-layers/git/ci-quality/calculatrice/.gitlab-ci.yml <<'EOF'
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
EOF
cd ~/byte-layers/git/ci-quality/calculatrice && git add .gitlab-ci.yml && git commit -m "Lance le pipeline sur les merge requests" && git push
```

## 01.3 - Interdire la fusion si le pipeline échoue

Ouvrez **Settings**, **Merge requests**, et dans la partie **Merge checks**, cochez **Pipelines must succeed**, puis enregistrez.

```verify
C=$(cat ~/byte-layers/git/ci-quality/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/byte-layers/git/ci-quality/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
if ! curl -fsS "$A/repository/files/.gitlab-ci.yml/raw?ref=main" 2>/dev/null | grep -q 'merge_request_event'; then
  echo "Le pipeline n'est pas publié sur main."
  exit 1
fi
echo "Le pipeline se lance sur les merge requests."
```

> 📖 [Pipelines de merge request](https://docs.gitlab.com/ci/pipelines/merge_request_pipelines/) · [Merge checks](https://docs.gitlab.com/user/project/merge_requests/auto_merge/#require-a-successful-pipeline-for-merge)
