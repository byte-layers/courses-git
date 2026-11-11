---
title: "Créer un historique propre, sans guide"
description: "Créer un dépôt, faire des commits ciblés, ignorer un fichier sensible et relire l'historique, à partir d'un cahier des charges."
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

Ce challenge prouve que vous savez créer un dépôt, faire des commits ciblés et relire un historique. Il n'y a **aucune commande à recopier** : chaque tâche donne un objectif et des critères, puis un bouton vérifie l'état réel du dépôt. Toute suite de commandes qui produit le bon résultat est acceptée.

Si vous êtes bloqué, les **indices** se dévoilent un par un, et la **solution** reste en dernier recours. Les utiliser ne coûte rien : seule la vérification compte.

## Avant de commencer

- **Ce qu'il faut savoir** : ce qu'enseigne [Enregistrer son travail avec Git](https://byte-layers.com/fr/skills/git-first-commits).
- **Ce qu'il faut avoir** : Git 2.28 ou plus récent, votre identité déjà réglée, et un terminal (Git Bash sous Windows).
- **Un dossier de travail** : `~/byte-layers/git/l1-challenge` est créé pour vous, et la dernière tâche le supprime.
- **L'ordre compte** : chaque tâche reprend le dépôt de la précédente.

# Tâche 1 : un dépôt et ses deux premiers fichiers

## Créer le dépôt statuspage avec une page et un runbook

```setup
mkdir -p ~/byte-layers/git/l1-challenge
```

Créez un dépôt Git dans `~/byte-layers/git/l1-challenge/statuspage`, puis enregistrez-y une page de statut et un runbook.

**Critères :**

- le dossier `~/byte-layers/git/l1-challenge/statuspage` est un dépôt Git, sur la branche `main` ;
- il contient au moins un commit ;
- le dernier commit contient les fichiers `index.html` et `runbook.md`, avec le contenu de votre choix ;
- il ne reste aucun changement en attente.

```hint
Créez le dossier, placez-vous dedans, et initialisez le dépôt en nommant sa branche.
```

```hint
Un fichier vide ne suffit pas à rendre un commit parlant : `echo 'du texte' > fichier` en crée un avec du contenu.
```

```verify
D=~/byte-layers/git/l1-challenge/statuspage
if ! git -C "$D" rev-parse --git-dir >/dev/null 2>&1; then
  echo "$D n'est pas un dépôt Git."
  exit 1
fi
if [ "$(git -C "$D" symbolic-ref --short HEAD)" != "main" ]; then
  echo "Le dépôt n'est pas sur la branche main."
  exit 1
fi
if ! git -C "$D" rev-parse HEAD >/dev/null 2>&1; then
  echo "Le dépôt n'a encore aucun commit."
  exit 1
fi
for F in index.html runbook.md; do
  if ! git -C "$D" ls-tree --name-only HEAD | grep -qx "$F"; then
    echo "$F n'est pas dans le dernier commit."
    exit 1
  fi
done
if [ -n "$(git -C "$D" status --porcelain)" ]; then
  echo "Il reste des changements en attente : regardez git status."
  exit 1
fi
echo "Le dépôt et ses deux fichiers sont enregistrés."
```

````solution
```bash
mkdir -p ~/byte-layers/git/l1-challenge/statuspage
cd ~/byte-layers/git/l1-challenge/statuspage && git init -b main
echo '<h1>Statut</h1>' > index.html && echo '# Runbook' > runbook.md
git add index.html runbook.md && git commit -m "Ajoute la page et le runbook"
```
````

# Tâche 2 : un secret qui reste hors du dépôt

## Faire ignorer un fichier .env

Placez dans le dépôt un fichier `.env` contenant une valeur factice, et faites en sorte qu'il n'entre jamais dans l'historique.

**Critères :**

- le fichier `.env` existe dans le dossier de travail ;
- Git l'ignore ;
- la règle qui l'ignore est enregistrée dans un commit, pour toute l'équipe ;
- `.env` n'apparaît dans aucun commit.

```hint
Git lit un fichier spécial, à raison d'un motif par ligne.
```

```hint
Ce fichier s'appelle `.gitignore`, et il s'enregistre comme les autres.
```

```verify
D=~/byte-layers/git/l1-challenge/statuspage
if [ ! -f "$D"/.env ]; then
  echo "Le fichier .env n'existe pas."
  exit 1
fi
if ! git -C "$D" check-ignore -q .env; then
  echo "Git n'ignore pas .env."
  exit 1
fi
if ! git -C "$D" ls-tree --name-only HEAD | grep -qx .gitignore; then
  echo "La règle n'est pas enregistrée dans un commit."
  exit 1
fi
if [ -n "$(git -C "$D" log --all --oneline -- .env)" ]; then
  echo ".env est entré dans l'historique. Recommencez ce challenge depuis un dossier vide."
  exit 1
fi
echo ".env est ignoré, et la règle est enregistrée."
```

````solution
```bash
cd ~/byte-layers/git/l1-challenge/statuspage && echo 'TOKEN=demo' > .env
cd ~/byte-layers/git/l1-challenge/statuspage && echo '.env' > .gitignore
cd ~/byte-layers/git/l1-challenge/statuspage && git add .gitignore && git commit -m "Ignore le fichier .env"
```
````

# Tâche 3 : un commit pour une seule intention

## Enregistrer un fichier et laisser l'autre en attente

Modifiez `index.html` et `runbook.md` en même temps, puis enregistrez uniquement le changement du runbook. Laissez celui de la page dans votre dossier.

**Critères :**

- le dernier commit modifie `runbook.md`, et lui seul ;
- `index.html` a un changement non enregistré et non préparé ;
- la zone de préparation est vide.

```hint
Ajouter une ligne à la fin de chaque fichier suffit, avec `>>`.
```

```hint
La commande qui prépare accepte un nom de fichier précis.
```

```verify
D=~/byte-layers/git/l1-challenge/statuspage
if [ "$(git -C "$D" log -1 --name-only --format= HEAD)" != "runbook.md" ]; then
  echo "Le dernier commit devrait modifier runbook.md, et lui seul."
  exit 1
fi
if ! git -C "$D" diff --name-only | grep -qx index.html; then
  echo "index.html devrait avoir un changement non préparé."
  exit 1
fi
if [ -n "$(git -C "$D" diff --staged --name-only)" ]; then
  echo "La zone de préparation devrait être vide."
  exit 1
fi
echo "Le commit est ciblé, et index.html attend son tour."
```

````solution
```bash
cd ~/byte-layers/git/l1-challenge/statuspage && echo '<p>API : OK</p>' >> index.html && echo 'Alerte au bout de : 5 minutes' >> runbook.md
cd ~/byte-layers/git/l1-challenge/statuspage && git add runbook.md && git commit -m "Ajoute le seuil d'alerte"
```
````

# Tâche 4 : retrouver le premier commit

## Écrire l'identifiant du tout premier commit dans un fichier

Retrouvez dans l'historique le hash du tout premier commit, celui qui n'a pas de parent, et écrivez-le dans le fichier `~/byte-layers/git/l1-challenge/premier-commit.txt`. Ce fichier est en dehors du dépôt. Le hash court comme le hash complet sont acceptés.

**Critères :**

- le fichier `~/byte-layers/git/l1-challenge/premier-commit.txt` existe ;
- il contient le hash du tout premier commit du dépôt, sur au moins 7 caractères.

```hint
L'historique se lit du plus récent au plus ancien : le premier commit est tout en bas.
```

```hint
`git log --oneline` le montre. Vous pouvez recopier le hash avec votre éditeur, ou avec `echo`.
```

```verify
D=~/byte-layers/git/l1-challenge
F="$D"/premier-commit.txt
if [ ! -s "$F" ]; then
  echo "Le fichier premier-commit.txt n'existe pas, ou il est vide."
  exit 1
fi
A=$(tr -d '[:space:]' < "$F")
if [ "${#A}" -lt 7 ]; then
  echo "L'identifiant doit faire au moins 7 caractères."
  exit 1
fi
R=$(git -C "$D"/statuspage rev-list --max-parents=0 HEAD)
case "$R" in
  "$A"*) echo "C'est bien le premier commit." ;;
  *) echo "Ce n'est pas l'identifiant du tout premier commit. Le fichier doit contenir uniquement le hash, sans le message."; exit 1 ;;
esac
```

````solution
```bash
cd ~/byte-layers/git/l1-challenge/statuspage && git log --format=%h --reverse | head -n 1 > ../premier-commit.txt
```
````

# Tâche 5 : ne rien laisser derrière soi

## Supprimer le dossier du challenge

Supprimez le dossier `~/byte-layers/git/l1-challenge` et tout ce qu'il contient. Vérifiez d'abord que votre terminal ne se trouve pas dedans.

**Critère :** le dossier `~/byte-layers/git/l1-challenge` n'existe plus.

```verify
if [ -e ~/byte-layers/git/l1-challenge ]; then
  echo "Le dossier ~/byte-layers/git/l1-challenge existe encore."
  exit 1
fi
echo "Le dossier est supprimé. Challenge terminé."
```

````solution
```bash
cd ~ && rm -rf ~/byte-layers/git/l1-challenge
```
````
