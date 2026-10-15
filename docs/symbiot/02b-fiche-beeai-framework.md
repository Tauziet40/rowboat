# Fiche d'analyse — BeeAI Framework

**Dépôt :** `tauziet40/beeai-framework`, clone local `/home/user/tauziet40/beeai-framework`, HEAD `52ebdb5` (2026-10-14) ; Python 0.1.85, TypeScript 0.1.31
**Statut :** version de travail du 2026-10-15, issue de la lecture du code par agents d'exploration ; chaque constat cite un fichier
**Référentiel :** [01-architecture-cible-symbiot.md](01-architecture-cible-symbiot.md). **Nature différente des clients :** BeeAI est une bibliothèque pour écrire des agents, pas un produit. La grille A0–A13 est appliquée avec l'interprétation indiquée par axe ; le total n'est pas comparable à ceux des clients. La fiche mesure en plus la capacité à porter les cinq principes d'Eigent (§4).

`PY` désigne `python/beeai_framework`, `TS` désigne `typescript/src`.

---

## 1. Identité

| | |
|---|---|
| Nature | Framework d'agents et de systèmes multi-agents en Python et TypeScript : agents (RequirementAgent, ReAct), outils, MCP client et serveur, A2A client et serveur, ACP, backend multi-fournisseurs, mémoire de conversation, RAG, workflows, templates |
| Gouvernance | LF AI & Data, « BeeAI a Series of LF Projects », 7 mainteneurs (`MAINTAINERS.md`), citation IBM Research (`CITATION.cff`), licence Apache 2.0 |
| Taille et tests | 343 fichiers Python dans le paquet ; Python 87 fichiers de test et 585 fonctions ; TypeScript 66 fichiers et ~344 tests |
| Activité | releases mensuelles : Python 0.1.83 (19/08), 0.1.84 (15/09), 0.1.85 (28/09) ; TS 0.1.31 (28/09). Clone shallow, dernier commit 2026-10-14 |
| Stabilité | 0.x (`major_version_zero = true`), ruptures consignées dans le changelog, dépréciations par décorateur ; pas de politique écrite |
| Outillage | Python 3.11 à 3.13, Poetry, mise ; ruff ; typage **pyrefly** ; TS ESM, tsup, vitest, `strict` |

## 2. Architecture en bref

- **Runnable et Run** (`PY/context.py`) : tout agent, outil ou modèle est un `Runnable` ; un `Run` est awaitable et itérable en flux d'événements, expose `.on`, `.observe`, `.middleware` ; `RunContext` porte `run_id`, `parent_id`, `group_id`, un émetteur enfant et un `AbortController` propagé. L'événement `start` peut fixer `output` et court-circuiter l'exécution (l. 213-229) : **c'est le point d'interception clé** pour approbation, gouvernance, routage, traçabilité.
- **Emitter hiérarchique** à namespaces (`PY/emitter/emitter.py:52-300`), matching par chemin ou regex ; `GlobalTrajectoryMiddleware` et `StreamToolCallMiddleware`.
- **Backend** : `ChatModel` et `EmbeddingModel` abstraits, résolution `from_name("provider:model")` par un **registre fermé** (`PY/backend/constants.py:8-95`).
- **Serve** : un `Server` à registre de factories par type (`PY/serve/server.py:19-90`) et des adaptateurs A2A, MCP, AgentStack, OpenAI, ACP, ACP Zed, watsonx Orchestrate.

## 3. Évaluation par axe

### A0 — Exploitation de ressources tierces et lisibilité des connexions (×2) — **note 3**

