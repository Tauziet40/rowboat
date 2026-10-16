---
type: Évaluation
title: Évaluation MemoryBear
description: Conversion OKF du document de travail 02d-fiche-memorybear.md du dossier docs/symbiot (cycle des 15 et 16 octobre 2026).
tags:
  - inspirant
  - mémoire
  - gouvernance
sources:
  - resource: /deprecated/2026-10-15/02d-fiche-memorybear.md
generated:
  by: claude-fable-5.1/session-01MK6
  at: 2026-10-16T18:00:00+02:00
status: stable
stale_after: 2027-01-16T00:00:00+02:00
---

# Évaluation MemoryBear

**Dépôt :** `tauziet40/memorybear`, clone local `/home/user/tauziet40/memorybear`, HEAD `0918ea7` (2026-10-08, PR #2360, v0.3.10 à v0.3.13)
**Statut d'origine :** version de travail du 2026-10-15, issue de la lecture du code par agents d'exploration ; chaque constat cite un fichier
**Référentiel :** [01-architecture-cible-symbiot.md](/conventions/architecture-cible.md). **Rôles examinés**, tels que précisés : (1) augmenter Cognee en **post-traitement** sans s'y substituer, Cognee restant le point d'unification du RAG et de la mémoire (C7) ; (2) la **gestion des tenants « spaces »** et la console d'administration des modèles, skills, plugins et contextes autorisés par space, candidate pour C15. L'axe A4 (agents et workflows de la plateforme) n'a pas été instruit : hors des deux rôles.

Chemins relatifs à `/home/user/tauziet40/memorybear`. `CM` désigne `api/app/core/memory`.

---

## 1. Identité

| | |
|---|---|
| Nature | Plateforme complète de RedBear AI : moteur de mémoire « science de la mémoire », mais aussi agents, workflows, multi-agents, bases de connaissances, facturation, sandbox Rust. 606 routes, ~320 k lignes Python dans `api/app`, dont ~62 k pour le moteur mémoire (`CM`) |
| Stack | Python 3.12 FastAPI (`api/`), identity-service et gateway-service séparés, `mem-knowledge/` (RAG documentaire), `sandbox/` (Rust, seccomp), `e2b-infra/` (bacs à sable Docker), `web/` (console), `packages/` (auth-sdk, redbear-model) |
| Stores | **PostgreSQL** (50 modèles, 104 migrations Alembic), **Neo4j** 5.x avec APOC et GDS (maître du graphe), **Elasticsearch** (lecture mémoire par défaut et RAG), **Redis** (Celery, sessions, caches, pub/sub, verrous) |
| Licence et gouvernance | Apache 2.0 ; pilotée par une entreprise (RedBear AI / SuanmoSuanyang), modules « premium » et « enterprise_ext » absents du dépôt, miroir Gitee quotidien |
| Tests | 30 fichiers, 517 fonctions, dont 13 sur le stockage et le reste sur les workflows ; **aucun test sur l'extraction, la réflexion, l'oubli ou les insights** ; 0 test dans `mem-knowledge` ; pas de workflow CI pytest |
| Activité | releases hebdomadaires de janvier à avril 2026 ; dernier commit 2026-10-08 ; commentaires et prompts majoritairement en chinois |

## 2. Architecture en bref

- **Moteur mémoire** (`CM`) : écriture asynchrone par message (fenêtre glissante, `pipelines/dispatcher.py:30`), pipeline en six étapes (`pipelines/write_pipeline.py:388-624`), réflexion « Layer2 » toutes les 10 min, oubli toutes les 5 min, score topologique GDS toutes les 60 min, insights quotidiens, le tout en Celery Beat sur Redis (`api/app/celery_app.py:260-370`).
- **Plan d'administration** : dans le même monolithe `api/`, PostgreSQL ; `identity-service` et `gateway-service` séparés mais dépendants du schéma du monolithe et de Redis ; console `web/` avec deux niveaux, « manage » (tenant) et « space ».
- **Interfaces** : `/api/*` (~60 contrôleurs, JWT), `/v1/*` (clé API : application, RAG, mémoire, ontologie), `/v1/mcp/memory` (FastMCP streamable-http), OpenAPI de référence de 105 chemins avec contrôle CI des ruptures (`api/openapi-baseline.json`, `.github/workflows/api-breaking-change.yml`).

## 3. Évaluation par axe

### A0 — Exploitation de ressources tierces et lisibilité des connexions (×2) — **note 2**

- **Consommation** : outils intégrés, Custom OpenAPI, MCP par URL avec synchronisation des outils (`/tools/{id}/sync_mcp_tools`) et marchés MCP configurables par tenant (Bailian, ModelScope, TokenFlux, 302.AI, auto-hébergé, `api/app/models/tool_model.py:171-180`) ; modèles multi-fournisseurs avec catalogue, canaux et chiffrement.
- **Fourniture à des tiers** : pauvre. Le MCP mémoire n'expose que **deux outils**, `write_memory(message)` et `read_memory(message, search_switch)` (`api/app/controllers/service/mcp_memory.py:46, 88`), authentifiés par clé API et en-tête `X-End-User-Other-Id`. L'ingestion REST n'accepte **que des messages** `{role, content, dialog_at, files}` (`api/app/schemas/memory_agent_schema.py:85-110`) ; **aucune ingestion de triplets ni de graphe**, **aucun export en masse** (`graph_data` plafonné à 1 000 nœuds et profondeur 3).
- **Lisibilité** : OpenAPI contrôlée en CI ; mais l'audit n'existe qu'en mode `gateway` d'entreprise absent du dépôt, et les actions d'administration ne sont pas auditées (`gateway-service/src/middleware.py:111-112`).

### A1 — Propriété des données (auto-hébergement) — **note 2**

Auto-hébergeable par docker-compose, mais les **poids des petits modèles BERT ne sont pas publiés** (émotion, topic-shift, trois classifieurs, `api/env.example:219-228`), l'ASR et la vidéo dépendent de fournisseurs chinois (Volc, DashScope), et les modules SSO et gateway réels sont privés.

### A2 — Séparation des composants — **note 1**

Monolithe `api/` de 320 k lignes mêlant mémoire, agents, workflows, administration et facturation ; identity et gateway séparés mais lisant les tables du monolithe ; `initialize()` ouvre toujours Neo4j et Elasticsearch (`CM/storage/provider/factory.py`).

### A3 — Environnement partagé : tenants et spaces (rôle 2, C15) — **note 2**

- **Hiérarchie claire en PostgreSQL** : `Tenants` → `Workspace` → `WorkspaceMember`, invitations à jeton haché (`api/app/models/tenant_model.py:10-43`, `workspace_model.py:24-112`) ; un utilisateur appartient à un seul tenant ; `is_superuser` fait office d'administrateur ; `current_workspace_id` est un état serveur.
- **Par espace** : six emplacements de modèles par défaut (`llm`, `embedding`, `rerank`, `vision`, `audio`, `video`), `memory_config`, `retention_days`, applications et agents, bases de connaissances et leur partage inter-espaces, clés API à scopes `app | rag | memory` avec QPS et quotas journaliers, utilisateurs finaux. **Par tenant seulement** : modèles, identifiants fournisseurs, outils dont MCP, skills, marchés MCP. Quotas au niveau tenant.
- **Pas de liste blanche de capacités par espace** : l'espace ne fixe que des défauts ; tout agent peut référencer n'importe quel modèle, outil ou skill du tenant (`api/app/services/app_dsl_service.py:535`) ; la création de modèles, outils et skills ne demande qu'un membre authentifié du tenant (`model_controller.py:289-307`, `tool_controller.py:98`, `skill_controller.py:19-28`).
- **Droits** : chaîne de politiques « OU » Superuser, Owner, SelfAccess, Tenant (`api/app/core/permissions/service.py:33-38`) ; `RoleBasedPolicy` jamais branchée ; deux rôles seulement (`manager`, `member`) ; **défaut grave** : les gardes ajoutent des politiques au singleton global à chaque requête sans les retirer (`api/app/dependencies.py:507-510, 733-736`) ; côté front le garde de routes renvoie toujours `true` (`web/src/hooks/useRouteGuard.ts:24-27`). Un seul tenant en édition communautaire.
- **Console** (`web/src/routes/routes.json`, menus `manage.json` et `space.json`) : niveau tenant `/model`, `/space`, `/tool` (intégrés, OpenAPI, MCP, marché, workflow), `/skills`, `/user-management`, `/ontology`, `/pricing` ; niveau espace `/member`, `/space-config`, `/api-key`, `/knowledge-base`, `/application`, mémoire, `/prompt`.

**Justification.** Le modèle de données et l'UX de la console sont réels et réutilisables ; mais ce qui fait une console de droits et capacités, la liste blanche par espace, l'application à l'exécution et l'audit, est absent, et le contrôle d'accès est défectueux.

### A4 — Agents et orchestration — **non évalué**

La plateforme contient agents, workflows, multi-agents et sandbox e2b ; hors des deux rôles examinés, non instruit.

### A5 — Mémoire et connaissances : post-traitement de Cognee (rôle 1, C7) — **note 2**

- **Science du pipeline, solide.** Élagage LLM ; découpage ; extraction orchestrée (`CM/storage_services/extraction_engine/extraction_pipeline_orchestrator.py`) : énoncés avec **ancrage temporel bitemporel** résolu depuis `dialog_at` (`valid_at`, `invalid_at`, `graph_models.py:170, 332-334`), classification FACT / OPINION, STATIC / DYNAMIC / ATEMPORAL par trois BERT avec repli LLM, triplets par énoncé (un appel LLM par énoncé), émotion, embeddings, déduplication déterministe puis LLM ; écriture Neo4j ; résumé épisodique ; regroupement par propagation de labels inspirée de Zep avec nommage LLM des communautés. **Réflexion Layer2** (`reflection_engine/layer2_inspector.py:315-2342`) : fusion d'alias (seuil 0,9), synthèse de descriptions et chronologie, résolution des références. **Insights** à huit facettes (`CM/analytics/memory_insight.py`). Mémoire affective et perceptive (image, vidéo, audio).
- **Oubli** : planifié, suppression logique pilotée par quota, formule G/T dont les poids valent « 0·G + 1·T », soit **l'âge seul** (`forgetting_engine/forget_service.py:148`), audité (`ForgetLog`) et réversible ; ACT-R seulement sur déclenchement manuel, **l'enregistrement des accès en lecture est commenté** et le cycle planifié désactivé (`api/app/repositories/neo4j/graph_search.py:60-100`, `celery_app.py`).
- **Modèle** : 13 labels de nœuds, 14 types de relations, **13 prédicats d'ontologie en libellés chinois** (`CM/utils/data/ontology.py:23-38`), provenance énoncé → morceau → dialogue, pas de confiance stockée sur les triplets, cloisonnement tenant → workspace → `end_user_id`.
- **Ontologie** : import et export OWL / TTL (`ontology_api_controller.py:300, 324`), types importés guidant l'extraction : compatible avec l'ontologie maintenue de Cognee.
- **Multilingue, bloquant** : `detect_memory_language` ne renvoie que `zh` ou `en` avec repli sur `zh` (`CM/utils/language_utils.py:36-60`) : **un texte français est traité avec les prompts chinois**.
- **Cognee → MemoryBear** : aujourd'hui seulement en réinjectant la sortie de `recall` comme messages `role:user`, donc ré-extraction LLM, pas consolidation. Pour consolider des triplets, il faut **écrire** un endpoint d'ingestion qui convertit l'export Cognee en `MemoryGraphWriteCommand` (`CM/storage/models/graph_write.py`) et appelle `dedup_step`, `WriteRouter.save_memory_graph` puis Layer2 et l'oubli.
- **MemoryBear → Cognee ou OKF** : exportateur batch à écrire (Cypher, en excluant `delete_at`). Correspondance OKF : `type` = label, `title` = nom ou énoncé, `sources` = ref du dialogue, `generated` = `created_at`, `stale_after` = `invalid_at`, `status` = actif ou oublié, `verified` = issu de la réflexion. Aucun Markdown ni frontmatter en sortie aujourd'hui.

**Justification.** La science vaut 3, les interfaces d'échange avec Cognee valent 1 ; la note 2 reflète qu'en post-traitement, MemoryBear est une **source de logique et de prompts à réutiliser**, pas un service branchable.

### A6 — Outillage et extensibilité — **note 2**

Outils intégrés, OpenAPI, MCP, workflow publié comme outil ; skills réduites à une ligne en base sans manifeste ni versionnement, `is_public` rendant une skill visible par **tous les tenants** ; « plugins » n'est que le chargeur d'édition community / enterprise ; sandbox Rust et e2b pour l'exécution de code.

### A7 — Modèles et routage LLM — **note 2**

Fournisseurs OpenAI-compatible, DashScope, Ollama, Xinference, GPUStack, Bedrock, Volcano (`packages/redbear-model/src/redbear_model/contracts.py:296`) ; catalogue global, config par tenant, canaux, identifiants chiffrés AES-GCM sous `MODEL_CREDENTIALS_KEY` ; pas de routage ; BERT externes non publiés ; benchmarks du README non reproductibles (images seulement, pas de harnais).

### A8 — Fichiers et ressources — **note 1**

Base de connaissances documentaire séparée dans Elasticsearch ; export de graphe plafonné ; rien de compatible S3 ou SeaweedFS relevé.

### A9 — Identité, secrets, politiques — **note 1**

Mot de passe local et JWT HS256 sous `SECRET_KEY`, liste noire Redis (un échec Redis donne 401) ; **aucun OIDC ni Keycloak**, SSO dans `premium.sso` absent ; identity-service émet des JWKS RS256 pour des jetons internes non tournés et gère une ACL service-à-service ; gateway communautaire en simple transmission. Réutilisable : `packages/auth-sdk` (`TokenVerifier` JWKS par `kid`, `AclMatcher`). Pas d'OpenBao ; pas d'API de politique interrogeable « U peut-il utiliser M / T / K dans S ? ».

### A10 — Interopérabilité standards — **note 2**

OpenAPI avec contrôle de ruptures, MCP serveur minimal, OWL / TTL ; pas d'A2A.

### A11 — Intégration services in-house — **note 1**

Rien ; connecteurs orientés écosystème chinois.

### A12 — Qualité d'ingénierie et pérennité — **note 1**

Cœur mémoire sans test, pas de CI pytest, ni mypy ni ruff, monolithe, README contredit par le code (« 12 types », « Neo4j 4.4+ » alors que les index vectoriels exigent 5.x) ; actif et Apache 2.0.

### A13 — Déployabilité on-premise — **note 1**

docker-compose (API, ~9 workers Celery, sandbox) et `e2b-infra` ; pas de Helm alors qu'identity et gateway supposent Kubernetes ; **quatre stores obligatoires**.

**Inventaire des stores (contrainte de stack).**

| Store | Usage | Verdict | Résorption par fork |
|---|---|---|---|
| PostgreSQL | tenants, espaces, modèles, outils, skills, clés, messages bruts, ontologie, outbox, journaux | conforme | — |
| **Neo4j + APOC + GDS** | maître du graphe et de toutes les écritures ; 159 constantes Cypher (`cypher_queries.py`, 3 458 lignes), 36 fichiers avec Cypher en ligne, `Neo4jConnector` dans 66 fichiers ; `elementId()` ×116, APOC ×23, GDS ×4, index full-text et vectoriels ×16 | **écart majeur** | `FalkorClient` via `BackendFactory.register` ; réécrire ~160 requêtes (`elementId` → `id()`, index `db.idx.*`, APOC → Python, GDS → pageRank FalkorDB ou désactivation) ; **3 à 6 semaines-personne sans filet de tests** ; ~70 % portable mécaniquement |
| **Elasticsearch** | lecture mémoire par défaut (`MEMORY_READ_BACKEND=ELASTIC`) via outbox PostgreSQL ; RAG documentaire et son graphe | **écart** | mémoire : facile, `MEMORY_READ_BACKEND=NEO4J` ou FalkorDB et outbox neutralisée ; RAG : lourde mais inutile, Cognee fait la RAG |
| **Redis** | broker et backend Celery, caches, files d'attente de conversations, pub/sub d'invalidation, verrous Lua, sessions, ACL, audit ; 58 fichiers | **écart** | broker remplaçable (amqp) ; le reste suppose Redis : migration vers PostgreSQL difficile |
| embeddings | propriétés des nœuds Neo4j, dupliqués dans ES ; pas de pgvector | — | suivent le graphe |

## 4. Les deux rôles, verdicts

### Rôle 1 — post-traitement de Cognee

- **Réutilisable tel quel** : prompts et étapes d'extraction temporelle et de triplets, logique Layer2 (déduplication, alias, synthèse, résolution), insights à huit facettes, modèles Pydantic, formules d'oubli (`CM/storage_services/`), import d'ontologie OWL / TTL.
- **À écrire** : l'ingestion de triplets depuis Cognee, l'exportateur Cypher → OKF ou → `remember`, la détection de langue française.
- **À forker** : le provider FalkorDB, Elasticsearch désactivé, Redis conservé ou remplacé.
- **Chemin le moins coûteux** : un batch qui exporte Cognee vers `/v1/memory/write` en messages `user`, puis un exportateur vers OKF ; le MCP (deux outils) ne sert qu'au flux en ligne.
- **Verdict** : MemoryBear n'est pas branchable derrière Cognee ; il est une **carrière de logique de consolidation** à transplanter dans un post-traitement écrit autour de Cognee et FalkorDB, où l'ontologie, les données et le graphe restent uniques. Transplanter la logique coûte moins que porter MemoryBear.

### Rôle 2 — console d'administration des spaces (C15)

- **Non utilisable tel quel** comme console gouvernant Harbor, DSH et Cognee : c'est la console *de* MemoryBear, sans liste blanche de capacités par espace, sans API de politique, sans OIDC, sans audit des actions d'administration, et imbriquée dans le moteur mémoire (créer un espace crée aussi des scènes d'ontologie et une configuration mémoire, `workspace_service.py:939-1118`).
- **Ce qu'il faudrait** : une table espace ↔ capacité, une API de politique et des jetons à scopes, Keycloak en fournisseur d'identité via `auth-sdk`, OpenBao, un vrai RBAC, l'extraction du plan d'administration en service PostgreSQL seul (~15 tables, ~10 contrôleurs, suppression du démarrage Neo4j / ES / Celery, remplacement de Redis pour les sessions). De l'ordre de plusieurs mois-personne.
- **Verdict** : y puiser **le modèle de données et l'UX** (tenant, espace, membre, invitations, clés API à scopes et quotas, six emplacements de modèles par espace, marchés MCP) pour concevoir la console Symbiot, plutôt que l'adopter.
- **État de fait (précisé le 2026-10-15)** : l'UX de MemoryBear a déjà été reprise, pas le back-office. C'est cohérent avec ce verdict : la console Symbiot garde l'UX et reçoit un back-office neuf sur PostgreSQL et Keycloak, avec la liste blanche par espace et l'API de politique que MemoryBear n'a pas. La position de MemoryBear reste incertaine ; elle est à trancher au §8 du comparatif.

## 5. Forces, faiblesses, risques

**Forces**
1. Extraction bitemporelle soignée et provenance énoncé → morceau → dialogue ; réflexion Layer2 et insights réutilisables comme logique de consolidation ; oubli audité et réversible ; ontologie OWL / TTL compatible Cognee.
2. Modèle tenant → espace → membre complet, clés API d'espace à scopes et quotas, gestion multi-fournisseurs des modèles et des marchés MCP, console riche.
3. Amorces réutilisables : `auth-sdk` (JWKS, ACL), identity-service (snapshots, audit en flux), OpenAPI contrôlée en CI, Apache 2.0.

**Faiblesses**
1. Quatre stores imposés dont Neo4j avec APOC et GDS massivement couplé : écart de stack le plus lourd du dossier.
2. Ingestion limitée aux conversations, pas d'export structuré ni Markdown ; MCP à deux outils ; français traité comme du chinois ; BERT non publiés.
3. Aucune autorisation de capacités par espace, identité fermée, contrôle d'accès défectueux, cœur mémoire sans test, modules réels d'entreprise absents.

**Risques**
- Projet piloté par un éditeur avec des modules privés : la version communautaire est tronquée (SSO, gateway, multi-tenant).
- Volume : 320 k lignes pour un rôle de post-traitement ; le fork porterait un poids sans rapport avec l'usage.

## 6. Tableau des notes (indicatif, A4 non évalué, total sur 56)

| Axe | Note | Pondération | Contribution |
|---|---|---|---|
| A0 ressources tierces et lisibilité | 2 | ×2 | 4 |
| A1 propriété des données | 2 | ×1 | 2 |
| A2 séparation | 1 | ×1 | 1 |
| A3 tenants et spaces (C15) | 2 | ×1 | 2 |
| A4 agents | n.é. | — | — |
| A5 mémoire, post-traitement de Cognee (C7) | 2 | ×1 | 2 |
| A6 extensibilité | 2 | ×1 | 2 |
| A7 modèles | 2 | ×1 | 2 |
| A8 fichiers | 1 | ×1 | 1 |
| A9 identité et secrets | 1 | ×1 | 1 |
| A10 standards | 2 | ×1 | 2 |
| A11 services in-house | 1 | ×1 | 1 |
| A12 qualité | 1 | ×1 | 1 |
| A13 déployabilité | 1 | ×1 | 1 |
| **Total** | | sur 56 | **22** |
