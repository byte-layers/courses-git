---
title: "Travailler en parallèle avec les branches"
description: "Cours pratique Git : créer des branches, les fusionner, et résoudre un conflit quand deux changements portent sur la même ligne."
tags:
  - skill
  - git
difficulty: beginner
duration: 75
introTitle: "Présentation"
requires: "0.4.0"
options:
  allowManualProgress: false
  autoCompleteOnNext: unverifiable
---

À la fin de ce cours, vous savez ouvrir une branche pour isoler un travail, fusionner deux historiques, et résoudre un conflit sans paniquer.

## Pour qui ?

Ce cours s'adresse aux **débutants sur les branches**. Il suppose que vous savez créer un dépôt et faire des commits, ce qu'enseigne [Enregistrer son travail avec Git](https://byte-layers.com/fr/skills/git-first-commits), et que votre identité Git est réglée.

Si vous pensez déjà savoir tout cela, tentez directement le challenge [Fusionner et résoudre un conflit, sans guide](https://byte-layers.com/fr/challenges/git-conflict-challenge).

## Comment ça se passe

Cinq étapes à suivre dans l'ordre, environ 1 h 15 en tout. La première étape crée un petit projet `statuspage`, avec une page `index.html` et un `runbook.md`, que vous faites ensuite évoluer sur plusieurs branches.

Vos fichiers vivent dans `~/layers-git/l2`. Comme dans le cours précédent, chaque commande de travail commence par `cd ~/layers-git/l2 &&` pour le bouton qui l'exécute, et un seul `cd` suffit quand vous tapez vous-même vos commandes. Votre terminal peut afficher les messages en français, et les identifiants de commit seront différents des exemples. La dernière étape supprime ce dossier.

Ce cours utilise `git switch`, la commande actuelle pour changer de branche. Vous rencontrerez aussi `git checkout` en entreprise et dans la documentation, qui fait le même travail, en plus d'autres choses.

**Sous Windows**, utilisez le terminal **Git Bash**, installé avec Git.
