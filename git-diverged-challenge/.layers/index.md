---
title: "Échanger avec un serveur, sans guide"
description: "Cloner, publier, réunir un historique divergent sans écraser un collègue et partager une branche, à partir d'un cahier des charges."
tags:
  - challenge
  - git
difficulty: beginner
duration: 20
introTitle: "Le défi"
requires: "0.4.0"
options:
  allowManualProgress: false
  autoCompleteOnNext: unverifiable
---

Ce challenge prouve que vous savez travailler avec un dépôt distant sans perdre le travail d'un collègue. Il n'y a **aucune commande à recopier** : chaque tâche donne un objectif et des critères, puis un bouton vérifie l'état réel des dépôts. Toute suite de commandes qui produit le bon résultat est acceptée.

Si vous êtes bloqué, les **indices** se dévoilent un par un, et la **solution** reste en dernier recours. Les utiliser ne coûte rien : seule la vérification compte.

## Avant de commencer

- **Ce qu'il faut savoir** : ce qu'enseigne [Partager son travail avec un dépôt distant](https://byte-layers.com/fr/skills/git-remotes).
- **Ce qu'il faut avoir** : Git 2.28 ou plus récent, votre identité réglée, et un terminal (Git Bash sous Windows).
- **Un serveur de départ** : le dépôt `~/byte-layers/git/l3-challenge/serveur.git` est créé pour vous à l'ouverture, avec un premier commit. Un collègue y publiera du travail pendant la tâche 2. La dernière tâche supprime tout.
- **L'ordre compte** : chaque tâche reprend l'état laissé par la précédente.

# Tâche 1 : rejoindre le projet

## Cloner le serveur et publier un premier fichier

```setup
D=~/byte-layers/git/l3-challenge
if [ ! -d "$D/serveur.git" ]; then
  mkdir -p "$D" && git init -q --bare -b main "$D/serveur.git"
  T=$(mktemp -d) && git init -q -b main "$T"
  echo '<h1>Statut des services</h1>' > "$T/index.html"
  git -C "$T" add index.html
  git -C "$T" -c user.name=byte_layers -c user.email=contact@byte-layers.com commit -q -m "État initial"
  git -C "$T" push -q "$D/serveur.git" main
  rm -rf "$T"
fi
```

Clonez le dépôt `~/byte-layers/git/l3-challenge/serveur.git` dans `~/byte-layers/git/l3-challenge/moi`. Ajoutez-y un fichier `runbook.md`, et publiez-le.

**Critères :**

- le dossier `~/byte-layers/git/l3-challenge/moi` est un clone du serveur ;
- la branche `main` du serveur contient `runbook.md`.

```hint
La commande de clonage prend l'adresse du dépôt, puis le nom du dossier à créer.
```

```verify
D=~/byte-layers/git/l3-challenge
case "$(git -C "$D/moi" remote get-url origin 2>/dev/null)" in
  *serveur.git|*serveur.git/) ;;
  *) echo "$D/moi n'est pas un clone de serveur.git."; exit 1 ;;
esac
if ! git -C "$D/serveur.git" show main:runbook.md >/dev/null 2>&1; then
  echo "Le serveur n'a pas runbook.md sur main."
  exit 1
fi
echo "Votre fichier est sur le serveur."
```

````solution
```bash
cd ~/byte-layers/git/l3-challenge && git clone serveur.git moi
cd ~/byte-layers/git/l3-challenge/moi && echo '# Runbook' > runbook.md && git add runbook.md && git commit -m "Ajoute le runbook" && git push
```
````

# Tâche 2 : publier après un collègue

## Réunir votre commit et celui du collègue

```setup
D=~/byte-layers/git/l3-challenge
if [ -d "$D/serveur.git" ] && [ ! -f "$D/.collegue-fait" ] && git -C "$D/serveur.git" rev-parse -q --verify main >/dev/null; then
  T=$(mktemp -d) && git clone -q "$D/serveur.git" "$T/c"
  echo '<p>API : OK</p>' >> "$T/c/index.html"
  git -C "$T/c" -c user.name="Sam Durand" -c user.email=sam@example.com commit -q -am "Affiche l'état de l'API"
  git -C "$T/c" push -q origin main
  rm -rf "$T"
  touch "$D/.collegue-fait"
fi
```

Un collègue vient de publier un commit sur le serveur, et vous ne l'avez pas encore. Sans récupérer son travail, ajoutez une ligne à `runbook.md` dans un commit, puis faites en sorte que votre commit soit sur le serveur.

**Critères :**

- la branche `main` du serveur contient votre ligne dans `runbook.md` ;
- elle contient toujours le commit du collègue, dont le message est `Affiche l'état de l'API` ;
- votre branche `main` locale est identique à celle du serveur.

```hint
Essayez d'abord de publier, et lisez le message de refus.
```

```hint
Quand les historiques divergent, `git pull` demande une option pour savoir comment les réunir.
```

```verify
D=~/byte-layers/git/l3-challenge
S="$D/serveur.git"
if [ "$(git -C "$S" log --format=%s main | grep -c "Affiche l'état de l'API")" -lt 1 ]; then
  echo "Le commit du collègue n'est plus sur le serveur. Il a été écrasé, ou la tâche n'a pas commencé."
  exit 1
fi
if [ "$(git -C "$S" log --format=%h main -- runbook.md | wc -l | tr -d ' ')" -lt 2 ]; then
  echo "Votre changement de runbook.md n'est pas sur le serveur."
  exit 1
fi
if [ "$(git -C "$S" rev-parse main)" != "$(git -C "$D/moi" rev-parse main)" ]; then
  echo "Votre branche main locale n'est pas identique à celle du serveur."
  exit 1
fi
echo "Les deux travaux sont sur le serveur."
```

````solution
```bash
cd ~/byte-layers/git/l3-challenge/moi && echo 'Alerte au bout de : 5 minutes' >> runbook.md && git commit -am "Ajoute le seuil d'alerte"
cd ~/byte-layers/git/l3-challenge/moi && git pull --no-rebase --no-edit && git push
```
````

# Tâche 3 : partager une branche

## Publier une branche reliée au serveur

Créez une branche `feature/contacts`, avec un commit, puis publiez-la en la reliant au serveur.

**Critères :**

- le serveur possède la branche `feature/contacts` ;
- votre branche locale du même nom suit `origin/feature/contacts`.

```hint
La première publication d'une branche demande une option, qui retient le lien pour la suite.
```

```verify
D=~/byte-layers/git/l3-challenge
if ! git -C "$D/serveur.git" show-ref --verify --quiet refs/heads/feature/contacts; then
  echo "Le serveur n'a pas la branche feature/contacts."
  exit 1
fi
if [ "$(git -C "$D/serveur.git" rev-list --count main..feature/contacts)" -lt 1 ]; then
  echo "La branche feature/contacts devrait avoir au moins un commit de plus que main sur le serveur."
  exit 1
fi
if [ "$(git -C "$D/moi" rev-parse --abbrev-ref feature/contacts@{upstream} 2>/dev/null)" != "origin/feature/contacts" ]; then
  echo "Votre branche feature/contacts n'est pas reliée à origin/feature/contacts."
  exit 1
fi
echo "La branche est publiée et reliée."
```

````solution
```bash
cd ~/byte-layers/git/l3-challenge/moi && git switch -c feature/contacts
cd ~/byte-layers/git/l3-challenge/moi && echo '## Contacts' >> runbook.md && git commit -am "Ajoute les contacts"
cd ~/byte-layers/git/l3-challenge/moi && git push -u origin feature/contacts
```
````

# Tâche 4 : ne rien laisser derrière soi

## Supprimer le dossier du challenge

Supprimez le dossier `~/byte-layers/git/l3-challenge` et tout ce qu'il contient. Vérifiez d'abord que votre terminal ne se trouve pas dedans.

**Critère :** le dossier `~/byte-layers/git/l3-challenge` n'existe plus.

```verify
if [ -e ~/byte-layers/git/l3-challenge ]; then
  echo "Le dossier ~/byte-layers/git/l3-challenge existe encore."
  exit 1
fi
echo "Le dossier est supprimé. Challenge terminé."
```

````solution
```bash
cd ~ && rm -rf ~/byte-layers/git/l3-challenge
```
````
