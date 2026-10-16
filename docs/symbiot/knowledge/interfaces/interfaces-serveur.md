---
type: Interface
title: Interfaces côté client de la stack serveur
description: Conversion OKF du document de travail annexe-A-interfaces-serveur.md du dossier docs/symbiot (cycle des 15 et 16 octobre 2026).
tags:
  - serveur
  - mcp
  - a2a
  - identité
sources:
  - resource: /deprecated/2026-10-15/annexe-A-interfaces-serveur.md
generated:
  by: claude-fable-5.1/session-01MK6
  at: 2026-10-16T18:00:00+02:00
status: stable
stale_after: 2027-01-16T00:00:00+02:00
---

# Interfaces côté client de la stack serveur

**Statut d'origine :** relevé du 2026-10-15, lecture limitée aux surfaces d'interface (routes, outils, auth, flux, config). Le fonctionnement interne n'est pas décrit.
**Rôle :** référence pour mesurer la distance entre ce qu'un client sait consommer et ce que le serveur expose (intégrations I2 à I5 du [référentiel](/conventions/architecture-cible.md)).

---

## 1. Harbor (serveur Rowboat Spaces)

Source du contrat : `apps/harbor/packages/protocol/src/api.ts` (routes), `events.ts` (frames), `mcp.ts` (outils), `CONTRACT.md` (sémantique).

### Familles de routes HTTP

| Famille | Routes |
|---|---|
| Orgs (apex) | `GET/POST /v1/orgs`, `DELETE /v1/me`, `/.well-known/oauth-protected-resource` (`packages/server/src/apex.ts:103-164`) ; logo d'org `GET/PUT/DELETE /v1/org/logo`, `GET /v1/images/:hash` |
| Session, identité | `POST/DELETE /v1/session`, `GET /v1/me`, `PUT/DELETE /v1/me/avatar` |
| Spaces | `GET/POST /v1/spaces`, `/v1/spaces/browse`, `/:id/join`, `rename`, `archive`, `unarchive`, `leave`, `DELETE /v1/spaces/:id`, `POST /v1/direct` |
| Membres, invitations | `GET /v1/members`, `GET/POST /v1/spaces/:id/members`, `POST /v1/invites`, `/v1/invites/resolve` (sans auth), `/v1/invites/accept` |
| Feed | `/stream`, `/threads/:root`, `/messages` (post, `/:id/edit`, `delete`, `reactions`, `poll/votes`, `poll/end`), `/topics` |
| Assets | `/assets` (create, `move`, `delete`, `restore`, `:assetId`), `/changes`, `/history`, `/diff` |
| Blobs | `PUT /v1/spaces/:id/blobs`, `GET …/blobs/:hash` |
| Agents | `GET/POST /v1/agents`, `/credential`, `/keys`, `/keys/:id/revoke`, `/capabilities`, `/option-defaults`, `/hook`, `POST /v1/hooks/:agentId/:token` (sans auth) |
| Invocations, côté connecteur (clé agent) | `GET /v1/agent/invocations`, `/:id/ack`, `/:id/update`, `/:id/approvals`, `POST /v1/agent/capabilities`, `/v1/agent/approvals/:id/applied`, `close` |
| Invocations, côté humain | `GET /v1/spaces/:id/invocations`, `POST /v1/invocations/:id/cancel`, `POST /v1/spaces/:id/approvals/:id/decide` |
| Recherche | `GET /v1/spaces/:id/search` |
| État de lecture | `POST /v1/spaces/:id/read`, `/threads/:root/follow`, `GET /v1/unread`, `GET /v1/activity`, `/activity/seen`, `/activity/read-all` |
| Push | `POST /v1/push/register`, `unregister` |
| Temps réel | `GET /v1/live` (WebSocket) |

### Frames WebSocket (`events.ts:166-357`)

- Une seule WebSocket par org. Abonnement par space avec `afterOffset` : le serveur rejoue l'historique puis passe en direct.
- Frames serveur : `event` (un `SpaceEvent` avec offset), `presence`, `subscribed`, `error`, `ping` (toutes les 25 s environ), `space_added`, `space_removed`, `org_changed`, `read_mark`, `notify`, `whiteboard`, `invocation`, `invocation_stop`, `approval_decided`, `invocation_state`.
- Frames client : `subscribe`, `unsubscribe`, `presence`, `whiteboard`.
- Contre-pression : la connexion est coupée au-delà de 2 MiB en attente (`CONTRACT.md:206`, `ws.ts:39`).

