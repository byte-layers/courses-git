---
title: "04 - Résoudre un conflit de fusion"
description: "Deux changements sur la même ligne : lire les marqueurs, décider, terminer la fusion"
---

Un **conflit** survient quand deux branches modifient la même ligne, ou des lignes voisines, et que Git ne peut pas décider à votre place. Ce n'est pas une erreur, et rien n'est perdu : Git s'arrête et vous demande de trancher. Ici, deux personnes changent le même seuil d'alerte du runbook, l'une à 2 minutes et l'autre à 10.

## 04.1 - Provoquer deux changements sur la même ligne

Créez la première branche, qui abaisse le seuil. Cette commande réécrit tout le fichier, et seule la ligne du seuil change. L'option `-a` de `git commit` prépare les fichiers déjà suivis, et vous évite ici un `git add` :

```exec
cd ~/byte-layers/git/l2 && git switch -c feature/seuil-bas
cat > ~/byte-layers/git/l2/runbook.md <<'EOF'
# Runbook

Alerte au bout de : 2 minutes
## Contacts
EOF
cd ~/byte-layers/git/l2 && git commit -am "Abaisse le seuil à 2 minutes"
```

Repartez de `main` pour créer la seconde branche, qui relève ce même seuil :

```exec
cd ~/byte-layers/git/l2 && git switch main && git switch -c feature/seuil-haut
cat > ~/byte-layers/git/l2/runbook.md <<'EOF'
# Runbook

Alerte au bout de : 10 minutes
## Contacts
EOF
cd ~/byte-layers/git/l2 && git commit -am "Relève le seuil à 10 minutes"
```

Revenez sur `main` et fusionnez la première branche. Tout se passe bien, c'est une avance rapide comme pour `feature/db` :

```exec
cd ~/byte-layers/git/l2 && git switch main && git merge feature/seuil-bas
```

```verify
D=~/byte-layers/git/l2
if ! git -C "$D" merge-base --is-ancestor feature/seuil-bas main 2>/dev/null; then
  echo "feature/seuil-bas devrait être fusionnée dans main."
  exit 1
fi
if ! git -C "$D" show-ref --verify --quiet refs/heads/feature/seuil-haut; then
  echo "La branche feature/seuil-haut n'existe pas."
  exit 1
fi
echo "main contient le seuil à 2 minutes, et feature/seuil-haut attend."
```

## 04.2 - Déclencher le conflit et le lire

Fusionnez maintenant la seconde branche. Elle modifie la ligne que `main` vient de changer :

```exec
cd ~/byte-layers/git/l2 && git merge feature/seuil-haut
```

Git s'arrête et nomme le fichier en cause :

```text
Auto-merging runbook.md
CONFLICT (content): Merge conflict in runbook.md
Automatic merge failed; fix conflicts and then commit the result.
```

Votre dépôt est dans un état intermédiaire, que `git status` décrit, et il vous donne aussi la marche à suivre :

```exec
cd ~/byte-layers/git/l2 && git status
```

La section `Unmerged paths` liste les fichiers à résoudre :

```text
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   runbook.md
```

Affichez le fichier pour voir comment Git a représenté le désaccord :

```exec
cd ~/byte-layers/git/l2 && cat runbook.md
```

Git a écrit les deux versions dans le fichier, encadrées par des **marqueurs de conflit** :

```text
# Runbook

<<<<<<< HEAD
Alerte au bout de : 2 minutes
=======
Alerte au bout de : 10 minutes
>>>>>>> feature/seuil-haut
## Contacts
```

Chaque marqueur a un rôle précis :

| Marqueur | Ce qu'il délimite |
|---|---|
| `<<<<<<< HEAD` | le début de votre version, celle de la branche où vous êtes |
| `=======` | la séparation entre les deux versions |
| `>>>>>>> feature/seuil-haut` | la fin de la version que vous tentiez d'amener |

Si vous préférez renoncer, `git merge --abort` remet le dépôt exactement comme avant la fusion. Vous allez plutôt résoudre ce conflit.

## 04.3 - Décider, puis terminer la fusion

Résoudre un conflit, c'est écrire le contenu final du fichier et retirer les trois marqueurs. La bonne réponse n'est pas forcément l'une des deux versions : ici, votre équipe tranche pour **5 minutes**. Ouvrez `runbook.md` avec l'une de ces commandes, depuis le dossier `~/byte-layers/git/l2` :

| Votre outil | La commande | Pour sauvegarder |
|---|---|---|
| VS Code | `code runbook.md` | Ctrl+S (Cmd+S sur Mac) |
| Bloc-notes, sous Windows | `notepad runbook.md` | Ctrl+S |
| nano, dans le terminal | `nano runbook.md` | Ctrl+O, Entrée, puis Ctrl+X pour quitter |

