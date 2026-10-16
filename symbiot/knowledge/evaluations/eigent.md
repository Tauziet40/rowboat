---
type: Évaluation
title: Évaluation Eigent
description: Conversion OKF du document de travail 03-fiche-eigent.md du dossier docs/symbiot (cycle des 15 et 16 octobre 2026).
tags:
  - inspirant
  - gouvernance
sources:
  - resource: /deprecated/2026-10-15/03-fiche-eigent.md
generated:
  by: claude-fable-5.1/session-01MK6
  at: 2026-10-16T18:00:00+02:00
status: stable
stale_after: 2027-01-16T00:00:00+02:00
---

# Évaluation Eigent

**Dépôt :** `tauziet40/eigent`, clone local `/home/user/eigent`, HEAD `98ce9fb` (2026-10-14)
**Statut d'origine :** version de travail du 2026-10-15, issue de la lecture du code par agents d'exploration ; chaque constat cite un fichier
**Référentiel :** [01-architecture-cible-symbiot.md](/conventions/architecture-cible.md) (axes A0–A13, intégrations I1–I5, composants C1–C14) ; interfaces serveur dans [annexe A](/interfaces/interfaces-serveur.md)

Chemins relatifs à `/home/user/eigent`.

---

## 1. Identité

| | |
|---|---|
| Nature | Application de bureau « Cowork » multi-agents, construite sur CAMEL-AI |
| Stack | Electron + React + TypeScript (`src/`, `electron/`) ; « Brain » Python FastAPI sur CAMEL (`backend/`) ; serveur de contrôle optionnel FastAPI + PostgreSQL + Celery + Redis (`server/`) |
| Licence | Apache 2.0 (`LICENSE`), mais `package.json:7` déclare MIT : incohérence à lever avant tout fork |
| Taille | `src` 698 fichiers TS/TSX (~189 k lignes), `backend/app` 295 fichiers Python (~128 k), `server/app` 179 (~23 k), `electron` 51 (~17 k) |
| Tests | `backend/tests` 211 fichiers (~101 k lignes), vitest 356 fichiers, `server/tests` 23 fichiers non exécutés en CI |
| Activité | clone shallow : 50 commits depuis le 2026-10-02, 46 du même auteur ; PR jusqu'à #2054 |
| Dépendance clé | `camel-ai[eigent]==0.2.91a7` (backend) et `camel-ai==0.2.90a6` (serveur) : deux préversions figées et divergentes (`backend/pyproject.toml:9`, `server/pyproject.toml:10`) |

## 2. Architecture en bref

Trois tiers (`electron/main/init.ts:217-231, 385-539`) :

1. **Electron + React** : interface, gestion du processus Python (spawn de `uvicorn` sur un port 5001–5050, port transmis par IPC), `uv`, Python 3.11 préconstruit, Git et Node embarqués, coffre de secrets `safeStorage`, OAuth, mises à jour.
2. **Brain Python** : agents CAMEL (Workforce ou mono-agent), toolkits, MCP, mémoire, journal des runs en SQLite, git de workspace. Le front lui parle en HTTP, SSE et WebSocket, avec une capacité aléatoire en en-tête `X-Eigent-Local-Capability` (`backend/app/auth/local_control.py:17-30`). Sans elle, `NoneAuth` renvoie `user_id: "local"`.
3. **Serveur** (`server/`) : comptes, fournisseurs de modèles, centre de configuration, historique de chat, Spaces, MCP, triggers, remote control. Le Brain l'atteint par `SERVER_URL` et un Bearer utilisateur.

Terminologie (`docs/product-terminology.md`) : Space → Session (= `Project` côté backend) → Task ; un Run vit dans le journal SQLite local.

**Cloud par défaut.** `DEFAULT_SERVER_URL = 'https://dev.eigent.ai'` (`electron/main/init.ts:44, 319`) et `.env.development` pointe le cloud. La synchronisation des runs, les bundles d'environnement, le proxy de modèles, la recherche de repli et le déploiement web sont réservés au cloud Eigent, souvent gardés par le nom d'hôte `*.eigent.ai` (`backend/app/run_sync/runtime.py:47-51`). Le serveur local n'implémente pas les endpoints `workspace-bundles` que le Brain appelle (`backend/app/workspace_bundle/cloud.py:161-330`).

## 3. Évaluation par axe

### A0 — Exploitation de ressources tierces et lisibilité des connexions (×2) — **note 2**

