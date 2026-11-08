---
title: "02 - Constater le blocage d'une merge request"
description: "Casser un test, voir la fusion refusée, puis corriger"
---

Vous allez introduire un bug, et voir le garde-fou fonctionner.

## 02.1 - Proposer un changement qui casse le test

Cette branche change l'addition en soustraction :

```exec
cd ~/layers-git/ci-quality/calculatrice && git pull && git switch -c fix/calcul
cd ~/layers-git/ci-quality/calculatrice && sed 's/(+x) + (+y)/(+x) - (+y)/' operations.js > operations.tmp && mv operations.tmp operations.js
cd ~/layers-git/ci-quality/calculatrice && git add operations.js && git commit -m "Modifie le calcul" && git push -u origin fix/calcul
```

Ouvrez une merge request de `fix/calcul` vers `main`. Le pipeline échoue, et GitLab affiche que la fusion est bloquée, avec le message `Merge blocked` et le bouton **Merge** indisponible.

## 02.2 - Corriger et fusionner

`git revert` annule le dernier commit en en créant un nouveau. Une fois celui-ci publié, le pipeline réussit, et le bouton **Merge** redevient disponible :

```exec
cd ~/layers-git/ci-quality/calculatrice && git revert --no-edit HEAD && git push
```

Fusionnez la merge request. Après ce revert, son onglet **Changes** est vide : la fusion ne sert ici qu'à clore l'exercice.

```verify
C=$(cat ~/layers-git/ci-quality/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/layers-git/ci-quality/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
if ! curl -fsS "$A/merge_requests?state=merged" 2>/dev/null | grep -q '"source_branch":"fix/calcul"'; then
  echo "La merge request de fix/calcul n'est pas fusionnée."
  exit 1
fi
if ! curl -fsS "$A/repository/files/operations.js/raw?ref=main" 2>/dev/null | grep -q '(+x) + (+y)'; then
  echo "L'addition devrait être rétablie sur main."
  exit 1
fi
echo "La merge request est fusionnée, et l'addition est rétablie sur main."
```
