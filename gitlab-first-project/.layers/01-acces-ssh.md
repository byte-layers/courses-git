---
title: "01 - Se connecter à GitLab avec une clé SSH"
description: "Créer un compte, générer une paire de clés et la déclarer sur GitLab"
---

Pour envoyer du code sur GitLab, votre poste doit prouver qui vous êtes. Une **clé SSH** remplace le mot de passe pour les échanges avec GitLab.

## 01.1 - Créer votre compte

Si vous n'en avez pas encore, créez un compte sur [gitlab.com/users/sign_up](https://gitlab.com/users/sign_up), puis confirmez votre adresse.

## 01.2 - Générer une paire de clés

Une clé SSH est une paire de fichiers : la **clé privée** reste sur votre poste, et la **clé publique** se donne au serveur. Regardez d'abord si vous en avez déjà une :

```exec
ls ~/.ssh/id_ed25519.pub
```

Si ce fichier existe, gardez-le et passez à la section suivante. S'il n'existe pas, générez la paire avec votre adresse. La commande demande un emplacement, acceptez celui qui est proposé avec Entrée. Elle demande ensuite une phrase de passe, qui protège la clé. Si vous en mettez une, l'agent SSH peut la retenir pour la session, avec `ssh-add`. L'option `-t` choisit l'algorithme, et `-C` ajoute un commentaire :

```bash
ssh-keygen -t ed25519 -C "john.doe@example.com"
```

## 01.3 - Déclarer la clé publique sur GitLab

Affichez la clé publique, et copiez toute la ligne :

```exec
cat ~/.ssh/id_ed25519.pub
```

Sur GitLab, ouvrez votre avatar, puis **Edit profile**, puis **SSH Keys**, et cliquez sur **Add new key**. Collez la clé, donnez-lui un titre comme le nom de votre poste, et validez.

Testez la connexion. La première fois, SSH vous demande de confirmer l'empreinte du serveur, répondez `yes` :

```bash
ssh -T git@gitlab.com
```

GitLab répond par votre nom d'utilisateur :

```text
Welcome to GitLab, @johndoe!
```

> 💡 **Remarque : si SSH est bloqué sur votre réseau.** Clonez en HTTPS, avec un **jeton d'accès personnel** à la place du mot de passe. Il se crée dans **Edit profile**, **Access tokens**, avec les droits `read_repository` et `write_repository`.

> 📖 [Utiliser des clés SSH avec GitLab](https://docs.gitlab.com/user/ssh/) · [Jetons d'accès personnels](https://docs.gitlab.com/user/profile/personal_access_tokens/)

```acknowledge
Mon poste est connecté à GitLab
```
