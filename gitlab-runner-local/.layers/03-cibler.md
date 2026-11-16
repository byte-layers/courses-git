---
title: "03 - Envoyer les jobs sur son runner"
description: "Demander le tag local dans le pipeline, voir le job tourner sur son poste, puis couper les runners partagés"
---

Le runner est relié au projet, mais il ne prend que les jobs qui demandent son tag `local`. C'est le pipeline qui choisit le runner, avec le mot-clé `tags:`. Dans cette étape, vous écrivez ce choix, vous constatez que le job tourne sur votre poste, puis vous coupez les runners partagés du projet.

## 03.1 - Demander le tag local

Le pipeline de départ contient un seul job, `qui-execute`, qui affiche le nom du runner, ses tags et l'architecture de la machine. Écrivez-le, puis complétez le `# TODO` dans votre éditeur. Ne relancez pas cette commande une fois le fichier complété : elle l'écraserait.

```exec
cat > ~/byte-layers/git/runner-local/projet/.gitlab-ci.yml <<'FIN'
default:
  image: alpine:3.22
  # TODO : envoyez tous les jobs sur un runner qui porte le tag local

qui-execute:
  script:
    - echo "Runner = $CI_RUNNER_DESCRIPTION"
    - echo "Tags du runner = $CI_RUNNER_TAGS"
    - uname -m
FIN
```

> 🔍 **Comprendre la commande**
>
> | Morceau | Rôle |
> |---|---|
> | `cat > … <<'FIN'` … `FIN` | écrit les lignes comprises entre les deux `FIN` dans `.gitlab-ci.yml` ; les apostrophes autour du premier `FIN` laissent les `$CI_…` tels quels, pour que GitLab les remplace au moment du job |
> | `default:` | les réglages appliqués à tous les jobs du pipeline |
> | `$CI_RUNNER_DESCRIPTION`, `$CI_RUNNER_TAGS` | des variables que GitLab fournit à chaque job : la description et les tags du runner qui l'exécute |
> | `echo "Runner = …"` | le signe `=` remplace les deux-points : dans une ligne YAML, un deux-points suivi d'une espace serait lu comme une clé, et GitLab refuserait le pipeline |
> | `uname -m` | affiche l'architecture de la machine : souvent `aarch64` sur un Mac récent, `x86_64` sur un PC et sur les runners partagés |

**Critère :** tous les jobs du pipeline, présents et futurs, demandent le tag `local`, et seulement lui, sans le répéter dans chaque job.

```hint
Le bit sur les runners montre le mot-clé `tags:` dans un job. Ici, il va dans le bloc `default:`, sous `image:`, avec la même indentation : deux espaces.
```

```hint
`tags:` attend une liste, même pour un seul tag : un tiret, une espace, puis le nom du tag, sur la ligne suivante et indenté de deux espaces de plus.
```

````solution
```yaml
default:
  image: alpine:3.22
  tags:
    - local

qui-execute:
  script:
    - echo "Runner = $CI_RUNNER_DESCRIPTION"
    - echo "Tags du runner = $CI_RUNNER_TAGS"
    - uname -m
```
````

```verify
F=~/byte-layers/git/runner-local/projet/.gitlab-ci.yml
[ -f "$F" ] || { echo "Le fichier $F n'existe pas : lancez la commande de la section 03.1."; exit 1; }
grep -q 'TODO' "$F" && { echo "Le fichier contient encore la ligne # TODO : remplacez-la par votre réponse."; exit 1; }
awk '/^default:/{d=1;next} /^[^ #]/{d=0} d&&/^  tags: *\[ *["\047]?local["\047]? *\] *(#.*)?$/{ok=1;n=1} d&&/^  tags: *(#.*)?$/{t=1;next} t&&/^    - /{n++; if($0 ~ /^    - *["\047]?local["\047]? *(#.*)?$/) ok=1; next} t{t=0} END{exit !(ok && n==1)}' "$F" || { echo "Le bloc default: ne demande pas le seul tag local. Il faut une ligne tags: indentée de deux espaces sous default:, puis - local indentée de quatre espaces, sans autre tag : un job qui demande deux tags attend un runner qui les porte tous les deux."; exit 1; }
echo "Tous les jobs demandent le tag local."
```

## 03.2 - Publier et regarder le job

Publiez le pipeline :

```exec
cd ~/byte-layers/git/runner-local/projet && git add .gitlab-ci.yml && git commit -m "Envoie les jobs sur le runner local" && git push
```