**Constat.**
- Serveurs MCP déclarés dans `~/.eigent/mcp.json` au format standard `mcpServers` (`electron/main/utils/mcpConfig.ts:18-20`, `backend/app/service/mcp_config.py:20-21`). Client `camel.toolkits.MCPToolkit` multi-transport : stdio, SSE, streamable-http avec `headers` (`backend/app/agent/tools.py:132-195`). `MCP_REMOTE_CONFIG_DIR=~/.mcp-auth` permet l'OAuth de `mcp-remote`.
- Trois chemins pour qu'un MCP atteigne un agent : worker personnalisé (`src/components/AddWorker/index.tsx:521`), passerelle cloud `${server}/connectors/mcp` (`src/store/chatStore.ts:681-723`), Workspace Bundle `workspace.yaml` avec `spec.mcpServers[]`, `secretSlots` et secrets dans le coffre `safeStorage` (`backend/app/workspace_config/manifest.py:47`, `workspace_bundle/agent_plugins.py:1147-1195`).
- **Cognee se branche sans code** (I5) : entrée stdio `uvx cognee-mcp` ou URL distante, ou mieux un bundle streamable-http avec en-tête secret. L'agent verra `remember`, `recall`, `search`, `forget`.
- **Mais la mémoire interne n'est pas remplaçable** : `get_lightweight_memory_service()` instancie directement le service sur `SQLiteRunJournal` (`backend/app/lightweight_memory/service.py:1071`) ; `MemoryToolkit` est attaché à tous les agents (`memory_toolkit.py:535-547`) ; le bloc « Lightweight Memory » est injecté dans le prompt (`memory/service.py:107-177`). Cognee ferait doublon avec `search_memory`, `remember_project_memory`, `forget_project_memory`, avec risque de confusion de noms d'outils. En faire la mémoire de référence demande de remplacer deux fonctions.
- **Lisibilité.** Positif : JSON clair, bundle YAML relu avec diff, approbations journalisées dans `security_audit_events`, logs CAMEL sous `~/.eigent/.../camel_logs`. Négatif : **les échecs de connexion MCP sont avalés** (`tools.py:193-195`, `except → return []`), l'utilisateur ne voit rien ; un MCP distant ajouté par l'UI n'a pas d'en-tête d'authentification (`AddCustomConnectorPage.tsx:172-214`) ; trajectoires multiples (V1/V2, gateway, worker, bundle) ; deux documents de conception cités dans le code sont absents du dépôt (`docs/core/space-project-memory-local-first-design.md`, `docs/design/06-protocol.md`).

**Justification de la note.** La consommation MCP est standard et complète, mais la mémoire est soudée, les erreurs sont silencieuses et la configuration est éclatée : la connexion à Cognee est possible, pas lisible ni centrale.

### A1 — Local-first et propriété des données — **note 2**

- Sur le disque : productions sous `~/eigent/<user>/project_<id>/task_<run>/` (`backend/app/model/chat.py:208-240`) ; `~/.eigent/` avec `.env`, `run-journal.sqlite3`, `memory/`, `rag_storage`, `skills/`, `workspace/<session>/uploads`. Beaucoup de toolkits écrivent dans `~/Downloads` (`file_write_toolkit.py:86`).
- Hors ligne : « only use local models and local MCP » (`server/README_EN.md:140`) ; le journal local continue.
- Cloud par défaut (§2). En mode cloud-connected, les **clés BYOK partent vers le serveur** (`ModelConfigurationDialog.tsx:289` → `/api/v1/provider`) et y sont stockées en clair (`server/app/model/provider/provider.py:37`) ; idem pour les secrets d'outils (`/api/v1/configs`), l'historique de chat, les steps SSE et le journal complet des runs.
- Télémétrie : pas de PostHog ni Sentry ; export OTLP vers Langfuse optionnel (`workforce_metrics.py:51-57`).

**Justification.** Les données de travail sont locales et lisibles, mais le produit est conçu cloud-first : URL par défaut, synchronisation gardée par nom d'hôte, secrets envoyés au serveur.

### A2 — Séparation client / serveur — **note 3**

- Trois tiers nets avec protocoles explicites (HTTP, SSE via `@microsoft/fetch-event-source`, WebSocket) et `SERVER_URL` configurable (`electron/main/init.ts:266-350`).
- Mode web pur avec `VITE_BRAIN_ENDPOINT` et `npm run dev:web` (`src/api/http.ts:140-146`, `scripts/smoke-web-local-brain.sh`).
- Mais le Brain distant n'a pas d'authentification réelle (`NoneAuth`, hook « future JWT/API-key » dans `brain_auth.py`) et suppose un home local (`Path.home()` partout).

