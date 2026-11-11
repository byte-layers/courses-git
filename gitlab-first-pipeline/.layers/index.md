---
title: "Créer son premier pipeline GitLab"
description: "Lab GitLab CI : écrire un fichier .gitlab-ci.yml, lancer des tests automatiquement, découper en stages et transmettre des fichiers."
tags:
  - lab
  - gitlab
  - ci
difficulty: beginner
duration: 45
introTitle: "Le lab"
requires: "0.4.0"
options:
  allowManualProgress: false
  autoCompleteOnNext: unverifiable
---

Dans ce lab, vous faites tester automatiquement une petite calculatrice JavaScript à chaque `git push`, d'abord avec un seul **job**, c'est-à-dire une tâche du pipeline, puis avec un pipeline à deux **stages**, ses étapes successives.

**Niveau** : savoir créer un projet GitLab et publier un commit, ce qu'enseigne [Créer son premier projet GitLab](https://byte-layers.com/fr/labs/gitlab-first-project). Le code est en JavaScript, et il tient en quelques lignes. Les tests s'exécutent dans le pipeline.

**Ce qu'il faut** : un compte gratuit sur [gitlab.com](https://gitlab.com/) et Git. Les vérifications utilisent `curl`, livré avec Git Bash sous Windows.

Sur gitlab.com, les jobs sont exécutés par des **runners partagés** : vous n'avez rien à installer. Si un job échoue en vous demandant de valider votre compte, suivez le lien affiché : GitLab demande par exemple un numéro de téléphone ou une carte bancaire, qui ne sera pas débitée. Les minutes de calcul sont limitées, et le détail se trouve sur la [page des tarifs](https://about.gitlab.com/pricing/).

**Vos fichiers** vivent dans `~/byte-layers/git/ci-first`, et le projet doit rester **public**. Vous complétez vous-même le fichier du pipeline à partir de ses `# TODO` : la solution est disponible en dernier recours.

**Sous Windows**, tapez les commandes dans le terminal **Git Bash**, livré avec Git.
