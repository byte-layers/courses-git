---
title: "03 - Livrer un hotfix depuis la production"
description: "Partir de main, publier 1.0.1, et reporter la correction dans develop"
---

Un bug est signalé en production. Imaginez que `develop` contienne déjà du travail qui n'est pas prêt. Une **branche de hotfix** part directement de `main`, et le correctif rejoint ensuite les deux branches permanentes.

## 03.1 - Corriger depuis le tag en production

La commande `git switch -c` accepte un point de départ, ici le tag de la version en production. Le correctif se résume ici au numéro de version, qui passe à `1.0.1` :

```exec
cd ~/layers-git/l5-release/depot && git switch -c hotfix/1.0.1 v1.0.0
cd ~/layers-git/l5-release/depot && echo '1.0.1' > VERSION && git commit -am "Corrige la version en production"
```

## 03.2 - Publier le correctif dans main

Vous reprenez les gestes de la release : fusion dans `main`, tag, publication.

```exec
cd ~/layers-git/l5-release/depot && git switch main
cd ~/layers-git/l5-release/depot && git merge --no-ff --no-edit hotfix/1.0.1
cd ~/layers-git/l5-release/depot && git tag -a v1.0.1 -m "Version 1.0.1"
cd ~/layers-git/l5-release/depot && git push origin main v1.0.1
```

```verify
S=~/layers-git/l5-release/serveur.git
if [ "$(git -C "$S" show v1.0.1:VERSION 2>/dev/null)" != "1.0.1" ]; then
  echo "Le tag v1.0.1 devrait exister sur le serveur, avec VERSION à 1.0.1."
  exit 1
fi
echo "La version 1.0.1 est publiée."
```

## 03.3 - Reporter le correctif dans develop

Sans cette étape, le bug reviendrait à la prochaine version. Fusionnez le hotfix dans `develop`, supprimez la branche, et publiez :

```exec
cd ~/layers-git/l5-release/depot && git switch develop
cd ~/layers-git/l5-release/depot && git merge --no-ff --no-edit hotfix/1.0.1
cd ~/layers-git/l5-release/depot && git branch -d hotfix/1.0.1 && git push
```

```verify
S=~/layers-git/l5-release/serveur.git
if [ "$(git -C "$S" show develop:VERSION 2>/dev/null)" != "1.0.1" ]; then
  echo "develop devrait contenir le correctif sur le serveur."
  exit 1
fi
echo "develop contient le correctif."
```

## 03.4 - Ranger le dossier de ce lab

Ce dossier ne servira plus, et vous pouvez le supprimer depuis votre dossier personnel. `rm -rf` efface le dossier et son contenu sans demander de confirmation :

```exec
cd ~ && rm -rf ~/layers-git/l5-release
```

```verify
if [ -e ~/layers-git/l5-release ]; then
  echo "Le dossier ~/layers-git/l5-release existe encore."
  exit 1
fi
echo "Le dossier est supprimé."
```

## Récap

- `main` reflète la production, et `develop` prépare la suite.
- Une fonctionnalité part de `develop` et y revient, avec `--no-ff` pour garder sa trace.
- Une release part de `develop`, rejoint `main` avec un tag, puis redescend dans `develop`.
- Un hotfix part de `main` ou d'un tag, rejoint `main` avec un nouveau tag, puis `develop`.
- Un simple `git push` n'envoie pas les tags.

Pour vous tester sans guide sur un autre modèle, après avoir aussi suivi [Rebase et cherry-pick](https://byte-layers.com/fr/skills/git-rebase-cherry-pick), faites le challenge [Maintenir deux versions, sans guide](https://byte-layers.com/fr/challenges/git-release-challenge).

> 📖 [L'article d'origine de Gitflow](https://nvie.com/posts/a-successful-git-branching-model/) · [`git tag`](https://git-scm.com/docs/git-tag)
