---
title: "04 - Conserver un rapport de tests avec un artefact"
description: "Garder un résultat, même quand le job échoue"
---

Les traces s'effacent de la mémoire, alors qu'un rapport se télécharge et se partage. Un artefact conserve ce fichier.

## 04.1 - Produire et conserver un rapport

Le reporter `json` de mocha écrit le résultat dans un format exploitable, et `--silent` empêche npm d'ajouter ses propres lignes au fichier. Le résultat des tests ne figure donc plus dans la trace, mais dans ce fichier. `when: always` conserve l'artefact même si les tests échouent, ce qui est justement le moment où il est utile :

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
    - npm test --silent -- --reporter json > rapport.json
  artifacts:
    when: always
    paths:
      - rapport.json
    expire_in: 7 days
EOF
cd ~/byte-layers/git/ci-essentials/calculatrice && git add .gitlab-ci.yml && git commit -m "Conserve le rapport de tests" && git push
```

Une fois le job terminé, le panneau de droite de sa page propose **Job artifacts**, avec un bouton de téléchargement.

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
if ! curl -fsS "$A/repository/files/.gitlab-ci.yml/raw?ref=main" 2>/dev/null | grep -q 'rapport.json'; then
  echo "Le pipeline publié ne conserve pas rapport.json."
  exit 1
fi
echo "Le rapport est conservé en artefact."
```

> 📖 [Artefacts de job](https://docs.gitlab.com/ci/jobs/job_artifacts/)
