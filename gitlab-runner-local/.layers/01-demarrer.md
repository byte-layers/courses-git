---
title: "01 - Créer le projet et démarrer le runner"
description: "Un projet gitlab.com vide, et le programme gitlab-runner qui tourne dans un conteneur"
---

Il faut deux choses avant de relier un runner à GitLab : un projet dont il exécutera les jobs, et le programme **gitlab-runner** lui-même. Cette étape prépare les deux ; elle ne contient rien à écrire vous-même.

## 01.1 - Créer et cloner le projet

Sur gitlab.com, créez un projet **public** nommé `runner-local`, avec un README : bouton **New project**, puis **Create blank project**, case *Initialize repository with a README* cochée. Copiez ensuite son adresse SSH, affichée par le bouton **Code**. Dans votre terminal, tapez ces deux lignes, en remplaçant l'adresse d'exemple par la vôtre : elles créent le dossier du lab et y enregistrent l'adresse.

```bash
mkdir -p ~/byte-layers/git/runner-local
echo 'git@gitlab.com:votre-nom/runner-local.git' > ~/byte-layers/git/runner-local/url
```

Clonez-le ensuite. Si SSH vous demande de confirmer l'empreinte de gitlab.com à la première connexion, répondez `yes`.

```exec
cd ~/byte-layers/git/runner-local && git clone "$(cat url)" projet
```

> 🔍 **Comprendre la commande**
>
> | Morceau | Rôle |
> |---|---|
> | `cat url` | affiche l'adresse que vous venez d'enregistrer |
> | `"$(…)"` | remplace ce morceau par l'affichage de la commande, ici l'adresse ; les guillemets la gardent en un seul argument |
> | `git clone … projet` | copie le projet dans le dossier `projet` |

```verify
C=$(cat ~/byte-layers/git/runner-local/url 2>/dev/null)
[ -n "$C" ] || { echo "L'adresse du projet n'est pas enregistrée dans ~/byte-layers/git/runner-local/url : lancez la commande de la section 01.1."; exit 1; }
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
grep -q 'votre-nom' ~/byte-layers/git/runner-local/url && { echo "Le fichier url contient encore l'exemple votre-nom : remplacez-le par l'adresse de votre projet."; exit 1; }
[ -d ~/byte-layers/git/runner-local/projet/.git ] || { echo "Le dossier ~/byte-layers/git/runner-local/projet n'est pas un clone Git : relancez git clone."; exit 1; }
curl -fsS "$A" >/dev/null 2>&1 || { echo "Le projet n'est pas lisible sur GitLab. Vérifiez qu'il est public, et que l'adresse enregistrée est la bonne."; exit 1; }
echo "Le projet est créé, public, et cloné."
```

## 01.2 - Démarrer le runner dans un conteneur

GitLab publie gitlab-runner sous forme d'image Docker : rien à installer d'autre. Le runner a besoin de deux choses en plus de son image :

- un endroit où **garder sa configuration**, qui contiendra son jeton une fois enregistré : un **volume** Docker, un espace de stockage géré par Docker, qui survit à la suppression du conteneur ;
- un accès au **Docker de votre poste**, pour créer un conteneur neuf à chaque job : c'est l'executor `docker`, présenté dans le bit sur les runners.

```exec
MSYS_NO_PATHCONV=1 docker run -d --name gitlab-runner --restart unless-stopped -v gitlab-runner-config:/etc/gitlab-runner -v /var/run/docker.sock:/var/run/docker.sock gitlab/gitlab-runner:v19.5.3
```

> 🔍 **Comprendre la commande**
>
> | Morceau | Rôle |
> |---|---|
> | `MSYS_NO_PATHCONV=1` | sous Git Bash, empêche la conversion des chemins `/var/run/…` en chemins Windows ; sans effet sous macOS et Linux |
> | `docker run -d` | démarre un conteneur en arrière-plan |
> | `--name gitlab-runner` | lui donne un nom, pour s'y adresser ensuite |
> | `--restart unless-stopped` | le relance après un redémarrage de Docker, sauf si vous l'avez arrêté vous-même |
> | `-v gitlab-runner-config:/etc/gitlab-runner` | range sa configuration dans le volume `gitlab-runner-config`, créé s'il n'existe pas |
> | `-v /var/run/docker.sock:/var/run/docker.sock` | donne au runner l'accès au Docker de votre poste, par son **socket**, le point d'entrée de Docker |
> | `gitlab/gitlab-runner:v19.5.3` | l'image officielle, à une version précise pour que le lab se rejoue à l'identique |

Au premier lancement, Docker télécharge l'image, avec des barres de progression, puis affiche une longue suite de chiffres et de lettres : l'identifiant du conteneur démarré.

Le socket Docker est un accès puissant : un programme qui l'utilise peut lancer n'importe quel conteneur sur votre poste. Ce runner n'exécutera que les jobs de **vos** projets, et vous l'arrêterez à la fin du lab.

Le runner tourne, mais il n'est relié à aucun GitLab : sa liste de runners enregistrés est vide.

```exec
docker exec gitlab-runner gitlab-runner list
```

> 🔍 **Comprendre la commande**
>
> | Morceau | Rôle |
> |---|---|
> | `docker exec gitlab-runner` | lance une commande dans le conteneur `gitlab-runner` déjà démarré |
> | `gitlab-runner list` | affiche les runners enregistrés dans sa configuration |

L'affichage tient en deux lignes : la version du runner, puis `Listing configured runners` avec le fichier de configuration, `/etc/gitlab-runner/config.toml`. Aucun runner n'est listé dessous.

```verify
docker version >/dev/null 2>&1 || { echo "Docker ne répond pas : démarrez Docker Desktop, ou le service Docker sous Linux."; exit 1; }
[ "$(docker inspect -f '{{.State.Running}}' gitlab-runner 2>/dev/null)" = true ] || { echo "Le conteneur gitlab-runner ne tourne pas. Relancez la commande docker run de la section 01.2 ; s'il existe déjà, docker start gitlab-runner le redémarre."; exit 1; }
docker inspect -f '{{range .Mounts}}{{.Name}} {{end}}' gitlab-runner | grep -q gitlab-runner-config || { echo "Le conteneur n'utilise pas le volume gitlab-runner-config. Supprimez-le avec docker rm -f gitlab-runner, puis relancez la commande de la section 01.2 en entier."; exit 1; }
MSYS_NO_PATHCONV=1 docker exec gitlab-runner test -S /var/run/docker.sock || { echo "Le conteneur n'a pas accès au socket Docker. Supprimez-le avec docker rm -f gitlab-runner, puis relancez la commande de la section 01.2 en entier."; exit 1; }
echo "Le runner tourne, avec sa configuration dans un volume et l'accès à Docker."
```
