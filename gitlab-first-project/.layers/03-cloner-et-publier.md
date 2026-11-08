---
title: "03 - Cloner le projet et publier un commit"
description: "Récupérer le dépôt, enregistrer un changement et le voir sur GitLab"
---

Le projet existe sur le serveur. Vous le récupérez maintenant sur votre poste pour y travailler.

## 03.1 - Cloner le projet

`git clone` lit ici l'adresse que vous venez d'enregistrer :

```exec
cd ~/layers-git/gitlab-first && git clone "$(cat url)" statuspage
cd ~/layers-git/gitlab-first/statuspage && ls
```

Vous retrouvez le fichier `README.md` créé par GitLab.

## 03.2 - Publier un premier commit

Ajoutez une page, enregistrez-la, puis envoyez-la sur GitLab :

```exec
cd ~/layers-git/gitlab-first/statuspage && echo '<h1>Statut des services</h1>' > index.html
cd ~/layers-git/gitlab-first/statuspage && git add index.html && git commit -m "Ajoute la page de statut"
cd ~/layers-git/gitlab-first/statuspage && git push
```

Rechargez la page du projet sur GitLab : `index.html` apparaît, avec le message de votre commit.

```verify
C=$(cat ~/layers-git/gitlab-first/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/layers-git/gitlab-first/url."
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
cd ~ && rm -rf ~/layers-git/gitlab-first
```

```verify
if [ -e ~/layers-git/gitlab-first ]; then
  echo "Le dossier ~/layers-git/gitlab-first existe encore."
  exit 1
fi
echo "Le dossier est supprimé."
```

## Récap

- Une clé SSH prouve votre identité à GitLab, à la place d'un mot de passe.
- Un groupe rassemble des projets, et les rôles disent ce que chacun peut y faire.
- Le bouton **Code** d'un projet donne son adresse de clonage.

> 📖 [Créer un projet](https://docs.gitlab.com/user/project/) · [Créer un groupe](https://docs.gitlab.com/user/group/)
