---
title: "02 - Créer le runner sur GitLab et l'enregistrer"
description: "Déclarer un runner de projet avec un tag, puis relier le conteneur à gitlab.com avec son jeton"
---

Le runner tourne sur votre poste, mais gitlab.com ne le connaît pas. Le relier se fait en deux temps : on **crée** le runner côté GitLab, qui fournit un jeton, puis on **enregistre** le conteneur avec ce jeton. C'est toujours le runner qui contacte GitLab, jamais l'inverse : votre poste n'a besoin d'aucun port ouvert.

## 02.1 - Créer un runner de projet

Dans votre projet `runner-local` sur gitlab.com, ouvrez **Settings**, **CI/CD**, et dépliez la section **Runners**. Cliquez sur **Create project runner**, puis remplissez le formulaire :

| Champ | Valeur | Pourquoi |
|---|---|---|
| **Operating systems** | **Linux** | le runner tourne dans un conteneur Linux, quel que soit le système de votre poste |
| **Tags** | `local` | un job qui demande le tag `local` ira sur ce runner, et seulement sur lui |
| **Run untagged jobs** | décoché | ce runner ne prend que les jobs qui demandent son tag ; les autres restent aux runners partagés (*instance runners*) |
| **Runner description** | `mon poste` | le nom affiché dans GitLab, pour reconnaître le runner |

Cliquez sur **Create runner**. GitLab affiche alors une page *Register runner*, avec un **jeton d'authentification** qui commence par `glrt-`. Copiez-le, et gardez la page ouverte : le jeton ne sera plus affiché une fois la page quittée. Ce jeton est un secret : il permet de se faire passer pour votre runner.

La page propose aussi une commande `gitlab-runner register` pour votre système : ne la lancez pas, la section suivante l'adapte au conteneur.

```acknowledge
J'ai créé le runner de projet avec le tag local, et copié son jeton glrt-.
```

## 02.2 - Enregistrer le conteneur

L'enregistrement écrit dans la configuration du runner l'adresse de GitLab, le jeton, et l'executor à utiliser. Cette commande vous demande le jeton sans l'afficher, puis enregistre le runner. Collez le jeton quand `Jeton :` apparaît, puis appuyez sur Entrée :

```exec
printf 'Jeton : '; stty -echo 2>/dev/null; read -r T; stty echo 2>/dev/null; echo; docker exec gitlab-runner gitlab-runner register --non-interactive --url https://gitlab.com --token "$T" --executor docker --docker-image alpine:3.22; unset T
```

> 🔍 **Comprendre la commande**
>
> | Morceau | Rôle |
> |---|---|
> | `printf 'Jeton : '` | affiche l'invite, sans retour à la ligne |
> | `;` | sépare les commandes, lancées l'une après l'autre |
> | `stty -echo` … `stty echo` | masque la saisie, puis la réaffiche : le jeton n'apparaît pas à l'écran |
> | `2>/dev/null` | cache le message d'erreur de `stty` si le terminal ne le permet pas |
> | `read -r T` | lit le jeton collé, et le range dans la variable `T` ; il ne reste pas dans l'historique du terminal |
> | `echo` | passe à la ligne, puisque la saisie masquée n'en a pas affiché |
> | `docker exec gitlab-runner gitlab-runner register` | lance l'enregistrement dans le conteneur |
> | `--non-interactive` | prend toutes les réponses dans les options, sans poser de question |
> | `--url https://gitlab.com` | le GitLab à contacter |
> | `--token "$T"` | le jeton de la page *Register runner* |
> | `--executor docker` | chaque job tournera dans un conteneur neuf |
> | `--docker-image alpine:3.22` | l'image utilisée quand un job n'en précise pas |
> | `unset T` | efface le jeton de la mémoire du terminal |

La commande se termine par `Runner registered successfully`. Les tags et la description ne figurent pas dans la commande : ils ont été choisis à la création, et GitLab les a associés au runner que désigne ce jeton.

Revenez sur la page *Register runner* : elle affiche que le runner est connecté. Dans **Settings**, **CI/CD**, **Runners**, votre runner apparaît sous *Assigned project runners*, avec un point vert et le tag `local`.

Vérifiez aussi, depuis le conteneur, que GitLab accepte le jeton :

```exec
docker exec gitlab-runner gitlab-runner verify
```

> 🔍 **Comprendre la commande**
>
> | Morceau | Rôle |
> |---|---|
> | `gitlab-runner verify` | contacte GitLab avec chaque jeton de la configuration, et dit s'il est accepté |

L'affichage se termine par une ligne qui contient `is valid`.

```verify
L=$(docker exec gitlab-runner gitlab-runner list 2>&1 | tr -d '\033' | sed 's/\[[0-9;]*m//g')
[ -n "$L" ] || { echo "Le conteneur gitlab-runner ne répond pas : redémarrez-le avec docker start gitlab-runner."; exit 1; }
echo "$L" | grep -q 'Executor=docker' || { echo "Aucun runner n'est enregistré dans le conteneur. Relancez la commande de la section 02.2 avec le jeton glrt- de votre runner. Si la page Register runner est fermée, supprimez le runner sur GitLab et recréez-le pour obtenir un nouveau jeton."; exit 1; }
echo "$L" | grep -q 'URL=https://gitlab.com' || { echo "Le runner est enregistré, mais pas sur https://gitlab.com. Vérifiez l'option --url de la commande."; exit 1; }
docker exec gitlab-runner gitlab-runner verify 2>&1 | tr -d '\033' | grep -q 'is valid' || { echo "GitLab refuse le jeton du runner. Repartez d'une configuration vide : docker rm -f gitlab-runner, puis docker volume rm gitlab-runner-config ; relancez la commande de la section 01.2, recréez le runner sur GitLab, puis relancez la section 02.2 avec le nouveau jeton."; exit 1; }
echo "Le runner est enregistré sur gitlab.com, et GitLab accepte son jeton."
```
