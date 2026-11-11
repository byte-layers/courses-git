---
title: "06 - git reflog : retrouver un commit perdu"
description: "Le journal de vos déplacements, et le choix de la bonne commande d'annulation"
---

Un `git reset --hard` semble définitif, mais un commit retiré reste dans le dépôt pendant un certain temps. Git tient un journal de tous les déplacements de `HEAD`, et ce journal permet de retrouver ce commit.

## 06.1 - Perdre un commit

Retirez votre dernier commit, comme si vous vous étiez trompé :

```exec
cd ~/byte-layers/git/l4-undo && git reset --hard HEAD~1
cd ~/byte-layers/git/l4-undo && git log --oneline -n 2
```

La procédure a disparu de l'historique.

## 06.2 - Lire le journal avec git reflog

`git reflog` affiche tout ce que `HEAD` a désigné, du plus récent au plus ancien. L'option `-n 3` limite aux trois dernières lignes :

```exec
cd ~/byte-layers/git/l4-undo && git reflog -n 3
```

Votre commit perdu est là, à la deuxième ligne. `HEAD@{1}` signifie « là où était `HEAD` un mouvement plus tôt » :

```text
54f03f6 (HEAD -> main) HEAD@{0}: reset: moving to HEAD~1
cdfd820 HEAD@{1}: commit: Ajoute une procédure
54f03f6 (HEAD -> main) HEAD@{2}: commit: Annonce la maintenance
```

## 06.3 - Revenir sur le commit perdu

`git reset --hard` accepte n'importe quelle position, y compris celle du journal :

```exec
cd ~/byte-layers/git/l4-undo && git reset --hard "HEAD@{1}"
cd ~/byte-layers/git/l4-undo && git log --oneline -n 2
```

Le commit est de retour, avec le même hash qu'avant.

> ⚠️ **Le journal est local, et il n'est pas éternel.** Il n'existe que sur votre machine, et Git finit par nettoyer ses entrées anciennes : par défaut au bout de 30 jours pour un commit retiré d'une branche, et de 90 jours sinon. Ce qui n'a jamais été enregistré dans un commit n'y figure pas.

```verify
D=~/byte-layers/git/l4-undo
if ! git -C "$D" log --format=%s | grep -q "Ajoute une procédure"; then
  echo "Le commit Ajoute une procédure n'est pas revenu. Lancez git reset --hard \"HEAD@{1}\" juste après le reset, ou utilisez son hash lu dans git reflog."
  exit 1
fi
echo "Le commit perdu est de retour."
```

## 06.4 - Ranger le dossier de ce cours

Ce dossier ne servira plus, et vous pouvez le supprimer depuis votre dossier personnel. `rm -rf` efface le dossier et son contenu sans demander de confirmation :

```exec
cd ~ && rm -rf ~/byte-layers/git/l4-undo
```

```verify
if [ -e ~/byte-layers/git/l4-undo ]; then
  echo "Le dossier ~/byte-layers/git/l4-undo existe encore."
  exit 1
fi
echo "Le dossier est supprimé."
```

## Récap

Chaque situation a sa commande :

| Situation | La commande |
|---|---|
| Une modification à abandonner, pas encore dans un commit | `git restore fichier` |
| Un fichier préparé par erreur | `git restore --staged fichier` |
| Le dernier commit à corriger, non publié | `git commit --amend` |
| Des commits locaux à retirer | `git reset`, avec `--soft`, sans option, ou `--hard` |
| Un commit publié à annuler | `git revert` |
| Un travail à mettre de côté | `git stash`, puis `git stash pop` |
| Un commit perdu à retrouver | `git reflog` |

Pour vous tester sans guide, après avoir aussi suivi [Rebase et cherry-pick](https://byte-layers.com/fr/skills/git-rebase-cherry-pick), faites le challenge [Réparer un dépôt, sans guide](https://byte-layers.com/fr/challenges/git-repair-challenge).

> 📖 [`git reflog`](https://git-scm.com/docs/git-reflog) · [Annuler des actions, dans le livre Pro Git](https://git-scm.com/book/fr/v2/Les-bases-de-Git-Annuler-des-actions)
