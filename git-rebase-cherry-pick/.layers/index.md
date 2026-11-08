---
title: "Rebase et cherry-pick : réécrire et reporter des commits"
description: "Cours pratique Git : aligner une branche avec git rebase, savoir quand le préférer au merge, publier prudemment avec --force-with-lease, et reporter un commit avec cherry-pick."
tags:
  - skill
  - git
difficulty: intermediate
duration: 60
introTitle: "Présentation"
requires: "0.4.0"
options:
  allowManualProgress: false
  autoCompleteOnNext: unverifiable
---

À la fin de ce cours, vous savez replacer une branche au-dessus d'une autre, choisir entre merge et rebase, publier le résultat prudemment, et reporter un commit précis d'une branche à une autre.

## Pour qui ?

Ce cours s'adresse aux personnes à l'aise avec les branches et les dépôts distants, ce qu'enseignent [Travailler en parallèle avec les branches](https://byte-layers.com/fr/skills/git-branches-merge) et [Partager son travail avec un dépôt distant](https://byte-layers.com/fr/skills/git-remotes). Votre identité Git doit être réglée.

Si vous pensez déjà savoir tout cela, tentez directement le challenge [Réparer un dépôt, sans guide](https://byte-layers.com/fr/challenges/git-repair-challenge).

## Comment ça se passe

Quatre étapes à suivre dans l'ordre, environ une heure en tout. La première crée un petit projet `statuspage`, avec un serveur local.

Vos fichiers vivent dans `~/layers-git/l4-rebase`, et chaque commande commence par `cd ~/layers-git/l4-rebase/depot &&` pour le bouton qui l'exécute. La dernière étape supprime ce dossier.

Votre terminal peut afficher les messages en français, et les identifiants de commit seront différents des exemples.

**Sous Windows**, utilisez le terminal **Git Bash**, installé avec Git. L'avertissement `LF will be replaced by CRLF` y est sans gravité.
