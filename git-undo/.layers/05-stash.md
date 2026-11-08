---
title: "05 - git stash : mettre un travail de côté"
description: "Libérer son dossier pour une urgence, puis reprendre où l'on en était"
---

Vous êtes au milieu d'un changement, et une urgence vous oblige à travailler sur autre chose. Votre travail n'est pas prêt pour un commit : `git stash` le met de côté et vous rend un dossier propre.

## 05.1 - Mettre de côté un travail en cours

Commencez un changement sur le runbook :

```exec
cd ~/layers-git/l4-undo && echo 'Procédure en cours de rédaction' >> runbook.md
cd ~/layers-git/l4-undo && git status --short
```

`git stash` range ce changement et remet le fichier à l'état du dernier commit :

```exec
cd ~/layers-git/l4-undo && git stash
cd ~/layers-git/l4-undo && git status --short
```

`git status --short` n'affiche plus rien. `git stash list` montre ce qui est rangé :

```exec
cd ~/layers-git/l4-undo && git stash list
```

Votre travail y figure, sous un nom généré par Git :

```text
stash@{0}: WIP on main: a0e9968 Revert "Refond la page"
```

## 05.2 - Traiter l'urgence puis reprendre le travail avec git stash pop

Votre dossier étant propre, faites le correctif urgent :

```exec
cd ~/layers-git/l4-undo && echo '<p>Maintenance ce soir</p>' >> index.html
cd ~/layers-git/l4-undo && git commit -am "Annonce la maintenance"
```

`git stash pop` remet votre travail en place et le retire de la liste :

```exec
cd ~/layers-git/l4-undo && git stash pop
```

Votre changement est revenu. Terminez-le avec un commit, qui servira à l'étape suivante :

```exec
cd ~/layers-git/l4-undo && git commit -am "Ajoute une procédure"
```

> 💡 **Remarque.** Par défaut, `git stash` ne prend pas les fichiers nouveaux, non suivis. L'option `-u` les inclut.

```verify
D=~/layers-git/l4-undo
if [ -n "$(git -C "$D" stash list)" ]; then
  echo "La liste de git stash n'est pas vide. Lancez git stash pop."
  exit 1
fi
if ! git -C "$D" log --format=%s | grep -q "Ajoute une procédure"; then
  echo "Le commit Ajoute une procédure n'existe pas. Lancez git commit -am \"Ajoute une procédure\"."
  exit 1
fi
if ! git -C "$D" log --format=%s | grep -q "Annonce la maintenance"; then
  echo "Le correctif urgent n'est pas enregistré."
  exit 1
fi
echo "L'urgence est traitée, et votre travail a repris sa place."
```

> 📖 [`git stash`](https://git-scm.com/docs/git-stash)
