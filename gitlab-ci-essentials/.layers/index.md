---
title: "Les essentiels de GitLab CI"
description: "Cours pratique GitLab CI : variables, cache, artefacts et rapports, règles de déclenchement et jobs manuels."
tags:
  - skill
  - gitlab
  - ci
difficulty: beginner
duration: 60
introTitle: "Présentation"
requires: "0.4.0"
options:
  allowManualProgress: false
  autoCompleteOnNext: unverifiable
---

À la fin de ce cours, vous savez paramétrer un pipeline avec des variables, l'accélérer avec un cache, conserver ses résultats, et décider quels jobs se lancent et quand.

## Pour qui ?

Ce cours s'adresse aux personnes qui ont écrit un premier pipeline, ce qu'enseigne [Créer son premier pipeline GitLab](https://byte-layers.com/fr/labs/gitlab-first-pipeline).

## Comment ça se passe

Cinq étapes, environ une heure. Le pipeline évolue à chaque étape : les commandes remplacent à chaque fois le fichier en entier, pour que vous puissiez comparer ce qui change. un compte gratuit sur [gitlab.com](https://gitlab.com/) et Git. Les vérifications utilisent `curl`, livré avec Git Bash sous Windows.

Vos fichiers vivent dans `~/layers-git/ci-essentials`, et le projet doit rester **public**.

Sur gitlab.com, les jobs sont exécutés par des **runners partagés** : vous n'avez rien à installer. Si un job échoue en vous demandant de valider votre compte, suivez le lien affiché : GitLab demande par exemple un numéro de téléphone ou une carte bancaire, qui ne sera pas débitée. Les minutes de calcul sont limitées, et le détail se trouve sur la [page des tarifs](https://about.gitlab.com/pricing/).

**Sous Windows**, tapez les commandes dans le terminal **Git Bash**, livré avec Git.
