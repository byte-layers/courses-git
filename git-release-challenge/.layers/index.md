---
title: "Maintenir deux versions, sans guide"
description: "Publier deux versions en trunk-based, créer leurs branches de maintenance, et reporter un correctif de l'une à l'autre, à partir d'un cahier des charges."
tags:
  - challenge
  - git
difficulty: intermediate
duration: 20
introTitle: "Le défi"
requires: "0.4.0"
options:
  allowManualProgress: false
  autoCompleteOnNext: unverifiable
---

Ce challenge prouve que vous savez publier des versions et en maintenir plusieurs. Le projet suit le trunk-based development : tout se passe sur `main`, et chaque version maintenue a sa propre branche. Il n'y a **aucune commande à recopier** : chaque tâche donne un objectif et des critères, puis un bouton vérifie l'état réel des dépôts.

Si vous êtes bloqué, les **indices** se dévoilent un par un, et la **solution** reste en dernier recours. Les utiliser ne coûte rien : seule la vérification compte.

## Avant de commencer

- **Ce qu'il faut savoir** : ce qu'enseignent [Livrer des versions avec Gitflow](https://byte-layers.com/fr/labs/git-release-flow) et [Rebase et cherry-pick](https://byte-layers.com/fr/skills/git-rebase-cherry-pick).
- **Ce qu'il faut avoir** : Git 2.28 ou plus récent, votre identité réglée, et un terminal (Git Bash sous Windows).
- **Un dépôt de départ** : `~/layers-git/l5-challenge/depot` et son serveur `serveur.git` sont créés pour vous à l'ouverture. Le fichier `runbook.md` contient une erreur de seuil, que vous corrigerez plus tard. La dernière tâche supprime tout.
- **L'ordre compte** : chaque tâche reprend l'état laissé par la précédente.

# Tâche 1 : publier la version 1

## Taguer v1.0 et créer sa branche de maintenance

```setup
D=~/layers-git/l5-challenge
if [ ! -d "$D/depot/.git" ]; then
  mkdir -p "$D/depot" && git init -q --bare -b main "$D/serveur.git"
  cd "$D/depot" && git init -q -b main
  G="git -c user.name=byte_layers -c user.email=contact@byte-layers.com"
  printf '# Runbook\n\nSeuil : 500 minutes\n' > runbook.md
  git add runbook.md && $G commit -q -m "État initial"
  git remote add origin "$D/serveur.git" && git push -q -u origin main
fi
```

Le commit actuel de `main` est prêt à être livré. Marquez-le comme version `v1.0`, créez la branche de maintenance `version/1.x` à partir de ce tag, et publiez le tout.

**Critères :**

- le serveur possède le tag `v1.0` ;
- le serveur possède la branche `version/1.x`, au même commit que le tag.

```hint
Un tag ne part pas sur le serveur tout seul, il faut le nommer.
```

```verify
S=~/layers-git/l5-challenge/serveur.git
if ! git -C "$S" rev-parse -q --verify refs/tags/v1.0 >/dev/null; then
  echo "Le serveur n'a pas le tag v1.0."
  exit 1
fi
if [ "$(git -C "$S" rev-parse v1.0^{commit})" != "$(git -C "$S" rev-parse version/1.x 2>/dev/null)" ]; then
  echo "La branche version/1.x devrait exister sur le serveur, au même commit que v1.0."
  exit 1
fi
echo "La version 1 est publiée, avec sa branche de maintenance."
```

````solution
```bash
cd ~/layers-git/l5-challenge/depot && git tag -a v1.0 -m "Version 1.0"
cd ~/layers-git/l5-challenge/depot && git branch version/1.x v1.0
cd ~/layers-git/l5-challenge/depot && git push origin v1.0 version/1.x
```
````

# Tâche 2 : publier la version 2

## Ajouter une fonctionnalité sur main puis publier v2.0

Sur `main`, ajoutez un fichier `feature2.txt` dans un commit, marquez ce commit comme `v2.0`, créez sa branche de maintenance `version/2.x`, et publiez le tout, `main` compris.

**Critères :**

- `main` sur le serveur contient `feature2.txt` ;
- le serveur possède le tag `v2.0` et la branche `version/2.x`, au même commit ;
- la branche `version/1.x` ne contient pas `feature2.txt`.

```hint
Le geste est le même qu'à la tâche précédente, après un commit sur `main`.
```

```verify
S=~/layers-git/l5-challenge/serveur.git
if ! git -C "$S" show main:feature2.txt >/dev/null 2>&1; then
  echo "main sur le serveur ne contient pas feature2.txt."
  exit 1
fi
if [ "$(git -C "$S" rev-parse v2.0^{commit} 2>/dev/null)" != "$(git -C "$S" rev-parse version/2.x 2>/dev/null)" ]; then
  echo "Le tag v2.0 et la branche version/2.x devraient exister sur le serveur, au même commit."
  exit 1
fi
if git -C "$S" show version/1.x:feature2.txt >/dev/null 2>&1; then
  echo "version/1.x ne devrait pas contenir feature2.txt."
  exit 1
fi
echo "La version 2 est publiée."
```

````solution
```bash
cd ~/layers-git/l5-challenge/depot && echo 'Nouveauté' > feature2.txt && git add feature2.txt && git commit -m "Ajoute la fonctionnalité 2"
cd ~/layers-git/l5-challenge/depot && git tag -a v2.0 -m "Version 2.0" && git branch version/2.x v2.0
cd ~/layers-git/l5-challenge/depot && git push origin main v2.0 version/2.x
```
````

# Tâche 3 : corriger la version 2

## Corriger le seuil sur version/2.x et publier v2.1

Le seuil du runbook est faux, et la version 2 en production est touchée. Ici, l'urgence fait partir le correctif de sa branche de version. En trunk-based, on le fait normalement sur `main`, puis on le reporte vers les versions. Sur la branche `version/2.x`, remplacez la ligne `Seuil : 500 minutes` par `Seuil : 5 minutes`, dans un seul commit, que vous reporterez à la tâche suivante. Marquez ce commit comme `v2.1`, et publiez la branche et le tag.

**Critères :**

- le tag `v2.1`, sur le serveur, contient la ligne `Seuil : 5 minutes` ;
- la branche `version/2.x` du serveur contient ce commit.

```hint
Placez-vous d'abord sur la bonne branche.
```

```verify
S=~/layers-git/l5-challenge/serveur.git
if ! git -C "$S" show v2.1:runbook.md 2>/dev/null | grep -qx "Seuil : 5 minutes"; then
  echo "Le tag v2.1 devrait exister sur le serveur et contenir la ligne Seuil : 5 minutes."
  exit 1
fi
if ! git -C "$S" merge-base --is-ancestor v2.1 version/2.x; then
  echo "version/2.x devrait contenir le commit du tag v2.1 sur le serveur."
  exit 1
fi
echo "La version 2.1 est publiée."
```

````solution
```bash
cd ~/layers-git/l5-challenge/depot && git switch version/2.x
cd ~/layers-git/l5-challenge/depot && printf '# Runbook\n\nSeuil : 5 minutes\n' > runbook.md && git commit -am "Corrige le seuil"
cd ~/layers-git/l5-challenge/depot && git tag -a v2.1 -m "Version 2.1" && git push origin version/2.x v2.1
```
````

# Tâche 4 : reporter le correctif

## Reporter la correction sur version/1.x et sur main

Reportez cette seule correction sur la branche `version/1.x`, marquez-la comme `v1.1`, et reportez-la aussi sur `main`. Publiez le tout.

**Critères :**

- le tag `v1.1`, sur le serveur, contient `Seuil : 5 minutes`, et ne contient pas `feature2.txt` ;
- `main` sur le serveur contient `Seuil : 5 minutes`.

```hint
Une commande reporte un commit précis sur la branche où vous êtes. `version/2.x` désigne son dernier commit.
```

```verify
S=~/layers-git/l5-challenge/serveur.git
if ! git -C "$S" show v1.1:runbook.md 2>/dev/null | grep -qx "Seuil : 5 minutes"; then
  echo "Le tag v1.1 devrait exister sur le serveur et contenir la ligne Seuil : 5 minutes."
  exit 1
fi
if git -C "$S" show v1.1:feature2.txt >/dev/null 2>&1; then
  echo "La version 1.1 ne devrait pas contenir feature2.txt."
  exit 1
fi
if ! git -C "$S" merge-base --is-ancestor v1.1 version/1.x; then
  echo "La branche version/1.x du serveur devrait contenir le commit du tag v1.1."
  exit 1
fi
if ! git -C "$S" show main:runbook.md | grep -qx "Seuil : 5 minutes"; then
  echo "main sur le serveur devrait contenir la correction."
  exit 1
fi
echo "La correction est reportée sur les deux lignes."
```

````solution
```bash
cd ~/layers-git/l5-challenge/depot && git switch version/1.x && git cherry-pick version/2.x
cd ~/layers-git/l5-challenge/depot && git tag -a v1.1 -m "Version 1.1" && git push origin version/1.x v1.1
cd ~/layers-git/l5-challenge/depot && git switch main && git cherry-pick version/2.x && git push origin main
```
````

# Tâche 5 : ne rien laisser derrière soi

## Supprimer le dossier du challenge

Supprimez le dossier `~/layers-git/l5-challenge` et tout ce qu'il contient. Vérifiez d'abord que votre terminal ne se trouve pas dedans.

**Critère :** le dossier `~/layers-git/l5-challenge` n'existe plus.

```verify
if [ -e ~/layers-git/l5-challenge ]; then
  echo "Le dossier ~/layers-git/l5-challenge existe encore."
  exit 1
fi
echo "Le dossier est supprimé. Challenge terminé."
```

````solution
```bash
cd ~ && rm -rf ~/layers-git/l5-challenge
```
````
