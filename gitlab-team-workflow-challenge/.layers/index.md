---
title: "Mener un projet GitLab, sans guide"
description: "Protéger une branche, livrer par merge request, résoudre un conflit et taguer une version, à partir d'un cahier des charges."
tags:
  - challenge
  - gitlab
difficulty: intermediate
duration: 30
introTitle: "Le défi"
requires: "0.4.0"
options:
  allowManualProgress: false
  autoCompleteOnNext: unverifiable
---

Ce challenge prouve que vous savez faire vivre un projet sur GitLab. Il n'y a **aucune commande à recopier** : chaque tâche donne un objectif et des critères, puis un bouton vérifie l'état réel du projet.

Si vous êtes bloqué, les **indices** se dévoilent un par un, et la **solution** reste en dernier recours. Les utiliser ne coûte rien : seule la vérification compte.

## Avant de commencer

- **Ce qu'il faut savoir** : ce qu'enseigne [Livrer du code avec les merge requests](https://byte-layers.com/fr/skills/gitlab-merge-requests).
- **Ce qu'il faut avoir** : un compte gratuit sur [gitlab.com](https://gitlab.com/) et Git. Les vérifications utilisent `curl`, livré avec Git Bash sous Windows.
- **Un dossier de travail** : `~/layers-git/gitlab-challenge` est créé pour vous, et la dernière tâche le supprime.
- **L'ordre compte** : chaque tâche reprend l'état laissé par la précédente.

# Tâche 1 : un projet protégé

## Créer le projet et protéger main

```setup
mkdir -p ~/layers-git/gitlab-challenge
```

Créez un projet public nommé `statuspage-challenge`, avec un README. Écrivez son adresse de clonage dans `~/layers-git/gitlab-challenge/url`. Interdisez tout envoi direct sur `main`.

**Critères :**

- le fichier `url` contient l'adresse d'un projet public existant ;
- personne ne peut pousser directement sur `main`.

```hint
Le réglage se trouve dans **Settings**, **Repository**, **Protected branches**.
```

```verify
C=$(cat ~/layers-git/gitlab-challenge/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/layers-git/gitlab-challenge/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
if ! curl -fsS "$A" >/dev/null 2>&1; then
  echo "GitLab ne trouve pas le projet. Vérifiez l'adresse et que le projet est public."
  exit 1
fi
R=$(curl -fsS "$A/protected_branches/main" 2>/dev/null)
if [ -n "$R" ] && ! echo "$R" | grep -qE '"push_access_levels":\[\{[^}]*"access_level":0'; then
  echo "Les envois directs sur main sont encore permis."
  exit 1
fi
if [ -n "$R" ]; then
  echo "Le projet existe, et main est protégée."
else
  echo "Le projet existe. GitLab ne laisse pas lire la protection sans connexion : vérifiez qu'un push direct est refusé."
fi
```

````solution
Créez le projet, et enregistrez son adresse avec `echo 'adresse' > ~/layers-git/gitlab-challenge/url`. Dans **Protected branches**, réglez **Allowed to push and merge** sur **No one** pour `main`.
````

# Tâche 2 : livrer par merge request

## Fermer une issue avec une merge request

Créez une issue. Sur une branche `feature/page`, ajoutez un fichier `index.html`, et faites en sorte que la fusion dans `main`, par une merge request, ferme automatiquement l'issue.

**Critères :**

- une merge request depuis `feature/page` est fusionnée ;
- `index.html` est sur `main` ;
- une issue est fermée.

```hint
Une phrase à placer dans le message du commit relie celui-ci à l'issue.
```

```verify
C=$(cat ~/layers-git/gitlab-challenge/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/layers-git/gitlab-challenge/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
if ! curl -fsS "$A/merge_requests?state=merged" 2>/dev/null | grep -q '"source_branch":"feature/page"'; then
  echo "Aucune merge request fusionnée depuis feature/page."
  exit 1
fi
if ! curl -fsS "$A/repository/files/index.html?ref=main" >/dev/null 2>&1; then
  echo "index.html n'est pas sur main."
  exit 1
fi
if ! curl -fsS "$A/issues?state=closed" 2>/dev/null | grep -q '"type":"ISSUE"'; then
  echo "Aucune issue n'est fermée."
  exit 1
fi
echo "La merge request est fusionnée, et l'issue est fermée."
```

````solution
Clonez le projet, créez la branche, puis enregistrez avec `git commit -m "Ajoute la page" -m "Closes #1"`. Publiez la branche, ouvrez la merge request sur GitLab et fusionnez-la.
````

# Tâche 3 : deux merge requests en conflit

## Fusionner deux changements concurrents

Sur deux branches `feature/a` et `feature/b`, parties du même commit de `main`, créez un fichier `seuil.txt` avec des contenus différents. Fusionnez-les toutes les deux par des merge requests. Sur `main`, le fichier final doit contenir exactement la ligne `Seuil : 5 minutes`.

**Critères :**

- les merge requests de `feature/a` et de `feature/b` sont fusionnées ;
- `seuil.txt` sur `main` contient exactement la ligne attendue.

```hint
La seconde merge request sera bloquée. Fusionnez `main` dans sa branche, sur votre poste.
```

```verify
C=$(cat ~/layers-git/gitlab-challenge/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/layers-git/gitlab-challenge/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
J=$(curl -fsS "$A/merge_requests?state=merged" 2>/dev/null)
for B in feature/a feature/b; do
  if ! echo "$J" | grep -q "\"source_branch\":\"$B\""; then
    echo "La merge request de $B n'est pas fusionnée."
    exit 1
  fi
done
if ! curl -fsS "$A/repository/files/seuil.txt/raw?ref=main" 2>/dev/null | grep -qx 'Seuil : 5 minutes'; then
  echo "seuil.txt sur main devrait contenir la ligne exacte Seuil : 5 minutes."
  exit 1
fi
echo "Le conflit est résolu."
```

````solution
Après la première fusion, placez-vous sur la seconde branche et lancez `git fetch` puis `git merge origin/main`. Écrivez la ligne attendue dans `seuil.txt`, puis lancez `git add seuil.txt`, `git commit --no-edit` et `git push`. Fusionnez ensuite la merge request.
````

# Tâche 4 : publier une version

## Taguer main en v1.0

Marquez le dernier commit de `main` avec un tag `v1.0`, présent sur le serveur.

**Critère :** le tag `v1.0` existe sur le projet.

```hint
Une fois la branche `main` à jour sur votre poste, un tag se crée puis se publie en le nommant.
```

```verify
C=$(cat ~/layers-git/gitlab-challenge/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/layers-git/gitlab-challenge/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
if ! curl -fsS "$A/repository/tags" 2>/dev/null | grep -q '"name":"v1.0"'; then
  echo "Le tag v1.0 n'est pas sur le serveur."
  exit 1
fi
echo "Le tag v1.0 est publié."
```

````solution
Sur `main` à jour, lancez `git tag -a v1.0 -m "Version 1.0"` puis `git push origin v1.0`.
````

# Tâche 5 : ne rien laisser derrière soi

## Supprimer le dossier du challenge

Supprimez le dossier `~/layers-git/gitlab-challenge`. Vous pouvez aussi supprimer le projet sur GitLab.

**Critère :** le dossier `~/layers-git/gitlab-challenge` n'existe plus.

```verify
if [ -e ~/layers-git/gitlab-challenge ]; then
  echo "Le dossier ~/layers-git/gitlab-challenge existe encore."
  exit 1
fi
echo "Le dossier est supprimé. Challenge terminé."
```

````solution
```bash
cd ~ && rm -rf ~/layers-git/gitlab-challenge
```
````