### Outils MCP sur `/mcp` (38 outils, `protocol/src/mcp.ts`)

Transport StreamableHTTP sans état (`server/src/mcp.ts:61`). En-têtes `x-acting-mode: scheduled` et `x-agent-name` pris en compte.

| Groupe | Outils |
|---|---|
| Identité, annuaire | `whoami`, `list_members` |
| Spaces | `list_spaces`, `browse_spaces`, `join_space`, `create_space`, `rename_space`, `archive_space`, `unarchive_space`, `delete_space`, `add_members`, `leave_space`, `open_direct`, `create_invite` |
| Feed | `read_stream`, `read_thread`, `search_space`, `post_message`, `edit_message`, `delete_message`, `react`, `vote_poll`, `end_poll`, `list_topics`, `create_topic`, `manage_topic` |
| Fichiers | `list_assets`, `create_asset`, `read_asset`, `propose_change`, `move_asset`, `delete_asset`, `restore_asset`, `asset_history`, `diff` (champ `reason` obligatoire) |
| Agents | `get_invocations`, `stop_invocation` |
| Activité | `read_activity`, `mark_all_read` |

Les lectures pures sont listées dans `readOnlyMcpToolNames` (`mcp.ts:731`).

### Authentification (`server/src/auth.ts`, `auth-oidc.ts`)

- Pilote `dev` : `Bearer dev-<memberId>`.
- Pilote `oidc` : un émetteur fixe, découverte RFC 8414, JWT vérifiés par JWKS (ES256 / RS256). Le couple (iss, sub) est associé à un membre existant, jamais créé automatiquement ; sinon `not_a_member`, et seule une invitation crée le lien. Le commentaire de `auth-oidc.ts:12` cite « Supabase Auth flagship, Keycloak, corporate IdP ». **Keycloak est donc configurable** par `AUTH_ISSUER` (obligatoire en déploiement), `AUTH_AUDIENCE` (optionnel), `AUTH_PUBLISHABLE_KEY` (page de consentement) (`main.ts:114-180`). Le serveur publie les métadonnées RFC 9728.
- Cookie `harbor_session` : posé par `POST /v1/session`, HttpOnly, accepté seulement depuis une origine de `HARBOR_WEB_ORIGINS`. Un en-tête `Authorization` est toujours prioritaire (`CONTRACT.md:26-31`).
- Clés agent `rbk_` : préfixe plus 43 caractères base64url, stockées en SHA-256, acceptées sur REST, sur `/v1/live?token=` et sur MCP, toujours en mode `direct` (`CONTRACT.md:37`, `auth.ts:60`).

### Blobs (`http.ts:21`, `:589`, `mime.ts`, `main.ts:57-87`)

- Envoi en deux temps : `PUT` des octets bruts avec l'en-tête obligatoire `x-blob-sha256`, le serveur recalcule le hash ; puis référence du hash dans un lien `/b/` ou un `propose_change`.
- Limite 100 MiB par défaut (`HARBOR_MAX_BLOB_BYTES`) ; avatar et logo 1 MiB.
- MIME détecté par le serveur (jpeg, png, gif, webp, pdf). Seules les images sont servies inline, le reste en pièce jointe avec `nosniff`.
- `GET` réservé aux membres du space ; flux depuis le disque (`BLOBS_DIR`) ou redirection 302 vers une URL S3 présignée (`BLOBS_S3_*`). **Point d'insertion de SeaweedFS : son API S3.**

### Contrat d'un agent externe (`examples/echo-agent.mjs`)

1. `GET /v1/me` avec sa clé, puis `POST /v1/agent/capabilities` pour déclarer `stop` et ses options.
2. WebSocket `/v1/live?token=rbk_…`, réaction aux frames `invocation` et `invocation_stop`.
3. Sweep `GET /v1/agent/invocations` au démarrage puis toutes les 60 s : la liste est la garantie, la frame le chemin rapide.
4. `ack`, puis `update` avec les états `working`, `waiting`, `done`, `failed`, `cancelled`.
5. Réponse par `POST /v1/spaces/:id/messages` avec `threadRoot`.

États d'une invocation : `queued`, `pending`, `working`, `waiting`, `done`, `failed`, `cancelled` (`invocation.ts:23`).

## 2. Centaur

### API de session (RFC 0002, `services/api-rs/rfcs/0002-session-control-plane.md:140-330`)

