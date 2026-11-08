---
title: "Créer son premier projet GitLab"
description: "Lab GitLab : se connecter en SSH, créer un groupe et un projet, comprendre les rôles, cloner et publier."
tags:
  - lab
  - gitlab
difficulty: beginner
duration: 30
introTitle: "Le lab"
requires: "0.4.0"
options:
  allowManualProgress: false
  autoCompleteOnNext: unverifiable
---

Dans ce lab, vous créez un groupe et un projet sur GitLab, vous donnez des droits, puis vous clonez le projet et y publiez un premier commit.

**Niveau** : à l'aise avec `git clone`, `git push` et les dépôts distants, ce qu'enseigne [Partager son travail avec un dépôt distant](https://byte-layers.com/fr/skills/git-remotes).

**Ce qu'il faut** : un compte gratuit sur [gitlab.com](https://gitlab.com/) et Git. Les vérifications utilisent `curl`, livré avec Git Bash sous Windows. Si votre organisation a sa propre instance GitLab, remplacez `gitlab.com` par son adresse.

**Vos fichiers** vivent dans `~/layers-git/gitlab-first`. La dernière étape supprime ce dossier. Sur GitLab, votre projet doit rester **public** pendant le lab : les boutons de vérification lisent son état sans se connecter.

**Sous Windows**, tapez les commandes dans le terminal **Git Bash**, livré avec Git.
