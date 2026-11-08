---
title: "Enregistrer son travail avec Git"
description: "Cours pratique Git : créer un dépôt, enregistrer des versions avec add et commit, relire l'historique et ignorer des fichiers."
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

À la fin de ce cours, vous savez créer un dépôt Git, y enregistrer des versions en choisissant ce qu'elles contiennent, relire l'historique et tenir certains fichiers à l'écart de Git.

## Pour qui ?

Ce cours s'adresse aux **débutants sur Git**. Il suppose que vous savez ouvrir un terminal, changer de dossier avec `cd` et lire un message d'erreur. Il ne suppose aucune connaissance de Git. Le bit [Pourquoi versionner son travail](https://byte-layers.com/fr/bits/why-version-control) présente le problème que Git résout, et se lit en dix minutes.

Si vous pensez déjà savoir tout cela, tentez directement le challenge [Créer un historique propre, sans guide](https://byte-layers.com/fr/challenges/git-first-commits-challenge).

## Comment ça se passe

Sept étapes à suivre dans l'ordre, environ une heure en tout. Vous construisez un petit dépôt, le projet `statuspage`, qui contient à la fois du code et de la documentation : la page `index.html` affiche l'état de services, et le fichier `runbook.md` décrit la marche à suivre en cas d'incident. Git traite les deux de la même façon.

Vos fichiers vivent dans `~/layers-git/l1`, le signe `~` désignant votre dossier personnel. La dernière étape supprime ce dossier, et Git n'est pas modifié en dehors de votre identité, réglée une fois pour toutes.

**Sous Windows**, les commandes de ce cours se tapent dans le terminal **Git Bash**, livré avec Git. La première étape vous l'explique.