Modifiez le fichier en quatre gestes, puis sauvegardez-le :

1. supprimez la ligne `<<<<<<< HEAD` ;
2. supprimez la ligne `=======` et la ligne `>>>>>>> feature/seuil-haut` ;
3. supprimez la ligne `Alerte au bout de : 10 minutes` ;
4. remplacez `2 minutes` par `5 minutes` sur la ligne restante.

VS Code affiche aussi des boutons pour accepter l'une ou l'autre version. Ici, aucune ne convient telle quelle, et c'est souvent le cas.

Si vous n'arrivez vraiment pas à éditer ce fichier, cette commande écrit le résultat à votre place. Essayez d'abord à la main, car c'est ce geste que vous referez au travail.

```exec
cat > ~/byte-layers/git/l2/runbook.md <<'EOF'
# Runbook

Alerte au bout de : 5 minutes
## Contacts
EOF
```

Vérifiez le résultat avant d'aller plus loin. Il ne doit rester ni marqueur, ni ligne à 10 minutes :

```exec
cd ~/byte-layers/git/l2 && cat runbook.md
```

Indiquez ensuite à Git que ce fichier est résolu. C'est encore `git add` qui s'en charge, et il prend ici un sens particulier :

```exec
cd ~/byte-layers/git/l2 && git add runbook.md
```

`git status` confirme qu'il ne reste plus qu'à conclure :

```exec
cd ~/byte-layers/git/l2 && git status
```

Git indique que tous les conflits sont réglés :

```text
On branch main
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)

Changes to be committed:
	modified:   runbook.md
```

Terminez la fusion avec un commit, et gardez le message proposé :

```exec
cd ~/byte-layers/git/l2 && git commit --no-edit
```

Le haut du graphe montre le résultat, et le conflit a laissé un commit de merge ordinaire :

```exec
cd ~/byte-layers/git/l2 && git log --oneline --all --graph
```

Les deux branches du seuil se rejoignent dans un nouveau commit :

```text
*   11b63ac (HEAD -> main) Merge branch 'feature/seuil-haut'
|\  
| * b911b0e (feature/seuil-haut) Relève le seuil à 10 minutes
* | cfe0bd2 (feature/seuil-bas) Abaisse le seuil à 2 minutes
|/  
*   4a8310c Merge branch 'feature/api'
```

```verify
D=~/byte-layers/git/l2
if git -C "$D" rev-parse -q --verify MERGE_HEAD >/dev/null; then
  echo "La fusion n'est pas terminée. Lancez git add, puis git commit --no-edit."
  exit 1
fi
if grep -qE '^(<<<<<<<|=======|>>>>>>>)' "$D"/runbook.md; then
  echo "runbook.md contient encore des marqueurs de conflit."
  exit 1
fi
if ! grep -q "Alerte au bout de : 5 minutes" "$D"/runbook.md; then
  echo "Le seuil retenu devrait être de 5 minutes."
  exit 1
fi
if ! git -C "$D" merge-base --is-ancestor feature/seuil-haut main; then
  echo "feature/seuil-haut devrait être fusionnée dans main."
  exit 1
fi
if [ "$(git -C "$D" rev-list --parents -n 1 HEAD | wc -w | tr -d ' ')" != "3" ]; then
  echo "Le dernier commit devrait être un commit de merge."
  exit 1
fi
echo "Conflit résolu : le seuil est à 5 minutes."
```

## Questions

```quiz
title: "Les conflits"
tracksProgress: false
questions:
  - prompt: "Quand Git déclare-t-il un conflit ?"
    answers:
      - "Dès que deux branches ont modifié le même fichier"
      - "Quand deux branches ont modifié les mêmes lignes d'un fichier, ou des lignes voisines"
      - "Dès que deux branches ont divergé"
    correct: 2
    explanation: "Deux changements sur des passages éloignés d'un même fichier se fusionnent seuls, comme deux changements dans deux fichiers."
  - prompt: "Vous êtes en plein conflit, et vous voulez revenir à l'état d'avant. Quelle commande utilisez-vous ?"
    answers:
      - "git commit --no-edit"
      - "git add ."
      - "git merge --abort"
    correct: 3
    explanation: "`git merge --abort` annule la fusion en cours. Un `git add .` marquerait au contraire les fichiers comme résolus, marqueurs compris."
```

> 📖 [Conflits de fusion, dans la documentation de `git merge`](https://git-scm.com/docs/git-merge#_how_conflicts_are_presented)
