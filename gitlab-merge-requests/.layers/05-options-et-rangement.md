---
title: "05 - Choisir sa façon de fusionner, et ranger"
description: "Les options de fusion d'un projet, et la suite"
---

Votre équipe peut décider de la forme que prend l'historique au moment de la fusion. Ces réglages se trouvent dans **Settings**, **Merge requests**.

## 05.1 - Comparer les méthodes de fusion

| Méthode | Ce qui se passe | Historique |
|---|---|---|
| Merge commit | un commit de merge est toujours créé | garde la trace de chaque branche |
| Merge commit with semi-linear history | fusion permise si la branche est à jour | fourches courtes et lisibles |
| Fast-forward merge | pas de commit de merge | linéaire |

L'option **Squash commits**, proposée sur chaque merge request, réunit tous les commits de la branche en un seul. Elle convient quand les commits intermédiaires n'apportent rien à l'historique.

> 💡 **Remarque.** Rendre une approbation obligatoire, ou désigner des relecteurs par dossier avec un fichier `CODEOWNERS`, fait partie des offres payantes de GitLab.

## 05.2 - Ranger le dossier de ce cours

Vous pouvez aussi supprimer le projet sur GitLab, depuis **Settings**, **General**, **Advanced**, **Delete project**.

```exec
cd ~ && rm -rf ~/byte-layers/git/gitlab-mr
```

```verify
if [ -e ~/byte-layers/git/gitlab-mr ]; then
  echo "Le dossier ~/byte-layers/git/gitlab-mr existe encore."
  exit 1
fi
echo "Le dossier est supprimé."
```

## Récap

- Une branche protégée limite qui peut y pousser : réglée sur **No one**, elle ne reçoit le code que par une merge request.
- Une issue, une branche à son numéro et `Closes #n` relient la tâche au code.
- Une merge request se relit dans **Changes** puis se fusionne, ce qui ferme l'issue.
- Un conflit se résout sur la branche, en fusionnant `main` dedans puis en publiant.

Pour pratiquer à plusieurs, faites le lab [Jouer Gitflow à deux sur GitLab](https://byte-layers.com/fr/labs/gitlab-team-workflow).

> 📖 [Méthodes de fusion](https://docs.gitlab.com/user/project/merge_requests/methods/) · [Squash](https://docs.gitlab.com/user/project/merge_requests/squash_and_merge/)
