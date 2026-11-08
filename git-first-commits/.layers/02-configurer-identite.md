---
title: "02 - Configurer votre identité Git"
description: "Indiquer le nom et l'adresse qui accompagneront vos commits"
---

Chaque version que vous enregistrerez portera un nom et une adresse. Cette configuration ne se fait qu'une fois par machine.

## 02.1 - Regarder si une identité existe déjà

Chaque version enregistrée porte le nom et l'adresse de son auteur, et sans réglage Git refuse d'enregistrer ou invente un nom à partir de votre machine. Ce n'est pas un compte : aucun mot de passe n'est demandé, et rien n'est envoyé. Votre adresse ne deviendra visible que si vous publiez un jour votre travail. Commencez par regarder si une identité existe déjà sur cette machine :

```exec
git config --global user.name
git config --global user.email
```

Si ces deux commandes affichent votre nom et votre adresse, ne changez rien et passez à l'étape suivante.

## 02.2 - Indiquer votre nom et votre adresse

Si elles n'affichent rien, copiez les deux lignes suivantes dans votre terminal, en remplaçant les valeurs d'exemple par les vôtres :

```bash
git config --global user.name "John Doe"
git config --global user.email "john.doe@example.com"
```

L'option `--global` range ce réglage dans votre dossier personnel (noté `~`), et il vaut alors pour tous vos projets. Git connaît trois niveaux de configuration, et le plus précis l'emporte :

| Option | Portée | Où c'est écrit |
|---|---|---|
| `--system` | tous les utilisateurs de la machine | `/etc/gitconfig` sous Linux |
| `--global` | votre utilisateur, tous vos projets | `~/.gitconfig` |
| `--local` | un seul projet | `.git/config`, dans le dossier du projet |

Le niveau `--local` sert par exemple à utiliser une autre adresse sur un projet professionnel.

Pour voir d'où vient chaque réglage, ajoutez `--show-origin` : Git affiche le fichier devant chaque valeur.

```exec
git config --global --list --show-origin
```

Vous y retrouvez votre fichier personnel, avec son chemin réel :

```text
file:/home/john/.gitconfig	user.name=John Doe
file:/home/john/.gitconfig	user.email=john.doe@example.com
```

```verify
N=$(git config --global user.name)
E=$(git config --global user.email)
if [ -z "$N" ] || [ -z "$E" ]; then
  echo "Il manque votre nom ou votre adresse. Lancez les deux commandes git config --global."
  exit 1
fi
echo "Vous signerez vos versions au nom de $N <$E>."
```

> 📖 [`git config`](https://git-scm.com/docs/git-config) · [Paramétrage à la première utilisation](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Param%C3%A9trage-%C3%A0-la-premi%C3%A8re-utilisation-de-Git)
