---
title: "01 - Préparer le projet et ses branches"
description: "Deux clones, une branche develop, deux branches protégées"
---

Le projet commence par son organisation : les branches `main` et `develop`, protégées toutes les deux, et les tâches.

## 01.1 - Créer le projet et les deux clones

Créez un projet public nommé `statuspage-team`, avec un README. Copiez son adresse **Clone with SSH** dans ce fichier, en remplaçant l'exemple :

```bash
mkdir -p ~/byte-layers/git/gitlab-team
echo 'git@gitlab.com:demo-votre-nom/statuspage-team.git' > ~/byte-layers/git/gitlab-team/url
```

Clonez-le dans deux dossiers, et donnez une identité au second, qui joue une autre personne. **À deux** : A invite B au projet, avec **Manage**, **Members** et le rôle **Maintainer**. B écrit le même fichier `url`. Chacun ne clone alors que son propre dossier, et B saute le `git config` :

```exec
cd ~/byte-layers/git/gitlab-team && git clone "$(cat url)" poste-a
cd ~/byte-layers/git/gitlab-team && git clone "$(cat url)" poste-b
cd ~/byte-layers/git/gitlab-team/poste-b && git config user.name "Sam Durand" && git config user.email "sam@example.com"
```

## 01.2 - Créer develop et protéger les branches

Depuis le poste A, créez `develop` et publiez-la :

```exec
cd ~/byte-layers/git/gitlab-team/poste-a && git switch -c develop && git push -u origin develop
```

Sur GitLab, ouvrez **Settings**, **Repository**, puis faites trois réglages :

1. dans **Branch defaults**, choisissez `develop` comme **Default branch** et enregistrez : sans cela, `Closes #1` ne fermerait pas l'issue, car GitLab ne ferme une issue qu'à la fusion dans la branche par défaut ;
2. dans **Protected branches**, cliquez sur **Add protected branch** et protégez `develop`, avec **Allowed to merge** sur **Maintainers** et **Allowed to push and merge** sur **No one** ;
3. sur la ligne `main`, réglez **Allowed to push and merge** sur **No one**.

```verify
C=$(cat ~/byte-layers/git/gitlab-team/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/byte-layers/git/gitlab-team/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
if ! curl -fsS "$A" 2>/dev/null | grep -q '"default_branch":"develop"'; then
  echo "La branche par défaut devrait être develop."
  exit 1
fi
echo "develop est la branche par défaut."
```

## 01.3 - Créer les deux user stories

Créez deux issues, depuis **Work items**, intitulées `U1 - Première ligne du journal` et `U2 - Seconde ligne du journal`. Elles portent les numéros `#1` et `#2`.

> 📖 [Branche par défaut](https://docs.gitlab.com/user/project/repository/branches/default/)
