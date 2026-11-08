---
title: "Bloquer une merge request qui casse les tests"
description: "Lab GitLab CI : lancer le pipeline sur les merge requests, interdire la fusion si les tests échouent, et auditer les dépendances."
tags:
  - lab
  - gitlab
  - ci
difficulty: beginner
duration: 30
introTitle: "Le lab"
requires: "0.4.0"
options:
  allowManualProgress: false
  autoCompleteOnNext: unverifiable
---

Dans ce lab, le pipeline devient un garde-fou : une merge request qui casse les tests ne peut plus être fusionnée. Vous ajoutez aussi un audit des dépendances, qui avertit sans bloquer.

**Niveau** : à l'aise avec les merge requests et les bases d'un pipeline, ce qu'enseignent [Livrer du code avec les merge requests](https://byte-layers.com/fr/skills/gitlab-merge-requests) et [Les essentiels de GitLab CI](https://byte-layers.com/fr/skills/gitlab-ci-essentials).

**Ce qu'il faut** : un compte gratuit sur [gitlab.com](https://gitlab.com/) et Git. Les vérifications utilisent `curl`, livré avec Git Bash sous Windows.

Sur gitlab.com, les jobs sont exécutés par des **runners partagés** : vous n'avez rien à installer. Si un job échoue en vous demandant de valider votre compte, suivez le lien affiché : GitLab demande par exemple un numéro de téléphone ou une carte bancaire, qui ne sera pas débitée. Les minutes de calcul sont limitées, et le détail se trouve sur la [page des tarifs](https://about.gitlab.com/pricing/).

**Vos fichiers** vivent dans `~/layers-git/ci-quality`, et le projet doit rester **public**.

**Sous Windows**, tapez les commandes dans le terminal **Git Bash**, livré avec Git.