- **Client MCP** (`PY/tools/mcp/mcp.py`) : `MCPTool.from_client` accepte tout context manager du SDK `mcp` (stdio, SSE, streamable-http, `tools/mcp/utils/session_provider.py:20-29`) ; auth déléguée au SDK (headers, `httpx.Auth`) ; découverte paginée ; `isError` → `ToolError` avec contexte ; `structuredContent` prioritaire ; session partagée comptée par références. Pas de filtrage intégré (un `filter()` Python), pas de reconnexion, pas d'OAuth. TS : parité de base (`TS/tools/mcp.ts`).
- **Brancher Cognee (I5)** : `tools = await MCPTool.from_client(streamablehttp_client(url, headers=...))`, garder `remember`, `recall`, `search`, `forget`, les passer à `RequirementAgent(tools=..., requirements=[AskPermissionRequirement(include=[forget])])`. Pour une injection automatique avant chaque appel LLM, écrire une `BaseMemory` qui appelle `recall`, sur le modèle de `TS/memory/dakeraMemory.ts` (mémoire distante REST qui persiste chaque `add()` et injecte les top-K rappelés), **sans équivalent Python**.
- **Outils** : `Tool[TInput, TRunOptions, TOutput]` (`PY/tools/tool.py:41-205`), schéma Pydantic, cache, retry, middlewares, événements `start / success / error / retry / finish`, décorateur `@tool`.
- **Approbation** : `AskPermissionRequirement(include, exclude, handler, remember_choices, always_allow)` (`PY/agents/requirement/requirements/ask_permission.py:29-104`), accroché en bloquant au `start` de l'outil, court-circuite la sortie en cas de refus ; **réservé à `RequirementAgent`, absent en TypeScript**.
- **Lisibilité** : emitter, `Run.on/observe/middleware`, trajectoire vers fichier ou flux (`PY/middleware/trajectory.py:41-66`), `Logger` ; OpenTelemetry par un paquet **externe** `openinference-instrumentation-beeai`, Python seulement ; `logger.debug` journalise entrées et sorties complètes des outils MCP (données sensibles).

**Justification.** Consommation MCP standard et points d'interception propres et bloquants ; retenu à 3 par l'absence d'auth, de reconnexion et d'OAuth intégrés, et par un seam mémoire mal adapté au distant (voir A5).

### A1 — Propriété des données (interprétation : bibliothèque sans service éditeur) — **note 3**

Aucune dépendance cloud propre ; tout s'exécute où le code tourne. Sans objet pour le poste.

### A2 — Séparation des composants — **note 3**

Modules nets (agents, tools, backend, memory, serve, workflows, emitter) ; adaptateurs par fournisseur sous `adapters/<module>/backend|serve`.

### A3 — Environnement partagé — **note 0**

Hors rôle : aucune notion d'utilisateur, de tenant ou d'espace ; `MemoryManager` indexe par `context_id` seulement (`PY/serve/utils.py:53-87`).

### A4 — Agents autonomes et orchestration — **note 2**

- `RequirementAgent` (`PY/agents/requirement/agent.py:46`) est l'agent de référence : `requirements`, `role`, `instructions`, `notes`, middlewares, détecteur de cycles, bornes `max_iterations=20`, `max_retries_per_step=3`. `ToolCallingAgent` est déprécié depuis 0.1.73, `agents.experimental` émet un `DeprecationWarning`.
- Règles : `Rule` (`allowed`, `reason`, `prevent_stop`, `forced`, `hidden`), `ConditionalRequirement` (`force_at_step`, `only_before`, `only_after`, `min/max_invocations`, `consecutive_allowed`, `custom_checks`, `priority`, `.../conditional.py:28-47`).
- Appels d'outils d'une étape en parallèle (`asyncio.gather`), étapes tracées en mémoire seulement (`RequirementAgentRunStateStep`).
- **Workflows séquentiels** (`PY/workflows/workflow.py:32`) : état Pydantic, pas réservés `START`, `SELF`, `PREV`, `NEXT`, `END`, boucle `while`, copie profonde de l'état, pas de branches parallèles ni de checkpoint, pas de retry. `AgentWorkflow` chaîne des agents clonés ; `HandoffTool` clone l'agent cible avec sa mémoire. Exemples : coordinateur avec experts par `HandoffTool` (`python/examples/agents/requirement/multi_agent.py`), `autoflow` avec un LLM routeur.
- **Aucune sérialisation en Python** (« Example coming soon ») ; TS a un `Serializer` et des snapshots, mais un snapshot n'est pas un journal : ni reprise ni rejeu d'un run.

### A5 — Mémoire et connaissances — **note 2**

