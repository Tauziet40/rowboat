# Plan d'évaluation — Rowboat vs Eigent comme socle client Symbiot

**Statut :** plan v2 soumis à validation (aucun contenu rédigé avant accord)
**Date :** 2026-10-15 (v2 : contraintes de stack, auth/secrets, ressources tierces ; v2.1 : DeepSeek Harness cloné comme référence du modèle de plugins ; v2.2 : OKF 0.2 ancré sur la spec Google ; v2.3 : le fork vise l'application, pas PostgreSQL ; v2.4 : rôles de PostgreSQL, OKF et Cognee précisés ; v3 : recentrage sur l'intégration des deux clients, stack serveur hors périmètre ; v3.1 : dépôts serveur lus sur leurs interfaces seulement ; v3.2 : livrable L5 OpenRig ajouté en suite ; v3.3 : couche agents pressentie, fiches BeeAI et Agent Stack, vérification DSH ; v3.4 : MemoryBear en post-traitement de Cognee et console d'administration des spaces, Synapse AI pour les workflows et apps ; v3.5 : L5 redéfini en méthode de déploiement V1, plan court soumis ; v3.6 : L5 rédigé)
**Auteur :** Claude (session de travail pour vs@method.watch)
**Format de travail :** Markdown ; conversion en formats finaux après validation du contenu

---

## 0. Analyse préalable du dossier

- Aucun fichier `.md` ou `.txt` à la racine du dossier de travail (`/home/user`) : pas de mémoire de recherches antérieures à réutiliser.
- Les deux dépôts sont présents, clonés sur la branche de travail `claude/gallant-heisenberg-6gsemz` :
  - `rowboat/` — monorepo TypeScript : client desktop Electron `apps/x` (+ mobile, web Spaces) et serveur Spaces **Harbor** `apps/harbor` (PostgreSQL, log append-only, 3 faces HTTP / WS / MCP). Licence Apache 2.0. Documents structurants déjà écrits par l'équipe : `apps/harbor/SPEC.md`, `CONTRACT.md`, `AGENTS.md`, `apps/x/SEPARATION_PLAN.md`, `REMOTE_SERVER.md`, `MINI_APPS_PLAN.md`, `proposal.md`.
  - `eigent/` — client desktop Electron + React (`src/`), backend agent Python/FastAPI sur **CAMEL-AI** (`backend/`), serveur local optionnel FastAPI + PostgreSQL + Celery (`server/`). Licence Apache 2.0. Documents structurants : `docs/design-system/design.md`, `docs/product-terminology.md`, `docs/model-capabilities.md`, `server/README_EN.md`.
- Dépôt de référence ajouté (v2.1) : `tauziet40/deepseek-harness` cloné en lecture seule dans `/home/user/tauziet40/deepseek-harness` (release dsh 0.2.1-alpha.1, licence MIT). C'est le harness DeepSeek sur Cordis : « tout est plugin » (adaptateur de modèle, registre d'outils, journal de session, boucle d'agent), profils et bundles composés par couches de patches YAML, **capability seams** (définition de service, fournisseur, consommateur) permettant de remplacer un fournisseur sans forker, packages `mcp/`, `skill/`, `subagent/`, `storage/` (JSON, SQLite), `credentials/`, `acp/`, `webhook/`, `schedule/`. Il sert de référentiel pour C10 et d'étalon pour l'axe A0 (une ressource tierce est-elle un seam remplaçable ?).
- Dépôts de contexte serveur clonés en lecture seule sous `/home/user/tauziet40/` (v3) : `centaur` (plateforme d'agents partagés, Rust + PostgreSQL, retenue pour la messagerie inter-espaces), `cognee` (v1.6.4, le RAG à ontologie, avec l'adaptateur communautaire FalkorDB) et `elephant-broker` (runtime cognitif sur Cognee, illustre la façon d'exploiter mémoire et RAG d'entreprise). **Cette stack fonctionne déjà et n'est pas évaluée.** Leur seul usage dans l'évaluation (v3.1) : caractériser les **interfaces serveur que le client doit parler** (API HTTP, serveur MCP, flux d'événements, formats d'identité et de secrets), pour mesurer la distance entre ce que chaque client sait consommer et ce que le serveur expose. Ils ne sont lus que sur ces surfaces d'interface, jamais sur leur fonctionnement interne.
- Signaux déjà repérés, à instruire dans l'évaluation :
  - Rowboat a un **connecteur Hermes** (`rowboatlabs/hermes-rowboat`, plugin plateforme Hermes) et un contrat d'invocation d'agents membres (spec §8) : l'axe « agents autonomes façon Hermes » est déjà traité côté Rowboat.
  - Eigent a une architecture backend très découpée (`memory`, `lightweight_memory`, `remote_sub_agent`, `router_layer`, `hands`, `permission_policy`, `workspace_git`, `workspace_runtime`) et un domaine `space` côté serveur, à comparer à Spaces/Harbor.
  - Aucune des deux bases ne mentionne A2A de manière structurante (seules mentions incidentes).
  - Activité : ~87 commits Rowboat et ~50 commits Eigent depuis juillet 2026 sur les clones (à confirmer sur les dépôts amont).

## 1. Objectif et critère de succès

**Objectif :** évaluer les deux clients, Rowboat et Eigent, sur leur capacité à s'intégrer à la stack serveur Symbiot existante, et choisir entre (a) partir de Rowboat, (b) partir d'Eigent, (c) hybrider (socle de l'un + emprunts à l'autre), avec les écarts à combler.

**Schéma d'intégration cible (v3, décidé) :**
- Le client exploite en local un **second cerveau** (mémoire et connaissances personnelles), que le serveur peut **optimiser à la demande**.
- Les **productions du poste** peuvent être partagées ou apportées au serveur, donc à l'organisation, à la façon des **Spaces** de Rowboat, les blobs étant gérés par **Harbor**.
- La **messagerie inter-espaces** s'appuie sur **Centaur**.
- La **mémoire et le RAG d'entreprise** sont exploités à la façon de **Cognee + ElephantBroker**, sur FalkorDB et PostgreSQL.

L'évaluation mesure donc, pour chaque client, quatre intégrations : client ↔ second cerveau local, second cerveau ↔ serveur (optimisation, partage), client ↔ Spaces/Harbor (productions, blobs), client ↔ Centaur (messages inter-espaces), plus l'accès client aux ressources mémoire/RAG serveur.

**Succès :** à la fin, tu disposes d'une grille comparative notée, d'une cartographie « composant cible Symbiot → ce que chaque dépôt fournit / ne fournit pas », et d'une recommandation argumentée avec liste d'écarts priorisés.

## 2. Architecture cible Symbiot (référentiel de l'évaluation)

Telle que décrite dans ta demande ; c'est le référentiel contre lequel les deux dépôts sont mesurés. À corriger si j'ai mal compris.

| # | Composant cible | Rôle |
|---|---|---|
| C1 | Client local-first | Données locales appartenant à l'utilisateur, fonctionnement hors ligne, projection vers l'environnement partagé |
| C2 | Environnement partagé serveur | Collaboration humains + agents IA dans un espace commun |
| C3 | Agents autonomes (modèle Hermes Agent) | Agents à longue durée, outillés, déclenchables, membres des espaces |
| C4 | PostgreSQL | Bases métier et ERP : la donnée transactionnelle de l'entreprise |
| C5 | FalkorDB | Base hybride vecteur + graphe |
| C6 | Connaissances au format OKF 0.2 + MCP dédié | Open Knowledge Format, spec Google (`GoogleCloudPlatform/open-knowledge-format`, `SPEC.md` v0.2) : un bundle est une arborescence de fichiers Markdown à frontmatter YAML, un concept par fichier (`type` obligatoire ; `title`, `description`, `resource`, `tags` recommandés), `index.md` et `log.md` réservés, provenance (`sources`), confiance (`generated`, `verified`, trois paliers), cycle de vie (`status`, `stale_after`), calculs attestés. La spec ne définit ni stockage ni protocole : le MCP dédié est notre couche d'accès. **Rôle dans Symbiot :** la donnée structurée et curatée, avec échelle d'accès (qui peut lire quoi) et validation (paliers de confiance `generated` / `verified`, statut, fraîcheur) |
| C7 | Cognee | Le RAG, avec une ontologie maintenue : construction RAG / KAG sur FalkorDB, mémoire sessions / agents / utilisateurs |
| C8 | SeaweedFS | Fichiers et ressources partagées |
| C9 | Agents décrits selon A2A | Interopérabilité et découverte d'agents (Agent Card, tâches) |
| C10 | Plugins façon Cordis (DeepSeek Harness) | Extensibilité par plugins : seams remplaçables, profils et bundles patchables, pas de cœur privilégié |
| C11 | Routeur LLM | Arbitrage opportuniste local on-premise vs API cloud |
| C12 | Services in-house | Nextcloud, email, suite bureautique (OpenOffice / équivalent) |
| C13 | Keycloak | Identité et authentification (OIDC) pour humains et agents |
| C14 | OpenBao | Secrets : clés de modèles, clés d'agents, jetons d'intégration |

**Répartition des rôles (décidée, v2.4) :** PostgreSQL porte le métier (ERP) ; OKF porte la connaissance structurée et curatée avec ses niveaux d'accès et de validation ; Cognee porte le RAG avec une ontologie maintenue, sur FalkorDB. L'évaluation vérifie pour chaque dépôt comment ses propres notions (mémoire, connaissance, fichiers, données d'app) se projettent sur ces trois rôles, sans les confondre.

**Contrainte de stack (décidée) :** aucune base de données, moteur vectoriel ou moteur de RAG supplémentaire n'est ajouté au serveur. Seules PostgreSQL et FalkorDB sont maintenues. Toute brique d'un dépôt qui impose une autre base (par exemple Qdrant dans le backend Eigent, SQLite dans DSH, ou tout store embarqué côté client qui devrait être partagé) est comptée comme un écart à résorber, pas comme un acquis. Le moyen de résorption est le **fork de l'application** pour migrer son store vers PostgreSQL ou FalkorDB ; l'évaluation chiffre donc, pour chaque store non conforme, la difficulté de cette migration (interface de stockage abstraite ou accès direct, volume de code, tests existants).

**Critère déterminant (décidé) :** au-delà de l'architecture, ce qui tranche est la capacité des outils à exploiter des ressources tierces (RAG, mémoire, connaissances) même lorsqu'elles ne sont pas exactement les nôtres, et la lisibilité de ces connexions : où elles sont déclarées, comment elles se configurent, comment on les lit et on les audite.

## 3. Grille d'évaluation (axes et sous-critères)

Chaque axe est noté pour chaque dépôt sur une échelle 0–4 (0 absent, 1 ébauche, 2 partiel, 3 solide, 4 directement réutilisable), avec références de fichiers à l'appui.

| Axe | Sous-critères | Composants cible couverts |
|---|---|---|
| A0 Exploitation de ressources tierces et lisibilité des connexions (axe déterminant, pondéré ×2) | comment chaque dépôt consomme une mémoire, un RAG ou une base de connaissances qu'il n'a pas produite : via MCP, API, connecteur, skill ; généricité des interfaces (un store de mémoire ou de retrieval est-il une interface remplaçable ou un composant soudé ?) ; lisibilité : où sont déclarées les connexions, format de configuration, traçabilité des appels, documentation ; effort pour brancher Cognee, FalkorDB et un MCP OKF sans toucher au cœur | C5, C6, C7 |
| A1 Local-first & propriété des données | stockage local, mode hors ligne, synchronisation, chiffrement/clés, dépendances cloud obligatoires ou optionnelles (Eigent cloud, Composio, TypeSafe, PostHog…) | C1 |
| A2 Séparation client / serveur | frontières de code, protocole, possibilité de faire tourner le cœur à distance (plan de séparation Rowboat, backend/serveur Eigent) | C1, C2 |
| A3 Environnement partagé | modèle d'espace, membres humains et agents, fil / fichiers / wiki, droits, invitations, multi-org | C2 |
| A4 Agents autonomes & orchestration | modèle d'agent, invocation, file d'attente, approbations, planification, workforce multi-agent, harness mono-agent, connecteur Hermes, sous-agents distants | C3 |
| A5 Mémoire & connaissances | graphe de connaissances (Rowboat Brain), mémoire Eigent (`memory`, `lightweight_memory`, Qdrant) ; conformité à la contrainte de stack (quelle base chaque brique exige, ce qui doit être retiré ou remplacé par PostgreSQL / FalkorDB) | C4, C5, C6, C7 |
| A6 Outillage & extensibilité | MCP (client et serveur), skills, plugins, navigateur, terminal, code mode (ACP), compatibilité avec un modèle de plugins type Cordis | C10 |
| A7 Modèles & routage LLM | abstraction fournisseur, modèles locaux (Ollama, vLLM…), capacités déclarées, point d'insertion d'un routeur local/cloud | C11 |
| A8 Fichiers & ressources | blobs, versions, fusion, git de workspace, point d'insertion de SeaweedFS | C8 |
| A9 Identité, secrets, politiques | auth OIDC et compatibilité Keycloak (humains et agents), gestion des secrets et compatibilité OpenBao (où les clés vivent aujourd'hui, scellement, variables d'environnement), politiques de permission, attribution des actes, audit | C13, C14, C2, C3 |
| A10 Interopérabilité standards | MCP, A2A, ACP, OpenAPI, protocoles typés (zod) ; effort pour décrire les agents en A2A | C9 |
| A11 Intégration services in-house | email, agenda, documents, Nextcloud, bureautique ; mécanismes d'intégration existants (OAuth, triggers, connecteurs) | C12 |
| A12 Qualité d'ingénierie & pérennité | tests, documentation, conventions, stack, activité, licence, communauté, dette, facilité de fork | transverse |
| A13 Déployabilité on-premise | Docker, migrations, dépendances externes, exposition réseau, multi-tenant ; inventaire exhaustif des bases et services requis, confronté à la contrainte de stack | C4 et transverse |

## 4. Livrables (tous en Markdown de travail, puis conversion)

| # | Livrable | Contenu |
|---|---|---|
| L0 | `00-plan-evaluation-rowboat-eigent.md` | ce plan |
| L1 | `01-architecture-cible-symbiot.md` | référentiel §2 détaillé (une page), pour que les fiches y renvoient sans le restater |
| L2 | `02-fiche-rowboat.md` | analyse de Rowboat : architecture, modules clés avec références de fichiers, notation A1–A13, forces, faiblesses, risques |
| L3 | `03-fiche-eigent.md` | même structure pour Eigent |
| L4 | `04-comparatif-et-recommandation.md` | grille notée côte à côte (A0 pondéré ×2), cartographie C1–C14 → couverture par chaque dépôt, inventaire des bases et stores imposés par chaque dépôt et plan de migration de chaque store non conforme vers PostgreSQL ou FalkorDB par fork de l'application, avec la difficulté estimée, scénarios (a)/(b)/(c), recommandation, écarts priorisés et ordre de chantiers |
| L2b | `02b-fiche-beeai-framework.md` | **Ajout v3.3.** Même analyse que les deux clients, appliquée au framework d'agents pressenti (`tauziet40/beeai-framework`, Python et TypeScript, Serve A2A et MCP, Workflows, Requirement Agent, Memory, RAG) ; mesure en plus sa capacité à porter les cinq principes d'Eigent (journal durable, permissions et humain dans la boucle, environnements d'exécution, bundles déclaratifs, workforce) |
| L2c | `02c-fiche-agentstack.md` | **Ajout v3.3.** Même analyse appliquée à la plateforme serveur de BeeAI (`tauziet40/agentstack` : agents exposés en A2A, Keycloak et OIDC, PostgreSQL et pgvector, Redis, S3, Helm) ; position entre Harbor et Centaur, inventaire des stores |
| L2d | `02d-fiche-memorybear.md` | **Ajout v3.4.** Même analyse appliquée à MemoryBear (`tauziet40/memorybear`), dans le rôle précisé par toi : augmenter Cognee en **post-traitement** (extraction, association, consolidation, oubli), sans s'y substituer, Cognee restant le point d'unification du RAG et de la mémoire ; et apporter la **gestion des tenants appelés « spaces »** avec administration des modèles, skills, plugins et contextes autorisés par space, soit la console d'administration qui pilote les droits et capacités de l'architecture Rowboat + Harbor et de DSH |
| L2e | `02e-note-synapse-ai-workflows-apps.md` | **Ajout v3.4.** Analyse ciblée de Synapse AI (`tauziet40/synapse-ai`, AGPL-3.0) limitée à la partie workflows et apps no-code, pressentie pour extraction et refactoring vers les mini-apps de Rowboat : architecture, **provenance** (le soupçon d'un framework d'origine non identifié, à confirmer), conséquences de licence, faisabilité de l'extraction |
| B | `annexe-B-dsh-seams.md` | **Ajout v3.3.** Vérification bornée de DeepSeek Harness, le harness pressenti, sur cinq seams (session, tools et guard, sandbox, bundles et credentials, subagents et Agent Teams) et sur son exposition MCP ou A2A |
| L5 | `05-methode-deploiement-v1.md` (plan court : `05-plan-methode-deploiement-v1.md`) | **Redéfini v3.5.** Méthode de déploiement de la stack V1 et équipe d'agents OpenRig, figeant les onze décisions validées le 2026-10-16 ; absorbe le contenu initial ci-après : |
| L5 (initial) | `05-contextes-okf-pour-equipe-openrig.md` | **Suite de l'évaluation, produite après le choix du client (L4 validé).** Comment déployer des contextes de connaissance produit, technique et projet pour une équipe d'agents coordonnée par OpenRig (`tauziet40/openrig`, cloné en lecture seule dans `/home/user/tauziet40/openrig` : rig défini en YAML, sièges Claude Code et Codex, agent lead, démon tmux, SQLite local) chargée de piloter l'intégration retenue ; et comment produire ces contextes en bundles OKF 0.2 (un concept par fichier, `sources`, `generated` / `verified`, `status`, `stale_after`) pour que l'équipe d'agents travaille sur une connaissance validée, datée et traçable plutôt que sur des hypothèses. Ce livrable aura son propre plan court soumis à validation avant rédaction. |
| L6 | `INDEX.md` | index des documents finaux (créé à la conversion) |

Note de modifications : non applicable (première version).

## 5. Méthode

1. Lecture des documents structurants des deux clients (specs, contrats, guides agents, plans), puis lecture ciblée du code des modules correspondant à chaque axe. **Gestion du contexte (v3) :** le dossier ne tient pas dans un seul contexte ; chaque lecture de code profonde est déléguée à un sous-agent d'exploration qui ne renvoie que la conclusion et les références de fichiers, et les fiches sont rédigées axe par axe. Les dépôts serveur ne sont ouverts que sur une question précise.
2. Pas d'exécution des applications : l'évaluation est documentaire et code-based. Les tests existants sont inventoriés, pas relancés (sauf demande).
3. Recherche web limitée à l'ancrage des standards cibles (A2A, Hermes Agent, Cognee, FalkorDB, SeaweedFS, OKF, Cordis) pour vérifier les points d'insertion ; pas de veille large.
4. Chaque affirmation sur un dépôt cite un fichier. Chaque note de la grille a une justification d'une à trois lignes.
5. Contrôle de cohérence final entre L1–L4 (terminologie, notes, noms de modules) avant livraison.

## 6. Points à valider ou à préciser avant rédaction

1. **Référentiel §2** (tranché, v2.4) : tu as clos la description de l'architecture globale. Le référentiel C1–C14 est celui-ci.
2. **OKF** (tranché) : spec Google OKF v0.2, récupérée et résumée dans C6. Conséquence pour l'évaluation : OKF étant « du Markdown à frontmatter dans une arborescence », l'axe A5 mesure pour chaque dépôt la distance entre son modèle de connaissance et un bundle OKF (le Brain de Rowboat est un graphe de notes Markdown rétro-liées, le wiki des Spaces est un dossier de fichiers Markdown versionnés ; la mémoire d'Eigent est à inventorier). Le MCP dédié est évalué sous A0 comme ressource tierce à brancher.
3. **DeepSeek Harness** (tranché, v3) : référence seulement, pour A0 et A6. Pas de troisième candidat : l'évaluation porte sur les deux clients.
4. **Hermes** : je retiens Hermes Agent de Nous Research (c'est celui que Rowboat connecte). Confirmer.
5. **Emplacement des livrables** : je propose `rowboat/docs/symbiot/` sur la branche `claude/gallant-heisenberg-6gsemz` (dépôt du client modèle, versionné et poussé). Alternative : dossier hors dépôt dans l'espace de travail, non versionné.
6. **Profondeur** : évaluation documentaire sans exécution (proposée) ou avec lancement des deux apps et de leurs tests (plus long, plus coûteux).
7. **Langue** : français pour tous les livrables (proposé), termes techniques en anglais quand ils désignent un identifiant du code.
8. **Formats finaux** après validation du contenu : `.md` final uniquement, ou aussi `.docx` / `.pdf` ?
9. **Fork** (tranché, v2.3) : le fork vise l'application évaluée, pour migrer ses stores non conformes (SQLite, Qdrant, etc.) vers PostgreSQL ou FalkorDB. Aucun fork ni extension de PostgreSQL n'est en jeu.

**Approche initiale rappelée par toi (v3.3) :** BeeAI Framework avec A2A pour les agents, DeepSeek Harness pour le harness, Cognee avec ElephantBroker pour le RAG et la mémoire, OKF pour la donnée structurée, MemoryBear envisagé pour la gestion des espaces (précisé en v3.4 : post-traitement de Cognee et console d'administration des spaces), Synapse AI pour les workflows et apps no-code (v3.4). L'évaluation des clients (L2, L3, L4) reste valide ; L2b, L2c et l'annexe B la complètent sur la couche agents, et le comparatif sera amendé d'un §8 « couche agents » après leur validation.

Points déjà tranchés par toi (v2) : stack serveur limitée à PostgreSQL + FalkorDB ; identité Keycloak ; secrets OpenBao ; l'exploitation de ressources tierces et la lisibilité des connexions est l'axe déterminant.

Dès validation (avec tes réponses aux points 1 à 8, ou « OK avec les valeurs proposées »), je produis L1 à L4 dans l'ordre, puis le contrôle de cohérence.
