---
title: "05 - Ranger ses branches et s'entraîner"
description: "Ce que -d protège, nommer ses branches, et un outil pour pratiquer visuellement"
---

Vous avez utilisé tous les gestes de base des branches. Il reste à ranger celles qui ne servent plus, à voir ce qui vous protège d'une suppression malheureuse, et à vous entraîner davantage.

## 05.1 - Supprimer les branches fusionnées

Les deux branches du seuil sont maintenant dans `main`, et vous pouvez supprimer leurs noms en une seule commande :

```exec
cd ~/layers-git/l2 && git branch -d feature/seuil-bas feature/seuil-haut
```

```verify
D=~/layers-git/l2
if [ "$(git -C "$D" for-each-ref --format='%(refname:short)' refs/heads/ | tr -d '\n')" != "main" ]; then
  echo "Il devrait ne rester que la branche main. git branch vous montre les autres."
  exit 1
fi
echo "Il ne reste que main."
```

## 05.2 - Vérifier que Git protège le travail non fusionné

Créez une branche avec un commit que vous n'avez pas fusionné, puis tentez de la supprimer :

```exec
cd ~/layers-git/l2 && git switch -c feature/brouillon
cd ~/layers-git/l2 && echo 'brouillon' > notes.txt && git add notes.txt && git commit -m "Ajoute un brouillon"
cd ~/layers-git/l2 && git switch main
```

La tentative suivante doit échouer, et c'est ce qu'on veut constater. Elle affichera une erreur, sans aucun dégât :

```exec
cd ~/layers-git/l2 && git branch -d feature/brouillon
```

Git refuse, parce que ce commit n'existe sur aucune autre branche :

```text
error: the branch 'feature/brouillon' is not fully merged
hint: If you are sure you want to delete it, run 'git branch -D feature/brouillon'
```

Avec un `D` majuscule, vous lui dites que vous abandonnez ce travail en connaissance de cause. C'est le cas ici :

```exec
cd ~/layers-git/l2 && git branch -D feature/brouillon
```

```verify
D=~/layers-git/l2
if git -C "$D" show-ref --verify --quiet refs/heads/feature/brouillon; then
  echo "La branche feature/brouillon existe encore. Lancez git branch -D feature/brouillon."
  exit 1
fi
echo "Le brouillon est abandonné."
```

## 05.3 - Nommer ses branches pour toute l'équipe

Git accepte presque n'importe quel nom, et c'est à l'équipe de se fixer une convention. Le plus courant est de préfixer par le type de travail :

| Préfixe | Usage |
|---|---|
| `feature/` | une nouvelle fonctionnalité |
| `fix/` | la correction d'un bug |
| `hotfix/` | une correction urgente en production |
| `docs/` | de la documentation |

Beaucoup d'équipes ajoutent le numéro du ticket concerné, par exemple `feature/42-etat-base`, pour relier le code au suivi des tâches.

## 05.4 - S'entraîner avec Learn Git Branching

[Learn Git Branching](https://learngitbranching.js.org/?locale=fr_FR) est un jeu gratuit qui s'utilise dans le navigateur. Il simule Git et dessine le graphe à chaque commande, ce qui en fait un bon entraînement pour vos réflexes. Faites la **Séquence d'introduction** de l'onglet **Principal**, qui reprend les commits, les branches et le merge.

Le graphe est également disponible dans votre éditeur : VS Code affiche l'historique dans son panneau de contrôle de code source.

## 05.5 - Ranger le dossier de ce cours

Ce dossier ne servira plus, et vous pouvez le supprimer depuis votre dossier personnel. `rm -rf` efface le dossier et son contenu sans demander de confirmation :

```exec
cd ~ && rm -rf ~/layers-git/l2
```

```verify
if [ -e ~/layers-git/l2 ]; then
  echo "Le dossier ~/layers-git/l2 existe encore."
  exit 1
fi
echo "Le dossier est supprimé."
```

## Récap

- Une branche isole un travail, et `git switch -c` la crée et s'y place.
- `git merge <branche>` amène cette branche sur celle où vous êtes.
- Si la destination n'a pas bougé, c'est une avance rapide ; si les historiques ont divergé, Git crée un commit de merge à deux parents.
- Un conflit signale deux changements sur les mêmes lignes ou sur des lignes voisines : écrivez le contenu final, retirez les marqueurs, puis `git add` et `git commit`.
- `git branch -d` ne supprime que ce qui est fusionné, et `-D` force la suppression.

Le bit [Une branche est un pointeur](https://byte-layers.com/fr/bits/git-branch-pointer) montre ce qu'est réellement une branche. Pour vous tester sans guide, faites le challenge [Fusionner et résoudre un conflit, sans guide](https://byte-layers.com/fr/challenges/git-conflict-challenge).

> 📖 [Les branches avec Git, dans le livre Pro Git](https://git-scm.com/book/fr/v2/Les-branches-avec-Git-Les-branches-en-bref)
