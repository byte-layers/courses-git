---
title: "02 - Merge ou rebase, et publier avec --force-with-lease"
description: "Choisir sa stratégie, comprendre le push refusé après un rebase"
---

Votre rebase a réécrit un commit que le serveur connaissait déjà. Cette situation montre à la fois le danger du rebase et la façon de le publier proprement.

## 02.1 - Voir le push refusé après un rebase

Tentez de publier. Le refus est attendu :

```exec
cd ~/layers-git/l4-rebase/depot && git push
```

Git refuse l'envoi :

```text
 ! [rejected]        feature/db -> feature/db (non-fast-forward)
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart.
```

Le serveur possède l'ancien commit, et votre branche ne le contient plus. Le terme `non-fast-forward` signifie que la branche du serveur ne peut pas simplement avancer jusqu'à la vôtre. Git vous suggère un `git pull` dans la suite de son message, mais ne le suivez pas ici : une fusion réintroduirait l'ancien commit à côté de sa copie. C'est bien la branche du serveur qu'il faut remplacer.

## 02.2 - Remplacer la branche du serveur avec --force-with-lease

`--force-with-lease` remplace la branche distante, **à condition** qu'elle soit encore là où vous l'aviez vue au dernier contact. Si un collègue y a poussé entre-temps et que vous ne l'avez pas vu, Git refuse, là où `--force` aurait écrasé son travail :

```exec
cd ~/layers-git/l4-rebase/depot && git push --force-with-lease
```

Le signe `+` signale un remplacement forcé :

```text
 + 7a6f809...b919324 feature/db -> feature/db (forced update)
```

> 💡 **Remarque.** Cette protection se base sur votre dernier contact avec le serveur. Un `git fetch`, y compris lancé automatiquement par un éditeur, la renouvelle : regardez `git log origin/feature/db` avant de forcer.

Le serveur a maintenant la branche réécrite, et elle peut rejoindre `main` en avance rapide, sans commit de merge :

```exec
cd ~/layers-git/l4-rebase/depot && git switch main
cd ~/layers-git/l4-rebase/depot && git merge feature/db
cd ~/layers-git/l4-rebase/depot && git log --oneline --all --graph
```

La fourche a disparu de l'historique :

```text
* b919324 (HEAD -> main, origin/feature/db, feature/db) Ajoute l'état de la base
* c433ca9 Complète le runbook
* 1fcdeec (origin/main) État initial
```

```verify
D=~/layers-git/l4-rebase
if [ "$(git -C "$D/serveur.git" rev-parse feature/db)" != "$(git -C "$D/depot" rev-parse feature/db)" ]; then
  echo "Le serveur n'a pas la branche réécrite. Lancez git push --force-with-lease depuis feature/db."
  exit 1
fi
if ! git -C "$D/depot" merge-base --is-ancestor feature/db main; then
  echo "main ne contient pas encore feature/db. Lancez git merge feature/db depuis main."
  exit 1
fi
echo "La branche est publiée, et main la contient."
```

## 02.3 - Choisir entre merge et rebase

Les deux réunissent le même travail, et leur différence porte sur l'historique :

| | `git merge` | `git rebase` |
|---|---|---|
| Historique | garde la fourche, avec un commit de merge | linéaire |
| Commits existants | intacts | recréés, avec de nouveaux hash |
| Sur une branche partagée | sans risque | à éviter |

La règle à retenir tient en une phrase : **ne rebasez pas une branche sur laquelle d'autres personnes travaillent.** Sur votre propre branche, un rebase avant la fusion donne un historique lisible. Sur `main` ou une branche commune, on fusionne.

> 💡 **Remarque.** Cela reste une convention d'équipe. Certaines équipes fusionnent toujours, d'autres rebasent systématiquement leurs branches avant de les intégrer.

## Question

```quiz
prompt: "Après un rebase sur votre branche déjà publiée, quelle commande convient pour la publier ?"
answers:
  - "git push --force-with-lease"
  - "git pull --no-rebase, puis git push"
  - "git push --force, sans précaution particulière"
correct: 1
explanation: "`git pull --no-rebase` réintroduirait l'ancienne version des commits. `--force-with-lease` refuse d'écraser un travail que vous n'avez pas vu."
```

> 📖 [Rebaser, dans le livre Pro Git](https://git-scm.com/book/fr/v2/Les-branches-avec-Git-Rebaser-Rebasing) · [`git push --force-with-lease`](https://git-scm.com/docs/git-push#Documentation/git-push.txt---force-with-leaseltrefnamegt)