- `BaseMemory(ABC)` (`PY/memory/base_memory.py:14-84`) : `messages` et `reset()` **synchrones**, `add` / `delete` asynchrones, `clone()` par défaut `type(self)()`. Implémentations : Unconstrained, Sliding, Token, Summarize, ReadOnly. Pensé pour l'historique de conversation, pas pour la mémoire sémantique ; une mémoire distante doit tenir un cache local et `forget` devient fire-and-forget ; pas de point « recall avant appel LLM ».
- `VectorStore(ABC)` (`PY/backend/vector_store.py:28-200`) : natifs `beeai:TemporalVectorStore` (InMemory LangChain) et `agentstack:NativeVectorStore` ; tout le reste via `LangChainVectorStore`, dont la résolution de nom ne couvre **ni pgvector ni FalkorDB** : instanciation manuelle `LangChainVectorStore(vector_store=PGVector(...))`. Ajouter un store natif demande d'éditer le registre fermé.
- RAG : pas de dossier `rag/` (lien de doc obsolète) ; `DocumentLoader` via LangChain, `TextSplitter`, `LLMDocumentReranker`, `RAGAgent` expérimental, `VectorStoreSearchTool`. **`RAGAgent` jette les métadonnées** (`agents/experimental/rag/agent.py:81`) : pas de citation ; l'outil renvoie `title` et `url`/`source`, suffisants pour citer un chemin OKF. Import `agents.experimental.rag` probablement cassé par la substitution de `sys.modules` (non exécuté, à vérifier).
- **Distance à OKF** : chargeable par `DirectoryLoader`, mais le frontmatter n'est pas parsé et `Document.metadata` n'accepte que des scalaires (`PY/backend/types.py:255-260`) : listes à aplatir. Un loader OKF d'environ 50 lignes et un agent qui cite sont à écrire.
- TypeScript : **aucune abstraction** VectorStore, DocumentLoader ou TextSplitter, seulement des outils Milvus, Qdrant, Elasticsearch, SQL.
- Contrainte de stack : aucune base imposée par la bibliothèque.

### A6 — Outillage et extensibilité — **note 2**

Tout par sous-classement : `Tool` ou `@tool`, `BaseMemory`, `ChatModel` / `EmbeddingModel` (plus édition du registre et convention de chemin `adapters/<module>/backend/<type>.py`), `Workflow.add_step`, `PromptTemplate` Mustache (exposable en prompt MCP), `RunMiddlewareProtocol`. Seuls registres : `Server.register_factory` et `Serializable.register()` en TS. **Ni entry points, ni découverte de plugins, ni cycle de vie, ni injection de services** : distance forte au modèle Cordis ; l'analogue le plus proche est l'arbre d'Emitters et de RunContext.

### A7 — Modèles et routage LLM — **note 3**

- Python : Ollama, OpenAI, watsonx, Groq, xAI, Vertex, Gemini, Bedrock, Anthropic, Azure, Mistral, **DeepSeek** (`PY/adapters/deepseek/backend/chat.py`), Qwen, MiniMax, Transformers local, LangChain, AgentStack ; presque tous via `LiteLLMChatModel`. Compatible OpenAI via `openai:` et `base_url`. Sortie structurée validée, repli des appels d'outils par `response_format` pour les modèles sans appel natif, réparation des appels invalides.
- **Aucun routage ni repli multi-modèles.** Point d'insertion (C11) : une sous-classe `ChatModel` qui délègue `run()`, sur le patron d'`AgentStackChatModel` (`PY/adapters/agentstack/backend/chat.py:47-189`) ; `from_name` ne convient pas, registre fermé.
- TS : SDK Vercel AI, **sans DeepSeek**, ni Gemini direct, ni Mistral.

### A8 — Fichiers et ressources — **note 1**

Outils FileRead, FileEdit, Glob, Grep en Python (absents en TS) ; `FileEditTool` écrit **puis** renvoie le diff. Pas de blobs, de versions ni de partage : hors rôle.

### A9 — Identité, secrets, politiques — **note 1**

- Clés en constructeur ou variables d'environnement ; `Settings` ne contient que `log_level` ; aucun `SecretStr`, aucune abstraction de coffre ; `LocalShellBackend` fusionne `os.environ` dans les sous-processus (`PY/tools/code/_shell_backend.py:56`) : **les secrets fuient vers les commandes**.
- Serveurs : **A2A sans aucune auth, sur `0.0.0.0` par défaut** (`PY/adapters/a2a/serve/server.py:57-73`, seuls `server_credentials` gRPC) ; MCP avec `AuthSettings` et `transport_security` du SDK mais pas de `token_verifier` passable (à vérifier) ; OpenAI avec `api_key` optionnelle ; watsonx avec `X-API-Key`. Ni OIDC, ni JWT, ni tenant.
- Gouvernance : `AskPermission` binaire ; exemples hors paquet `action_bound_governance.py` (approve / require_approval / reject) et `hol_guard.py` (fail-closed).