- `POST /api/session/{thread_key}` crée ou renvoie la session ; un `harness_type` différent donne 409.
- `POST …/messages` ajoute des messages durables au format `parts`.
- `POST …/execute` prend des `input_lines` opaques en NDJSON et renvoie une exécution `queued`.
- `GET …/events?after_event_id=` diffuse en SSE, replay compris. Aussi `/interrupt`, `/pause` (`crates/centaur-api-server/src/routes.rs`).
- Autres familles : `/api/workflows/{schedules, runs, runs/{id}/cancel, events, actions/invoke}`, `/api/webhooks/{slug}`, `/api/admin/*-sync`, `/api/sandboxes/drain`, `/mcp`, `/.well-known/oauth-protected-resource[/mcp]`, `/healthz`, `/readyz`, `/metrics`.

### Événements

- `id` SSE monotone par session. Types : `session.execution_started`, `session.output.line` (ligne brute du harness, non ré-encodée), `session.execution_completed`. Le flux ne se ferme pas à la fin d'une exécution.
- Les types de lignes (protocole app-server de style Codex : `item.agentMessage.delta`, `turn.completed`…) sont dans `packages/harness-events/src/index.ts`.

### Authentification (`src/auth.rs`)

- Jetons statiques comparés par SHA-256 : `CENTAUR_APIRS_ADMIN_API_KEY` (toutes capacités) et les clés d'ingress `SLACKBOT_`, `DISCORDBOT_`, `GITHUBBOT_`, `LINEARBOT_`, `TEAMSBOT_API_KEY`, chacune limitée par `platform_prefixes` (`slack:`, `teams:`…) avec `SessionsRead` et `SessionsWrite`.
- JWT HS256 signés par `CENTAUR_JWT_SIGNING_SECRET` (iss `centaur-console`, aud `centaur-api`) : `token_use=console_service` a toutes les capacités ; un JWT de principal n'a que `sessions_read`, `workflows_read` ou `workflows_write`.
- MCP : jeton OAuth émis par la console, PKCE et DCR, portant `principal_id` et `scope mcp:tools` (RFC 0004).
- Le SSO Slack, Google ou Okta ne sert qu'à se connecter à la console (`services/console/README.md:76-98`). **Pas d'OIDC générique sur l'API elle-même.**

### Un client de bureau comme ingress

Le JWT de principal n'a pas `SessionsWrite`. Une application de bureau doit donc soit obtenir une nouvelle entrée `INGRESS_SPECS` (variable d'environnement et préfixe dédié, par exemple `desktop:`), ce qui demande une modification du code, soit utiliser la clé admin. Elle suit ensuite le flux d'un ingress : create → messages → execute → events (`auth.rs:295-345` ; `AGENTS.md` racine, « Architecture boundaries »).

### Endpoint MCP (`mcp.rs:225-470`)

Expose `centaur_catalog_search`, `centaur_catalog_load`, `centaur_tool_call`, `centaur_artifact_get`, `centaur_whoami` aux humains passés par l'OAuth de la console ; exécute des outils avec leurs droits via un runner associé à `principal_id`.

### Bibliothèque client, plugins, harness, stockage

- `packages/api-client` : `CentaurClient` ne couvre que les workflows (`startWorkflowRun`, `getWorkflowRun`, `listWorkflowRuns`, `getWorkflowChildren`, `cancelWorkflowRun`, `sendWorkflowEvent`, `client.ts:34-107`). **Pas de client de session.**
- Identifiants des agents : la sandbox ne voit que des placeholders ; iron-proxy substitue les vraies valeurs pour les hôtes et en-têtes liés au secret (`README.md:210-218`). Secrets issus de 1Password (`OP_SERVICE_ACCOUNT_TOKEN`). **Point d'insertion d'OpenBao : la source de secrets d'iron-proxy.**
- Plugins d'outils (`tools/README.md`) : `pyproject.toml` avec `[tool.centaur]` et `[project.scripts]`, `client.py` avec `secret("KEY")`, `cli.py` en typer ; exposés comme shims CLI, découverts par `centaur-tools list`.
- Plugins de workflow (RFC 0003) : module avec `WORKFLOW_NAME`, `Input`, `WEBHOOKS`, `SCHEDULE`, `async handler(params, ctx)` ; `ctx` fournit `step`, `agent_turn`, `run_agents`, `call_tool`, `post_to_slack`. Moteur Absurd sur Postgres.
- Harness : `harness/claude/settings.json`, `harness/codex/config.toml` ; adaptateurs `crates/harness-server/src/` : `amp`, `claude`, `codex`, `hermes`, `pi`, `omp`, `nanocodex`. **Hermes est un harness reconnu.**
- Stockage : Postgres avec pgvector obligatoire (`api-rs/AGENTS.md:50`), ParadeDB `pg_search` optionnel (BM25), Kubernetes ou k3s pour les sandboxes. Pas de Redis dans le chart.

