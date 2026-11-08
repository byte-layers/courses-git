---
title: "05 - Publier une branche pour la partager"
description: "git push -u sur une nouvelle branche, et la récupérer depuis un autre poste"
---

Les branches restent sur votre machine tant que vous ne les publiez pas. En publier une permet de la sauvegarder sur le serveur, et de la faire relire ou reprendre par un collègue.

## 05.1 - Envoyer une nouvelle branche sur le serveur

Sur `poste-b`, créez une branche avec un commit :

```exec
cd ~/layers-git/l3/poste-b && git switch -c feature/contacts
cd ~/layers-git/l3/poste-b && echo '## Contacts' >> runbook.md
cd ~/layers-git/l3/poste-b && git commit -am "Ajoute les contacts"
```

Le serveur ne connaît pas encore cette branche, et `-u` crée le lien avec `origin`, comme lors du premier envoi de `main` :

```exec
cd ~/layers-git/l3/poste-b && git push -u origin feature/contacts
```

Le serveur possède maintenant cette branche :

```text
 * [new branch]      feature/contacts -> feature/contacts
branch 'feature/contacts' set up to track 'origin/feature/contacts'.
```

## 05.2 - Récupérer la branche depuis l'autre poste

Sur `poste-a`, `git fetch` découvre la nouvelle branche :

```exec
cd ~/layers-git/l3/poste-a && git fetch
cd ~/layers-git/l3/poste-a && git branch -a
```

Elle apparaît sous `remotes/origin/`, mais vous n'avez pas encore de branche locale à ce nom. `git switch` la crée pour vous, reliée au serveur :

```exec
cd ~/layers-git/l3/poste-a && git switch feature/contacts
```

Git crée la branche locale et la relie au serveur :

```text
Switched to a new branch 'feature/contacts'
branch 'feature/contacts' set up to track 'origin/feature/contacts'.
```

```verify
D=~/layers-git/l3
if ! git -C "$D/serveur.git" show-ref --verify --quiet refs/heads/feature/contacts; then
  echo "Le serveur n'a pas la branche feature/contacts."
  exit 1
fi
if [ "$(git -C "$D/poste-a" rev-parse --abbrev-ref feature/contacts@{upstream} 2>/dev/null)" != "origin/feature/contacts" ]; then
  echo "poste-a n'a pas de branche feature/contacts reliée au serveur. Lancez git fetch, puis git switch feature/contacts."
  exit 1
fi
echo "La branche est partagée entre les deux postes."
```

## 05.3 - Ranger le dossier de ce cours

Ce dossier ne servira plus, et vous pouvez le supprimer depuis votre dossier personnel. `rm -rf` efface le dossier et son contenu sans demander de confirmation :

```exec
cd ~ && rm -rf ~/layers-git/l3
```

```verify
if [ -e ~/layers-git/l3 ]; then
  echo "Le dossier ~/layers-git/l3 existe encore."
  exit 1
fi
echo "Le dossier est supprimé."
```

## Récap

- Un dépôt distant est un dépôt de référence, nommé `origin` par convention. `git remote add` le déclare, et `git clone` le fait pour vous.
- `git push` publie vos commits, et `-u` relie la branche la première fois.
- `git fetch` télécharge sans rien changer. `git pull` télécharge et intègre.
- Un push refusé signale du travail que vous n'avez pas : récupérez-le, réunissez les historiques, puis publiez.

Le bit [Main et origin/main](https://byte-layers.com/fr/bits/git-remote-tracking) précise ce que Git retient du serveur. Pour vous tester sans guide, faites le challenge [Échanger avec un serveur, sans guide](https://byte-layers.com/fr/challenges/git-diverged-challenge).

> 📖 [Travailler avec des dépôts distants, dans le livre Pro Git](https://git-scm.com/book/fr/v2/Les-bases-de-Git-Travailler-avec-des-d%C3%A9p%C3%B4ts-distants)
