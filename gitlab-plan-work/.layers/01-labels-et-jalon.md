---
title: "01 - Préparer des labels et un jalon"
description: "Classer les tâches et fixer une échéance"
---

Avant de créer des tâches, on prépare la façon de les classer. Créez un nouveau projet public nommé `statuspage-plan`, dans votre groupe ou votre espace personnel, avec **+**, **New project/repository**, **Create blank project**, et un README, puis copiez son adresse **Clone with SSH** dans ce fichier :

```bash
mkdir -p ~/byte-layers/git/gitlab-plan
echo 'git@gitlab.com:demo-votre-nom/statuspage-plan.git' > ~/byte-layers/git/gitlab-plan/url
```

## 01.1 - Créer des labels

Un **label** est une étiquette qui classe les tâches et permet de les filtrer. Dans le menu **Manage**, ouvrez **Labels**, puis **New label**. Créez ces trois labels :

| Label | Sert à |
|---|---|
| `feature` | une fonctionnalité |
| `bug` | une anomalie |
| `en cours` | une tâche commencée |

## 01.2 - Créer un jalon

Un **jalon** (*milestone*) regroupe les tâches d'une même échéance, comme une version. Dans le menu **Plan**, ouvrez **Milestones**, puis **New milestone**. Nommez-le `V1`, donnez-lui une date de fin si vous le souhaitez, et validez.

> 📖 [Labels](https://docs.gitlab.com/user/project/labels/) · [Jalons](https://docs.gitlab.com/user/project/milestones/)

```acknowledge
Les trois labels et le jalon V1 sont créés
```