### A10 — Interopérabilité standards — **note 3**

- **A2A client et serveur** (`PY/adapters/a2a/serve/server.py`) : un agent par serveur, JSON-RPC, HTTP+JSON ou gRPC, `/health`, Agent Card générée (`name`, `description`, `url`, `version`, modes, `capabilities(streaming=True)`, `skills`), personnalisable par `A2AServerMetadata` avec `task_store`, `queue_manager`, `push_notifier` ; **pas de `security_schemes`** ; streaming par statuts, pas token par token ; réponse finale en message, pas en artefact.
- **MCP serveur** : expose `Tool`, `Runnable` (outil `run(input)`), `PromptTemplate` (prompts MCP), ressources ; stdio, SSE, streamable-http.
- AgentStack serve (métadonnées riches : `security`, `security_schemes`, `AgentDetail`), OpenAI Chat Completions et Responses, ACP legacy, **ACP Zed** (`io_confirm` routé vers `session/request_permission`), watsonx Orchestrate. `OpenAPITool.from_schema` : un outil par chemin et méthode, résolution des `$ref`, en-têtes statiques seulement.
- TS : A2A, MCP, OpenAI ; **pas d'AgentStack, ACP ni watsonx**.
- **Faille pour Harbor** : l'`A2AServer` simple n'installe aucun contexte d'E/S, l'exécuteur ne passe jamais en `input_required`, `io_confirm` retombe sur `input()` côté serveur (`PY/utils/io.py:36-55`). Seul l'adaptateur AgentStack fait un vrai flux d'approbation par A2A (`PY/adapters/agentstack/context.py:55-137`).

### A11 — Intégration services in-house — **note 1**

Outils DuckDuckGo, Wikipedia, OpenMeteo, Think, Handoff, Python, Sandbox, Shell ; interpréteur de code en service HTTP séparé `bee-code-interpreter` (`127.0.0.1:50081`) ; ni Docker ni e2b. Aucune intégration email, agenda, Nextcloud ou WebDAV : par MCP ou `OpenAPITool`.

### A12 — Qualité d'ingénierie et pérennité — **note 3**

Gouvernance LF, CI (`py_main.yml`, e2e TS), ~930 tests, releases mensuelles, typage pyrefly ; mais 0.x, docs en migration Mintlify → Astro inachevée (`docs/MIGRATION.md`), liens obsolètes, parité Python / TS non déclarée : observabilité, évaluation, `AskPermission`, ACP Zed, outils shell et fichiers en Python seulement ; sérialisation en TS seulement.

### A13 — Déployabilité (interprétation : empaquetage et services annexes) — **note 2**

Paquets PyPI et npm, extras `a2a`, `mcp`, `acp`, `agentstack`, `rag`, `evaluation` ; serveurs à lancer soi-même ; interpréteur de code externe ; aucune image ni chart.

## 4. Capacité à porter les cinq principes d'Eigent

| Principe | Statut | Ce qui existe | Ce qui manque |
|---|---|---|---|
| (1) Journal durable et rejouable | partiel | événements hiérarchiques, `state.steps`, `GlobalTrajectoryMiddleware`, OpenInference | persistance, reprise, rejeu, trace des approbations ; serializer Python |
| (2) Politique allow / prompt / deny et HITL typé | partiel | `AskPermission` binaire, `ConditionalRequirement` comme deny, `io_read` pour une question libre, court-circuit au `start` | types choice et diff review, langage de politique, étiquettes de risque, routage de `io_confirm` vers A2A `input_required` hors AgentStack |
| (3) Environnements d'exécution | partiel | `ShellBackend` et `FileBackend` par ContextVar (local ou éditeur ACP), interpréteur distant HTTP | Docker, e2b, abstraction distante générique, confinement |
| (4) Bundles déclaratifs, secrets hors environnement | absent | — | tout : manifeste versionné, courtier de secrets |
| (5) Workforce coordinateur / planificateur / workers | partiel | coordinateur `RequirementAgent` avec `HandoffTool`, `autoflow` | planificateur, file de tâches, pool de workers, parallélisme de workflow |

