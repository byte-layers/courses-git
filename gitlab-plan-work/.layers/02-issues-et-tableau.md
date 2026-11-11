---
title: "02 - Créer des issues et les suivre sur un tableau"
description: "Une tâche par besoin, rattachée au jalon, suivie sur un kanban"
---

Une **issue** décrit un travail à faire, avec une discussion, une personne assignée et un état. C'est le point de départ d'une modification de code.

## 02.1 - Créer trois issues

Dans le menu du projet, ouvrez **Work items**, puis **New item**, et choisissez le type **Issue**. Créez ces trois issues, chacune avec le jalon `V1` et le label `feature` :

| Titre | Description |
|---|---|
| `U1 - Afficher le statut de l'API` | Ajouter une ligne pour l'API sur la page |
| `U2 - Afficher le statut de la base` | Ajouter une ligne pour la base |
| `U3 - Ajouter le contact d'astreinte` | Ajouter le contact dans le runbook |

Assignez-vous la première avec le champ **Assignee**.

```verify
C=$(cat ~/byte-layers/git/gitlab-plan/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/byte-layers/git/gitlab-plan/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
J=$(curl -fsS "$A/issues?state=all&per_page=100" 2>/dev/null)
if [ -z "$J" ]; then
  echo "GitLab ne trouve pas les issues du projet. Vérifiez l'adresse et que le projet est public."
  exit 1
fi
N=$(echo "$J" | grep -o '"type":"ISSUE"' | wc -l | tr -d ' ')
if [ "$N" -lt 3 ]; then
  echo "Le projet devrait contenir au moins trois issues, il en a $N."
  exit 1
fi
if [ "$(echo "$J" | grep -o '"title":"V1"' | wc -l | tr -d ' ')" -lt 3 ]; then
  echo "Les trois issues devraient être rattachées au jalon V1."
  exit 1
fi
if [ "$(echo "$J" | grep -o '"labels":\[[^]]*"feature"' | wc -l | tr -d ' ')" -lt 3 ]; then
  echo "Les trois issues devraient porter le label feature."
  exit 1
fi
echo "Les trois issues sont créées et classées."
```

## 02.2 - Suivre l'avancement sur un tableau

Un **tableau** (*issue board*) affiche les issues en colonnes, façon kanban. Dans **Plan**, ouvrez **Issue boards**. Le bouton **New list** ajoute une colonne : choisissez le label `en cours`, puis validez avec **Add to board**.

Faites glisser l'issue `U1` de la colonne **Open** vers la colonne `en cours`. GitLab lui ajoute le label correspondant : déplacer une carte, c'est modifier l'issue.

```verify
C=$(cat ~/byte-layers/git/gitlab-plan/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/byte-layers/git/gitlab-plan/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
J=$(curl -fsS "$A/issues?state=all&per_page=100" 2>/dev/null)
if ! echo "$J" | grep -q '"en cours"'; then
  echo "Aucune issue ne porte le label en cours. Faites glisser U1 dans cette colonne."
  exit 1
fi
echo "U1 est dans la colonne en cours."
```

> 📖 [Issues](https://docs.gitlab.com/user/project/issues/) · [Tableaux d'issues](https://docs.gitlab.com/user/project/issue_board/)
