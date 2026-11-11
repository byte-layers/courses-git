---
title: "04 - Résoudre le conflit d'une merge request"
description: "Quand deux merge requests modifient les mêmes lignes"
---

Deux merge requests peuvent modifier la même ligne. La première passe, et la seconde se retrouve bloquée. Vous allez provoquer ce cas, puis le résoudre sur votre poste.

## 04.1 - Ouvrir deux merge requests en concurrence

Créez deux branches depuis `main`, qui fixent chacune une valeur différente pour le seuil :

```exec
cd ~/byte-layers/git/gitlab-mr/statuspage && git switch -c feature/seuil-bas && echo 'Seuil : 2 minutes' > seuil.txt && git add seuil.txt && git commit -m "Fixe le seuil à 2 minutes" && git push -u origin feature/seuil-bas
cd ~/byte-layers/git/gitlab-mr/statuspage && git switch main && git switch -c feature/seuil-haut && echo 'Seuil : 10 minutes' > seuil.txt && git add seuil.txt && git commit -m "Fixe le seuil à 10 minutes" && git push -u origin feature/seuil-haut
```

Sur GitLab, ouvrez une merge request pour chacune, vers `main`, puis fusionnez celle de `feature/seuil-bas`.

## 04.2 - Lire le blocage dans la merge request

Ouvrez la seconde merge request. La fusion est bloquée, et GitLab affiche :

```text
Merge blocked: 1 check failed
Merge conflicts must be resolved.
```

Deux boutons vous proposent de résoudre : **Resolve conflicts** dans le navigateur pour les cas simples, ou **Resolve locally** sur votre poste. Vous allez le faire localement, ce qui marche dans tous les cas.

## 04.3 - Résoudre le conflit sur votre poste

Sur la branche en conflit, récupérez `main` et fusionnez-la. Le conflit est attendu :

```exec
cd ~/byte-layers/git/gitlab-mr/statuspage && git fetch
cd ~/byte-layers/git/gitlab-mr/statuspage && git merge origin/main
```

Ouvrez le fichier avec votre éditeur, en donnant son chemin complet, par exemple `code ~/byte-layers/git/gitlab-mr/statuspage/seuil.txt`. Faites-lui contenir une seule ligne, `Seuil : 5 minutes`, sans aucun marqueur, puis sauvegardez-le.

Si vous n'arrivez vraiment pas à éditer ce fichier, cette commande écrit le résultat à votre place :

```exec
echo 'Seuil : 5 minutes' > ~/byte-layers/git/gitlab-mr/statuspage/seuil.txt
```

Terminez la fusion et publiez. `--no-edit` garde le message proposé par Git :

```exec
cd ~/byte-layers/git/gitlab-mr/statuspage && git add seuil.txt && git commit --no-edit
cd ~/byte-layers/git/gitlab-mr/statuspage && git push
```

Rechargez la merge request : le blocage a disparu. Cliquez sur **Merge**.

```verify
C=$(cat ~/byte-layers/git/gitlab-mr/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/byte-layers/git/gitlab-mr/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
if ! curl -fsS "$A/merge_requests?state=merged" 2>/dev/null | grep -q '"source_branch":"feature/seuil-haut"'; then
  echo "La merge request de feature/seuil-haut n'est pas encore fusionnée."
  exit 1
fi
if ! curl -fsS "$A/repository/files/seuil.txt/raw?ref=main" 2>/dev/null | grep -qx 'Seuil : 5 minutes'; then
  echo "seuil.txt devrait contenir la ligne Seuil : 5 minutes sur main."
  exit 1
fi
echo "Le conflit est résolu, et les deux merge requests sont fusionnées."
```

> 📖 [Conflits de merge request](https://docs.gitlab.com/user/project/merge_requests/conflicts/)
