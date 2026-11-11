---
title: "03 - Résoudre un conflit pendant un rebase"
description: "git rebase --continue et --abort, et le sens des marqueurs"
---

Un rebase rejoue vos commits un par un, et chacun peut entrer en conflit. La résolution ressemble à celle d'un merge, avec une commande différente pour conclure.

## 03.1 - Provoquer un conflit sur le seuil d'alerte

Deux changements portent sur le même fichier, l'un sur une branche, l'autre sur `main` :

```exec
cd ~/byte-layers/git/l4-rebase/depot && git switch -c feature/seuil
cd ~/byte-layers/git/l4-rebase/depot && echo 'Seuil : 2 minutes' > seuil.txt && git add seuil.txt && git commit -m "Fixe le seuil à 2 minutes"
cd ~/byte-layers/git/l4-rebase/depot && git switch main
cd ~/byte-layers/git/l4-rebase/depot && echo 'Seuil : 10 minutes' > seuil.txt && git add seuil.txt && git commit -m "Fixe le seuil à 10 minutes"
```

Replacez la branche au-dessus de `main`. Le conflit est attendu :

```exec
cd ~/byte-layers/git/l4-rebase/depot && git switch feature/seuil
cd ~/byte-layers/git/l4-rebase/depot && git rebase main
```

Git s'arrête sur le commit qui pose problème. La mention `add/add` indique que les deux côtés ont créé le même fichier :

```text
CONFLICT (add/add): Merge conflict in seuil.txt
error: could not apply 2ac1536... Fixe le seuil à 2 minutes
hint: Resolve all conflicts manually, mark them as resolved with
hint: "git add/rm <conflicted_files>", then run "git rebase --continue".
```

Regardez le fichier, qui contient les marqueurs habituels :

```exec
cd ~/byte-layers/git/l4-rebase/depot && cat seuil.txt
```

Les deux versions sont encadrées par les marqueurs :

```text
<<<<<<< HEAD
Seuil : 10 minutes
=======
Seuil : 2 minutes
>>>>>>> 2ac1536 (Fixe le seuil à 2 minutes)
```

> ⚠️ **Pendant un rebase, les côtés sont inversés par rapport à un merge.** `HEAD` désigne ici `main`, sur laquelle vos commits sont rejoués, et le commit nommé en bas est le vôtre.

## 03.2 - Écrire le résultat et poursuivre avec --continue

L'équipe tranche pour **5 minutes**. Ouvrez le fichier avec votre éditeur, en donnant son chemin complet, par exemple `code ~/byte-layers/git/l4-rebase/depot/seuil.txt`, `notepad ~/byte-layers/git/l4-rebase/depot/seuil.txt` ou `nano ~/byte-layers/git/l4-rebase/depot/seuil.txt`. Faites en sorte que le fichier contienne une seule ligne, `Seuil : 5 minutes`, sans aucun marqueur, puis sauvegardez-le.

Si vous n'arrivez vraiment pas à éditer ce fichier, cette commande écrit le résultat à votre place :

```exec
echo 'Seuil : 5 minutes' > ~/byte-layers/git/l4-rebase/depot/seuil.txt
```

Marquez le fichier comme résolu, puis demandez à Git de continuer. L'option `-c core.editor=true` accepte le message du commit sans ouvrir d'éditeur, pour le bouton qui exécute la commande. Au quotidien, tapez simplement `git rebase --continue` : si Vim s'ouvre, quittez avec `:wq` puis Entrée :

```exec
cd ~/byte-layers/git/l4-rebase/depot && git add seuil.txt
cd ~/byte-layers/git/l4-rebase/depot && git -c core.editor=true rebase --continue
```

Si vous préférez renoncer en plein milieu, `git rebase --abort` remet la branche exactement dans son état d'avant.

```verify
D=~/byte-layers/git/l4-rebase/depot
if [ -d "$D/.git/rebase-merge" ] || [ -d "$D/.git/rebase-apply" ]; then
  echo "Le rebase est encore en cours. Lancez git add seuil.txt, puis git -c core.editor=true rebase --continue."
  exit 1
fi
if ! git -C "$D" merge-base --is-ancestor main feature/seuil 2>/dev/null; then
  echo "feature/seuil n'est pas au-dessus de main. Lancez git rebase main depuis feature/seuil."
  exit 1
fi
if ! git -C "$D" show feature/seuil:seuil.txt | grep -qx "Seuil : 5 minutes"; then
  echo "seuil.txt devrait contenir exactement la ligne Seuil : 5 minutes. Corrigez le fichier, puis lancez git add seuil.txt et git commit -m \"Fixe le seuil à 5 minutes\"."
  exit 1
fi
echo "Le conflit est résolu, et la branche est replacée."
```
