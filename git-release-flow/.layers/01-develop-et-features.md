---
title: "01 - Créer develop et y fusionner des fonctionnalités"
description: "La branche d'intégration, les branches feature et le merge --no-ff"
---

Gitflow sépare ce qui est en production, sur `main`, de ce qui se prépare, sur `develop`. Vous mettez en place ces deux branches, puis vous y intégrez deux fonctionnalités.

## 01.1 - Créer le dépôt, le serveur et la branche develop

Ce dépôt part d'un commit sur `main`, publié sur un serveur local :

```exec
mkdir -p ~/byte-layers/git/l5-release/depot && cd ~/byte-layers/git/l5-release/depot && git init -b main
echo '<h1>Statut</h1>' > index.html && git add index.html && git commit -m "État initial"
git init --bare -b main ../serveur.git
git remote add origin ../serveur.git
git push -u origin main
```

Créez `develop` à partir de `main`, et publiez-la, pour que toute l'équipe parte de la même base :

```exec
cd ~/byte-layers/git/l5-release/depot && git switch -c develop
cd ~/byte-layers/git/l5-release/depot && git push -u origin develop
```

```verify
if ! git -C ~/byte-layers/git/l5-release/serveur.git show-ref --verify --quiet refs/heads/develop; then
  echo "Le serveur n'a pas la branche develop. Vérifiez votre identité avec git config --global user.name, puis reprenez cette section."
  exit 1
fi
echo "Les branches main et develop existent sur le serveur."
```

## 01.2 - Développer une fonctionnalité et la fusionner avec --no-ff

Une fonctionnalité part toujours de `develop` :

```exec
cd ~/byte-layers/git/l5-release/depot && git switch -c feature/api
cd ~/byte-layers/git/l5-release/depot && echo '<p>API : OK</p>' >> index.html && git commit -am "Affiche l'état de l'API"
```

Fusionnez-la dans `develop`. Comme `develop` n'a pas bougé, Git ferait une avance rapide (*fast-forward*), et la trace de la branche disparaîtrait. L'option `--no-ff` (*no fast-forward*) force la création d'un commit de merge, qui garde dans l'historique les contours de chaque fonctionnalité :

```exec
cd ~/byte-layers/git/l5-release/depot && git switch develop
cd ~/byte-layers/git/l5-release/depot && git merge --no-ff --no-edit feature/api
cd ~/byte-layers/git/l5-release/depot && git log --oneline --all --graph
```

Le commit de merge garde la trace de la fonctionnalité :

```text
*   b9e0f0e (HEAD -> develop) Merge branch 'feature/api' into develop
|\  
| * c4d82d3 (feature/api) Affiche l'état de l'API
|/  
* 83468d7 (origin/main, origin/develop, main) État initial
```

Faites de même pour une seconde fonctionnalité, puis supprimez les branches terminées et publiez `develop` :

```exec
cd ~/byte-layers/git/l5-release/depot && git switch -c feature/db
cd ~/byte-layers/git/l5-release/depot && echo '<p>Base : OK</p>' >> index.html && git commit -am "Affiche l'état de la base"
cd ~/byte-layers/git/l5-release/depot && git switch develop && git merge --no-ff --no-edit feature/db
cd ~/byte-layers/git/l5-release/depot && git branch -d feature/api feature/db && git push
```

```verify
D=~/byte-layers/git/l5-release
if [ "$(git -C "$D/serveur.git" rev-list --merges --count develop)" -lt 2 ]; then
  echo "develop devrait contenir deux commits de merge sur le serveur."
  exit 1
fi
if ! git -C "$D/serveur.git" show develop:index.html | grep -q "Base : OK"; then
  echo "La seconde fonctionnalité n'est pas sur le serveur."
  exit 1
fi
echo "Les deux fonctionnalités sont dans develop."
```
