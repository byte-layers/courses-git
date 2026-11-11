---
title: "05 - Décider quand un job se lance avec rules"
description: "Conditionner un job à la branche, et le rendre manuel"
---

Tous les jobs n'ont pas à tourner à chaque envoi. Le mot-clé `rules` fixe les conditions d'un job, à partir des variables.

## 05.1 - Ajouter un job de livraison manuel

Ce job n'existe que sur la branche par défaut, et n'est lancé que sur décision humaine. C'est la différence entre livraison et déploiement continus. Le job se contente ici d'un message :

```exec
cat > ~/byte-layers/git/ci-essentials/calculatrice/.gitlab-ci.yml <<'EOF'
stages:
  - test
  - livraison

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
    - npm test --silent -- --reporter json > rapport.json
  artifacts:
    when: always
    paths:
      - rapport.json
    expire_in: 7 days

livrer:
  stage: livraison
  script:
    - echo "Livraison de $NOM_APP"
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
      allow_failure: true
EOF
cd ~/byte-layers/git/ci-essentials/calculatrice && git add .gitlab-ci.yml && git commit -m "Ajoute une livraison manuelle sur la branche principale" && git push
```

Sur la page du pipeline, le job `livrer` affiche un bouton de lecture : il attend votre clic. `allow_failure: true` évite que le pipeline reste bloqué en attendant ce clic. Sur une autre branche, il n'apparaîtrait pas.

> 💡 **Remarque.** Dans d'anciens pipelines, vous verrez `only:` et `except:`. Pour un nouveau pipeline, on préfère `rules:`, plus expressif.

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
Y=$(curl -fsS "$A/repository/files/.gitlab-ci.yml/raw?ref=main" 2>/dev/null)
if ! echo "$Y" | grep -q 'rules:' || ! echo "$Y" | grep -q 'when: manual'; then
  echo "Le pipeline publié ne contient pas de job manuel avec rules."
  exit 1
fi
if ! curl -fsS "$A/pipelines?ref=main&per_page=1" 2>/dev/null | grep -qE '"status":"(success|manual)"'; then
  echo "Le dernier pipeline de main n'a pas abouti, ou il est encore en cours."
  exit 1
fi
echo "La livraison attend votre décision."
```

## 05.2 - Ranger le dossier de ce cours

Vous pouvez aussi supprimer le projet sur GitLab, depuis **Settings**, **General**, **Advanced**, **Delete project**.

```exec
cd ~ && rm -rf ~/byte-layers/git/ci-essentials
```

```verify
if [ -e ~/byte-layers/git/ci-essentials ]; then
  echo "Le dossier ~/byte-layers/git/ci-essentials existe encore."
  exit 1
fi
echo "Le dossier est supprimé."
```

## Récap

- Les variables évitent les valeurs en dur, et les secrets se rangent dans les réglages du projet.
- Le cache accélère, l'artefact conserve un résultat.
- `rules` décide si un job existe, et `when: manual` le laisse en attente d'un clic.

> 📖 [`rules`](https://docs.gitlab.com/ci/yaml/#rules) · [Jobs manuels](https://docs.gitlab.com/ci/jobs/job_control/)
