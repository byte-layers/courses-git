---
title: "01 - Partir d'un pipeline qui fonctionne"
description: "Créer le projet et son pipeline de base"
---

Vous partez d'un pipeline simple, avec un seul job qui installe les dépendances, puis lance les tests.

## 01.1 - Créer le projet et publier le code

Créez un projet public nommé `calculatrice-essentiels`, avec un README, puis enregistrez son adresse en remplaçant l'exemple :

```bash
mkdir -p ~/byte-layers/git/ci-essentials
echo 'git@gitlab.com:demo-votre-nom/calculatrice-essentiels.git' > ~/byte-layers/git/ci-essentials/url
```

Clonez-le :

```exec
cd ~/byte-layers/git/ci-essentials && git clone "$(cat url)" calculatrice
```

Cette commande crée le code à tester, puis le publie :

```exec
cd ~/byte-layers/git/ci-essentials/calculatrice
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

## 01.2 - Publier le pipeline de départ

À chaque pipeline, le job réinstalle ses dépendances, ce qui est lent, et vous allez l'améliorer :

```exec
cat > ~/byte-layers/git/ci-essentials/calculatrice/.gitlab-ci.yml <<'EOF'
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
cd ~/byte-layers/git/ci-essentials/calculatrice && git add .gitlab-ci.yml && git commit -m "Ajoute le pipeline de départ" && git push
```

```verify
C=$(cat ~/byte-layers/git/ci-essentials/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/byte-layers/git/ci-essentials/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
if ! curl -fsS "$A/repository/files/.gitlab-ci.yml/raw?ref=main" 2>/dev/null | grep -q 'npm test'; then
  echo "Le pipeline n'est pas sur main."
  exit 1
fi
echo "Le pipeline de départ est publié."
```
