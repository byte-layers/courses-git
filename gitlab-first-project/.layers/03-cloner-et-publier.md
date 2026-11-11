---
title: "03 - Cloner le projet et publier un commit"
description: "Récupérer le dépôt, enregistrer un changement et le voir sur GitLab"
---

Le projet existe sur le serveur. Vous le récupérez maintenant sur votre poste pour y travailler.

## 03.1 - Cloner le projet

`git clone` copie le projet du serveur dans un nouveau dossier, ici `statuspage`. Plutôt que de recopier l'adresse, la commande la lit dans le fichier `url` de l'étape précédente : `$(cat url)` est remplacé par le contenu du fichier avant que `git clone` ne s'exécute.

```exec
cd ~/byte-layers/git/gitlab-first && git clone "$(cat url)" statuspage
```

Listez le contenu du dossier cloné avec `ls` :

```exec
cd ~/byte-layers/git/gitlab-first/statuspage && ls
```

Vous retrouvez le fichier `README.md` créé par GitLab.

## 03.2 - Publier un premier commit

Vous allez faire le cycle complet en trois commandes : créer un fichier, l'enregistrer dans un commit, puis l'envoyer sur GitLab.

D'abord, créez la page `index.html`. Comme à l'étape précédente, `echo` et `>` écrivent le texte dans le fichier :

```exec
cd ~/byte-layers/git/gitlab-first/statuspage && echo '<h1>Statut des services</h1>' > index.html
```

Ensuite, `git add` prépare le fichier et `git commit` l'enregistre dans l'historique de votre dépôt local, avec un message :

```exec
cd ~/byte-layers/git/gitlab-first/statuspage && git add index.html && git commit -m "Ajoute la page de statut"
```

Le commit n'existe encore que sur votre poste. `git push` l'envoie sur GitLab :

```exec
cd ~/byte-layers/git/gitlab-first/statuspage && git push
```

Rechargez la page du projet sur GitLab : `index.html` apparaît, avec le message de votre commit.

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
if ! curl -fsS "$A/repository/files/index.html?ref=main" >/dev/null 2>&1; then
  echo "index.html n'est pas sur la branche main du projet. Lancez git push."
  exit 1
fi
echo "Votre commit est sur GitLab."
```

## 03.3 - Ranger le dossier de ce lab

Ce dossier local ne servira plus. Vous pouvez aussi supprimer le projet sur GitLab, depuis **Settings**, **General**, **Advanced**, **Delete project**.

```exec
cd ~ && rm -rf ~/byte-layers/git/gitlab-first
```

```verify
if [ -e ~/byte-layers/git/gitlab-first ]; then
  echo "Le dossier ~/byte-layers/git/gitlab-first existe encore."
  exit 1
fi
echo "Le dossier est supprimé."
```

## Récap

- Une clé SSH prouve votre identité à GitLab, à la place d'un mot de passe.
- Un groupe rassemble des projets, et les rôles disent ce que chacun peut y faire.
- Le bouton **Code** d'un projet donne son adresse de clonage.

> 📖 [Créer un projet](https://docs.gitlab.com/user/project/) · [Créer un groupe](https://docs.gitlab.com/user/group/)
