---
title: "Annuler ses erreurs avec Git"
description: "Cours pratique Git : abandonner un changement, corriger un commit, revenir en arrière avec reset et revert, mettre de côté avec stash, et retrouver un commit perdu."
tags:
  - skill
  - git
difficulty: beginner
duration: 60
introTitle: "Présentation"
requires: "0.4.0"
options:
  allowManualProgress: false
  autoCompleteOnNext: unverifiable
---

À la fin de ce cours, vous savez choisir la bonne commande pour annuler ce que vous venez de faire, selon que le travail est encore local ou déjà publié.

## Pour qui ?

Ce cours s'adresse aux personnes qui savent faire des commits et utiliser un dépôt distant, ce qu'enseignent [Enregistrer son travail avec Git](https://byte-layers.com/fr/skills/git-first-commits) et [Partager son travail avec un dépôt distant](https://byte-layers.com/fr/skills/git-remotes). Votre identité Git doit être réglée.

Si vous pensez déjà savoir tout cela, tentez directement le challenge [Réparer un dépôt, sans guide](https://byte-layers.com/fr/challenges/git-repair-challenge).

## Comment ça se passe

Six étapes à suivre dans l'ordre, environ une heure en tout, chacune pour une situation différente. La première crée un petit projet `statuspage`.

Vos fichiers vivent dans `~/layers-git/l4-undo`, et chaque commande commence par `cd ~/layers-git/l4-undo &&` pour le bouton qui l'exécute. Quand vous tapez vous-même vos commandes, un seul `cd` suffit. La dernière étape supprime ce dossier.

Votre terminal peut afficher les messages en français, et les identifiants de commit seront différents des exemples.

**Sous Windows**, utilisez le terminal **Git Bash**, installé avec Git. L'avertissement `LF will be replaced by CRLF` y est sans gravité.
