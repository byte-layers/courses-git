---
title: "02 - git clone : récupérer un projet sur un second poste"
description: "Copier un dépôt complet, et voir les branches distantes"
---

Une collègue arrive sur le projet. Elle ne recommence pas à zéro : elle fait une copie complète du dépôt qui se trouve sur le serveur, ce qu'on appelle un **clone**.

## 02.1 - Cloner le dépôt

Le dossier `poste-b` représente la machine de cette collègue. `git clone` prend l'adresse du dépôt et le nom du dossier à créer :

```exec
cd ~/byte-layers/git/l3 && git clone ~/byte-layers/git/l3/serveur.git poste-b
```

Le clone a tout fait à la fois : il a copié l'historique, extrait les fichiers, et déclaré le serveur sous le nom `origin`. Vérifiez-le :

```exec
cd ~/byte-layers/git/l3/poste-b && ls && git remote -v
```

Comme vous jouez deux personnes sur une seule machine, donnez à ce dépôt sa propre identité. Sans `--global`, le réglage ne vaut que pour ce dépôt, et vous ne touchez pas à votre identité habituelle :

```exec
cd ~/byte-layers/git/l3/poste-b && git config user.name "Sam Durand" && git config user.email "sam@example.com"
```

```verify
D=~/byte-layers/git/l3/poste-b
if [ ! -f "$D/index.html" ]; then
  echo "poste-b n'a pas le fichier index.html. Lancez git clone."
  exit 1
fi
if [ "$(git -C "$D" config --local user.name)" != "Sam Durand" ]; then
  echo "Le dépôt poste-b n'a pas son identité locale. Lancez la commande git config de cette section."
  exit 1
fi
echo "Le second poste a sa copie, et sa propre identité."
```

## 02.2 - Voir les branches distantes

L'option `-a` de `git branch` montre toutes les branches connues de ce dépôt :

```exec
cd ~/byte-layers/git/l3/poste-b && git branch -a
```

À côté de votre branche `main`, Git garde une trace des branches du serveur, sous le préfixe `remotes/origin/` :

```text
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main
```

Retenez cette distinction : `main` est votre branche, celle sur laquelle vous travaillez, et `origin/main` est la dernière position connue de la branche `main` du serveur. Le bit [Main et origin/main](https://byte-layers.com/fr/bits/git-remote-tracking) y revient en détail.

> 📖 [`git clone`](https://git-scm.com/docs/git-clone)