### A3 — Environnement partagé — **note 1**

- Un Space appartient à **un seul `user_id`** (`server/app/model/space/space.py:37-66`) : ni membres, ni ACL, ni organisation, ni tenant. Une recherche de `space_member|organization_id|team_id|tenant|collaborator` ne trouve que la config Slack.
- Overlays et apply servent à relire les écritures de l'agent avant application au dossier, pas à partager (`space_controller.py:51-380`).
- Partage de chat : lien signé `itsdangerous` donnant une relecture anonyme ; `verify_token(token, False)` **désactive le contrôle d'expiration** (`share_controller.py:40, 55`), le TTL d'un jour annoncé n'est pas appliqué.
- Pas de fils multi-humains ni de mentions (`{{@…}}` reste du texte, `UserMessageRichContent.tsx:138`). `IChannelAdapter` est un contrat sans implémentation (`backend/app/channels/interface.py`).
- `remote_control` pilote **son propre bureau** depuis le web ou le mobile (`remote_control_controller.py:573, 960, 1255`), ce n'est pas de la collaboration.

**Justification.** Tout le modèle d'espace d'organisation (I3) est à construire.

### A4 — Agents autonomes et orchestration — **note 3**

- Workforce CAMEL étendue (retry, métriques, timeouts, `backend/app/utils/workforce.py:178-241`) : coordinateur, planificateur, workers Developer, Browser, Document, Multi-Modal, agent MCP, créés en parallèle (`chat_service.py:2788-2985`). Workforce « managé » fermé sans terminal ni MCP. Harness mono-agent (`single_agent_service.py`).
- Journal des runs durable en SQLite : `runs`, `run_attempts`, `run_events` rejouables, `tool_calls`, `approvals`, `human_interactions` typées (question, choice, form, approval, diff_review, merge_conflict, credential_binding) attribuées par `actor_type` et `source` (`run_journal/store.py:298-391, 991-1047`).
- Moteur de permissions : effets allow / prompt / deny, 23 opérations, profils, tags de risque déduits des arguments (`permission_policy/engine.py:31-77`, `models.py:628-653`, `tool_actions.py:654-860`).
- Sous-agents distants : `Protocol RemoteSubAgentProvider.run → AsyncIterator[event]` (`remote_sub_agent/types.py:77-84`), registre avec **un seul fournisseur**, Gemini Interactions API ; désactivé par défaut, politique de globs interdits. Aucun adaptateur Hermes, Claude Code ou Codex comme agent.
- Hands : `IHands` (terminal, fs, mcp, browser), `SandboxHands`, `RemoteHands` « placeholder », `HttpHandsCluster` acquire / release / health en TOML.
- Triggers serveur : cron, webhook, Slack, quotas, exécution par Celery vers la session desktop.
- Description d'agent : Workspace Bundle `apiVersion: eigent.ai/v1alpha1` avec `agents`, `mcp_servers`, `connectors`, `permissions`, `skills`, lockfile (`workspace_config/models.py:572-722`) ; import Agent Plugins 1.0.0. **Aucune Agent Card A2A.**
- Point d'insertion A2A ou Hermes : un `RemoteSubAgentProviderAdapter` client A2A, un worker via `add_single_agent_worker`, et le champ `agents` du bundle.

**Justification.** Orchestration et gouvernance d'agents solides ; extension distante prévue mais embryonnaire.

### A5 — Mémoire et connaissances — **note 2**

- Deux générations : V1 `backend/app/memory` (arborescence JSON / JSONL / `summary.md` par run, quasi morte) et V2 `backend/app/lightweight_memory` (active) en tables SQLite : `memory_entries` avec `kind` (fact, decision, constraint, preference, todo, lesson), `priority`, `version`, `pinned_by_user`, `confirmed_by_user`, `source_trust` (7 valeurs), `sensitivity`, `source_refs_json`, `usage_count` ; `memory_mutations`, outbox cloud, réconciliation (`run_journal/store.py:1620-1681`). Quotas de jetons par portée (project 1024, space 640, user 384).
- Extraction conservatrice par regex (« remember… », « I prefer… », 记住) derrière un `Protocol MemoryExtractor` remplaçable (`maintainer.py:186-266`). Recherche par intersection lexicale, sans embeddings.
- Qdrant : dépendance obligatoire (`backend/pyproject.toml:23`) mais utilisé par le seul `RAGToolkit`, local sous `~/.eigent/rag_storage`, masqué dans l'UI, dépendant d'`OPENAI_API_KEY` : en pratique inactif.
- Seule classe mémoire CAMEL utilisée : `AgentMemory` (historique vif).
- **Distance à OKF : élevée sur la forme, moyenne sur le fond.** Correspondances possibles : entrée → concept, `kind` → `type`, `source_refs` → `sources`, `confirmed_by_user` / `source_trust` → `verified`, `deleted_at` → `status`, `created_by=extractor` → `generated`, `memory_mutations` → `log.md`. Absents : `title`, `description`, `tags`, `resource`, `stale_after`, `index.md`. Stockage relationnel de notes courtes, pas de documents. Un exporteur SQLite ↔ Markdown à frontmatter est à écrire (I1, I2).

