---
title: "04 - Faire le point et ranger"
description: "Quand un runner sur son poste est utile, ses limites, et comment tout arrêter"
---

Votre projet n'utilise plus que votre runner. Avant de ranger, voici quand ce montage est le bon choix, et ce qu'il ne remplace pas.

## 04.1 - Quand utiliser un runner sur son poste

| Situation | Pourquoi votre runner aide |
|---|---|
| les minutes des runners partagés sont épuisées, ou GitLab demande de valider votre compte | vos jobs tournent sur votre machine, sans compter de minutes |
| un job doit joindre un service de votre poste ou de votre réseau, comme un SonarQube local | le runner est dans votre réseau ; un runner partagé ne voit pas votre poste |
| vous voulez une architecture précise, ou plus de mémoire | le job tourne sur votre matériel |

Et ses limites :

| Limite | Conséquence |
|---|---|
| le runner ne tourne que quand votre poste est allumé | poste éteint, les jobs restent en attente ; une équipe installe plutôt un runner sur un serveur |
| l'accès au socket Docker | un job peut lancer n'importe quel conteneur sur votre poste : n'enregistrez ce runner que sur des projets dont vous maîtrisez le code |
| le jeton dans la configuration | qui le récupère peut se faire passer pour votre runner ; supprimez le runner sur GitLab quand vous n'en avez plus besoin |

## 04.2 - Tout arrêter

Le rangement se fait des deux côtés, en commençant par votre poste. Cette commande désenregistre le runner, ce qui prévient GitLab, puis supprime le conteneur, les volumes et les images du lab, et son dossier :

```exec
ID=$(docker exec gitlab-runner cat /etc/gitlab-runner/.runner_system_id); docker exec gitlab-runner gitlab-runner unregister --all-runners; docker rm -f gitlab-runner; docker volume rm gitlab-runner-config $(docker volume ls -q --filter "label=com.gitlab.gitlab-runner.runner.system_id=$ID"); docker rmi gitlab/gitlab-runner:v19.5.3 alpine:3.22 $(docker images -q --filter "reference=registry.gitlab.com/gitlab-org/gitlab-runner/gitlab-runner-helper:*-v19.5.3"); rm -rf ~/byte-layers/git/runner-local
```

> 🔍 **Comprendre la commande**
>
> | Morceau | Rôle |
> |---|---|
> | `ID=$(docker exec gitlab-runner cat …/.runner_system_id)` | lit l'identifiant de ce runner sur votre poste, avant de supprimer le conteneur : il sert à retrouver ses volumes de cache |
> | `gitlab-runner unregister --all-runners` | retire les runners de la configuration, et prévient GitLab |
> | `;` | enchaîne la commande suivante même si la précédente a échoué : le rangement va jusqu'au bout |
> | `docker rm -f gitlab-runner` | arrête et supprime le conteneur |
> | `docker volume rm gitlab-runner-config` | supprime le volume de configuration, et le jeton qu'il contenait |
> | `$(docker volume ls -q --filter "label=…system_id=$ID")` | ajoute les volumes de cache que l'executor `docker` a créés pour les jobs de **ce** runner, et seulement eux : un autre runner de votre poste garde les siens |
> | `docker rmi …` | supprime les images téléchargées par le lab : le runner, `alpine:3.22`, et l'image *helper* de la même version, que le runner utilise pour cloner le projet dans chaque job ; ignorez l'erreur si une autre application utilise encore `alpine:3.22` |
> | `rm -rf ~/byte-layers/git/runner-local` | supprime le dossier du lab |

Sur GitLab, dans **Settings**, **CI/CD**, **Runners**, votre runner a disparu de la liste ; s'il y est encore, supprimez-le avec l'icône de corbeille, pour que son jeton ne vaille plus rien. Vous pouvez aussi supprimer le projet, depuis **Settings**, **General**, **Advanced**, **Delete project**.

```verify
docker inspect gitlab-runner >/dev/null 2>&1 && { echo "Le conteneur gitlab-runner existe encore : docker rm -f gitlab-runner."; exit 1; }
docker volume inspect gitlab-runner-config >/dev/null 2>&1 && { echo "Le volume gitlab-runner-config existe encore : docker volume rm gitlab-runner-config."; exit 1; }
[ -e ~/byte-layers/git/runner-local ] && { echo "Le dossier ~/byte-layers/git/runner-local existe encore."; exit 1; }
echo "Le runner, son volume de configuration et le dossier du lab sont supprimés."
```

## Récap

- Un runner sur son poste tourne dans un conteneur, avec sa configuration dans un **volume** et l'accès au **socket Docker** pour l'executor `docker`.
- On le **crée** sur GitLab, qui donne un jeton `glrt-` et fixe ses tags, puis on l'**enregistre** avec `gitlab-runner register`.
- Un job va sur ce runner s'il demande son tag avec `tags:` ; dans `default:`, le tag vaut pour tous les jobs.
- Couper les runners partagés du projet garantit qu'aucun job ne consomme de minutes chez GitLab.
- Le runner ne tourne que poste allumé, et l'accès au socket Docker réserve ce montage à vos propres projets.

> 📖 [Lancer GitLab Runner dans un conteneur (en anglais)](https://docs.gitlab.com/runner/install/docker/) · [Enregistrer un runner (en anglais)](https://docs.gitlab.com/runner/register/) · [Gérer les runners d'un projet (en anglais)](https://docs.gitlab.com/ci/runners/runners_scope/) · [Le mot-clé tags (en anglais)](https://docs.gitlab.com/ci/yaml/#tags)
