---
title: "Livrer des versions avec Gitflow"
description: "Lab Git : organiser develop et ses branches de fonctionnalité, publier une version taguée, et livrer un hotfix, avec des commandes Git standards."
tags:
  - lab
  - git
difficulty: intermediate
duration: 45
introTitle: "Le lab"
requires: "0.4.0"
options:
  allowManualProgress: false
  autoCompleteOnNext: unverifiable
---

Dans ce lab, vous faites vivre le projet `statuspage` selon Gitflow : deux fonctionnalités, une version `1.0.0`, puis un correctif urgent `1.0.1`.

**Niveau** : à l'aise avec les branches et les dépôts distants, ce qu'enseignent [Travailler en parallèle avec les branches](https://byte-layers.com/fr/skills/git-branches-merge) et [Partager son travail avec un dépôt distant](https://byte-layers.com/fr/skills/git-remotes). Le bit [Workflows Git](https://byte-layers.com/fr/bits/git-workflows) présente les rôles des branches.

**Ce qu'il faut** : Git 2.28 ou plus récent, votre identité réglée, et un terminal (Git Bash sous Windows). Votre terminal peut afficher les messages en français.

**Vos fichiers** vivent dans `~/layers-git/l5-release`, avec un dépôt `depot` et son serveur local. Chaque commande commence par `cd ~/layers-git/l5-release/depot &&` pour le bouton qui l'exécute. La dernière étape supprime ce dossier.

> 💡 **Remarque.** Ce lab n'utilise que des commandes Git standards. Il existe une commande `git flow` qui enchaîne ces gestes. L'implémentation la plus répandue n'est plus maintenue. Connaître les commandes sous-jacentes vous rend indépendant de l'outil.
