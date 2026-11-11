---
title: "02 - De l'issue à la merge request"
description: "Relier une tâche, une branche et une proposition de changement"
---

Une **merge request** (MR) est une demande de fusion d'une branche dans une autre. C'est là que l'équipe discute et relit le code. On parle de *pull request* sur GitHub.

## 02.1 - Créer l'issue de départ

Créez une issue intitulée `Ajouter la page de statut`, depuis **Work items**. Son numéro s'affiche à côté de son titre, ici `#1`.

## 02.2 - Faire le travail sur une branche

Mettez le numéro de l'issue dans le nom de la branche, pour vos collègues. La phrase `Closes #1` dans le message du commit demande à GitLab de fermer l'issue quand ce commit arrive dans la branche par défaut. Un second `-m` ajoute un paragraphe au message :

```exec
cd ~/byte-layers/git/gitlab-mr/statuspage && git switch -c feature/1-page-statut
cd ~/byte-layers/git/gitlab-mr/statuspage && echo '<h1>Statut des services</h1>' > index.html && git add index.html
cd ~/byte-layers/git/gitlab-mr/statuspage && git commit -m "Ajoute la page de statut" -m "Closes #1"
cd ~/byte-layers/git/gitlab-mr/statuspage && git push -u origin feature/1-page-statut
```

GitLab répond avec un lien qui prépare la merge request :

```text
remote: To create a merge request for feature/1-page-statut, visit:
remote:   https://gitlab.com/demo-votre-nom/statuspage-mr/-/merge_requests/new?merge_request%5Bsource_branch%5D=feature%2F1-page-statut
```

## 02.3 - Ouvrir la merge request

Suivez ce lien, ou ouvrez **Code**, **Merge requests**, **New merge request**. Vérifiez la branche source `feature/1-page-statut` et la cible `main`. Le titre et la description reprennent votre commit, et sont là pour votre relecteur. Validez avec **Create merge request**.

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
if ! curl -fsS "$A/merge_requests?state=all" 2>/dev/null | grep -q '"source_branch":"feature/1-page-statut"'; then
  echo "Aucune merge request depuis feature/1-page-statut. Créez-la sur GitLab."
  exit 1
fi
echo "La merge request est ouverte."
```

> 📖 [Merge requests](https://docs.gitlab.com/user/project/merge_requests/) · [Fermer une issue automatiquement](https://docs.gitlab.com/user/project/issues/managing_issues/#closing-issues-automatically)
