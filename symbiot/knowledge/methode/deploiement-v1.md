---
type: Méthode
title: Méthode de déploiement de la stack V1 et équipe d'agents
description: Conversion OKF du document de travail 05-methode-deploiement-v1.md du dossier docs/symbiot (cycle des 15 et 16 octobre 2026).
tags:
  - serveur
  - poste
  - k3s
  - okf
  - gouvernance
sources:
  - resource: /deprecated/2026-10-15/05-methode-deploiement-v1.md
generated:
  by: claude-fable-5.1/session-01MK6
  at: 2026-10-16T18:00:00+02:00
status: stable
stale_after: 2027-01-16T00:00:00+02:00
---

# Méthode de déploiement de la stack V1 et équipe d'agents

**Statut d'origine :** version de travail du 2026-10-16, rédigée après validation du plan court ([05-plan-methode-deploiement-v1.md](/references/plan-methode-deploiement-v1.md)) et des décisions D1 à D11
**Sources :** le dossier `docs/symbiot/` en entier ; ce document renvoie, il ne restate pas
**Deux vérifications de code faites pour ce document :** Cognee pointe un S3 compatible par configuration (`cognee/infrastructure/files/storage/S3FileStorage.py`, `.env.template:135-147` : `STORAGE_BACKEND=s3`, `DATA_ROOT_DIRECTORY=s3://…`) ; Centaur place les fichiers de travail des sandboxes sur des volumes persistants Kubernetes (`contrib/chart/values.yaml:377-380`, CRD Agent Sandbox), sans stockage objet dans `services/api-rs/crates`

---

## Partie A — La stack V1, qui fait quoi

### A.1 Trois couches

```
POSTE                      SERVEUR (k3s, une machine d'évaluation)              CONNAISSANCE
client Symbiot (D3)        Harbor ─ Spaces, blobs → SeaweedFS                   bundle OKF `symbiot/knowledge`
  second cerveau Markdown  Cognee ─ mémoire + RAG, FalkorDB + PostgreSQL        bundles de documentation
  mini-apps, tâches de fond  └ MCP OKF, convertisseur, post-traitement (V2)      fournis par toi, un par brique
  DSH local (sandbox OS)   Agent Stack ─ registre A2A, proxy LLM, agents de service   ontologie Cognee (OWL)
  routeur local            Centaur ─ sessions en sandbox (CRD), workflows durables
                           Keycloak ─ identité  │ OpenBao ─ secrets │ SeaweedFS ─ fichiers
                           GPU A5000 publié au cluster (Ollama / vLLM)
```

### A.2 Fiches de rôle des briques core

Chaque fiche renvoie à l'analyse qui la fonde. Le quintuplet de tenance (D3) est : rôle et schéma PostgreSQL · graphe FalkorDB · bucket SeaweedFS · client Keycloak · namespace k3s.

