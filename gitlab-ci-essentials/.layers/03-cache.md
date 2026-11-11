---
title: "03 - Accélérer le pipeline avec un cache"
description: "Réutiliser les dépendances d'un pipeline à l'autre"
---

Chaque pipeline retélécharge les dépendances. Un **cache** les conserve pour la fois suivante.

## 03.1 - Déclarer un cache

La clé `key` identifie le cache. `$CI_COMMIT_REF_SLUG` est le nom de la branche adapté aux URL, ce qui donne un cache par branche :

```exec
cat > ~/byte-layers/git/ci-essentials/calculatrice/.gitlab-ci.yml <<'EOF'
stages:
  - test

default:
  image: node:24-bookworm-slim
  cache:
    key: $CI_COMMIT_REF_SLUG
    paths:
      - node_modules/

variables:
  NOM_APP: calculatrice

tests:
  stage: test
  script:
    - echo "Test de $NOM_APP au commit $CI_COMMIT_SHORT_SHA"
    - npm install
    - npm test
EOF
cd ~/byte-layers/git/ci-essentials/calculatrice && git add .gitlab-ci.yml && git commit -m "Ajoute un cache pour les dépendances" && git push
```

Le job garde `npm install`, car un cache peut être absent. Au prochain passage, la trace indique que le cache a été extrait, et l'installation est plus rapide. Pour constater le gain, relancez le job avec son bouton **Retry**.

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
if ! curl -fsS "$A/repository/files/.gitlab-ci.yml/raw?ref=main" 2>/dev/null | grep -q 'cache:'; then
  echo "Le pipeline publié ne contient pas de cache."
  exit 1
fi
echo "Le pipeline a un cache."
```

> 📖 [Mise en cache](https://docs.gitlab.com/ci/caching/)