## 3. Cognee

### Outils MCP (`cognee-mcp/src/server.py`)

| Outil | Signature | Ligne |
|---|---|---|
| `remember` | `data, filename, content_base64, dataset_name, session_id, custom_prompt, background, ontology_key, self_improvement` | 357 |
| `recall` | `query, search_type, datasets, session_id, system_prompt, top_k=15, scope, code_query` | 531 |
| `code_search` | `operation = query_facts, explore, traverse, find_path, impact_analysis…` | 654 |
| `forget` | `dataset, everything, data_id, dataset_id` | 714 |
| `cognify_status` | `dataset_name, pipelines` (non annoncé par défaut) | 899 |
| `improve` | défini mais non exposé selon le README | 791 |

`COGNEE_MCP_TOOL_MODE=default|minimal|all`, avec `search_tools` pour découvrir les outils non annoncés.

- Périmètre agent : dataset par défaut `{clientInfo.name nettoyé}_memory` ; `COGNEE_MCP_AGENT_SCOPED=false` ramène à `main_dataset` (`server.py:993-1040`).
- Transports : `--transport stdio|sse|http` (`--path /mcp`) ou `TRANSPORT_MODE` sous Docker. Seul garde trouvé : Host/Origin (`MCP_ALLOWED_HOSTS`). **Pas d'authentification entrante sur le MCP.**
- Auth sortante vers le backend : `--api-url`, `--api-token` ou `COGNEE_API_KEY`, `--api-auth-scheme bearer|x-api-key`.

### Routes HTTP (`cognee/api/client.py:360-474`)

Sous `/api/v1/` : `auth` (register, reset, verify, clés API), `add`, `cognify`, `memify`, `search`, `permissions`, `datasets`, `ontologies`, `settings`, `visualize`, `schema`, `skills`, `proposals`, `configuration`, `delete`, `validate`, `update`, `responses`, `llm`, `sync`, `users`, `checks`, `agents`, `activity`, `sessions`, `remember`, `recall`, `improve`, `forget`, `slack`, `integrations` ; plus `/health`.

### Contrôle d'accès

- fastapi-users : JWT Bearer ou cookie, plus `X-Api-Key`.
- Permissions par dataset : `read`, `write`, `delete`, `share` ; capacités par tenant : `manage_users`, `grant_capabilities` (`permission_types.py`) ; routes `/permissions` (`get_permissions_router.py:38-736`).
- `ENABLE_BACKEND_ACCESS_CONTROL=true` (défaut) isole chaque couple (utilisateur, dataset) dans sa propre base. À `false`, base partagée et authentification non exigée sauf `REQUIRE_AUTHENTICATION=true`.

### Ontologie et FalkorDB

- `POST /api/v1/ontologies` avec `ontology_key` et un fichier `.owl` RDF/XML, référencé ensuite par `ontology_key` dans cognify ou remember (`get_ontology_router.py:22-35`). Le résolveur rdflib accepte aussi turtle, n3, nt, json-ld, trig, nquads. Variables : `ontology_resolver=rdflib`, `matching_strategy=fuzzy`, `ontology_file_path`, `ontology_mode=annotate|strict`.
- FalkorDB : adaptateur communautaire hybride ; installer `cognee-community-*-falkordb`, importer son `register`, puis `GRAPH_DATABASE_PROVIDER` et `VECTOR_DB_PROVIDER` à `falkordb`, avec `GRAPH_DATABASE_URL` et `GRAPH_DATABASE_PORT`. Gestionnaire par dataset, compatible avec le contrôle d'accès (`.agents/skills/cognee-community/SKILL.md:18-60`, `graph/config.py:47-56`).

## 4. ElephantBroker (forme d'un contrat client ↔ runtime de mémoire)