### A6 — Outillage et extensibilité — **note 3**

- Skills `SKILL.md` standard (`name`, `description`), découverte dans dépôt, utilisateur et système (`skill_toolkit.py:251-259, 392-397`), import ZIP, assignation par bundle.
- Toolkits natifs : classes Python enregistrées dans un dictionnaire (`tools.py:71-96`), ajout par code.
- Bundles et Agent Plugins : format déclaratif versionné avec lockfile et garde « secret-free ».
- Navigateur hybride (CDP + Electron), terminal avec safe_mode.
- **Distance à Cordis** : pas de plugin tree ni de seams remplaçables ; la mémoire, le journal et les toolkits natifs sont du code. Le bundle est un format de composition, pas un système de plugins.

### A7 — Modèles et routage LLM — **note 2**

- `ModelFactory.create` de CAMEL (`agent/agent_model.py:116, 434-441`), alias de plateformes vers `openai-compatible-model`. Modèles locaux prévus : Ollama 11434, vLLM 8000, SGLang 30000, LM Studio 1234, llama.cpp 8080 (`localModels.ts`).
- Modèle par worker (`custom_model_config`) et par profil de bundle (`modelProfile`).
- Catalogue de capacités : 6 entrées `gpt-6-*` seulement, effort et transport, remplaçable par `EIGENT_MODEL_CAPABILITY_CATALOG` (`docs/model-capabilities.md`).
- Aucun routage sémantique ; `ModelManager` en round-robin. Point d'insertion d'un routeur (C11) : `agent_model()` avant `ModelFactory.create`, ou sans code en pointant `openai-compatible-model` vers un proxy routeur.

### A8 — Fichiers et ressources — **note 2**

- `workspace_git` riche : git local géré, checkpoints, refs `refs/eigent/*`, worktrees privés par Task / Run, ordonnanceur d'écritures, snapshots plafonnés à 256 MiB, rétention 7 / 90 / 180 jours, `publish_policy` avec détection de secrets et refus du force-push (`workspace_git/content.py:540`, `snapshot.py:14-29`, `publish_policy.py:24-55`, `advanced.py:600-610`).
- Vers le serveur : le Brain envoie des **métadonnées** (path, hash, source_path), jamais le contenu (`space_overlay_client.py:232-246`) ; `apply` copie sur le système de fichiers du serveur, permis seulement si `SPACE_LOCAL_FILE_OPERATIONS_ENABLED=true` (désactivé par défaut, `file_ops_guard.py:20-26`), donc utile seulement si serveur et poste sont la même machine.
- Snapshots (captures navigateur) stockés en fichiers sur le serveur sans volume Docker (`docker-compose.yml:56-60`).
- Point d'insertion de SeaweedFS (C8) : inexistant côté serveur ; il faudrait créer un téléversement de contenu. Côté client, `publish_policy` vers un remote git est la seule « publication » existante.

### A9 — Identité, secrets, politiques — **note 1**

