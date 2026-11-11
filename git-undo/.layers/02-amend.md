---
title: "02 - git commit --amend : corriger le dernier commit"
description: "Changer un message, ou ajouter un changement oublié"
---

Vous venez de faire un commit, et vous voyez une faute dans le message, ou vous avez oublié un fichier. Tant que ce commit n'est pas publié, `--amend` le corrige.

## 02.1 - Corriger le message du dernier commit

Faites un commit avec un message fautif, et regardez l'historique :

```exec
cd ~/byte-layers/git/l4-undo && echo '<p>API : OK</p>' >> index.html
cd ~/byte-layers/git/l4-undo && git commit -am "Affiche l'API avec une fote"
cd ~/byte-layers/git/l4-undo && git log --oneline
```

L'option `--amend` remplace le dernier commit, et `-m` donne le nouveau message :

```exec
cd ~/byte-layers/git/l4-undo && git commit --amend -m "Affiche l'état de l'API"
cd ~/byte-layers/git/l4-undo && git log --oneline
```

Le message est corrigé, et il y a toujours deux commits. Regardez aussi le début de la ligne : **le hash a changé**, parce que Git a créé un nouveau commit à la place de l'ancien.

```text
9eaba93 (HEAD -> main) Affiche l'état de l'API
da2228a État initial
```

```verify
D=~/byte-layers/git/l4-undo
if git -C "$D" log --format=%s | grep -q "fote"; then
  echo "Le message fautif est encore dans l'historique. Lancez git commit --amend -m avec le bon message."
  exit 1
fi
echo "Le message est corrigé."
```

## 02.2 - Ajouter un changement oublié au dernier commit

Vous auriez dû inclure une ligne dans le runbook, déjà suivi par Git. Préparez-la, puis relancez `--amend`. L'option `--no-edit` conserve le message :

```exec
cd ~/byte-layers/git/l4-undo && echo 'Contact : astreinte' >> runbook.md
cd ~/byte-layers/git/l4-undo && git add runbook.md
cd ~/byte-layers/git/l4-undo && git commit --amend --no-edit
```

Regardez le contenu du commit, qui comporte maintenant les deux fichiers. L'option `--stat` résume les fichiers touchés, et `--format=%s` limite l'en-tête au message :

```exec
cd ~/byte-layers/git/l4-undo && git show --stat --format=%s
```

Le commit comprend maintenant les deux fichiers :

```text
Affiche l'état de l'API

 index.html | 1 +
 runbook.md | 1 +
 2 files changed, 2 insertions(+)
```

> ⚠️ **N'utilisez `--amend` que sur un commit non publié.** Comme le hash change, un commit déjà partagé divergerait de celui de vos collègues.

```verify
D=~/byte-layers/git/l4-undo
if ! git -C "$D" log --format= --name-only --all | grep -qx runbook.md; then
  echo "runbook.md devrait faire partie de l'historique."
  exit 1
fi
if ! git -C "$D" show HEAD:runbook.md | grep -q "astreinte"; then
  echo "La ligne sur l'astreinte n'est pas enregistrée. Préparez runbook.md puis lancez git commit --amend --no-edit."
  exit 1
fi
echo "Le dernier commit contient le changement oublié."
```

> 📖 [Réécrire l'historique, dans le livre Pro Git](https://git-scm.com/book/fr/v2/Utilitaires-Git-R%C3%A9%C3%A9crire-l%E2%80%99historique)
