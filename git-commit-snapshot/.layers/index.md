---
title: "Un commit est un instantané"
description: "Ce qu'un commit contient réellement : un état complet des fichiers, un parent, un auteur et un message."
tags:
  - bit
  - git
difficulty: beginner
duration: 10
requires: "0.4.0"
---

Un commit enregistre l'état complet de vos fichiers, et non une liste de différences. Le comprendre explique pourquoi un commit ne se modifie jamais. Vous allez en ouvrir un pour lire ce qu'il contient.

**Prérequis** : savoir créer des commits, ce qu'enseigne [Enregistrer son travail avec Git](https://byte-layers.com/fr/skills/git-first-commits), et avoir réglé votre identité Git.

# Un commit est un instantané

Un **commit** enregistre l'état complet du projet à un instant donné, ce qu'on appelle un **instantané** (en anglais *snapshot*). La différence que montre `git show` n'est pas ce que le modèle de Git enregistre : il la calcule à la demande, en comparant deux instantanés.

> 💡 **Remarque.** Pour gagner de la place, Git compresse ensuite ses données sur le disque, sans que cela change ce modèle.

## 1 - Ouvrir un commit pour lire son contenu

Créez un petit dépôt de deux commits. Ce sont les commandes du cours en prérequis, et le second commit ne change que `index.html`.

```exec
mkdir -p ~/layers-git/l1-snapshot && cd ~/layers-git/l1-snapshot && git init -b main
echo '# Runbook' > runbook.md && echo '<h1>Statut des services</h1>' > index.html
git add runbook.md index.html && git commit -m "État initial"
echo '<p>API : OK</p>' >> index.html && git add index.html && git commit -m "Affiche l'état de l'API"
```

`git cat-file -p` affiche le contenu brut d'un objet de Git, et `HEAD` désigne l'endroit où vous êtes, ici le dernier commit de votre branche :

```exec
cd ~/layers-git/l1-snapshot && git cat-file -p HEAD
```

Tout le commit tient en ces quelques lignes, et aucune ne décrit une différence :

```text
tree 91c72057b6cf61b4149f6598866d1353d60f5674
parent d4275902578bcf024d5cd5d99656a5bf65254620
author John Doe <john.doe@example.com> 1794163238 +0100
committer John Doe <john.doe@example.com> 1794163238 +0100

Affiche l'état de l'API
```

| Ligne | Ce qu'elle dit |
|---|---|
| `tree` | l'instantané des fichiers à cet instant, sous la forme d'une liste |
| `parent` | le commit précédent, c'est lui qui relie les commits en historique |
| `author`, `committer` | qui a écrit le changement, et qui l'a enregistré, avec la date en secondes depuis 1970 |
| le texte final | le message |

## 2 - Comparer deux instantanés qui partagent un fichier

Tout instantané n'est pas pour autant une copie de tous les fichiers. `git ls-tree` liste le contenu de l'instantané d'un commit, et `HEAD~1` désigne le commit juste avant `HEAD` :

```exec
cd ~/layers-git/l1-snapshot && git ls-tree HEAD
cd ~/layers-git/l1-snapshot && git ls-tree HEAD~1
```

Chaque fichier est désigné par le hash de son contenu, et Git nomme **blob** ce contenu stocké. Les deux premières lignes viennent du commit récent, les deux suivantes du précédent. Le hash de `index.html` change, et celui de `runbook.md` est identique puisque ce fichier n'a pas changé : Git réutilise le même blob et ne le stocke qu'une fois.

```text
100644 blob 6a65fe2ec139511129dda750537a6b4278f16322	index.html
100644 blob 6d4af6828c69f8f2fade4354ff3b1305ff255dc6	runbook.md
100644 blob 94d6643972b6d08e11ea02310c631be25ee310d5	index.html
100644 blob 6d4af6828c69f8f2fade4354ff3b1305ff255dc6	runbook.md
```

## 3 - Pourquoi un commit ne se modifie jamais

Le hash d'un commit est calculé à partir de tout ce que vous venez de lire : l'instantané, le parent, l'auteur, la date, le message. Changez une seule lettre du message et le hash change, donc ce n'est plus le même commit. Une commande qui semble « modifier » un commit, comme `git commit --amend`, en crée en réalité un nouveau.

## 4 - Ranger le dossier de cette manipulation

Ce dossier ne sert plus, et vous pouvez le supprimer depuis votre dossier personnel :

```exec
cd ~ && rm -rf ~/layers-git/l1-snapshot
```

## Récap

- Un commit contient un instantané complet (`tree`), son parent, un auteur, une date et un message.
- La différence affichée par `git show` est calculée en comparant deux instantanés.
- Un fichier inchangé n'est stocké qu'une fois, ce qui garde le dépôt léger.
- Le hash dépend de tout le contenu du commit : un commit « modifié » est un nouveau commit.

> 📖 [Les objets de Git, dans le livre Pro Git](https://git-scm.com/book/fr/v2/Les-tripes-de-Git-Les-objets-de-Git) · [`git cat-file`](https://git-scm.com/docs/git-cat-file)