| Brique | Responsabilité unique | Expose | Consomme | Tenance | Degré (B.3) | Statut réel | Analyse |
|---|---|---|---|---|---|---|---|
| **Client Symbiot** (Rowboat forké) | poste : second cerveau, productions, assistant local, projection vers les Spaces | — (client) | Harbor REST, WS, MCP ; MCP Cognee et OKF ; proxy LLM ; A2A des agents de service | client Keycloak public | D3 + D1 + D4a | bêta UX et bêta refactoring existantes | [fiche Rowboat](/evaluations/rowboat.md) |
| **Harbor** | orgs, spaces, membres humains et agents, journal append-only canonique (D11), blobs | REST `/v1`, WS `/v1/live`, MCP `/mcp` (38 outils), contrat d'agent `rbk_` | Keycloak par `AUTH_ISSUER` ; SeaweedFS par `BLOBS_S3_*` ; API de politique (V1 incr. 5) | schéma `harbor` · — · bucket `harbor-blobs` · client · ns `harbor` | D2 | à déployer sur k3s, qualification M3 | [annexe A §1](/interfaces/interfaces-serveur.md), [fiche Rowboat A3, A8, A9](/evaluations/rowboat.md) |
| **Cognee** | point d'unification RAG et mémoire, ontologie maintenue, middleware de peuplement de FalkorDB (D1) | MCP `remember / recall / search / forget`, REST `/api/v1`, ontologies OWL | PostgreSQL, FalkorDB, SeaweedFS (`STORAGE_BACKEND=s3`), Keycloak via provisionnement | schéma `cognee` · graphes par dataset · bucket `cognee-data` · client · ns `cognee` | D2 (adaptateur communautaire) | **installé et réglé par toi** ; convention de tenance à consigner (D8) | [annexe A §3](/interfaces/interfaces-serveur.md) |
| **Agent Stack** | registre et hébergement des agents de service en A2A, proxy LLM autorité de routage et de quota (D9), connecteurs MCP OAuth par utilisateur | A2A `/api/v1/a2a/{id}`, REST `/api/v1`, proxy OpenAI | PostgreSQL (dont procrastinate et Keycloak), SeaweedFS (natif), FalkorDB via Cognee pour les vecteurs (D1), Keycloak `externalOidcProvider` | schéma `agentstack` · via Cognee · bucket `agentstack-files` · clients server, ui, cli · ns `agentstack` | D0 chart + D2 patchs (`sub`, sans Redis, `connectors.auth` chiffré) | à qualifier M3 | [fiche Agent Stack](/evaluations/agentstack.md) |
| **Centaur** | sessions d'agents en sandbox par fil, workflows durables, courtier de credentials (D6) | API de session HTTP + SSE, MCP console, webhooks | PostgreSQL, CRD Agent Sandbox, volumes persistants (voir A.5), Keycloak JWT (patch), OpenBao via iron-proxy (D5) | schéma `centaur` · — · PVC · client · ns `centaur` | D0 chart + D2 patchs (JWT Keycloak, source de secrets, adaptateur DSH) | à qualifier M3 | [annexe A §2](/interfaces/interfaces-serveur.md) |
| **DSH** | harness d'exécution des agents : journal rejouable, profils et bundles, sandbox OS, ACP | ACP stdio, SDK JSON-RPC | MCP Cognee et OKF (overlays `mcp-client`), OpenBao via `CredentialProvider` (D5), API de politique via plugin `tools/pre-execute` (D7) | pod dans une sandbox Centaur · — · — · — · ns `centaur` | D1 (plugins) + D0 (image épinglée) | à qualifier M3 ; developer preview, version épinglée (D11) | [annexe B](/evaluations/dsh-seams.md) |
| **BeeAI Framework** | bibliothèque pour écrire les agents de service : outils, MCP client, serve A2A et MCP, RequirementAgent | serve A2A derrière le proxy Keycloak, serve MCP | MCP Cognee, API de politique (middleware), proxy LLM | selon l'agent hébergé par Agent Stack | D1 (sous-classes) | à qualifier M3 | [fiche BeeAI](/evaluations/beeai-framework.md) |
| **Keycloak** | identité unique, `sub` partout (D4) | OIDC, JWKS | PostgreSQL (schéma propre) | schéma `keycloak` · — · — · — · ns `identity` | D0 | à déployer | — |
| **OpenBao** | source unique des secrets (D5) | API KV, auth Kubernetes | — | ns `identity` | D0 | à déployer | — |
| **SeaweedFS** | fichiers et blobs, API S3 | S3 | — | ns `storage` | D0 | **installé par toi** | — |
| **PostgreSQL, FalkorDB** | relationnel ; vecteurs et graphe | SQL ; Cypher et vecteurs | — | ns `storage` | D0 | **installés par toi** | — |
| **Proxy LLM** | c'est celui d'Agent Stack (D9) ; GPU publié par le plugin NVIDIA | OpenAI compatible | Ollama ou vLLM dans le cluster, API cloud | ns `agentstack` | D0 | — | [fiche Agent Stack A7](/evaluations/agentstack.md) |
| **API de politique et console des spaces** | gouvernance unique (D7), C15 | REST, consultée par toutes les briques | PostgreSQL, Keycloak, Harbor (source des spaces) | schéma `console` · — · — · client · ns `console` | nôtre (D4a sur l'UX MemoryBear, D5 sur son modèle) | à écrire, incrément 5 | [fiche MemoryBear §4](/evaluations/memorybear.md), [comparatif §8.7](/evaluations/comparatif.md) |
| **MCP OKF, convertisseur Brain ↔ OKF** | accès outil à la connaissance curatée ; aller-retour second cerveau ↔ serveur | MCP | bundle, Cognee | ns `knowledge` | nôtre | MCP OKF existant chez toi ; convertisseur à écrire, incrément 2 | [fiche Rowboat A5](/evaluations/rowboat.md) |

### A.3 Table des flux, les cinq intégrations

| Flux | De → vers | Appels (annexe A) | Authentification de chaque saut |
|---|---|---|---|
| I1 second cerveau local | client → disque | fichiers Markdown, git local | — |
| I2 optimisation par le serveur | client → MCP Cognee `remember` (bundle OKF) → Cognee → FalkorDB ; retour `recall` ou bundle réécrit | MCP streamable-http | Bearer Keycloak du membre ; reverse proxy devant le MCP Cognee qui vérifie le JWT (risque relevé, annexe A §3) |
| I3 productions partagées | client → Harbor `PUT /blobs` puis `create_asset` ou `propose_change` ; `@rowboat` → session locale → `post_message` | REST, WS, MCP | Bearer Keycloak ; clé `rbk_` pour les agents |
| I4 messagerie inter-espaces | Harbor connecteur → Centaur `POST /api/session/{thread_key}` → `execute` → SSE → `post_message` | HTTP + SSE | clé d'ingress dédiée au connecteur, puis JWT Keycloak après patch D4 |
| I5 mémoire et RAG d'entreprise | client, DSH, BeeAI, Agent Stack → MCP Cognee et MCP OKF | MCP | Bearer Keycloak ; chez Agent Stack, connecteur OAuth par utilisateur |
| agents de service | client, Harbor connecteur → Agent Stack proxy A2A → agent BeeAI | A2A JSON-RPC | Bearer Keycloak ; jeton de contexte RS256 pour l'agent |
| exécution en sandbox | Centaur → CRD Agent Sandbox → pod DSH ou Hermes | ACP ou adaptateur harness | iron-proxy injecte les credentials depuis OpenBao |

### A.4 Ce que V1 ne fait pas

Post-traitement de Cognee, workflows no-code serveur, gouvernance par tags de risque, Agent Cards générées depuis des bundles, services in-house (IMAP, CalDAV, WebDAV). Tout est en [partie E](#partie-e--v2-laugmentation-par-les-inspirants).

### A.5 Deux points issus des vérifications

- **Cognee → SeaweedFS** : conforme par configuration, à inscrire dans la convention de tenance.
- **Centaur → volumes persistants** : les fichiers de travail des sandboxes vivent sur des PVC. Pour rester sur SeaweedFS, qualifier le pilote CSI de SeaweedFS comme StorageClass du cluster ; sinon StorageClass locale, consignée comme exception temporaire avec `stale_after`.

---

## Partie B — Le dépôt `symbiot` et le bundle de connaissance

### B.1 Arborescence

```
symbiot/                          dépôt privé
  knowledge/                      bundle OKF 0.2, un concept par fichier
    index.md  log.md
    composants/  interfaces/  appels/  decisions/  chantiers/  conventions/
    evaluations/ scenarios/ inventaire/ provenance/
    documentation/<brique>/       bundles OKF de documentation fournis par toi, un par brique,
                                  conservés tels quels avec leur index.md ; nos concepts y renvoient
    references/                   matériel externe cité (OKF §6.3)
    vues/                         index générés : par tag, statut, composant, incrément, date, provenance
  stack/
    cluster/                      amorçage k3s, namespaces, NetworkPolicy, StorageClass, GPU
    charts/                       un chart ou kustomization par brique core
    forks/                        sous-modules épinglés, branche symbiot/storage : harbor, agentstack,
                                  centaur, cognee, dsh, beeai, symbiot-client
    services/                     ce que nous écrivons : api-politique, console, mcp-okf, convertisseur-okf,
                                  consolidation (V2), workflows (V2)
    runbooks/                     un fichier par action `symbiot <action>`, avec son retour arrière
    env/                          valeurs par environnement, sans aucun secret
  rigs/
    shared/                       prompts de rôle, règles du gardien de stack
    increment-0/ … increment-5/   rig.yaml et prompts spécifiques
  deprecated/                     documents de travail datés après conversion, avec index des finaux
```

Le client Symbiot reste dans son dépôt et entre en sous-module. Les bundles de documentation que tu fournis sont des bundles imbriqués : on ne les édite pas, on les cite par lien bundle-absolu (`/documentation/harbor/...`) et on les met à jour en bloc, avec `generated.at` du bundle.

### B.2 Gabarits par type et règles de confiance

Champs OKF utilisés partout : `type`, `title`, `description`, `tags`, `resource`, `sources`, `generated`, `verified`, `status`, `stale_after`. Règles :
- `generated.by` : `human:<id>`, `process:<runbook>`, ou `<agent>/<version>` pour un siège OpenRig.
- Un concept écrit par un agent naît `status: draft` et sans `verified` ; il passe `stable` à ton `verified: human:…`.
- `stale_after` obligatoire sur inventaire, provenance, évaluations et sur tout concept qui cite une version amont ; un trimestre par défaut.
- Rien ne s'édite rétroactivement : un nouvel arbitrage crée un concept `stable` et passe l'ancien en `deprecated` avec un lien « remplacé par ».

| Type | Champs propres (clés d'extension, préservées par OKF) | Exemple à produire en M1 |
|---|---|---|
| Composant | `role`, `expose`, `consomme`, `tenance` (quintuplet), `degre`, `version_epinglee`, `statut_reel` | `composants/harbor.md` depuis A.2 |
| Interface | `protocole`, `auth`, `contrat` (lien vers le fichier de schéma), `evenements_emis` | `interfaces/harbor-mcp.md` depuis l'annexe A |
| Appel | `besoin` (lien scénario), `service_client`, `interface`, `fonction_servie` (fichier:ligne), `test_fil` | `appels/propose-change.md` |
| Décision | `impacte` (liste de concepts), `remplace` | `decisions/D4-identite.md` depuis le plan court §0 |
| Chantier | `decision`, `incrément`, `depend_de`, `effort`, `scenario` | `chantiers/19-console-spaces.md` depuis le comparatif §5 et §8.5 |
| Convention | `s_applique_a` | `conventions/tenance.md`, `derivation.md`, `taxonomie.md`, `postgresql.md` |
| Scénario | `incrément`, `pas` (liste d'appels), `critere_de_fini` | `scenarios/journee-increment-2.md` (annexe D) |
| Provenance | voir B.4 | `provenance/consolidation.md` |
| Inventaire | `machine`, `installé`, `versions`, `mesures` | `inventaire/machine-evaluation.md` |
| Évaluation | `grille`, `notes`, `total` | les fiches converties |

La **taxonomie des tags** (`conventions/taxonomie.md`) est un vocabulaire fermé : poste, serveur, connaissance, identité, secrets, mémoire, rag, okf, mcp, a2a, acp, sandbox, k3s, routage, stockage, tenance, gouvernance, workflows, inspirant, core. Toute extension passe par une PR sur ce fichier.

**Alignement avec l'ontologie Cognee (D8)** : chaque `type` OKF correspond à une classe de l'ontologie OWL maintenue dans Cognee, dans un fichier de correspondance `conventions/okf-ontologie.md` ; le bundle est ingéré par `remember` avec `ontology_key` de cette ontologie, de sorte que `recall` navigue les mêmes classes que les répertoires.

### B.3 L'échelle de dérivation (convention `derivation.md`)

| Degré | Relation à l'amont | Où | Licence | Maintenance |
|---|---|---|---|---|
| D0 utilisé tel quel | image, chart, bibliothèque | `stack/charts/`, `resource` = digest | celle de l'amont, isolation par réseau pour le copyleft | montée de version |
| D1 étendu sans fork | plugin, sous-classe, overlay, connecteur hors dépôt amont | `stack/services/`, paquets `@symbiot/*` | la nôtre | suit l'API amont |
| D2 fork mince | adaptateur derrière une interface, un commit par patch, contribuable | `stack/forks/<x>`, branche `symbiot/storage` | celle de l'amont | rebase sur tag amont, trimestriel |
| D3 fork profond | notre produit ; nos paquets `@symbiot/*` séparés ; `UPSTREAM.md` des zones synchronisées et gelées | sous-module propre | amont pour l'amont, nôtre pour `@symbiot/*` | cherry-pick, point de non-retour déclaré ; réduction tardive et tracée, jamais initiale |
| D4a réimplémentation dérivée | logique reprise d'un amont permissif, fragments autorisés avec en-tête et notices | `stack/services/` | Apache, MIT | aucune ; amont surveillé par `stale_after` |
| D4b clean-room | logique reprise d'un amont copyleft, à partir d'une spécification, aucun fragment | `stack/services/` | AGPL incompatible ; la spec est la frontière | aucune |
| D5 principe seul | idée notée, aucune lecture de code pour implémenter | `knowledge/` | — | — |

Une brique se classe par partie, pas en bloc : Agent Stack = D0 chart + D2 patchs + D1 connecteurs ; client Symbiot = D3 + D1 skills + D4a permissions d'Eigent ; MemoryBear = D5 console + D4a consolidation, rien d'autre. Core = D0 à D3 ; inspirants = D4 et D5 (D10).

### B.4 Tranches verticales et provenance

**Règle par degré.** D0 et D2 : on importe tout, la verticalité s'obtient par configuration, jamais par suppression. D4 et nos services : on part du bas, le core qualifié, et on greffe des tranches. D3 : fork entier, ajouts isolés, verticales amont désactivées par flags, suppression seulement quand une verticale est déclarée gelée, dans une PR de retrait consignée.

**Extraction par tranche**, en six pas : définir la tranche par un besoin (scénario ou appel OKF) ; trouver les points d'entrée amont ; calculer la fermeture de dépendances (`grimp` ou `pydeps` en Python, `dependency-cruiser` en TypeScript) par le runbook `symbiot slice <dépôt> <point d'entrée>` ; lire le verdict (confinée : importer ; traverse l'infrastructure amont : couper et écrire un adaptateur ; moitié du dépôt : ce n'est pas une tranche, revenir à D2, D3 ou D4b) ; importer avec les tests et l'en-tête `Derived from <dépôt>@<commit>:<chemin> (licence)` ; brancher au bas (FalkorDB via Cognee, CronJob k3s, OpenBao, `sub` Keycloak).

**Concept `Provenance`**, un par brique ou par tranche : `degres` (liste de parties avec degré), `amont` (dépôt, commit, licence), `patchs`, `fragments` (origine fichier:ligne → destination), `fermeture` (fichiers, frontières traversées), `decision` (importer, couper, renoncer), `adaptateurs`, `tests_importes`, `zones_gelees` (D3).

**Lint OKF en CI** (`symbiot lint`), refuse une PR si : frontmatter invalide ; lien non résolu ; lien vers un concept `deprecated` sans note ; `stale_after` dépassé sans revalidation ; `generated.at` postérieur au dernier `verified` sur un concept `stable` ; fichier à en-tête de dérivation absent d'une provenance, ou l'inverse ; service D4b avec une `sources` vers le code d'un dépôt copyleft ; fork D2 dont le tag amont a plus d'un trimestre ; brique sans degré déclaré. Validateur : la crate `okf` 0.2 pour la conformité, un script maison pour les règles de projet.

**Clean-room D4b** : deux sièges OpenRig, un rédacteur de spécification qui lit l'amont et n'écrit que le concept, un implémenteur sans accès à l'amont qui n'écrit que depuis la spec.

---

## Partie C — Les six mouvements

| Mouvement | Entrée | Sortie | Agents | Vérifié par |
|---|---|---|---|---|
| **M1 Formaliser** | `docs/symbiot/` | bundle `knowledge/` : composants, interfaces, appels initiaux, décisions, chantiers, conventions, évaluations converties ; originaux dans `deprecated/2026-10-15/` avec index des finaux | cartographe, scribe | toi : `verified` sur chaque décision et convention |
| **M2 Relever l'existant** | la machine d'évaluation, Cognee réglé, bêta UX, bêta client | `inventaire/` avec `generated: process:inventaire`, versions, mesures du pipeline Cognee, convention de tenance Cognee consignée (D8) | opérateur, cartographe ; scripts en lecture seule | toi |
| **M2 bis Carte des appels** | scénarios I1 à I5, contrats des briques (zod Harbor, OpenAPI Agent Stack et Cognee, `routes.rs` Centaur, catalogue DSH), bundles de documentation fournis | `appels/` : chaîne besoin → service client → appel → fonction servie → test au fil ; passe montante des événements émis | un extracteur par brique, un assembleur, un vérificateur | arrêt à la frontière d'interface ; toi sur les appels retenus |
| **M3 Qualifier par fork** | une brique, son degré, son quintuplet | branche `symbiot/storage`, adaptateurs, chart, suite amont verte sur stores forkés, tranche d'acceptation verte, décision go ou no-go en concept | intégrateur par adaptateur, vérificateur, gardien de stack | ordre : Harbor et client, DSH et BeeAI, Agent Stack, Centaur ; Cognee déjà fait |
| **M4 Dépôt et outils unifiés** | — | `symbiot-infra` sous la commande unique `symbiot` (mise ou just) ; conventions Rowboat (pourquoi + date + PR, un fait par document, doc dans la même PR) ; règle « les agents n'agissent que par runbook » | opérateur | revue de PR |
| **M5 Équipe OpenRig** | un incrément | un `rig.yaml`, prompts de rôle, permissions par rôle, contexte chargé par MCP OKF et Cognee | — | — |
| **M6 Incréments vérifiés** | un incrément qualifié | scénario d'acceptation exécuté, démonstration sur la machine, bundle mis à jour et vérifié, `log.md` tenu, sauvegardes avant et retour arrière connu | tous | toi, revue hebdomadaire |

**Rôles OpenRig (M5)**, séparés par siège :
- **opérateur** (lead) : lit le bundle avant toute action, découpe, ne code pas, ne touche pas au serveur.
- **cartographe** : tient le bundle, la provenance, les `stale_after` ; seul à écrire dans `knowledge/`.
- **intégrateur** (un par chantier ou adaptateur) : code et configuration dans une branche, PR ; permissions `workspace-write` sur sa branche.
- **vérificateur** : exécute suites et scénarios, jamais le siège de l'intégrateur ; lecture seule plus exécution des runbooks de test.
- **gardien de stack** : refuse tout store hors PostgreSQL et FalkorDB, toute exécution hors k3s, toute identité hors `sub` Keycloak, tout secret hors OpenBao, tout degré ou licence non déclaré, toute `sources` copyleft dans un D4b.
- **scribe** : `log.md`, vues, note de modifications par cycle.

Sièges Claude Code ou Codex en V1 ; DSH dès que son plugin de politique existe (chantier 13). Aucun siège n'a `danger-full-access` sur le serveur ; les actions serveur passent par `symbiot <runbook>` sous l'identité du siège, journalisées.

---

## Partie D — Plan V1 par incréments

Chaque incrément : chantiers couverts (numéros du [comparatif §5 et §8.5](/evaluations/comparatif.md)), scénario d'acceptation, rig, risques. Définition de fini en trois points (M6).

### Incrément 0 — Identité et tenance (D3, D4, D8)
- **Chantiers** : 1 (Keycloak), nouveau 0a « tenance ».
- **Fait** : realm unique, clients par brique ; rôles et schémas PostgreSQL ; graphes FalkorDB nommés ; buckets ; namespaces et NetworkPolicy ; convention `tenance.md` et `postgresql.md` consignées ; convention Cognee relevée depuis ton installation.
- **Scénario** : un utilisateur créé dans Keycloak obtient son `sub` ; chaque schéma n'est lisible que par son rôle ; un `kubectl` hors namespace est refusé.
- **Risques** : versions majeures PostgreSQL à concilier ; isolation par base de Cognee à documenter.

### Incrément 1 — Socle client (chantiers 0, 1, 7, 8)
- Nettoyage cloud et télémétrie opt-in, secrets du poste par `safeStorage`, Keycloak avec `client_id` statique ou DCR autorisée, routeur local limité au mode local ou hors ligne (D9), levée d'une instance par fournisseur, SeaweedFS par `BLOBS_S3_*`.
- **Scénario** : installation du client sur un poste vierge, connexion Keycloak, création d'une org Harbor et d'un space, dépôt d'un fichier, sans qu'aucun appel ne sorte vers un domaine éditeur.

### Incrément 2 — Cœur de valeur (chantiers 2, 3)
- Cognee en outils natifs du client (modèle `domains/spaces.ts`), amendement du prompt, double écriture de `save-to-memory` ; convertisseur Brain ↔ OKF ; commande « soumettre au serveur » et réintégration.
- **Scénario** : [annexe D](#annexe-d--scénario-dacceptation-de-lincrément-2).

### Incrément 3 — Socle serveur qualifié (chantiers 12, 14, et qualification M3)
- Harbor sur k3s ; Agent Stack forké (`sub`, sans Redis, `connectors.auth` chiffré, vecteurs via Cognee) ; Centaur avec validation JWT Keycloak, source de secrets OpenBao pour iron-proxy, StorageClass pour les PVC ; OpenBao déployé, courtier unique ; MCP Cognee derrière le reverse proxy Keycloak.
- **Scénario** : les suites amont vertes sur les stores forkés ; un agent de service A2A répond à un appel authentifié par Keycloak ; une session Centaur démarre une sandbox et y injecte un credential sans l'exposer.

### Incrément 4 — Harness et agents (chantiers 15, 16, 17)
- DSH épinglé en pod dans une sandbox Centaur, adaptateur DSH ou ACP dans `harness-server` ; overlays MCP Cognee et OKF ; BeeAI pour les agents de service, serve A2A derrière Keycloak, `io_confirm` → `input_required` ; connecteurs Harbor vers Agent Stack et Centaur ; Agent Cards en concepts OKF.
- **Scénario** : une mention dans un space invoque un agent BeeAI hébergé par Agent Stack, qui rappelle la mémoire par Cognee, demande une approbation, répond dans le fil ; un second agent, DSH en sandbox Centaur, exécute une tâche de code et dépose son résultat en blob.

### Incrément 5 — Gouvernance (chantiers 13, 18, 19)
- Console des spaces (UX reprise, back-office neuf sur PostgreSQL et Keycloak, espaces alignés sur Harbor, table espace ↔ capacité) ; API de politique consultée par Harbor, DSH, BeeAI, Agent Stack, Cognee ; proxy LLM d'Agent Stack autorité de routage et de quota, GPU publié.
- **Scénario** : un administrateur retire un modèle d'un space ; dans la minute, le client, DSH et un agent BeeAI se voient refuser ce modèle, et l'audit le montre.

### Après V1
Revue de V1 : scénarios rejoués bout à bout, bundle entièrement `verified`, décisions D1 à D11 confirmées ou amendées, puis V2.

---

## Partie E — V2, l'augmentation par les inspirants

| Augmentation | Inspirant | Degré | Brique hôte | Chantier |
|---|---|---|---|---|
| Post-traitement de Cognee : ancrage bitemporel, réflexion, insights, oubli audité | MemoryBear | D4a par tranches (B.4) | `stack/services/consolidation`, derrière Cognee sur FalkorDB, CronJob k3s | 20 |
| Gouvernance avancée : règles par outil et arguments, tags de risque, interactions typées | Eigent | D4a | API de politique ; plugin DSH ; middleware BeeAI | 13 étendu |
| Workflows no-code serveur | Synapse AI | D0 isolé (service AGPL séparé, v1 mono-processus) puis D4b clean-room en TypeScript dans les tâches de fond du client | client Symbiot, `stack/services/workflows` | 21 |
| Contrat client ↔ runtime de mémoire | ElephantBroker | D5 | MCP Cognee et OKF | — |
| Agent Cards générées depuis des bundles ; services in-house par MCP | — | nôtre | Agent Stack ; MCP IMAP, CalDAV, WebDAV | 16, 10 |

---

## Annexe C — Rig OpenRig de l'incrément 0

```yaml
# rigs/increment-0/rig.yaml — à valider contre la spec de rig d'OpenRig (docs/reference/rig-spec.md)
name: symbiot-increment-0
description: Identité et tenance : Keycloak, rôles et schémas PostgreSQL, graphes FalkorDB, buckets, namespaces.
context:
  bundle: knowledge/            # chargé par le MCP OKF ; recall Cognee sur le dataset symbiot-stack
  read_first:
    - knowledge/decisions/D3-tenance.md
    - knowledge/decisions/D4-identite.md
    - knowledge/conventions/tenance.md
    - knowledge/inventaire/machine-evaluation.md
seats:
  - name: operateur
    harness: claude-code
    prompt: rigs/shared/roles/operateur.md
    permissions: read-only
  - name: cartographe
    harness: claude-code
    prompt: rigs/shared/roles/cartographe.md
    permissions: workspace-write
    scope: [knowledge/]
  - name: integrateur-identite
    harness: codex
    prompt: rigs/increment-0/prompts/integrateur-identite.md   # Keycloak realm, clients, mappers
    permissions: workspace-write
    scope: [stack/charts/keycloak, stack/cluster]
  - name: integrateur-tenance
    harness: codex
    prompt: rigs/increment-0/prompts/integrateur-tenance.md    # rôles, schémas, graphes, buckets, namespaces
    permissions: workspace-write
    scope: [stack/charts, stack/runbooks, stack/env]
  - name: verificateur
    harness: claude-code
    prompt: rigs/shared/roles/verificateur.md
    permissions: read-only
    allowed_commands: ["symbiot test *", "symbiot verify *"]
  - name: gardien
    harness: claude-code
    prompt: rigs/shared/roles/gardien.md
    permissions: read-only
    triggers: [pull_request]
  - name: scribe
    harness: claude-code
    prompt: rigs/shared/roles/scribe.md
    permissions: workspace-write
    scope: [knowledge/log.md, knowledge/vues/]
rules:
  - no seat may run commands on the server except through `symbiot <runbook>`
  - integrateur and verificateur are never the same seat
  - every PR carries a provenance concept or a `no-provenance-change` label validated by gardien
definition_of_done:
  - scenario: knowledge/scenarios/journee-increment-0.md passes via `symbiot verify increment-0`
  - demo recorded on the evaluation machine
  - all concepts touched are `verified: human:vs` within the week
```

Extrait du prompt de rôle `gardien.md` : « Tu refuses toute PR qui introduit un store autre que PostgreSQL ou FalkorDB, une exécution hors k3s, une identité qui n'est pas le `sub` Keycloak, un secret hors OpenBao, un fichier sans degré de dérivation déclaré, ou une `sources` vers du code AGPL dans un service clean-room. Tu cites la convention violée. Tu ne proposes pas de correctif. »

## Annexe D — Scénario d'acceptation de l'incrément 2

Une journée dans la vie, jouée par le vérificateur avec `symbiot verify increment-2`.

| Pas | Action | Appel de la carte | Preuve |
|---|---|---|---|
| 1 | L'utilisateur prend des notes de réunion ; le Brain crée `People/…` et `Projects/…` avec wikilinks | fichiers locaux, `build_graph` | fichiers présents, frontmatter de tagging |
| 2 | « Soumettre au serveur » convertit le dossier en bundle OKF : `type` par dossier, `title` du H1, `sources`, `generated: symbiot-client/<v>`, `index.md`, `log.md` depuis git | convertisseur | bundle valide par `okf` lint |
| 3 | Le client appelle `remember` avec le bundle, `dataset_name = sub + "_brain"`, `ontology_key` de l'ontologie Symbiot | MCP Cognee, Bearer Keycloak | `cognify_status` terminé, graphe FalkorDB peuplé |
| 4 | L'assistant répond à « qui travaille sur le projet X ? » par l'outil natif `memory-recall` | MCP Cognee `recall` projeté en outil natif | réponse citant les `source` OKF |
| 5 | Le serveur renvoie un bundle enrichi (relations déduites) ; le client le réintègre en notes `status: draft` et `verified` absent | convertisseur, sens retour | notes nouvelles marquées non vérifiées, aucune note existante écrasée |
| 6 | L'utilisateur vérifie une note : `verified: human:<sub>` ; `log.md` du Brain l'enregistre | fichiers locaux | ligne de `log.md` |
| 7 | Hors ligne : les pas 1, 4 (sur le grep local) et 6 fonctionnent ; 3 et 5 sont mis en file et rejoués au retour | — | file visible, rejeu sans doublon |
| 8 | Aucun appel sortant vers un domaine éditeur pendant la journée | — | capture réseau vide hors du cluster |

## Annexe E — Runbooks `symbiot` de V1

| Runbook | Effet | Retour arrière |
|---|---|---|
| `symbiot cluster up` | amorce k3s, namespaces, NetworkPolicy, StorageClass, plugin GPU | `cluster down` ; état déclaratif |
| `symbiot tenancy apply <brique>` | rôle et schéma PostgreSQL, graphe FalkorDB, bucket, client Keycloak, namespace | `tenancy drop <brique>` après sauvegarde |
| `symbiot deploy <brique> --version <tag>` | applique le chart épinglé | `deploy <brique> --version <précédent>` |
| `symbiot backup` / `restore <horodatage>` | PostgreSQL par schéma (`pg_dump -n`), FalkorDB par graphe, SeaweedFS par bucket | — |
| `symbiot fork sync <brique>` | rebase de `symbiot/storage` sur le tag amont, rapport de conflits | branche précédente conservée |
| `symbiot slice <dépôt> <point d'entrée>` | fermeture de dépendances et squelette du concept de provenance | lecture seule |
| `symbiot test <brique>` | suite amont sur les stores forkés | lecture seule |
| `symbiot verify <incrément>` | scénario d'acceptation | lecture seule |
| `symbiot lint` | OKF et règles de projet (B.4) | lecture seule |
| `symbiot knowledge ingest` | bundle → Cognee `remember` sur le dataset `symbiot-stack` | `forget` du dataset |
| `symbiot knowledge views` | régénère `knowledge/vues/` | lecture seule |
| `symbiot inventory` | relevé de la machine et des versions en concept d'inventaire | lecture seule |
| `symbiot secrets rotate <brique>` | rotation dans OpenBao et redémarrage | version précédente d'OpenBao |
