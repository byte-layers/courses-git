---
title: "01 - Préparer le projet calculatrice"
description: "Créer le projet et y publier le code à tester"
---

Le pipeline a besoin de code à tester : une fonction d'addition et son test, écrits avec **mocha**, un outil de test pour JavaScript.

## 01.1 - Créer et cloner le projet

Créez un projet public nommé `calculatrice-ci`, avec un README, puis enregistrez son adresse en remplaçant l'exemple :

```bash
mkdir -p ~/byte-layers/git/ci-first
echo 'git@gitlab.com:demo-votre-nom/calculatrice-ci.git' > ~/byte-layers/git/ci-first/url
```

Clonez-le ensuite :

```exec
cd ~/byte-layers/git/ci-first && git clone "$(cat url)" calculatrice
```

## 01.2 - Ajouter le code et ses tests

Cette commande crée quatre fichiers, puis les publie : `package.json` déclare les dépendances, `operations.js` contient le code, `test.js` son test, et `.gitignore` écarte les paquets téléchargés.

```exec
cd ~/byte-layers/git/ci-first/calculatrice
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
if ! curl -fsS "$A/repository/files/test.js?ref=main" >/dev/null 2>&1; then
  echo "test.js n'est pas sur GitLab. Vérifiez que le git push a réussi."
  exit 1
fi
echo "Le code est sur GitLab."
```