**Verdict.** BeeAI peut porter les principes 2, 3 et 5 en tant que bibliothèque. Il faut construire par-dessus un runtime : journal append-only rejouable, moteur de politique avec interactions typées, bundles versionnés avec injection de secrets hors processus, backends sandbox et distant, authentification OIDC sur A2A, mapping `io_confirm` → `input_required` pour Harbor, planificateur. C'est précisément ce que DSH ou Agent Stack fournissent en partie (voir [annexe B](annexe-B-dsh-seams.md) et [fiche Agent Stack](02c-fiche-agentstack.md)).

## 5. Points d'insertion pour la cible

| Cible | Où | Effort |
|---|---|---|
| Cognee MCP (I5) | `MCPTool.from_client` + `AskPermission` sur `forget` ; `BaseMemory` Cognee sur le modèle Dakera pour le rappel automatique | faible ; moyen pour la mémoire |
| OKF (C6) | loader OKF (frontmatter → métadonnées aplaties) + prompt qui cite `source` | faible |
| A2A (C9) | serve A2A natif ; ajouter `security_schemes` et une auth (reverse proxy Keycloak) ; ou serve AgentStack | faible |
| Harbor, agent membre (I3) | base A2A + reproduction du contexte d'E/S d'AgentStack (approbation par `input_required`) ; ou connecteur Harbor REST écrit avec le client MCP de Harbor | moyen |
| DSH (harness) | ACP Zed, serveur OpenAI, ou A2A ; backend DeepSeek natif en Python | faible à moyen |
| Routeur LLM (C11) | sous-classe `ChatModel` déléguant `run()` | faible |
| OpenBao (C14) | rien n'existe ; injecter les clés au constructeur depuis un client OpenBao, et remplacer `LocalShellBackend` pour nettoyer l'environnement | moyen |

## 6. Forces, faiblesses, risques

**Forces**
1. La couverture de protocoles la plus large du dossier : A2A, MCP, ACP et ACP Zed, OpenAI, AgentStack, en client et en serveur.
2. `RequirementAgent` et le court-circuit bloquant au `start` de l'outil : une base directe pour une politique et une gouvernance, avec le modèle `Run` / `RunContext` comme source d'un journal.
3. Fournisseurs larges dont DeepSeek et Ollama, sortie structurée et repli d'appels d'outils ; gouvernance LF et licence Apache 2.0.

**Faiblesses**
1. Pas de runtime : ni journal durable, ni reprise, ni rejeu, ni serializer Python ; workflows séquentiels sans planificateur.
2. Sécurité : aucun secret store, `os.environ` hérité, A2A ouvert sans auth, ni OIDC ni tenant.
3. Mémoire et RAG pensés pour l'historique et LangChain : seam synchrone, pas de pgvector ni FalkorDB natifs, provenance perdue, TS sans RAG ; pas de système de plugins ; parité Python / TS incomplète.

**Risques**
- 0.x avec ruptures, documentation en migration, modules expérimentaux instables.
- Le choix du langage fixe la parité : Python pour tout ce qui compte ici (AskPermission, ACP Zed, outils fichiers, DeepSeek).

## 7. Tableau des notes (indicatif, bibliothèque)

| Axe | Note | Pondération | Contribution |
|---|---|---|---|
| A0 ressources tierces et lisibilité | 3 | ×2 | 6 |
| A1 propriété des données | 3 | ×1 | 3 |
| A2 séparation | 3 | ×1 | 3 |
| A3 environnement partagé | 0 | ×1 | 0 |
| A4 agents | 2 | ×1 | 2 |
| A5 mémoire et connaissances | 2 | ×1 | 2 |
| A6 extensibilité | 2 | ×1 | 2 |
| A7 modèles | 3 | ×1 | 3 |
| A8 fichiers | 1 | ×1 | 1 |
| A9 identité et secrets | 1 | ×1 | 1 |
| A10 standards | 3 | ×1 | 3 |
| A11 services in-house | 1 | ×1 | 1 |
| A12 qualité | 3 | ×1 | 3 |
| A13 déployabilité | 2 | ×1 | 2 |
| **Total** | | sur 60 | **32** |
