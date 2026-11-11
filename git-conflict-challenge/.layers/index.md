---
title: "Fusionner et résoudre un conflit, sans guide"
description: "Créer une branche, fusionner en avance rapide, fusionner des historiques divergents et résoudre un conflit, à partir d'un cahier des charges."
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

Ce challenge prouve que vous savez brancher, fusionner et résoudre un conflit. Il n'y a **aucune commande à recopier** : chaque tâche donne un objectif et des critères, puis un bouton vérifie l'état réel du dépôt. Toute suite de commandes qui produit le bon résultat est acceptée.

Si vous êtes bloqué, les **indices** se dévoilent un par un, et la **solution** reste en dernier recours. Les utiliser ne coûte rien : seule la vérification compte.

## Avant de commencer

- **Ce qu'il faut savoir** : ce qu'enseigne [Travailler en parallèle avec les branches](https://byte-layers.com/fr/skills/git-branches-merge).
- **Ce qu'il faut avoir** : Git 2.28 ou plus récent, votre identité réglée, et un terminal (Git Bash sous Windows).
- **Un dépôt de départ** : `~/byte-layers/git/l2-challenge` est créé pour vous à l'ouverture. Il contient le projet `statuspage`, avec la branche `main` et deux branches prêtes à être fusionnées, `feature/seuil-bas` et `feature/seuil-haut`. La dernière tâche le supprime.
- **L'ordre compte** : chaque tâche reprend l'état laissé par la précédente.

# Tâche 1 : une nouveauté en avance rapide

## Ajouter une bannière sur une branche et la fusionner

```setup
D=~/byte-layers/git/l2-challenge
if [ ! -d "$D/.git" ]; then
  mkdir -p "$D" && cd "$D" && git init -q -b main
  G="git -c user.name=byte_layers -c user.email=contact@byte-layers.com"
  echo '<h1>Statut des services</h1>' > index.html
  printf '# Runbook\n\nAlerte au bout de : 5 minutes\n' > runbook.md
  git add . && $G commit -q -m "État initial"
  git switch -q -c feature/seuil-bas
  printf '# Runbook\n\nAlerte au bout de : 2 minutes\n' > runbook.md
  $G commit -q -am "Abaisse le seuil à 2 minutes"
  git switch -q main && git switch -q -c feature/seuil-haut
  printf '# Runbook\n\nAlerte au bout de : 15 minutes\n' > runbook.md
  $G commit -q -am "Relève le seuil à 15 minutes"
  git switch -q main
fi
```

Le dépôt de départ se trouve dans `~/byte-layers/git/l2-challenge`. Créez-y une branche `feature/banniere`, ajoutez une ligne contenant le mot `Maintenance` à `index.html` dans un commit, puis amenez ce travail sur `main`.

**Critères :**

- la branche `feature/banniere` existe, et elle a au moins un commit de plus que l'état de départ ;
- `main` contient le travail de cette branche ;
- `index.html` contient le mot `Maintenance` sur `main` ;
- `main` n'a pas de commit de merge : la fusion s'est faite en avance rapide ;
- vous êtes sur `main`, et aucun changement n'est en attente.

```hint
Une commande crée la branche et vous y place en même temps.
```

```hint
Une fusion se lance depuis la branche qui reçoit le travail.
```

```verify
D=~/byte-layers/git/l2-challenge
if ! git -C "$D" show-ref --verify --quiet refs/heads/feature/banniere; then
  echo "La branche feature/banniere n'existe pas."
  exit 1
fi
if [ "$(git -C "$D" symbolic-ref --short HEAD)" != "main" ]; then
  echo "Vous devriez être sur main."
  exit 1
fi
if ! git -C "$D" merge-base --is-ancestor feature/banniere main; then
  echo "main ne contient pas encore le travail de feature/banniere."
  exit 1
fi
if [ "$(git -C "$D" rev-list --count main)" -lt 2 ]; then
  echo "feature/banniere devrait ajouter au moins un commit."
  exit 1
fi
if ! git -C "$D" show main:index.html | grep -q Maintenance; then
  echo "index.html ne contient pas le mot Maintenance sur main."
  exit 1
fi
if [ -n "$(git -C "$D" rev-list --merges main)" ]; then
  echo "main contient un commit de merge : la fusion n'était pas une avance rapide."
  exit 1
fi
if [ -n "$(git -C "$D" status --porcelain)" ]; then
  echo "Il reste des changements en attente."
  exit 1
fi
echo "La bannière est sur main, en avance rapide."
```

````solution
```bash
cd ~/byte-layers/git/l2-challenge && git switch -c feature/banniere
cd ~/byte-layers/git/l2-challenge && echo '<p>Maintenance prévue</p>' >> index.html && git commit -am "Ajoute la bannière"
cd ~/byte-layers/git/l2-challenge && git switch main && git merge feature/banniere
```
````

# Tâche 2 : fusionner un historique qui a divergé

## Amener le seuil bas sur main

Fusionnez la branche `feature/seuil-bas` dans `main`. Comme `main` a avancé depuis sa création, Git doit réunir les deux historiques.

**Critères :**

- `main` contient le travail de `feature/seuil-bas` ;
- le dernier commit de `main` est un commit de merge ;
- le runbook de `main` indique `2 minutes`.

```hint
Sans option, Git ouvrira un éditeur pour le message du commit. Une option de `git merge` accepte le message proposé.
```

```verify
D=~/byte-layers/git/l2-challenge
if ! git -C "$D" merge-base --is-ancestor feature/seuil-bas main; then
  echo "main ne contient pas encore le travail de feature/seuil-bas."
  exit 1
fi
if [ "$(git -C "$D" rev-list --parents -n 1 main | wc -w | tr -d ' ')" != "3" ]; then
  echo "Le dernier commit de main devrait être un commit de merge."
  exit 1
fi
if ! git -C "$D" show main:runbook.md | grep -q "2 minutes"; then
  echo "Le runbook de main devrait indiquer 2 minutes."
  exit 1
fi
echo "Les deux historiques sont réunis."
```

````solution
```bash
cd ~/byte-layers/git/l2-challenge && git merge --no-edit feature/seuil-bas
```
````

# Tâche 3 : résoudre le désaccord sur le seuil

## Fusionner le seuil haut en retenant 10 minutes

Fusionnez `feature/seuil-haut` dans `main`. Les deux branches ne sont pas d'accord sur le seuil d'alerte, et votre équipe tranche pour une troisième valeur : la ligne finale doit être exactement `Alerte au bout de : 10 minutes`.

**Critères :**

- aucune fusion n'est en cours ;
- `main` contient le travail de `feature/seuil-haut` ;
- le runbook ne contient plus aucun marqueur de conflit ;
- il contient la ligne exacte `Alerte au bout de : 10 minutes`.

```hint
Le fichier en conflit montre les deux versions entre des marqueurs. Vous écrivez le contenu final.
```

```hint
Après avoir corrigé le fichier, deux commandes concluent la fusion, et la première marque le fichier comme résolu.
```

```verify
D=~/byte-layers/git/l2-challenge
if git -C "$D" rev-parse -q --verify MERGE_HEAD >/dev/null; then
  echo "Une fusion est encore en cours : terminez-la."
  exit 1
fi
if ! git -C "$D" merge-base --is-ancestor feature/seuil-haut main; then
  echo "main ne contient pas encore le travail de feature/seuil-haut."
  exit 1
fi
if git -C "$D" show main:runbook.md | grep -qE '^(<<<<<<<|=======|>>>>>>>)'; then
  echo "Le runbook de main contient encore des marqueurs de conflit."
  exit 1
fi
if ! git -C "$D" show main:runbook.md | grep -qx "Alerte au bout de : 10 minutes"; then
  echo "Le runbook de main ne contient pas la ligne exacte attendue."
  exit 1
fi
echo "Le conflit est résolu : 10 minutes."
```

````solution
```bash
cd ~/byte-layers/git/l2-challenge && git merge feature/seuil-haut
printf '# Runbook\n\nAlerte au bout de : 10 minutes\n' > ~/byte-layers/git/l2-challenge/runbook.md
cd ~/byte-layers/git/l2-challenge && git add runbook.md && git commit --no-edit
```
````

# Tâche 4 : supprimer les branches devenues inutiles

## Supprimer les trois branches fusionnées

Supprimez les trois branches qui ont été fusionnées. Vérifiez qu'il ne reste que `main`, puis passez à la dernière tâche.

**Critère :** `main` est la seule branche du dépôt.

```hint
L'option qui supprime une branche refuse de le faire si elle n'est pas fusionnée, ce qui vous protège ici.
```

```verify
D=~/byte-layers/git/l2-challenge
if [ "$(git -C "$D" for-each-ref --format='%(refname:short)' refs/heads/ | tr -d '\n')" != "main" ]; then
  echo "Il devrait ne rester que la branche main."
  exit 1
fi
echo "Il ne reste que main."
```

````solution
```bash
cd ~/byte-layers/git/l2-challenge && git branch -d feature/banniere feature/seuil-bas feature/seuil-haut
```
````

# Tâche 5 : ne rien laisser derrière soi

## Supprimer le dossier du challenge

Supprimez le dossier `~/byte-layers/git/l2-challenge` et tout ce qu'il contient. Vérifiez d'abord que votre terminal ne se trouve pas dedans.

**Critère :** le dossier `~/byte-layers/git/l2-challenge` n'existe plus.

```verify
if [ -e ~/byte-layers/git/l2-challenge ]; then
  echo "Le dossier ~/byte-layers/git/l2-challenge existe encore."
  exit 1
fi
echo "Le dossier est supprimé. Challenge terminé."
```

````solution
```bash
cd ~ && rm -rf ~/byte-layers/git/l2-challenge
```
````
