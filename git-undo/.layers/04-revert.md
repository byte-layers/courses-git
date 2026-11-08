---
title: "04 - git revert : annuler un commit déjà publié"
description: "Créer un commit inverse, sans réécrire l'historique partagé"
---

Quand un commit est publié, le retirer avec `git reset` obligerait vos collègues à réparer leur propre historique. `git revert` procède autrement : il crée un nouveau commit qui fait exactement l'inverse.

## 04.1 - Enregistrer un commit qui casse la page

Imaginez que ce commit soit déjà publié et qu'il casse la page en production :

```exec
cd ~/layers-git/l4-undo && echo 'PANNE' > index.html
cd ~/layers-git/l4-undo && git commit -am "Refond la page"
```

## 04.2 - Annuler ce commit avec un commit inverse

`git revert` prend le commit à annuler, ici `HEAD`, et `--no-edit` accepte le message proposé :

```exec
cd ~/layers-git/l4-undo && git revert --no-edit HEAD
cd ~/layers-git/l4-undo && git log --oneline
```

L'historique a gagné une ligne, et rien n'a disparu. En voici le début :

```text
a0e9968 (HEAD -> main) Revert "Refond la page"
e4ea1c3 Refond la page
```

La page a retrouvé son contenu :

```exec
cd ~/layers-git/l4-undo && cat index.html
```

```verify
D=~/layers-git/l4-undo
if grep -q "PANNE" "$D/index.html"; then
  echo "index.html contient encore PANNE. Lancez git revert --no-edit HEAD."
  exit 1
fi
if ! git -C "$D" log --format=%s | grep -q "Refond la page"; then
  echo "Le commit annulé devrait rester dans l'historique."
  exit 1
fi
echo "Le commit est annulé, et l'historique reste complet."
```

Sur un vrai projet, terminez par `git push` pour publier ce commit inverse.

## 04.3 - Choisir entre reset et revert

Le choix dépend d'une seule question : le commit est-il déjà partagé ?

| Le commit est… | La commande | Pourquoi |
|---|---|---|
| seulement sur votre machine | `git reset` | l'historique reste net, et personne n'est gêné |
| publié sur le serveur | `git revert` | personne ne doit réparer son historique |

> 📖 [`git revert`](https://git-scm.com/docs/git-revert)