- Serveur : email + mot de passe bcrypt, JWT HS256 à secret partagé, access d'une semaine (le commentaire dit 1 h), blacklist Redis (`user_auth.py:39-152`, `login_controller.py:87-129`). `auto-login` local crée `admin@local.eigent.ai`.
- SSO : via **Stack Auth** SaaS (`src/stack/client.ts`, `User.stack_id`). Le domaine `oauth` ne fait pas de login, il gère l'OAuth des connecteurs (Slack, Notion, X, Google, LinkedIn). **Aucun fournisseur OIDC générique, pas de discovery ni de JWKS : Keycloak (C13) n'est pas branchable sans réécrire la chaîne d'authentification.** Le README revendique SSO entreprise (`README.md:46, 139-146`), le code ne l'a pas.
- Front → serveur : Bearer stocké par zustand `persist` dans le localStorage (`authStore.ts:438`). Front → Brain : `NoneAuth`.
- Secrets : clés modèles et outils en clair dans `~/.eigent/.env` et `.env.<email>` (0600) ; côté serveur `Config.config_value` et `Provider.api_key` / `encrypted_config` en clair, **aucune bibliothèque crypto malgré le nom** (`server/app/model/config/config.py`, `provider.py:37-41`). Exception : coffre `safeStorage` pour les secrets de bundles et les jetons Codex, servi par un broker HTTP loopback à capacité retiré de l'environnement des agents (`electron/main/workspaceSecrets/vault.ts:70-265`, `broker.ts`). Pas de Vault, OpenBao ni keytar.
- Point d'insertion OpenBao (C14) : le broker de secrets à capacité est le bon endroit, un fournisseur OpenBao peut le remplacer ; côté serveur tout est à faire.
- Audit : `security_audit_events` (actor_type, actor_id, action_digest) et décisions attribuées, en local seulement.

### A10 — Interopérabilité standards — **note 2**

- MCP consommé (stdio, SSE, streamable-http) ; **aucun serveur MCP exposé** (pas de FastMCP ni `mcp.server`). ACP et A2A absents. OpenAPI : Swagger FastAPI par défaut sur les deux tiers Python.
- Contrats front / backend écrits à la main (`src/service/*.ts`, `src/types`), pas de génération pydantic → TS. Versions : `/api/v1`, `semantic_schema_version` des événements, `apiVersion` du bundle, migrations SQLite numérotées ; pas de négociation.
- Pour I4 (Centaur) : rien n'expose les agents Eigent ; un client de session Centaur serait à écrire dans le Brain ou en `RemoteSubAgentProvider`.

### A11 — Intégration services in-house — **note 2**

- Gmail via MCP npm `@gongrzhe/server-gmail-autoauth-mcp`, Google Drive via MCP, Google Calendar via toolkit CAMEL, Notion via `mcp-remote`, Slack / Lark / WhatsApp / LinkedIn / Reddit / Twitter / GitHub par toolkits CAMEL configurés en variables d'environnement.
- Documents : FileToolkit (docx, pdf), Excel, PPTX, MarkItDown, skills docx / xlsx / pptx / pdf utilisant LibreOffice `soffice` (`resources/example-skills/docx/scripts/office/soffice.py`).
- **Nextcloud, WebDAV, CalDAV, IMAP / SMTP, OnlyOffice, Collabora : aucune occurrence.** Seul chemin réaliste : un MCP personnalisé, ou les fichiers montés en Space « folder ».

### A12 — Qualité d'ingénierie et pérennité — **note 2**

- Positif : très gros volume de tests, TS strict, discipline du design system et de la terminologie (`AGENTS.md`, `docs/design-system/design.md`), CI multi-OS, CodeQL, pre-commit ruff et bandit, dependabot.
- Négatif : fichiers monstres (`run_journal/store.py` 22 700 lignes, `chatStore.ts` 9 019, `chat_controller.py` et `chat_service.py` ~3 000), pas de mypy ni pyright, préversions CAMEL divergentes, licence incohérente, `server/tests` hors CI, bus factor faible, documents de conception manquants, documentation serveur obsolète (Redis et Celery absents du README).

### A13 — Déployabilité on-premise — **note 2**

- Build `electron-builder` avec Python et venv préconstruits ; cibles mac, Windows NSIS, Linux AppImage ; mises à jour via `cdn.eigent.ai`.
- `server/docker-compose.yml` : postgres:15 (mot de passe `123456`, port exposé), redis:7 (port exposé), api, celery_worker, celery_beat ; volumes `postgres_data`, `eigent_redis_data` ; uploads non persistés.
- Alembic, 14 révisions, exécutées au démarrage.
- Triggers webhook et Slack exigent un domaine HTTPS public.

**Inventaire des stores (contrainte de stack, §5 du référentiel).**

