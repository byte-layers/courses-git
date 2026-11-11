---
title: "02 - Publier une version : branche de release et tag"
description: "Stabiliser sur release/1.0.0, fusionner dans main, poser un tag, redescendre dans develop"
---

`develop` contient ce que vous voulez livrer. Une **branche de release** fige cette version pour la finaliser, pendant que `develop` peut continuer d'avancer.

## 02.1 - Préparer la version sur une branche de release

Créez la branche et finalisez la version. Ici, cela consiste à écrire le numéro de version dans un fichier :

```exec
cd ~/byte-layers/git/l5-release/depot && git switch -c release/1.0.0
cd ~/byte-layers/git/l5-release/depot && echo '1.0.0' > VERSION && git add VERSION && git commit -m "Prépare la version 1.0.0"
```

## 02.2 - Fusionner dans main et poser un tag

Un **tag** est un nom permanent attaché à un commit, utilisé pour marquer une version. Contrairement à une branche, il ne se déplace pas tout seul. Le numéro suit souvent la **gestion sémantique de version**, majeure, mineure et correctif, comme dans `1.0.0`. L'option `-a` crée un tag annoté, qui garde son auteur, sa date et un message :

```exec
cd ~/byte-layers/git/l5-release/depot && git switch main
cd ~/byte-layers/git/l5-release/depot && git merge --no-ff --no-edit release/1.0.0
cd ~/byte-layers/git/l5-release/depot && git tag -a v1.0.0 -m "Version 1.0.0"
```

Un simple `git push` n'envoie pas les tags, et il faut les nommer :

```exec
cd ~/byte-layers/git/l5-release/depot && git push origin main v1.0.0
```

Git publie la branche et le tag :

```text
   83468d7..ff7c201  main -> main
 * [new tag]         v1.0.0 -> v1.0.0
```

```verify
S=~/byte-layers/git/l5-release/serveur.git
if ! git -C "$S" rev-parse -q --verify refs/tags/v1.0.0 >/dev/null; then
  echo "Le serveur n'a pas le tag v1.0.0."
  exit 1
fi
if [ "$(git -C "$S" show v1.0.0:VERSION 2>/dev/null)" != "1.0.0" ]; then
  echo "Le tag v1.0.0 devrait contenir VERSION à 1.0.0."
  exit 1
fi
if ! git -C "$S" merge-base --is-ancestor v1.0.0 main; then
  echo "Le tag v1.0.0 devrait être sur main."
  exit 1
fi
echo "La version 1.0.0 est publiée et taguée."
```

> 💡 **Remarque.** En entreprise, `main` est souvent protégée : ces fusions passent alors par une pull request ou une merge request.

## 02.3 - Redescendre la release dans develop

La branche de release a pu recevoir des ajustements, et `develop` doit les avoir aussi. Fusionnez-la, supprimez-la, et publiez :

```exec
cd ~/byte-layers/git/l5-release/depot && git switch develop
cd ~/byte-layers/git/l5-release/depot && git merge --no-ff --no-edit release/1.0.0
cd ~/byte-layers/git/l5-release/depot && git branch -d release/1.0.0 && git push
```

```verify
S=~/byte-layers/git/l5-release/serveur.git
if [ "$(git -C "$S" show develop:VERSION 2>/dev/null)" != "1.0.0" ]; then
  echo "develop devrait contenir le fichier VERSION sur le serveur."
  exit 1
fi
echo "develop contient la version."
```

> 📖 [Étiquetage, dans le livre Pro Git](https://git-scm.com/book/fr/v2/Les-bases-de-Git-%C3%89tiquetage) · [Gestion sémantique de version](https://semver.org/lang/fr/)