- MemoryPlugin : 24 outils en 6 groupes (memory, goals, procedures, artifacts, guards, admin), plus hooks de session.
- ContextEnginePlugin : 7 méthodes (bootstrap, ingest, assemble, compact, afterTurn, subagent spawn/end), mode dégradé bufferisé ; chacune correspond à un `POST /context/{bootstrap, ingest, ingest/batch, assemble, compact, after-turn, subagent/spawn, subagent/ended}`.
- MemorySearchManager : `POST /memory/search`, `GET /memory/read`, `/status`, `POST /memory/sync`, `GET /memory/probe/*` (`docs/openclaw-contract-mapping.md:59-106`). Le hook `before_prompt_build` renvoie un `SystemPromptOverlay`.
- En-têtes d'identité : `X-EB-Gateway-ID`, `X-EB-Agent-ID`, `X-EB-Agent-Key`, `X-EB-Actor-Id`, `X-EB-Session-Key`. `AuthMiddleware` est un stub qui laisse toujours passer (`api/middleware/auth.py`).
- 84 endpoints en groupes : `/memory`, `/context`, `/goals`, `/procedures`, `/guards`, `/working-set`, `/trace`, `/consolidation`, `/sessions`, `/admin`, `/health`, `/metrics`, `actors`, `profiles`, `claims`, `artifacts`, `rerank`, `stats`.

## 5. Synthèse

| Surface | Protocole | Auth | Ce qu'un client doit implémenter |
|---|---|---|---|
| Harbor REST | HTTP JSON (schémas zod) | OIDC JWT (JWKS), cookie, ou `rbk_` | Découverte RFC 9728, OAuth 2.1 avec PKCE, blob en deux temps (hash), pagination par offsets |
| Harbor live | WebSocket `/v1/live` | Bearer ou `?token=` | `subscribe` avec `afterOffset`, reprise, tolérance aux frames inconnues, détection du silence via `ping` |
| Harbor MCP | MCP StreamableHTTP sans état | Bearer OIDC ou `rbk_` | Client MCP, en-têtes `x-acting-mode`, `x-agent-name` |
| Harbor agent | REST + WS | `rbk_` | ack / update / approvals, sweep 60 s, réponse par messages |
| Centaur sessions | HTTP + SSE | Clé d'ingress statique ou admin | `thread_key`, `input_lines` NDJSON au format du harness, SSE `after_event_id`, parsing harness-events |
| Centaur MCP | MCP HTTP | OAuth console (JWT HS256) | DCR et PKCE, puis catalog search, load, call |
| Cognee MCP | MCP stdio, SSE ou HTTP | Aucune en entrée ; clé API ou Bearer vers le backend | `clientInfo.name` stable (périmètre), `dataset_name` |
| Cognee REST | HTTP | JWT, cookie ou `X-Api-Key` | Users, tenants, datasets, envoi d'ontologie `.owl` |
| ElephantBroker | HTTP JSON via plugins TS | En-têtes `X-EB-*`, auth en stub | 7 hooks de cycle de vie, en-têtes d'identité |

**Dénominateurs communs**
- MCP sur HTTP avec bearer : Harbor, Centaur, Cognee.
- Une identité OIDC ou JWT mise en correspondance avec un principal interne : (iss, sub) → membre chez Harbor, `principal_id` chez Centaur, utilisateur fastapi-users chez Cognee.
- Des flux en ajout seul rejouables par curseur : offsets par space (Harbor), `after_event_id` SSE (Centaur), ledger de traces (ElephantBroker).
- Découverte RFC 9728 chez Harbor et Centaur.

**Divergences**
- Temps réel : WebSocket (Harbor), SSE (Centaur), rien (Cognee, ElephantBroker).
- Fournisseur d'identité : OIDC quelconque chez Harbor (Keycloak possible) ; la console comme serveur d'autorisation en HS256 partagé chez Centaur ; JWT locaux chez Cognee ; aucun chez ElephantBroker. **Unifier sur Keycloak demande un travail côté Centaur et Cognee, pas côté Harbor.**
- Isolation : org et space (Harbor), préfixe de `thread_key` et principal (Centaur), (utilisateur, dataset) (Cognee), gateway / agent / session (ElephantBroker).
- Schéma : contrat zod partagé chez Harbor, lignes de harness opaques chez Centaur.
- Stockage : Postgres chez Harbor (PGlite en dev) ; Postgres avec pgvector et Kubernetes chez Centaur ; Kuzu et LanceDB par défaut ou FalkorDB chez Cognee ; Neo4j, Qdrant, Redis chez ElephantBroker (illustration seulement, hors contrainte de stack).
