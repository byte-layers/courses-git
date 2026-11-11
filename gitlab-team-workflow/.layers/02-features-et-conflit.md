---
title: "02 - Livrer deux features en parallèle"
description: "Chacun sa branche et sa merge request, puis le conflit"
---

Chaque personne développe sa user story en même temps que l'autre. Les deux modifient `src/log.txt`, donc la seconde merge request sera en conflit.

## 02.1 - Développer U1 et U2 en parallèle

Le poste A part de `develop` :

```exec
cd ~/byte-layers/git/gitlab-team/poste-a && git switch -c feature/1-u1 develop
cd ~/byte-layers/git/gitlab-team/poste-a && mkdir -p src && echo 'U1' > src/U1.txt && echo 'Hello world U1 !' > src/log.txt
cd ~/byte-layers/git/gitlab-team/poste-a && git add src && git commit -m "Ajoute U1" -m "Closes #1"
cd ~/byte-layers/git/gitlab-team/poste-a && git push -u origin feature/1-u1
```

Pendant ce temps, le poste B récupère `develop` depuis le serveur, et crée sa propre branche à partir du même point :

```exec
cd ~/byte-layers/git/gitlab-team/poste-b && git fetch && git switch -c feature/2-u2 origin/develop
cd ~/byte-layers/git/gitlab-team/poste-b && mkdir -p src && echo 'U2' > src/U2.txt && echo 'Hello from U2 !' > src/log.txt
cd ~/byte-layers/git/gitlab-team/poste-b && git add src && git commit -m "Ajoute U2" -m "Closes #2"
cd ~/byte-layers/git/gitlab-team/poste-b && git push -u origin feature/2-u2
```

## 02.2 - Ouvrir les deux merge requests et fusionner U1

Sur GitLab, ouvrez une merge request vers `develop` pour chacune des deux branches. Fusionnez celle de `feature/1-u1`. La seconde est alors bloquée par un conflit sur `src/log.txt`.

## 02.3 - Résoudre le conflit et fusionner U2

Sur le poste B, fusionnez `develop` dans la branche. Le conflit est attendu :

```exec
cd ~/byte-layers/git/gitlab-team/poste-b && git fetch
cd ~/byte-layers/git/gitlab-team/poste-b && git merge origin/develop
```

Ouvrez `~/byte-layers/git/gitlab-team/poste-b/src/log.txt` dans votre éditeur, et gardez les deux lignes, sans marqueur. Si vous n'y arrivez pas, cette commande écrit le résultat à votre place :

```exec
printf 'Hello world U1 !\nHello from U2 !\n' > ~/byte-layers/git/gitlab-team/poste-b/src/log.txt
```

Terminez la fusion, publiez, puis fusionnez la merge request sur GitLab :

```exec
cd ~/byte-layers/git/gitlab-team/poste-b && git add src/log.txt && git commit --no-edit && git push
```

```verify
C=$(cat ~/byte-layers/git/gitlab-team/url 2>/dev/null)
if [ -z "$C" ]; then
  echo "L'adresse du projet n'est pas enregistrée dans ~/byte-layers/git/gitlab-team/url."
  exit 1
fi
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
if ! curl -fsS "$A/repository/files/src%2Flog.txt/raw?ref=develop" 2>/dev/null | grep -q 'Hello from U2'; then
  echo "src/log.txt sur develop ne contient pas la ligne de U2."
  exit 1
fi
if ! curl -fsS "$A/repository/files/src%2Flog.txt/raw?ref=develop" 2>/dev/null | grep -q 'Hello world U1'; then
  echo "src/log.txt sur develop ne contient pas la ligne de U1."
  exit 1
fi
if [ "$(curl -fsS "$A/issues?state=closed" 2>/dev/null | grep -o '"type":"ISSUE"' | wc -l | tr -d ' ')" -lt 2 ]; then
  echo "Les deux issues devraient être fermées."
  exit 1
fi
echo "Les deux features sont sur develop, et les issues sont fermées."
```
