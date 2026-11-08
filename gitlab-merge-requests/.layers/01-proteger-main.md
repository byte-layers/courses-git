---
title: "01 - Protéger la branche main"
description: "Empêcher les envois directs, pour que tout passe par une relecture"
---

Sur un projet d'équipe, `main` doit rester stable. Une **branche protégée** limite qui peut y pousser et y fusionner. Réglée sur **No one**, elle ne reçoit le code que par une merge request.

## 01.1 - Créer et cloner le projet

Créez un projet public nommé `statuspage-mr`, dans votre groupe ou votre espace personnel, avec **+**, **New project/repository**, **Create blank project**, et un README. Copiez son adresse **Clone with SSH** dans ce fichier, en remplaçant l'exemple :

```bash
mkdir -p ~/layers-git/gitlab-mr
echo 'git@gitlab.com:demo-votre-nom/statuspage-mr.git' > ~/layers-git/gitlab-mr/url
```

Clonez ensuite le projet :

```exec
cd ~/layers-git/gitlab-mr && git clone "$(cat url)" statuspage
```

## 01.2 - Interdire les envois directs sur main

Par défaut, GitLab protège déjà `main`, mais les Maintainers, dont vous faites partie, peuvent toujours y pousser. Vous allez fermer cette porte. Ouvrez **Settings**, **Repository**, et dépliez **Protected branches**. Sur la ligne `main`, réglez **Allowed to push and merge** sur **No one**, en laissant **Allowed to merge** sur **Maintainers**.

```verify
C=$(cat ~/layers-git/gitlab-mr/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/layers-git/gitlab-mr/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
R=$(curl -fsS "$A/protected_branches/main" 2>/dev/null)
if [ -z "$R" ]; then
  echo "GitLab ne laisse pas lire ce réglage sans connexion. Le test de la section suivante le prouvera : un push direct doit être refusé."
  exit 0
fi
if ! echo "$R" | grep -qE '"push_access_levels":\[\{[^}]*"access_level":0'; then
  echo "Les envois directs sur main sont encore permis. Réglez Allowed to push and merge sur No one."
  exit 1
fi
echo "Plus personne ne peut pousser directement sur main."
```

## 01.3 - Constater le refus d'un push direct

Faites un commit sur `main` et tentez de l'envoyer. Le refus est attendu :

```exec
cd ~/layers-git/gitlab-mr/statuspage && echo '<h1>Statut</h1>' > index.html && git add index.html && git commit -m "Ajoute la page directement sur main"
cd ~/layers-git/gitlab-mr/statuspage && git push
```

GitLab bloque l'envoi et explique pourquoi :

```text
remote: GitLab: You are not allowed to push code to protected branches on this project.
 ! [remote rejected] main -> main (pre-receive hook declined)
```

Retirez ce commit local. `git reset --hard origin/main` ramène votre branche à l'état du serveur :

```exec
cd ~/layers-git/gitlab-mr/statuspage && git reset --hard origin/main
```

> 📖 [Branches protégées](https://docs.gitlab.com/user/project/repository/branches/protected/)
