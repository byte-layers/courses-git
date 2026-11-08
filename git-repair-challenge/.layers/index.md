---
title: "Réparer un dépôt, sans guide"
description: "Corriger un commit, annuler un commit publié, retrouver un commit perdu et reporter un correctif, à partir d'un cahier des charges."
tags:
  - challenge
  - git
difficulty: intermediate
duration: 30
introTitle: "Le défi"
requires: "0.4.0"
options:
  allowManualProgress: false
  autoCompleteOnNext: unverifiable
---

Ce challenge prouve que vous savez choisir la bonne commande pour réparer un dépôt. Il n'y a **aucune commande à recopier** : chaque tâche donne un objectif et des critères, puis un bouton vérifie l'état réel du dépôt. Toute suite de commandes qui produit le bon résultat est acceptée.

Si vous êtes bloqué, les **indices** se dévoilent un par un, et la **solution** reste en dernier recours. Les utiliser ne coûte rien : seule la vérification compte.

## Avant de commencer

- **Ce qu'il faut savoir** : ce qu'enseignent [Annuler ses erreurs avec Git](https://byte-layers.com/fr/skills/git-undo) et [Rebase et cherry-pick](https://byte-layers.com/fr/skills/git-rebase-cherry-pick).
- **Ce qu'il faut avoir** : Git 2.28 ou plus récent, votre identité réglée, et un terminal (Git Bash sous Windows).
- **Un dépôt abîmé** : `~/layers-git/l4-challenge/depot` et son serveur `serveur.git` sont créés pour vous à l'ouverture. Regardez son historique avant de commencer. La dernière tâche supprime tout.
- **L'ordre compte** : chaque tâche reprend l'état laissé par la précédente.

# Tâche 1 : un message à corriger

## Corriger le message du dernier commit

```setup
D=~/layers-git/l4-challenge
if [ ! -d "$D/depot/.git" ]; then
  mkdir -p "$D/depot" && git init -q --bare -b main "$D/serveur.git"
  cd "$D/depot" && git init -q -b main
  G="git -c user.name=byte_layers -c user.email=contact@byte-layers.com"
  echo '<h1>Statut des services</h1>' > index.html && echo '# Runbook' > runbook.md
  git add index.html runbook.md && $G commit -q -m "État initial"
  git remote add origin "$D/serveur.git"
  echo '<p>PANNE</p>' >> index.html && $G commit -q -am "Ajoute le bandeau"
  git push -q -u origin main
  echo 'Plan de reprise' > reprise.md && git add reprise.md && $G commit -q -m "Ajoute le plan de reprise"
  git reset -q --hard HEAD~1
  git switch -q -c fix/page
  echo 'Titre corrigé' > titre.txt && git add titre.txt && $G commit -q -m "Corrige le titre"
  echo 'essai' > essai.txt && git add essai.txt && $G commit -q -m "Ajoute un essai"
  git switch -q main
  echo 'Astreinte : voir le planning' >> runbook.md && $G commit -q -am "Ajoute la procédure d'astrinte"
fi
```

Le dernier commit de `main`, pas encore publié, comporte une faute dans son message. Corrigez-le pour qu'il devienne exactement `Ajoute la procédure d'astreinte`.

**Critères :**

- le message exact `Ajoute la procédure d'astreinte` est dans l'historique de `main` ;
- le message fautif n'y est plus.

```hint
Une option de `git commit` remplace le dernier commit au lieu d'en créer un nouveau.
```

```verify
D=~/layers-git/l4-challenge/depot
if git -C "$D" log --format=%s main | grep -q "astrinte"; then
  echo "Le message fautif est encore dans l'historique de main."
  exit 1
fi
if ! git -C "$D" log --format=%s main | grep -qx "Ajoute la procédure d'astreinte"; then
  echo "Le message exact attendu n'est pas dans l'historique de main."
  exit 1
fi
echo "Le message est corrigé."
```

````solution
```bash
cd ~/layers-git/l4-challenge/depot && git commit --amend -m "Ajoute la procédure d'astreinte"
```
````

# Tâche 2 : un commit publié qui casse la page

## Annuler le commit « Ajoute le bandeau », sans réécrire l'historique

Le commit `Ajoute le bandeau`, déjà publié, affiche `PANNE` sur la page. Annulez ses effets et publiez le résultat, sans réécrire l'historique du serveur.

**Critères :**

- `index.html` ne contient plus `PANNE` sur la branche `main` du serveur ;
- le commit `Ajoute le bandeau` est toujours dans l'historique du serveur.

```hint
Ce commit n'est pas le dernier. Retrouvez son hash avec `git log --oneline`.
```

```hint
La commande qui crée un commit inverse accepte un hash.
```

```verify
S=~/layers-git/l4-challenge/serveur.git
if git -C "$S" show main:index.html | grep -q "PANNE"; then
  echo "index.html contient encore PANNE sur le serveur."
  exit 1
fi
if ! git -C "$S" log --format=%s main | grep -qx "Ajoute le bandeau"; then
  echo "Le commit Ajoute le bandeau a disparu de l'historique du serveur : il fallait l'annuler sans réécrire."
  exit 1
fi
echo "Le commit est annulé sur le serveur, et l'historique est intact."
```

````solution
Lisez le hash du commit avec `git log --oneline`, puis lancez `git revert --no-edit <hash>` et `git push`. La commande ci-dessous retrouve ce hash automatiquement :

```bash
cd ~/layers-git/l4-challenge/depot && git revert --no-edit $(git log --format=%h --grep="Ajoute le bandeau" main | head -n 1)
cd ~/layers-git/l4-challenge/depot && git push
```
````

# Tâche 3 : un commit perdu

## Retrouver le plan de reprise sur une branche

Un commit au message `Ajoute le plan de reprise` a été retiré par un `git reset --hard`, et il n'apparaît plus dans `git log`. Retrouvez-le, et créez une branche nommée `recuperation` qui pointe dessus.

**Critères :**

- la branche `recuperation` existe ;
- son dernier commit a pour message `Ajoute le plan de reprise` ;
- elle contient le fichier `reprise.md`.

```hint
Git tient un journal de tous les déplacements de `HEAD`.
```

```hint
`git branch` accepte un second argument, le commit sur lequel créer la branche.
```

```verify
D=~/layers-git/l4-challenge/depot
if ! git -C "$D" show-ref --verify --quiet refs/heads/recuperation; then
  echo "La branche recuperation n'existe pas."
  exit 1
fi
if [ "$(git -C "$D" log -1 --format=%s recuperation)" != "Ajoute le plan de reprise" ]; then
  echo "Le dernier commit de recuperation n'est pas le plan de reprise."
  exit 1
fi
if ! git -C "$D" show recuperation:reprise.md >/dev/null 2>&1; then
  echo "La branche recuperation ne contient pas reprise.md."
  exit 1
fi
echo "Le commit perdu est retrouvé."
```

````solution
Lisez le hash du commit avec `git reflog`, puis lancez `git branch recuperation <hash>`. La commande ci-dessous retrouve ce hash automatiquement :

```bash
cd ~/layers-git/l4-challenge/depot && git branch recuperation $(git log -g --format=%h --grep="Ajoute le plan de reprise" | head -n 1)
```
````

# Tâche 4 : un seul commit à reporter

## Reporter « Corrige le titre » sur main

La branche `fix/page` contient un commit `Corrige le titre` et un commit `Ajoute un essai`. Amenez uniquement le premier sur `main`.

**Critères :**

- `main` contient le fichier `titre.txt` ;
- `main` ne contient pas le fichier `essai.txt`.

```hint
Une fusion amènerait les deux commits. Une autre commande en prend un seul.
```

```verify
D=~/layers-git/l4-challenge/depot
if ! git -C "$D" show main:titre.txt >/dev/null 2>&1; then
  echo "main ne contient pas titre.txt."
  exit 1
fi
if git -C "$D" show main:essai.txt >/dev/null 2>&1; then
  echo "main ne devrait pas contenir essai.txt."
  exit 1
fi
echo "Seul le correctif est reporté."
```

````solution
```bash
cd ~/layers-git/l4-challenge/depot && git switch main && git cherry-pick fix/page~1
```
````

# Tâche 5 : ne rien laisser derrière soi

## Supprimer le dossier du challenge

Supprimez le dossier `~/layers-git/l4-challenge` et tout ce qu'il contient. Vérifiez d'abord que votre terminal ne se trouve pas dedans.

**Critère :** le dossier `~/layers-git/l4-challenge` n'existe plus.

```verify
if [ -e ~/layers-git/l4-challenge ]; then
  echo "Le dossier ~/layers-git/l4-challenge existe encore."
  exit 1
fi
echo "Le dossier est supprimé. Challenge terminé."
```

````solution
```bash
cd ~ && rm -rf ~/layers-git/l4-challenge
```
````
