---
title: "02 - Écrire un pipeline à un seul job"
description: "Le fichier .gitlab-ci.yml, les stages, les jobs, l'image"
---

GitLab cherche à la racine du projet un fichier nommé `.gitlab-ci.yml`. S'il existe, chaque `git push` déclenche un pipeline.

## 02.1 - Lire la structure d'un pipeline

Ce petit exemple contient tout ce qu'il vous faut pour commencer :

```yaml
stages:
  - demo

salut:
  stage: demo
  image: alpine:3.22
  script:
    - echo "Bonjour"
```

| Mot-clé | Rôle |
|---|---|
| `stages` | la liste ordonnée des étapes |
| `salut` | le nom du **job**, choisi librement |
| `stage` | l'étape à laquelle appartient le job |
| `image` | l'image Docker dans laquelle tourne le job |
| `script` | les commandes à exécuter |

Les stages s'enchaînent, et les jobs d'un même stage tournent en parallèle.

## 02.2 - Compléter le pipeline

Créez le fichier à compléter :

```exec
cat > ~/layers-git/ci-first/calculatrice/.gitlab-ci.yml <<'EOF'
stages:
  # TODO : déclarez un stage nommé test

tests:
  # TODO : rattachez ce job au stage test
  # TODO : utilisez l'image node:24-bookworm-slim
  script:
    # TODO : installez les dépendances avec npm install
    # TODO : lancez les tests avec npm test
EOF
```

Ouvrez `~/layers-git/ci-first/calculatrice/.gitlab-ci.yml` dans votre éditeur, et remplacez chaque `# TODO` en suivant l'exemple ci-dessus. En YAML, l'indentation compte : utilisez des espaces, et pas de tabulation. Pour valider sa syntaxe, vous pouvez le coller dans GitLab, avec **Build**, **Pipeline editor**, sans l'y enregistrer.

## 02.3 - Publier et regarder le pipeline

Publiez le fichier :

```exec
cd ~/layers-git/ci-first/calculatrice && git add .gitlab-ci.yml && git commit -m "Ajoute le pipeline de tests" && git push
```

Sur GitLab, ouvrez **Build**, **Pipelines**. Le pipeline apparaît, passe à l'état **Running**, puis **Passed**. Cliquez sur le job `tests` pour lire sa **trace**, le journal de son exécution : vous y voyez l'image téléchargée, vos commandes, et le rapport de mocha.

```text
  operations
    ✓ additionne 20 et 20

  1 passing (4ms)
```

````solution
```yaml
stages:
  - test

tests:
  stage: test
  image: node:24-bookworm-slim
  script:
    - npm install
    - npm test
```
````

```verify
C=$(cat ~/layers-git/ci-first/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/layers-git/ci-first/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
if ! curl -fsS "$A/pipelines?ref=main&status=success" 2>/dev/null | grep -q '"status":"success"'; then
  echo "Aucun pipeline réussi sur main. Regardez la trace du job dans Build, Pipelines."
  exit 1
fi
echo "Votre premier pipeline a réussi."
```

> 📖 [Référence de `.gitlab-ci.yml`](https://docs.gitlab.com/ci/yaml/)
