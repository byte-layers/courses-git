---
title: "07 - Tenir un fichier secret hors de Git"
description: ".gitignore : éviter d'enregistrer ce qui ne doit pas l'être, puis ranger le dossier"
---

Certains fichiers ne doivent jamais entrer dans un dépôt : un mot de passe, des journaux, des fichiers générés. Comme un commit reste dans l'historique, le plus sûr est de dire à Git de ne même pas les regarder.

## 07.1 - Créer un fichier sensible et le voir apparaître dans git status

Le fichier `.env` sert souvent à stocker des valeurs de configuration, parfois secrètes. Créez-en un, avec une valeur factice :

```exec
cd ~/layers-git/l1 && echo 'TOKEN=valeur-de-demonstration' > .env
```

L'option `--short` de `git status` donne une version courte de l'état, où `??` signifie non suivi :

```exec
cd ~/layers-git/l1 && git status --short
```

La ligne qui apparaît concerne votre fichier sensible :

```text
?? .env
```

Le fichier est listé parmi ceux à ajouter, et un `git add .`, qui prépare tout le dossier d'un coup, l'embarquerait sans vous demander votre avis.

## 07.2 - Déclarer ce qu'il faut ignorer dans .gitignore

Le fichier `.gitignore` liste ce que Git doit ignorer, à raison d'un motif par ligne. Créez-le :

```exec
cd ~/layers-git/l1 && echo '.env' > .gitignore
```

Regardez de nouveau l'état du dépôt :

```exec
cd ~/layers-git/l1 && git status --short
```

Le fichier `.env` a disparu de la liste, et c'est `.gitignore` qui apparaît à sa place :

```text
?? .gitignore
```

Enregistrez ce fichier : il fait partie du projet, et toute l'équipe profitera ainsi des mêmes règles.

```exec
cd ~/layers-git/l1 && git add .gitignore
cd ~/layers-git/l1 && git commit -m "Ignore le fichier .env"
```

`.gitignore` accepte aussi des motifs comme `*.log` pour tous les journaux, ou `node_modules/` pour un dossier entier.

> ⚠️ **`.gitignore` n'agit que sur les fichiers non suivis.** Un fichier déjà enregistré dans un commit reste suivi même si vous l'ajoutez ensuite à `.gitignore`, et un secret enregistré reste lisible dans l'historique. Si cela arrive, considérez le secret comme compromis et remplacez-le.

```verify
D=~/layers-git/l1
if ! git -C "$D" check-ignore -q .env; then
  echo "Git n'ignore pas .env. Vérifiez le contenu de .gitignore."
  exit 1
fi
if ! git -C "$D" ls-tree --name-only HEAD | grep -qx .gitignore; then
  echo ".gitignore n'est pas enregistré. Lancez git add, puis git commit."
  exit 1
fi
if [ -n "$(git -C "$D" log --all --oneline -- .env)" ]; then
  echo ".env est entré dans l'historique. Supprimez ~/layers-git/l1 et reprenez le cours depuis la création du dépôt."
  exit 1
fi
echo ".env est ignoré, et .gitignore est enregistré."
```

## 07.3 - Ranger le dossier de ce cours

Ce dossier ne servira plus. Revenez d'abord dans votre dossier personnel, car on ne supprime pas le dossier où l'on se trouve, puis effacez-le avec `rm -rf`, où `-r` parcourt ses sous-dossiers et `-f` ne demande aucune confirmation. L'historique vivant dans `.git`, cette commande l'efface aussi, définitivement.

```exec
cd ~ && rm -rf ~/layers-git/l1
```

```verify
if [ -e ~/layers-git/l1 ]; then
  echo "Le dossier ~/layers-git/l1 existe encore."
  exit 1
fi
echo "Le dossier est supprimé."
```

## Récap

- `git init -b main` transforme un dossier en dépôt, et tout l'historique vit dans `.git`.
- `git status` dit où vous en êtes, `git diff` montre ce qui a changé.
- `git add` prépare, `git commit -m` enregistre. Un commit porte une seule intention, et son message dit ce qu'il apporte.
- `git log --oneline` et `git show` relisent l'historique.
- `.gitignore` tient à l'écart ce qui ne doit jamais entrer dans le dépôt.

Le bit [Un commit est un instantané](https://byte-layers.com/fr/bits/git-commit-snapshot) regarde ce qu'il y a réellement dans ce que vous venez de créer. Pour vous tester sans guide, faites le challenge [Créer un historique propre, sans guide](https://byte-layers.com/fr/challenges/git-first-commits-challenge).

> 📖 [`gitignore`](https://git-scm.com/docs/gitignore) · [Modèles de `.gitignore` par langage, de GitHub](https://github.com/github/gitignore)
