---
title: "02 - Créer un groupe, un projet et donner des droits"
description: "La hiérarchie de GitLab en pratique, et les rôles"
---

Un groupe rassemble vos projets et votre équipe. Vous le créez d'abord, puis vous y placez un projet.

## 02.1 - Créer un groupe public

Cliquez sur le **+** en haut de page, puis sur **New group**, et sur **Create group**. Donnez-lui un nom libre, comme `demo-votre-nom` : l'adresse doit être unique sur gitlab.com. Choisissez la visibilité **Public**, car un projet public doit se trouver dans un groupe public, puis validez.

## 02.2 - Créer le projet statuspage

Depuis la page du groupe, cliquez sur **New project**, puis **Create blank project**. Renseignez ces champs :

| Champ | Valeur |
|---|---|
| Project name | `statuspage` |
| Visibility Level | Public |
| Initialize repository with a README | coché |

Validez avec **Create project**.

> 💡 **Remarque.** Tout est public ici : le nom de votre groupe et l'adresse `user.email` de vos commits sont visibles. Si besoin, utilisez un pseudo et l'adresse *no-reply* que GitLab fournit dans **Edit profile**.

## 02.3 - Préparer le dossier du lab

Tous les labs de byte_layers rangent leurs fichiers sous `~/byte-layers`, un dossier par sujet. Celui-ci travaille dans `~/byte-layers/git/gitlab-first`. Créez-le : `mkdir -p` crée le dossier et, au besoin, les dossiers parents qui manquent.

```exec
mkdir -p ~/byte-layers/git/gitlab-first
```

## 02.4 - Noter l'adresse du projet pour les vérifications

Sur la page du projet, le bouton **Code** donne son adresse de clonage. Copiez celle de **Clone with SSH** : elle ressemble à `git@gitlab.com:demo-votre-nom/statuspage.git`.

Les boutons de vérification de ce lab ont besoin de connaître votre projet. Vous leur donnez son adresse en l'écrivant dans un fichier nommé `url`, dans le dossier du lab. Cette étape sert seulement aux vérifications : Git, lui, n'en a pas besoin.

La commande `echo` affiche le texte entre apostrophes, et `>` envoie ce texte dans le fichier au lieu de l'écran. Remplacez l'adresse d'exemple par la vôtre avant de lancer la commande :

```exec
echo 'git@gitlab.com:demo-votre-nom/statuspage.git' > ~/byte-layers/git/gitlab-first/url
```

Vérifiez que le fichier contient bien votre adresse. `cat` affiche le contenu d'un fichier :

```exec
cat ~/byte-layers/git/gitlab-first/url
```

```verify
C=$(cat ~/byte-layers/git/gitlab-first/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/byte-layers/git/gitlab-first/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
if ! curl -fsS "$A" >/dev/null 2>&1; then
  echo "GitLab ne trouve pas le projet $P. Vérifiez l'adresse et que le projet est public."
  exit 1
fi
echo "Le projet existe et il est public."
```

## 02.5 - Donner un rôle à un membre

Dans le menu du projet, ouvrez **Manage**, puis **Members**. Le bouton **Invite members** ajoute une personne avec un **rôle**, qui définit ce qu'elle peut faire :

| Rôle | Ce qu'il permet, en résumé |
|---|---|
| Guest | voir les issues d'un projet |
| Planner | gérer les issues et les jalons, sans accès en écriture au code |
| Reporter | lire le code, gérer les issues |
| Developer | pousser sur les branches non protégées, ouvrir des merge requests |
| Maintainer | gérer les branches protégées et les réglages du dépôt |
| Owner | administrer le projet ou le groupe, jusqu'à sa suppression |

Si vous travaillez en binôme, invitez votre collègue avec le rôle **Developer**. Un membre ajouté au groupe a le même rôle sur **tous** ses projets : pour donner des droits différents selon le projet, ajoutez-le projet par projet.

> 📖 [Rôles et permissions](https://docs.gitlab.com/user/permissions/) · [Membres d'un projet](https://docs.gitlab.com/user/project/members/)
