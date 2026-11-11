---
title: "01 - git restore : abandonner un changement pas encore enregistré"
description: "Revenir au contenu du dernier commit, ou retirer un fichier de la zone de préparation"
---

Le cas le plus fréquent est aussi le plus simple : vous avez modifié un fichier, et ce changement ne vous convient pas. Tant qu'il n'est pas dans un commit, `git restore` le fait disparaître.

## 01.1 - Créer le dépôt de départ

Ce dépôt contient une page et un runbook, avec un commit. La construction `cat > fichier <<'EOF'` écrit dans le fichier tout ce qui suit, jusqu'à la ligne `EOF` :

```exec
mkdir -p ~/byte-layers/git/l4-undo && cd ~/byte-layers/git/l4-undo && git init -b main
echo '<h1>Statut des services</h1>' > index.html
cat > runbook.md <<'EOF'
# Runbook

Alerte au bout de : 5 minutes
EOF
git add index.html runbook.md && git commit -m "État initial"
```

```verify
if ! git -C ~/byte-layers/git/l4-undo rev-parse HEAD >/dev/null 2>&1; then
  echo "Le dépôt n'a pas de commit. Vérifiez votre identité avec git config --global user.name, puis relancez la commande."
  exit 1
fi
echo "Le dépôt de départ est prêt."
```

## 01.2 - Abandonner une modification avec git restore

Abîmez la page, puis regardez ce que Git en dit :

```exec
cd ~/byte-layers/git/l4-undo && echo 'une ligne ratée' >> index.html
cd ~/byte-layers/git/l4-undo && git status --short
```

Le `M` signale un fichier modifié. Il est placé en deuxième colonne, celle du dossier de travail :

```text
 M index.html
```

`git restore` remet le fichier tel qu'il était au dernier commit :

```exec
cd ~/byte-layers/git/l4-undo && git restore index.html
cd ~/byte-layers/git/l4-undo && cat index.html
```

Le fichier a retrouvé son contenu :

```text
<h1>Statut des services</h1>
```

> ⚠️ **Ce changement est perdu pour de bon.** Git ne l'avait jamais enregistré, et aucune commande ne le récupérera.

```verify
D=~/byte-layers/git/l4-undo
if grep -q "ratée" "$D/index.html"; then
  echo "index.html contient encore la ligne ratée. Lancez git restore index.html."
  exit 1
fi
echo "La modification est abandonnée."
```

## 01.3 - Retirer un fichier de la zone de préparation avec --staged

Vous avez préparé un fichier par erreur, avec `git add`. L'option `--staged` le retire de la zone de préparation, sans toucher à votre modification :

```exec
cd ~/byte-layers/git/l4-undo && echo 'un essai' >> index.html
cd ~/byte-layers/git/l4-undo && git add index.html
cd ~/byte-layers/git/l4-undo && git status --short
```

Le `M` est maintenant en première colonne, celle de la zone de préparation :

```text
M  index.html
```

Retirez-le, puis regardez l'état :

```exec
cd ~/byte-layers/git/l4-undo && git restore --staged index.html
cd ~/byte-layers/git/l4-undo && git status --short
```

Le `M` est revenu en deuxième colonne, et votre modification est toujours là :

```text
 M index.html
```

Abandonnez-la maintenant pour repartir d'un dépôt propre :

```exec
cd ~/byte-layers/git/l4-undo && git restore index.html
```

```verify
if [ -n "$(git -C ~/byte-layers/git/l4-undo status --porcelain)" ]; then
  echo "Il reste des changements. git status vous dira lesquels."
  exit 1
fi
echo "Le dépôt est propre."
```

> 💡 **Remarque.** Dans de nombreux tutoriels, vous verrez `git checkout -- fichier` à la place de `git restore fichier`, et `git reset fichier` à la place de `git restore --staged fichier`. Ce sont les formes plus anciennes.

> 📖 [`git restore`](https://git-scm.com/docs/git-restore)
