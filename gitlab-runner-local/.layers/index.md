---
title: "Un runner GitLab sur son poste"
description: "Lab GitLab CI : faire tourner un runner dans Docker sur son poste, l'enregistrer sur un projet gitlab.com, y envoyer les jobs avec un tag, et couper les runners partagés."
tags:
  - lab
  - gitlab
  - ci
difficulty: beginner
duration: 40
introTitle: "Le lab"
requires: "0.4.0"
options:
  allowManualProgress: false
  autoCompleteOnNext: unverifiable
---

Sur gitlab.com, vos jobs tournent par défaut sur les **runners partagés** de GitLab, appelés *instance runners* dans son interface. C'est pratique pour démarrer, mais leurs minutes de calcul sont comptées, GitLab peut demander de valider votre compte avant de les utiliser, et vos jobs tournent sur des machines tierces. Dans ce lab, vous faites tourner **votre propre runner** sur votre poste, dans un conteneur Docker, et vous y envoyez les jobs d'un projet gitlab.com.

**Niveau** : savoir écrire un petit pipeline, ce qu'enseigne [Créer son premier pipeline GitLab](https://byte-layers.com/fr/labs/gitlab-first-pipeline), et savoir ce qu'est un runner, ce qu'explique [Les runners : qui exécute vos pipelines](https://byte-layers.com/fr/bits/gitlab-runner). Avoir déjà lancé un conteneur avec `docker run` aide, mais chaque commande est expliquée.

**Ce qu'il faut** :

- un compte gratuit sur [gitlab.com](https://gitlab.com/), avec une clé SSH enregistrée, et Git ;
- **Docker** qui tourne sur votre poste : Docker Desktop sous macOS et Windows, Docker Engine sous Linux, installé en mode standard (pas en mode *rootless*). `docker run hello-world` doit afficher `Hello from Docker!` ;
- `curl` pour les vérifications : livré avec macOS et avec Git Bash sous Windows, à installer sous Linux s'il manque.

**Vos fichiers** vivent dans `~/byte-layers/git/runner-local`, et le projet doit rester **public** pour que les vérifications puissent le lire. Vous complétez vous-même le pipeline à partir de son `# TODO` : la solution est disponible en dernier recours.

**Sous Windows**, tapez les commandes dans le terminal **Git Bash**, livré avec Git.
