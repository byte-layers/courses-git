---
title: "Jouer Gitflow à deux sur GitLab"
description: "Lab GitLab : Gitflow à deux, avec branches protégées, merge requests, conflit, version taguée et hotfix."
tags:
  - lab
  - gitlab
difficulty: intermediate
duration: 60
introTitle: "Le lab"
requires: "0.4.0"
options:
  allowManualProgress: false
  autoCompleteOnNext: unverifiable
---

Dans ce lab, deux personnes font vivre un projet selon **Gitflow**, un modèle de branches où `main` reflète la production et `develop` prépare la suite. Chacune prend une **user story**, c'est-à-dire un besoin décrit du point de vue de l'utilisateur, leurs merge requests entrent en conflit, puis l'équipe publie une version et livre un correctif.

**Niveau** : à l'aise avec les merge requests, ce qu'enseigne [Livrer du code avec les merge requests](https://byte-layers.com/fr/skills/gitlab-merge-requests). un compte gratuit sur [gitlab.com](https://gitlab.com/) et Git. Les vérifications utilisent `curl`, livré avec Git Bash sous Windows.

**À deux ou seul** : à deux, chacun joue un rôle sur son poste, A ou B, et lance les commandes du poste qui le concerne. Seul, vous jouez les deux rôles depuis les dossiers `poste-a` et `poste-b`.

> 💡 **Remarque.** Gitflow convient surtout aux livraisons par versions. Ce lab l'utilise pour pratiquer les merge requests, sans en faire la norme.

**Vos fichiers** vivent dans `~/layers-git/gitlab-team`, et le projet doit rester **public**.

**Sous Windows**, tapez les commandes dans le terminal **Git Bash**, livré avec Git.
