---
title: "Partager son travail avec un dépôt distant"
description: "Cours pratique Git : publier un dépôt sur un serveur, le cloner, échanger avec fetch, pull et push, et gérer un historique divergent."
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

À la fin de ce cours, vous savez relier un dépôt à un serveur, récupérer le travail de vos collègues, publier le vôtre, et réagir quand Git refuse votre envoi.

## Pour qui ?

Ce cours s'adresse aux **débutants sur le travail à plusieurs**. Il suppose que vous savez faire des commits et fusionner une branche, ce qu'enseignent [Enregistrer son travail avec Git](https://byte-layers.com/fr/skills/git-first-commits) et [Travailler en parallèle avec les branches](https://byte-layers.com/fr/skills/git-branches-merge), et que votre identité Git est réglée.

Si vous pensez déjà savoir tout cela, tentez directement le challenge [Échanger avec un serveur, sans guide](https://byte-layers.com/fr/challenges/git-diverged-challenge).

## Comment ça se passe

Cinq étapes à suivre dans l'ordre, environ une heure en tout. Il ne vous faut **ni compte ni réseau** : le serveur sera un simple dossier de votre machine, et vous jouerez deux personnes, chacune dans son dossier.

Vos fichiers vivent dans `~/byte-layers/git/l3`. Chaque commande de travail commence par `cd` vers le bon poste, pour le bouton qui l'exécute et parce qu'ici vous passez sans cesse d'un poste à l'autre. La dernière étape supprime ce dossier.

Votre terminal peut afficher les messages en français, et les identifiants de commit seront différents des exemples.

**Sous Windows**, utilisez le terminal **Git Bash**, installé avec Git. L'avertissement `LF will be replaced by CRLF` y est sans gravité.