Sur GitLab, ouvrez **Build**, **Pipelines**, puis le job `qui-execute`. Sa trace, le journal de son exécution, commence par `Running with gitlab-runner 19.5.3`, la version de votre runner, puis `Using Docker executor with image alpine:3.22`. Plus bas, les commandes du job affichent :

```text
Runner = mon poste
Tags du runner = ["local"]
aarch64
```

La dernière ligne dépend de votre machine. Le job a tourné dans un conteneur neuf, créé sur votre poste pour lui et supprimé à la fin : il dure quelques secondes, trop peu pour le voir passer dans `docker ps`.

```verify
C=$(cat ~/byte-layers/git/runner-local/url 2>/dev/null)
[ -n "$C" ] || { echo "L'adresse du projet n'est pas enregistrée dans ~/byte-layers/git/runner-local/url : lancez la commande de la section 01.1."; exit 1; }
case "$C" in
  git@*) H="https://$(echo "$C" | sed -E 's#git@([^:]+):.*#\1#')"; P=$(echo "$C" | sed -E 's#git@[^:]+:##') ;;
  *) H=$(echo "$C" | sed -E 's#^(https?://)([^/@]*@)?([^/]+)/.*#\1\3#'); P=$(echo "$C" | sed -E 's#^https?://[^/]+/##') ;;
esac
P=$(echo "$P" | sed -E 's#\.git$##; s#/#%2F#g')
A="$H/api/v4/projects/$P"
B=$(curl -fsS "$A" 2>/dev/null | sed -n 's/.*"default_branch":"\([^"]*\)".*/\1/p'); B=${B:-main}
I=$(curl -fsS "$A/pipelines?ref=$B&per_page=1" 2>/dev/null | sed -n 's/^\[{"id":\([0-9]*\).*/\1/p')
[ -n "$I" ] || { echo "Aucun pipeline sur la branche $B : vérifiez que le git push de la section 03.2 a réussi."; exit 1; }
S=$(curl -fsS "$A/pipelines/$I" 2>/dev/null | sed -n 's/.*"status":"\([a-z_]*\)".*/\1/p' | head -1)
case "$S" in
  success) ;;
  pending|created) echo "Le pipeline attend un runner. Vérifiez que le conteneur tourne (docker ps) et que le runner a un point vert dans Settings, CI/CD, Runners."; exit 1 ;;
  running|preparing|waiting_for_resource|scheduled) echo "Le pipeline est encore en cours : attendez quelques secondes, puis vérifiez de nouveau."; exit 1 ;;
  *) echo "Le dernier pipeline de $B est dans l'état $S : ouvrez la trace du job sur GitLab pour lire l'erreur."; exit 1 ;;
esac
J=$(curl -fsS "$A/pipelines/$I/jobs" 2>/dev/null)
echo "$J" | grep -q '"runner_type":"instance_type"' && { echo "Un job du dernier pipeline a tourné sur un runner partagé de GitLab : le tag local n'était pas demandé."; exit 1; }
echo "$J" | grep -q '"runner_type":"project_type"' || { echo "GitLab n'indique pas votre runner de projet pour ce pipeline. Relancez le pipeline depuis Build, Pipelines, puis vérifiez de nouveau."; exit 1; }
echo "Le pipeline a réussi, et son job a tourné sur votre runner de projet."
```

## 03.3 - Couper les runners partagés

Les jobs qui demandent `local` vont déjà sur votre runner. Mais un job sans tag, ajouté plus tard par vous ou par un collègue, partirait encore sur un runner partagé et consommerait des minutes. Pour que **rien** de ce projet ne tourne chez GitLab, on coupe les runners partagés du projet.

Dans **Settings**, **CI/CD**, **Runners**, ouvrez l'onglet **Instance**, puis désactivez l'interrupteur **Turn on instance runners for this project**.

Un job sans tag n'aura désormais plus de runner : il restera en attente, et GitLab affichera un message du type *This job is stuck…*, qui dit qu'aucun runner disponible ne peut le prendre. C'est le comportement voulu : on le corrige en lui ajoutant le tag, ou en cochant *Run untagged jobs* sur votre runner.

> 💡 **Qui choisit quoi.** C'est le fichier du pipeline qui choisit le runner, par ses tags. Le réglage du projet décide seulement s'il reste une solution de repli chez GitLab pour les jobs sans tag.

```acknowledge
J'ai désactivé les runners partagés du projet.
```
