---
title: "01 - Installer Git et vérifier sa version"
description: "Voir si Git est déjà présent, l'installer selon votre système, et ouvrir le bon terminal"
---

Git est un logiciel libre et gratuit, qui s'installe sur une machine, par exemple votre poste. Dans ce cours, vous l'utilisez depuis un terminal, avec des commandes qui commencent toutes par `git`.

## 01.1 - Vérifier si Git est déjà installé

Git est souvent déjà présent, surtout sous Linux et macOS. Cette commande affiche sa version :

```exec
git --version
```

Si Git est installé, vous lisez une ligne semblable à celle-ci, avec un numéro qui peut différer :

```text
git version 2.50.1
```

Ce cours demande **Git 2.28 ou plus récent**. Si votre version convient, passez à la dernière section de cette étape. Si le terminal répond `command not found` ou `'git' n'est pas reconnu`, ou si votre version est plus ancienne, installez Git.

## 01.2 - Installer Git sous Windows, macOS ou Linux

La page officielle [git-scm.com](https://git-scm.com/) donne la marche à suivre et la dernière version pour chaque système. Voici les moyens les plus courants :

| Système | Comment installer | Détails |
|---|---|---|
| Windows | l'installeur de [Git for Windows](https://git-scm.com/install/windows) | gardez les options proposées par défaut ; une étape permet de choisir l'éditeur utilisé par Git, comme VS Code |
| macOS | les outils en ligne de commande d'Apple, ou Homebrew | voir les commandes ci-dessous, et la [page macOS](https://git-scm.com/install/mac) |
| Linux | le gestionnaire de paquets de votre distribution | voir les commandes ci-dessous, et la [page Linux](https://git-scm.com/install/linux) |

Sous macOS, lancez l'une de ces deux commandes. La seconde suppose que [Homebrew](https://brew.sh/) soit installé :

```bash
xcode-select --install
brew install git
```

Sous Linux, utilisez la ligne de votre distribution, la première pour Debian et Ubuntu, la seconde pour Fedora :

```bash
sudo apt-get install git
sudo dnf install git
```

Une fois l'installation terminée, fermez votre terminal, rouvrez-en un, et relancez `git --version`.

## 01.3 - Sous Windows, taper les commandes dans Git Bash

L'installeur de Git for Windows ajoute **Git Bash**, un terminal qui comprend les mêmes commandes que Linux et macOS, comme `echo`, `cat`, `ls` ou le raccourci `~` vers votre dossier personnel. **Sous Windows, toutes les commandes de ce cours se tapent dans Git Bash**, et non dans l'invite de commandes ou PowerShell, où `git` fonctionne mais pas le reste.

Ouvrez-le depuis le menu Démarrer, en cherchant « Git Bash ». Pour y coller du texte, utilisez Maj+Inser ou le clic droit, car Ctrl+V n'y fonctionne pas.

> 📖 [Installation de Git, dans le livre Pro Git](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git)
