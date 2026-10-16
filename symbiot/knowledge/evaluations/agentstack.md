---
type: Évaluation
title: Évaluation Agent Stack
description: Conversion OKF du document de travail 02c-fiche-agentstack.md du dossier docs/symbiot (cycle des 15 et 16 octobre 2026).
tags:
  - core
  - a2a
  - identité
  - k3s
sources:
  - resource: /deprecated/2026-10-15/02c-fiche-agentstack.md
generated:
  by: claude-fable-5.1/session-01MK6
  at: 2026-10-16T18:00:00+02:00
status: stable
stale_after: 2027-01-16T00:00:00+02:00
---

# Évaluation Agent Stack

**Dépôt :** `tauziet40/agentstack`, clone local `/home/user/tauziet40/agentstack`, HEAD `79c7860` (instantané d'environ six mois, version 0.7.2)
**Statut d'origine :** version de travail du 2026-10-15, issue de la lecture du code par agents d'exploration ; chaque constat cite un fichier
**Référentiel :** [01-architecture-cible-symbiot.md](/conventions/architecture-cible.md). **Nature différente des clients :** Agent Stack est une plateforme serveur qui héberge et expose des agents. La grille A0–A13 est appliquée telle quelle, avec l'interprétation indiquée par axe ; le total n'est pas comparable à ceux des clients, il sert à situer la plateforme face à la cible.

Chemins relatifs à `/home/user/tauziet40/agentstack`. `$S` désigne `apps/agentstack-server/src/agentstack_server`, `$K` désigne `apps/agentstack-sdk-py/src/agentstack_sdk`.

---

## 1. Identité

| | |
|---|---|
| Nature | « Open infrastructure for turning AI agents into running services » : runtime et registre d'agents exposés en A2A, passerelle LLM compatible OpenAI, fichiers S3, vecteurs, connecteurs MCP avec OAuth, UI, CLI, SDK |
| Stack | serveur FastAPI Python 3.14 (`apps/agentstack-server`), UI Next.js avec next-auth OIDC (`apps/agentstack-ui`), CLI Python (`apps/agentstack-cli`), SDK Python et TypeScript, thème Keycloak, `supergateway` stdio→HTTP, image VM MicroShift pour le dev local ; Helm pour le déploiement |
| Licence | Apache 2.0 ; projet de la série LF Projects « BeeAI », badge LF AI & Data, 13 mainteneurs (`MAINTAINERS.md`) |
| Tests | serveur 243 fonctions (53 unit, 86 integration, 104 e2e) ; SDK Python 48 ; SDK TS 1 ; UI 0 ; CLI aucun |
| Stabilité | pré-1.0 ; les connecteurs MCP sont documentés sous « experimental » ; ruptures d'API consignées dans un changelog (`CLAUDE.md`) |

## 2. Architecture en bref

- **Un agent est une image conteneur** avec une entrée Python qui lance le serveur A2A du SDK sur le port 8000 (`agents/chat/Dockerfile`, `agents/rag/src/rag/agent.py:326-337`). Le registre `agent-registry.yaml` n'est qu'une liste `providers: - location: <image>` avec `auto_stop_timeout_sec` et `variables` (`$S/domain/models/registry.py:40-63`), synchronisée par cron.
- **Exécution sur Kubernetes seulement**, via kr8s : le serveur crée Deployment, Service et Secret depuis des templates (`$S/bootstrap.py:93-121`, `helm/templates/config/provider_templates.yaml`) ; scaling binaire 0 ou 1 replica, montée au premier appel et descente après inactivité (`$S/service_layer/services/a2a.py:400-447`). Builds d'images depuis GitHub par Kaniko ou BuildKit.
- **Agents « unmanaged »** enregistrés par URL : la plateforme lit `/.well-known/agent-card.json` et fait proxy (`$S/domain/models/provider.py:93-194`, `docs/stable/deploy-agents/a2a-agents.mdx`).
- **Le serveur est un proxy A2A** (`/api/v1/a2a/{provider_id}`, JSON-RPC et REST, carte réécrite, `$S/api/routes/a2a.py:31-140`) et expose les familles `/api/v1/` : user, users, providers, provider_builds, model_providers, configurations, files, variables, contexts (avec `/token`, `/history`), openai, vector_stores, user_feedback, connectors, `/.well-known`.
- **Architecture en ports et adaptateurs** (Protocols et injection) : `IVectorDatabaseRepository`, `IObjectStorageRepository`, `IEnvVariableRepository`, `ICacheFactory`, `ITextExtractionBackend`.

## 3. Évaluation par axe

### A0 — Exploitation de ressources tierces et lisibilité des connexions (×2) — **note 3**

Interprétation : comment les agents hébergés consomment des ressources externes, et comment on le voit.

- **Injection de services par extensions A2A** (`$K/a2a/extensions/services/`) : `llm` (renvoie `api_base`, `api_key`, `api_model` compatibles OpenAI), `embedding`, `mcp`, `form`, `platform_api` (jeton de contexte pour fichiers et vector stores), `platform-self-registration`. L'agent déclare une **demande** (`MCPServiceExtensionSpec.single_demand(suggested=("github",))`, transports streamable_http ou stdio, `services/mcp.py:79-130`) et le client la satisfait. L'agent est ainsi découplé de ses dépendances.
- **Connecteurs MCP de la plateforme** : OAuth authorization code géré par le serveur (découverte des métadonnées, DCR, callback, refresh, révocation, `$S/service_layer/services/external_mcp_service.py:46-300`), machine à états created → auth_required → connected → disconnected, connexions **par utilisateur**, proxy `GET|POST /api/v1/connectors/{id}/mcp` qui injecte le Bearer ou les en-têtes stockés (`$S/api/routes/connectors.py:116-124`, `services/connector.py:328-380`). Presets `mcp+stdio` déployés en pods derrière supergateway. Enregistrement par API, CLI (`agentstack connector create|connect|…`) ou Helm (`connector.presets`, `helm/values.yaml:465-485`).
- **Cognee et le MCP OKF (I5)** : se déclarent comme connecteurs ; tout agent qui demande `mcp` les reçoit à travers le proxy, avec l'identité de l'utilisateur. Aucun code côté plateforme.
- **Limites** : fonction **expérimentale**, UI des connecteurs désactivée par défaut (`features.uiConnectors: false`, `helm/values.yaml:19`), appariement par simple égalité de nom avec un TODO « randomly pick the latest connector » (`build-fulfillments.ts:122-151`), pas de catalogue d'outils agrégé, **aucune exposition MCP** des agents ou des outils.
- **Lisibilité** : état et `disconnect_reason` exposés (`routes/connectors.py:141-160`), webhooks `connector.created/updated/deleted`, OpenTelemetry sur FastAPI, httpx, SQLAlchemy et OpenAI (`$S/telemetry.py:83-98`).

**Justification.** Le découplage par demandes et le proxy OAuth par utilisateur sont exactement la forme attendue pour exploiter des ressources tierces de façon lisible ; le statut expérimental et l'absence d'exposition MCP retiennent la note à 3.

### A1 — Propriété des données (interprétation : auto-hébergement, absence de cloud éditeur) — **note 3**

- Entièrement auto-hébergé, aucun service cloud de l'éditeur ; télémétrie OTLP vers un collecteur local, Phoenix optionnel (licence ELv2) désactivable (`helm/values.yaml:552-597`).
- Données cloisonnées par utilisateur : contexts, files, vector stores, variables et connecteurs sont des « User-Private Entities » (`docs/development/custom-ui/permissions-and-tokens.mdx`).
- Non applicable au poste de travail : ce n'est pas un client.

### A2 — Séparation des composants — **note 3**

Serveur, UI, CLI et SDK séparés, API REST et A2A documentées, OpenAPI publiée ; les workers procrastinate tournent dans le processus serveur (`$S/application.py:218`).

### A3 — Environnement partagé — **note 1**

- **Aucune notion de workspace, space, organisation ou tenant** ; toutes les requêtes filtrent sur `user_id` (`$S/service_layer/services/contexts.py:53-138`, `files.py:153-204`). Le « partage » est la copie d'un lien d'agent (`AgentShareButton.tsx`). Pas de collaboration sur une conversation.
- Seuls les agents et les fournisseurs de modèles sont globaux à l'instance.
- Pour I3, Harbor reste indispensable ; Agent Stack n'y contribue pas.

### A4 — Agents autonomes et orchestration — **note 3**

- Tout agent est un serveur A2A (décorateur `@server.agent`, tous les champs d'Agent Card, `$K/server/agent.py:78-185`) ; tâches, streaming, push notifications, artefacts via a2a-sdk 0.3.24 ; TaskStore en mémoire par défaut, `PlatformContextStore` persistant via la plateforme.
- Extensions d'interaction : `approval` (`interactions/approval.py:104`) et acceptation ou refus d'un appel d'outil MCP (`tools/call.py:73`), `trajectory`, `citation`, `form_request`, `canvas`, `settings`, `error`.
- Cycle de vie : managés (scale-to-zero) ou unmanaged ; `agentstack add|update|logs|run` ; agents de référence chat, rag, canvas, form, langgraph-reflection, deepagents_content_builder.
- **Limites** : pas de bac à sable dédié (un pod par agent et une NetworkPolicy d'exemple, `policy.yaml`), pas d'orchestration multi-agents côté plateforme (elle est dans le framework), **rien pour un harness non Python** : DSH ou Hermes doivent être enveloppés par un wrapper Python en sous-processus ou exposer eux-mêmes un serveur A2A puis être enregistrés unmanaged. Les agents sont des serveurs passifs, pas des clients d'un espace partagé : être membre actif de Harbor demande un adaptateur côté Harbor.

### A5 — Mémoire et connaissances — **note 1**

- Vector store pgvector seulement : une table `HALFVEC` par dimension avec index HNSW (`$S/infrastructure/vector_database/vector_db.py:43-86`) ; **bug probable** : index créé en `halfvec_l2_ops` (l. 82) alors que la recherche utilise `cosine_distance` (l. 186, 199), l'index ne serait donc pas utilisé. Indexation faite côté agent (Docling, découpage LangChain, embeddings par le proxy, `PUT /vector_stores/{id}`), recherche par vecteur seul.
- **Ni mémoire, ni graphe, ni OKF.** Cognee reste le fournisseur, branché en connecteur MCP. `IVectorDatabaseRepository` existe mais est instancié en dur dans l'unité de travail (`$S/infrastructure/persistence/unit_of_work.py:87`).

### A6 — Outillage et extensibilité — **note 3**

- Extensions A2A propriétaires (`https://a2a-extensions.agentstack.beeai.dev/...`) pour UI, services, auth, interactions ; SDK Python et TS ; enveloppement d'agents LangGraph, CrewAI ou Python quelconque (`docs/stable/deploy-agents/wrap-existing-agents.mdx`), skill `skills/agentstack-wrapper/SKILL.md` **limitée au Python** ; presets de connecteurs ; 16 catégories d'exemples.
- **Distance à Cordis** : pas de plugin tree ; l'extensibilité est par SDK, extensions et composants remplaçables derrière des Protocols. Un client tiers doit implémenter les extensions pour satisfaire les demandes LLM et MCP.

### A7 — Modèles et routage LLM — **note 2**

- Proxy compatible OpenAI (`/api/v1/openai/chat/completions`, `/embeddings`, `/models`) sur 22 types de fournisseurs dont Ollama, OpenRouter, watsonx, Bedrock, **DeepSeek** (`$S/domain/models/model_provider.py:24-46`) ; rate limit par rôle en jetons et requêtes.
- **Le « LLM routing » annoncé est marketing** : fournisseur déduit de l'identifiant du modèle, choix par correspondance floue difflib avec les modèles suggérés par l'agent (`model_providers.py:250-308`) ; ni politique, ni coût, ni repli, ni équilibrage.
- **Point d'insertion du routeur Symbiot (C11) : le proxy OpenAI lui-même**, un seul endroit pour tous les agents hébergés, avec l'identité de l'utilisateur et le rôle.

### A8 — Fichiers et ressources — **note 3**

- Client `aioboto3` avec endpoint, clés, bucket, région, SSL configurables (`$S/infrastructure/object_storage/repository.py:33-42`) ; **SeaweedFS déjà embarqué dans le chart** en mode all-in-one, S3 sur le port 9009, bucket `agentstack-files` (`helm/Chart.yaml:17-20`, `values.yaml:680-720`) ou S3 externe ; URLs présignées 1 h ; quotas 1 GiB par utilisateur et 100 MiB par fichier ; extraction Docling optionnelle en tâche asynchrone.
- Fichiers privés par utilisateur : pas de partage à une organisation.

### A9 — Identité, secrets, politiques — **note 3**

- **Keycloak intégré au chart et activé par défaut** (`helm/values.yaml:155-233`) : job de provisioning qui crée le realm `agentstack`, les rôles `agentstack-admin` et `agentstack-developer`, les clients server, ui (confidentiel) et cli (public, PKCE), les mappers d'audience (`templates/keycloak/provision-job.yaml:41-131`). **OIDC externe possible** via `externalOidcProvider` avec `rolesPath` (`values.yaml:248-259`). Keycloak utilise le même PostgreSQL.
- Validation côté serveur (`$S/api/auth/auth.py`) : découverte RFC 8414 puis OIDC, JWKS en cache 15 min, validation de `iss` et `aud`, repli sur l'introspection pour les jetons opaques, userinfo si l'email manque.
- Agents → plateforme : **context tokens**, JWT RS256 internes de 20 min limités à un contexte et à des permissions, validés par l'agent avec la JWKS de la plateforme (`$S/api/routes/contexts.py:108-138`, `$K/server/middleware/platform_auth_backend.py:62-80`).
- Secrets : table polymorphe `variables` chiffrée en Fernet avec `encryptionKey`, stockage annoncé remplaçable derrière `IEnvVariableRepository` (get, get_all, update, delete, `$S/domain/repositories/env.py:19-43`) : **adaptateur OpenBao faisable, effort moyen** (sortir le repository de l'unité de travail transactionnelle). Variables d'agent injectées en Secrets Kubernetes.
- **Faiblesses** : utilisateur identifié par l'**email** et non par `sub`, créé automatiquement ; aucun tenant ; provisioning avec `redirectUris=["*"]`, `webOrigins=["*"]` et direct access grants ; **jetons OAuth des connecteurs MCP stockés en JSON non chiffré** (`$S/infrastructure/persistence/repositories/connector.py:31`) ; mots de passe par défaut faibles ; pas de clés API utilisateur. `policy.yaml` est une NetworkPolicy Kubernetes d'exemple, pas une politique applicative.

### A10 — Interopérabilité standards — **note 3**

- A2A famille 0.3.x (a2a-sdk 0.3.24, `@a2a-js/sdk ^0.3.10`), transports JSON-RPC et REST, cartes réécrites par le proxy, guide de migration ACP → A2A ; OIDC ; OpenAPI publiée ; webhooks sortants.
- Extensions A2A propriétaires ; aucune exposition MCP ; versionnage des agents par tag Docker résolu en digest, carte embarquée dans un label d'image, champ `version` libre.

### A11 — Intégration services in-house — **note 1**

Presets de connecteurs Stripe, Box, GitHub ; rien pour Nextcloud, IMAP, CalDAV ou WebDAV. Tout passe par des connecteurs MCP à fournir.

### A12 — Qualité d'ingénierie et pérennité — **note 3**

Monorepo mise, uv, pnpm ; typage pyrefly et ruff, `py.typed` ; 243 tests serveur ; docs Mintlify avec OpenAPI et changelog des ruptures ; gouvernance LF ; **mais** UI et CLI sans tests, pré-1.0, instantané ancien (activité non mesurable sur le clone).

### A13 — Déployabilité on-premise — **note 2**

- Chart Helm complet : sous-charts Bitnami postgresql, seaweedfs, phoenix, redis ; templates server, ui, keycloak, docling, collector, registry, managed-mcp, RBAC ; Alembic 36 versions en initContainer avec pgvector ; configuration pydantic-settings.
- **Kubernetes obligatoire, même en local** : `agentstack platform start` lance une VM Lima ou WSL avec MicroShift, 4 Go minimum ; **aucun docker-compose** ; Keycloak demande 1,7 Gi ; compter 3 à 4 Go sans les agents. La documentation qualifie l'auth « basic » de « intended for development ».

**Inventaire des stores (contrainte de stack).**

| Store | Usage | Verdict | Résorption |
|---|---|---|---|
| PostgreSQL 17 + pgvector | état métier, vecteurs (schéma `vector_db`), file de jobs procrastinate, suivi A2A, **et Keycloak** (schéma dédié) | **conforme** | — |
| SeaweedFS S3 | fichiers | **conforme, déjà la cible** | — |
| Redis (optionnel, désactivé par défaut) | stockage du rate-limiter (`limits`) et cache de la liste des modèles (TTL 1 j) ; obligatoire si `replicaCount > 1` (`helm/templates/_validators.tpl:68-82`) | écart mineur | cache derrière `ICacheFactory` → table UNLOGGED avec TTL (1 jour) ; rate-limit → `Storage` PostgreSQL à écrire ou `MemoryStorage` mono-replica ; **2 à 4 jours** |
| Phoenix (optionnel) | traces LLM, SQLite, licence ELv2 | hors cible | désactiver, exporter en OTLP ailleurs |
| Registre Docker local (optionnel) | images buildées | sans objet | — |

Aucune file ni pub/sub sur Redis : la file est déjà dans PostgreSQL.

## 4. Points d'insertion pour la cible

| Cible | Où | Effort |
|---|---|---|
| Cognee MCP, MCP OKF (I5) | connecteurs de la plateforme (preset Helm ou `agentstack connector create`), consommés par demande `mcp` | nul |
| Keycloak (C13) | natif ; `externalOidcProvider` pour un Keycloak existant ; corriger `redirectUris` et l'identification par email → `sub` | faible |
| OpenBao (C14) | adaptateur `IEnvVariableRepository` ; chiffrer `connectors.auth` | moyen |
| A2A (C9) | natif ; agents externes unmanaged ; DSH ou Hermes via wrapper Python ou leur propre serveur A2A | faible à moyen |
| Routeur LLM (C11) | proxy `/api/v1/openai` | faible à moyen |
| SeaweedFS (C8) | natif | nul |
| Harbor, agents membres (I3) | adaptateur côté Harbor : connecteur `connectors/agentstack/` appelant le proxy A2A ; ou Harbor exposé en connecteur MCP consommé par les agents | moyen |
| Centaur (I4) | recouvrement fonctionnel, voir §5 | décision |
| Rowboat (client) | client A2A vers `/api/v1/a2a/{provider_id}/` avec Bearer Keycloak, REST pour contexts et files, jeton de contexte pour satisfaire les demandes LLM et MCP (`docs/stable/custom-ui/`) | moyen |

## 5. Position entre Harbor et Centaur

- **Harbor** : quasi aucun recouvrement ; Agent Stack n'a pas d'espace partagé et ne peut pas le remplacer.
- **Centaur** : recouvrement large. Les deux hébergent des agents partagés à l'échelle de l'instance, sur PostgreSQL et Kubernetes, avec des sessions persistées (contexts chez Agent Stack, sessions par `thread_key` chez Centaur). Agent Stack apporte A2A natif, Keycloak, la passerelle LLM, les fichiers et les vecteurs ; Centaur apporte les sandboxes d'exécution, l'ingress Slack, les workflows durables Absurd et l'injection de credentials par iron-proxy, mais sans OIDC générique. **Le choix entre les deux, ou leur articulation (Agent Stack comme runtime A2A et registre, Centaur comme messagerie inter-espaces et sandboxes), est une décision d'architecture serveur à prendre au §8 du comparatif.**

## 6. Forces, faiblesses, risques

**Forces**
1. Conformité de stack quasi native : PostgreSQL pour tout, y compris la file de jobs et Keycloak ; SeaweedFS dans le chart ; Redis optionnel.
2. A2A de bout en bout : Agent Card, proxy authentifié, agents unmanaged, extensions d'approbation et d'appel d'outil ; c'est la brique C9 qui manque partout ailleurs.
3. Découplage des ressources tierces par demandes et connecteurs OAuth par utilisateur, derrière des Protocols remplaçables (secrets, cache, fichiers, vecteurs).

**Faiblesses**
1. Aucun espace partagé ni organisation ; identité par email ; sécurité « development-grade » (jetons MCP en clair, `redirectUris=*`, mots de passe par défaut).
2. Kubernetes obligatoire jusque sur le poste du développeur ; empreinte mémoire ; pas de bac à sable d'exécution.
3. Fonctions survendues : « LLM routing » sans politique, RAG minimal avec index probablement inutilisé, MCP expérimental et caché ; rien pour un harness non Python.

**Risques**
- Pré-1.0 avec ruptures d'API consignées ; l'instantané évalué date d'environ six mois.
- Extensions A2A propriétaires : un client qui n'est pas l'UI d'Agent Stack doit les réimplémenter.

## 7. Tableau des notes (indicatif, plateforme serveur)

| Axe | Note | Pondération | Contribution |
|---|---|---|---|
| A0 ressources tierces et lisibilité | 3 | ×2 | 6 |
| A1 propriété des données (auto-hébergement) | 3 | ×1 | 3 |
| A2 séparation | 3 | ×1 | 3 |
| A3 environnement partagé | 1 | ×1 | 1 |
| A4 agents | 3 | ×1 | 3 |
| A5 mémoire et connaissances | 1 | ×1 | 1 |
| A6 extensibilité | 3 | ×1 | 3 |
| A7 modèles | 2 | ×1 | 2 |
| A8 fichiers | 3 | ×1 | 3 |
| A9 identité et secrets | 3 | ×1 | 3 |
| A10 standards | 3 | ×1 | 3 |
| A11 services in-house | 1 | ×1 | 1 |
| A12 qualité | 3 | ×1 | 3 |
| A13 déployabilité | 2 | ×1 | 2 |
| **Total** | | sur 60 | **37** |
