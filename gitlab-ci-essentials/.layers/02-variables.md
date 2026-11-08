---
title: "02 - Paramétrer le pipeline avec des variables"
description: "Variables prédéfinies, variables du fichier, et secrets"
---

Une **variable** évite d'écrire une valeur en dur. GitLab en fournit beaucoup, et vous pouvez ajouter les vôtres.

## 02.1 - Utiliser des variables dans un job

`$CI_COMMIT_SHORT_SHA` est une variable **prédéfinie**, remplie par GitLab avec le début du hash du commit. `variables:` déclare les vôtres dans le fichier :

```exec
cat > ~/layers-git/ci-essentials/calculatrice/.gitlab-ci.yml <<'EOF'
stages:
  - test

default:
  image: node:24-bookworm-slim

variables:
  NOM_APP: calculatrice

tests:
  stage: test
  script:
    - echo "Test de $NOM_APP au commit $CI_COMMIT_SHORT_SHA"
    - npm install
    - npm test
EOF
cd ~/layers-git/ci-essentials/calculatrice && git add .gitlab-ci.yml && git commit -m "Affiche le contexte du pipeline" && git push
```

La trace du job, dans **Build**, **Jobs**, affiche la phrase avec ses valeurs réelles.

```verify
C=$(cat ~/layers-git/ci-essentials/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/layers-git/ci-essentials/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
if ! curl -fsS "$A/repository/files/.gitlab-ci.yml/raw?ref=main" 2>/dev/null | grep -q 'CI_COMMIT_SHORT_SHA'; then
  echo "Le pipeline publié n'utilise pas CI_COMMIT_SHORT_SHA."
  exit 1
fi
echo "Le pipeline utilise des variables."
```

## 02.2 - Ranger un secret hors du dépôt

Un mot de passe ne s'écrit jamais dans `.gitlab-ci.yml`, qui est versionné. Il se déclare dans **Settings**, **CI/CD**, **Variables**, avec **Add variable**. Trois options comptent :

| Option | Effet |
|---|---|
| Visibility : **Masked** | la valeur est remplacée par `[MASKED]` dans les traces |
| **Protect variable** | la variable n'existe que sur les branches et tags protégés |
| Type **File** | le job reçoit le chemin d'un fichier contenant la valeur |

Sans le masquage, un simple `echo` afficherait le secret dans une trace, lisible sur un projet public. Dans ce cours, gardez à l'esprit le principe sans créer de vrai secret.

> 📖 [Variables CI/CD](https://docs.gitlab.com/ci/variables/) · [Variables prédéfinies](https://docs.gitlab.com/ci/variables/predefined_variables/)

```acknowledge
J'ai compris où ranger un secret
```