| Tier | Moteur | Rôle | Verdict |
|---|---|---|---|
| Front | localStorage | session, UI, cache modèles | local au poste, toléré (mais le jeton y est stocké) |
| Electron | JSON chiffré `safeStorage` | secrets bundles, OAuth | local, toléré |
| Brain | SQLite `run-journal.sqlite3` | runs, mémoire V2, faits workspace, leases, permissions | local, toléré ; **mais c'est la source de vérité de la mémoire** : pour I2 (optimisation par le serveur) il faut un export |
| Brain | Qdrant local | RAG masqué | local, inactif ; à retirer au fork pour alléger |
| Brain | JSON / JSONL, git, fichiers | mémoire V1, checkpoints, productions | local, toléré |
| Serveur | PostgreSQL 15 | métier | **conforme** |
| Serveur | **Redis 7** | broker Celery, sessions, blacklist de jetons, pub/sub | **écart** : à migrer par fork (file de tâches et pub/sub sur PostgreSQL, par exemple `LISTEN/NOTIFY` et une table de jobs) |
| Serveur | fichiers disque | captures d'écran | **écart** : vers SeaweedFS |

## 4. Points d'insertion pour la cible

| Cible | Où | Effort |
|---|---|---|
| Cognee MCP (I5) | `~/.eigent/mcp.json` ou bundle streamable-http avec en-tête secret | nul en configuration ; moyen pour en faire la mémoire de référence (remplacer `build_durable_context_projection_for_task_lock` et `add_memory_tools`) |
| OKF (I1, I2) | exporteur `memory_entries` ↔ bundle Markdown ; `ContextSource` `bundle_asset` / `memory://` pour injecter un bundle OKF comme contexte (`workspace_config/models.py:443-493`) | moyen |
| Keycloak (C13) | `IAuthProvider` du Brain pour valider un JWT ; chaîne d'auth du serveur à réécrire (OIDC discovery, JWKS, mapping sub → user) | élevé |
| OpenBao (C14) | remplacer le fournisseur du broker de secrets Electron ; côté serveur, chiffrer puis externaliser `configs` et `provider.api_key` | moyen côté client, élevé côté serveur |
| A2A, Hermes (C3, C9) | `RemoteSubAgentProviderAdapter` + worker + champ `agents` du bundle | moyen |
| Centaur (I4) | aucun point existant ; client de session à écrire (ingress dédié côté Centaur, voir annexe A §2) | élevé |
| Spaces d'organisation (I3) | aucun modèle multi-utilisateurs ; tout à construire ou à déléguer à Harbor | très élevé |
| Routeur LLM (C11) | `agent_model()` ou proxy `openai-compatible-model` | faible |
| SeaweedFS (C8) | pas de téléversement de contenu côté serveur | élevé |

## 5. Forces, faiblesses, risques

**Forces**
1. Gouvernance d'agents de premier ordre : journal durable rejouable, interactions humaines typées, moteur de permissions avec tags de risque, audit attribué.
2. Consommation MCP standard et bundles déclaratifs avec coffre de secrets : Cognee et tout MCP tiers s'ajoutent par configuration.
3. Primitives locales solides : productions en fichiers simples, git de workspace sûr, index de fichiers par hash, serveur déjà centré PostgreSQL.

**Faiblesses**
1. Aucun espace partagé multi-utilisateurs, aucune organisation, aucun contenu téléversé : I3 et I4 sont entièrement à construire.
2. Identité fermée (Stack Auth SaaS + HS256 maison, pas d'OIDC) et secrets en clair sur le poste et dans la base serveur : C13 et C14 demandent une réécriture.
3. Mémoire soudée au SQLite local et loin d'OKF ; erreurs MCP silencieuses ; dépendance au cloud Eigent codée en dur.

**Risques de fork**
- Coût de maintenance élevé : fichiers de 10 à 20 k lignes, préversions CAMEL figées, activité concentrée sur une personne.
- Deux stores serveur non conformes (Redis, fichiers) à migrer, en plus du modèle d'espace à inventer.

## 6. Tableau des notes

| Axe | Note | Pondération | Contribution |
|---|---|---|---|
| A0 ressources tierces et lisibilité | 2 | ×2 | 4 |
| A1 local-first | 2 | ×1 | 2 |
| A2 séparation | 3 | ×1 | 3 |
| A3 environnement partagé | 1 | ×1 | 1 |
| A4 agents | 3 | ×1 | 3 |
| A5 mémoire et connaissances | 2 | ×1 | 2 |
| A6 extensibilité | 3 | ×1 | 3 |
| A7 modèles | 2 | ×1 | 2 |
| A8 fichiers | 2 | ×1 | 2 |
| A9 identité et secrets | 1 | ×1 | 1 |
| A10 standards | 2 | ×1 | 2 |
| A11 services in-house | 2 | ×1 | 2 |
| A12 qualité | 2 | ×1 | 2 |
| A13 déployabilité | 2 | ×1 | 2 |
| **Total** | | sur 60 | **31** |
