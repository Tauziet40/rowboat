# Architecture cible Symbiot — référentiel de l'évaluation

**Statut :** référentiel validé le 2026-10-15 (plan v3.1)
**Rôle de ce document :** la seule description de la cible. Les fiches [Rowboat](02-fiche-rowboat.md) et [Eigent](03-fiche-eigent.md) et le [comparatif](04-comparatif-et-recommandation.md) y renvoient par identifiant (C1…C14, A0…A13) et ne la restatent pas.
**Plan :** [00-plan-evaluation-rowboat-eigent.md](00-plan-evaluation-rowboat-eigent.md)

---

## 1. Ambition

Symbiot unifie plusieurs stacks qui ont chacune leur spécialité : un client de travail local-first sur le poste de l'utilisateur, un environnement partagé d'organisation où humains et agents collaborent, une mémoire et un RAG d'entreprise, une messagerie inter-espaces portée par des agents partagés, et des services in-house. L'évaluation porte sur le **client** : lequel de Rowboat ou d'Eigent s'intègre le mieux à la stack serveur existante, qui fonctionne et n'est pas remise en cause.

## 2. Schéma d'intégration

```
┌──────────────────────── poste de l'utilisateur ────────────────────────┐
│  Client Symbiot (Rowboat ou Eigent)                                     │
│   ├─ second cerveau local : mémoire et connaissances personnelles       │
│   ├─ productions locales : documents, notes, code, fichiers             │
│   ├─ assistant et agents locaux (modèle Hermes Agent)                   │
│   └─ routeur LLM : modèle local on-premise ou API cloud, par opportunité│
└───────┬──────────────────────┬──────────────────────┬──────────────────┘
        │ optimisation du      │ partage des          │ messages
        │ second cerveau       │ productions          │ inter-espaces
        ▼                      ▼                      ▼
┌──────────────────────────── serveur in-house ──────────────────────────┐
│  Mémoire & RAG         Espaces partagés        Agents partagés          │
│  Cognee (ontologie     Spaces / Harbor         Centaur                  │
│  maintenue) + MCP OKF  (blobs, fichiers,       (sessions, exécution     │
│                        fil, membres)           en sandbox, workflows)   │
│  ───────────────────────────────────────────────────────────────────    │
│  PostgreSQL (métier, ERP)   FalkorDB (vecteur + graphe)   SeaweedFS     │
│  Keycloak (identité)        OpenBao (secrets)                           │
│  Nextcloud · email · bureautique                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

Quatre intégrations sont mesurées pour chaque client, plus l'accès aux ressources mémoire et RAG :

| Id | Intégration | Ce que le client doit savoir faire |
|---|---|---|
| I1 | Client ↔ second cerveau local | Tenir une mémoire et des connaissances personnelles sur le poste, dans un format lisible et exportable (cible : bundle OKF) |
| I2 | Second cerveau ↔ serveur | Soumettre le second cerveau à une optimisation par le serveur (Cognee) à la demande, et en récupérer le résultat |
| I3 | Client ↔ Spaces / Harbor | Apporter des productions locales à un espace d'organisation : fichiers, blobs, messages, avec attribution et droits |
| I4 | Client ↔ Centaur | Émettre et recevoir des messages inter-espaces via un agent partagé : session par fil, exécution, flux d'événements |
| I5 | Client ↔ mémoire et RAG d'entreprise | Consommer les outils MCP de Cognee (remember, recall, search, forget) et les bundles OKF exposés par le MCP dédié |

## 3. Composants cible

| # | Composant | Rôle dans Symbiot |
|---|---|---|
| C1 | Client local-first | Données locales appartenant à l'utilisateur, fonctionnement hors ligne, projection vers l'environnement partagé |
| C2 | Environnement partagé serveur | Collaboration humains + agents IA dans un espace commun (modèle : Spaces de Rowboat) |
| C3 | Agents autonomes (modèle Hermes Agent) | Agents à longue durée, outillés, déclenchables, membres des espaces |
| C4 | PostgreSQL | Bases métier et ERP : la donnée transactionnelle de l'entreprise |
| C5 | FalkorDB | Base hybride vecteur + graphe, support de Cognee via l'adaptateur communautaire |
| C6 | OKF 0.2 + MCP dédié | Connaissance structurée et curatée, avec échelle d'accès et validation (voir §4) |
| C7 | Cognee | Le RAG, avec une ontologie maintenue : construction RAG / KAG sur FalkorDB, mémoire sessions / agents / utilisateurs |
| C8 | SeaweedFS | Fichiers et ressources partagées |
| C9 | A2A | Description et découverte des agents (Agent Card, tâches) |
| C10 | Plugins façon Cordis (DeepSeek Harness) | Extensibilité par plugins : seams remplaçables, profils et bundles patchables, pas de cœur privilégié |
| C11 | Routeur LLM | Arbitrage opportuniste local on-premise vs API cloud |
| C12 | Services in-house | Nextcloud, email, suite bureautique |
| C15 | Console d'administration des spaces | Gestion des tenants : modèles, skills, plugins, contextes et droits autorisés par space, appliqués à Harbor, DSH et Cognee (candidat : MemoryBear) |
| C16 | Workflows et apps no-code | Construction d'applications et de pipelines sans code par l'utilisateur, sur le poste (mini-apps Rowboat) ou sur le serveur (candidat : extraction de Synapse AI) |
| C13 | Keycloak | Identité et authentification (OIDC) pour humains et agents |
| C14 | OpenBao | Secrets : clés de modèles, clés d'agents, jetons d'intégration |

Deux composants serveur supplémentaires sont des acquis, pas des cibles d'évaluation : **Harbor** (serveur des Spaces, dans le dépôt Rowboat) et **Centaur** (plateforme d'agents partagés).

## 4. OKF 0.2 en bref

Spécification Google, dépôt `GoogleCloudPlatform/open-knowledge-format`, fichier `SPEC.md` v0.2.

- Un **bundle** est une arborescence de fichiers Markdown à frontmatter YAML ; distribuable comme dépôt git, archive ou sous-dossier.
- **Un concept par fichier.** Seul `type` est obligatoire ; `title`, `description`, `resource`, `tags` sont recommandés. Les clés inconnues sont préservées.
- Fichiers réservés : `index.md` (listing d'un répertoire) et `log.md` (historique, plus récent en tête).
- **Provenance :** `sources` (liste de `{ resource, id, title, author, usage_count, last_modified }`).
- **Confiance :** `generated: { by, at }` et `verified: [{ by, at }]` ; trois paliers dérivés : non vérifié, confirmé par machine, relu par un humain. Acteurs notés `<producteur>/<version>`, `human:<id>`, `process:<id>`.
- **Cycle de vie :** `status` (`draft`, `stable`, `deprecated`) et `stale_after` (instant ISO 8601).
- **Calculs attestés :** type `Attested Computation` avec `runtime`, `parameters`, `computation`, `executor`, `attester`.
- La spec ne définit **ni stockage ni protocole** : le MCP dédié de Symbiot est la couche d'accès.

## 5. Contraintes décidées

- **Stack serveur fermée.** Aucune base, aucun moteur vectoriel ni moteur de RAG en plus de PostgreSQL et FalkorDB. Toute brique d'un client qui impose un autre store partagé est un écart ; le moyen de résorption est le **fork de l'application** pour migrer ce store vers PostgreSQL ou FalkorDB. Un store strictement local au poste (cache, index personnel) n'est pas concerné par cette contrainte, mais il est inventorié.
- **Identité** : Keycloak (OIDC). **Secrets** : OpenBao.
- **Critère déterminant** : la capacité du client à exploiter des ressources tierces (mémoire, RAG, connaissances) et la lisibilité de ces connexions. Pondération ×2 dans la grille.

## 6. Grille d'évaluation

Notation 0–4 par axe et par client : 0 absent, 1 ébauche, 2 partiel, 3 solide, 4 directement réutilisable. Chaque note est justifiée par des références de fichiers dans la fiche du client.

| Axe | Sous-critères | Composants / intégrations |
|---|---|---|
| **A0** Exploitation de ressources tierces et lisibilité des connexions (×2) | consommation d'une mémoire, d'un RAG ou d'une base de connaissances externe via MCP, API, connecteur ou skill ; généricité (store remplaçable ou soudé) ; lisibilité (déclaration, configuration, traçabilité, documentation) ; effort pour brancher Cognee, FalkorDB et le MCP OKF sans toucher au cœur | I5, C5, C6, C7 |
| A1 Local-first et propriété des données | stockage local, hors ligne, synchronisation, chiffrement, dépendances cloud obligatoires ou optionnelles | I1, C1 |
| A2 Séparation client / serveur | frontières de code, protocole, cœur exécutable à distance | C1, C2 |
| A3 Environnement partagé | espaces, membres humains et agents, fil, fichiers, droits, invitations, multi-org | I3, C2 |
| A4 Agents autonomes et orchestration | modèle d'agent, invocation, approbations, planification, multi-agent, harness, compatibilité Hermes, sous-agents distants | C3 |
| A5 Mémoire et connaissances | modèle de connaissance local, distance à un bundle OKF, conformité à la contrainte de stack | I1, I2, C4, C5, C6, C7 |
| A6 Outillage et extensibilité | MCP client et serveur, skills, plugins, navigateur, terminal, code mode ; distance au modèle Cordis | C10 |
| A7 Modèles et routage LLM | abstraction fournisseur, modèles locaux, capacités déclarées, point d'insertion d'un routeur | C11 |
| A8 Fichiers et ressources | blobs, versions, fusion, git de workspace, point d'insertion de SeaweedFS | I3, C8 |
| A9 Identité, secrets, politiques | OIDC et compatibilité Keycloak, gestion des secrets et compatibilité OpenBao, politiques de permission, attribution, audit | C13, C14 |
| A10 Interopérabilité standards | MCP, A2A, ACP, OpenAPI, contrats typés ; effort pour décrire les agents en A2A | C9, I4 |
| A11 Intégration services in-house | email, agenda, documents, Nextcloud, bureautique ; mécanismes existants | C12 |
| A12 Qualité d'ingénierie et pérennité | tests, documentation, conventions, stack, activité, licence, communauté, facilité de fork | transverse |
| A13 Déployabilité on-premise | build, Docker, migrations, exposition réseau, multi-tenant ; inventaire des bases et services requis | transverse |

## 7. Dépôts de référence

| Dépôt | Chemin local | Usage dans l'évaluation |
|---|---|---|
| `tauziet40/rowboat` | `/home/user/rowboat` | Client candidat (apps/x) ; Harbor (apps/harbor) est un acquis serveur |
| `tauziet40/eigent` | `/home/user/eigent` | Client candidat |
| `tauziet40/deepseek-harness` | `/home/user/tauziet40/deepseek-harness` | Référence du modèle de plugins Cordis (A0, A6) |
| `tauziet40/centaur` | `/home/user/tauziet40/centaur` | Interfaces client de la messagerie inter-espaces (I4) |
| `tauziet40/cognee` | `/home/user/tauziet40/cognee` | Interfaces client de la mémoire et du RAG (I2, I5) |
| `tauziet40/elephant-broker` | `/home/user/tauziet40/elephant-broker` | Forme d'un contrat client ↔ runtime de mémoire (I5) |
| `tauziet40/beeai-framework` | `/home/user/tauziet40/beeai-framework` | Framework d'agents pressenti, avec A2A (C3, C9) ; fiche L2b |
| `tauziet40/agentstack` | `/home/user/tauziet40/agentstack` | Plateforme serveur de BeeAI : agents en A2A, Keycloak, Helm ; fiche L2c |
| `tauziet40/memorybear` | `/home/user/tauziet40/memorybear` | Post-traitement de Cognee (consolidation, oubli) et console d'administration des tenants « spaces » : modèles, skills, plugins, contextes autorisés par space ; fiche L2d. Impose Neo4j, Redis et Elasticsearch : écart de stack à instruire |
| `tauziet40/synapse-ai` | `/home/user/tauziet40/synapse-ai` | Partie workflows et apps no-code pressentie pour extraction vers les mini-apps de Rowboat ; AGPL-3.0, provenance à établir ; note L2e |
| `tauziet40/openrig` | `/home/user/tauziet40/openrig` | Coordination d'une équipe d'agents de pilotage de l'intégration ; livrable L5 |

Centaur, Cognee et ElephantBroker ne sont lus que sur leurs surfaces d'interface. DSH est vérifié sur cinq seams (annexe B).

**Couche agents pressentie (rappel du 2026-10-15) :** BeeAI Framework avec A2A pour écrire et décrire les agents, DeepSeek Harness comme harness d'exécution, Cognee et ElephantBroker pour la mémoire et le RAG, OKF pour la donnée structurée. La relation entre cette couche et le client retenu est l'objet du §8 du comparatif.
