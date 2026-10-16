# Note d'analyse — Synapse AI, partie workflows et apps

**Dépôt :** `tauziet40/synapse-ai`, clone local `/home/user/tauziet40/synapse-ai`, HEAD `9ee485d` (un seul commit squashé du 2026-08-13, 369 fichiers, +93 318 lignes : généalogie invérifiable par git)
**Statut :** version de travail du 2026-10-15, analyse **ciblée** sur le moteur de workflow, le builder, la provenance et les licences ; le reste de la plateforme n'est pas instruit ; chaque constat cite un fichier
**Question posée :** extraire et refactoriser la partie workflows et apps no-code vers les mini-apps de Rowboat (C16), sous contrainte de licence ; vérifier le soupçon d'un framework d'origine non identifié
**Référentiel :** [01-architecture-cible-symbiot.md](01-architecture-cible-symbiot.md) ; forme cible des mini-apps dans `apps/x/MINI_APPS_PLAN.md` et `apps/x/packages/shared/src/rowboat-app.ts`

---

## 1. Réponse courte

1. **Le soupçon de dérivation n'est pas confirmé.** Le moteur de workflow est du Python écrit en propre, avec son schéma et son vocabulaire. n8n n'est qu'une intégration externe, appelée en REST et affichée dans un iframe ; React Flow est une dépendance MIT ; « dify », « refine » et « lobe » sont des faux positifs de recherche.
2. **Il n'existe pas de builder d'apps no-code.** `native_builder` est un méta-workflow piloté par LLM qui produit du JSON d'orchestration et d'agents, jamais une interface.
3. **La licence AGPL-3.0, sans CLA, interdit toute extraction de code vers Rowboat (Apache 2.0).** Restent deux voies : faire tourner Synapse non modifié comme service séparé, ou réécrire en clean-room un sous-ensemble de steps en TypeScript dans le moteur de tâches de fond de Rowboat.

## 2. Le moteur de workflow

- **Où** : `backend/core/orchestration/` (4 720 lignes : `engine.py` 751, `steps.py` 1 822, `context.py` 956, `journal.py`, `runner.py`, `state.py`, `summarizer.py`), modèle `backend/core/models_orchestration.py`, routes `routes/orchestrations.py`, `api_v1.py`, `api_v2.py`.
- **Format** : modèles Pydantic sérialisés dans `data/orchestrations.json`. `Orchestration` porte `steps[]`, `entry_step_id`, `state_schema {key: {type, default, description}}`, garde-fous `max_total_turns`, `max_total_cost_usd`, `timeout_minutes`, `trigger: manual | scheduled` (`models_orchestration.py:122-140`). `StepConfig` est un modèle plat (`:29-119`). **Les arêtes sont implicites** (`next_step_id`, `route_map`, `if_true/false_step_id`, `switch_cases`, `parallel_branches`, `loop_step_ids`) et reconstruites par le canvas (`frontend/src/components/orchestration/WorkflowCanvas.tsx:37-80`). Aucun schéma nodes / edges à la n8n.
- **14 types de step** (`StepType`, `:12-26` ; registre `STEP_EXECUTORS`, `steps.py:1806-1822`) : IA `agent` (boucle ReAct), `llm`, `evaluator` (routage LLM par `route_map`) ; outils `tool` (MCP, HTTP, Python), `transform` (Python dans Docker ou sur l'hôte), `extract_json` ; contrôle `if_else`, `switch`, `parallel`, `merge`, `loop`, `end` ; `human` (pause avec formulaire), `print`. Sous-orchestration par un step `agent`, profondeur 3. **Pas de catalogue de nœuds d'intégration** façon n8n : tout passe par MCP ou outils personnalisés.
- **Exécution** : générateur asynchrone step par step avec événements SSE (`engine.py:107-357`), timeout par step (`anyio.fail_after`), plafonds de tours et de boucle, `runner.py` à tâche unique qui journalise chaque événement. **Checkpoint JSON atomique à chaque frontière de step** (`state.py:41-58`), reprise `resume`, `resume_failed`, `_resume_nested_orch` (`engine.py:359-610`). Mode « scale » : état sur PostgreSQL (`scale/state_pg.py`), file **ARQ sur Redis** (pas Celery), worker avec retries, timeout 3 600 s et DLQ (`scale/worker.py:614-624`), événements sur Redis Streams, webhook sortant signé HMAC.
- **Expressions** : interpolation `{state.key}` par regex dans les prompts, placeholders d'URL pour les outils HTTP, et **`eval()` Python** sur l'objet `state` pour `if_else` et `switch` (`steps.py:1649-1745`, `__builtins__: {}`, protection contournable).
- **Déclencheurs** : manuel, clé API `sk-syn-` sur `/api/v1` et `/api/v2` (de fait le webhook entrant), cron par croniter (`core/scheduler.py:34-58`), messageries pour l'étape humaine.
- **Identifiants** : **aucun modèle de credentials** ; en-têtes HTTP des outils, `n8n_api_key` et `global_config` stockés en clair ; `vault.py` stocke des sorties volumineuses d'outils, pas des secrets.

## 3. `native_builder` et la notion d'« app »

- Une orchestration seedée au démarrage (`backend/core/native_builder/seed.py`) de 15 steps : routage d'intention, collecte des besoins avec boucle humaine, brouillon de plan, revue humaine, création d'agents, sauvegarde ; 5 sous-agents et 23 outils de builder (`core/builder_tools.py`, 1 589 lignes, validation `:1283`). Exposée par `/api/builder/chat` et `/api/builder/resume` et le panneau `BuilderPanel.tsx`.
- **Elle produit du JSON d'orchestration et d'agents, jamais de HTML, de React ni de schéma d'UI.**
- Ce qui s'approche d'une app : les champs de formulaire de l'étape `human`, l'outil MCP `collect_data` qui affiche un formulaire dans le chat, et « Deploy », qui transforme une orchestration en agent orchestrateur, pas en application publiée.
- Front : canvas `@xyflow/react`, `StepNode`, `StepConfigPanel` (1 069 lignes), `OrchestrationTab` (2 115), environ 5 000 lignes TSX.
- Sandbox : seul `transform` est isolé dans Docker (512 Mo, système de fichiers en lecture seule) ; le mode `host` n'a aucun sandbox ; le seul iframe embarque l'éditeur n8n.

## 4. Provenance

| Amont suspecté | Preuves | Catégorie |
|---|---|---|
| n8n | 15 fichiers d'intégration : client REST de 95 lignes (`routes/n8n.py`, `X-N8N-API-KEY`, `/api/v1/workflows`, recherche du nœud `n8n-nodes-base.webhook`), iframe `${n8nUrl}/workflow/{id}` (`N8nFullscreenOverlay.tsx:30-41`), sélecteur dans le Tool Builder, settings. **Aucun** `INodeTypeDescription`, `IExecuteFunctions`, `$json`, `NodeConnectionType`, ni paquet `n8n-workflow` / `n8n-core` | intégration externe, pas de code n8n |
| React Flow | `"@xyflow/react": "^12.10.1"` (`frontend/package.json:20`), imports normaux, surcharges CSS | dépendance MIT |
| Dify | 0 occurrence en mot entier ; les 22 résultats viennent de « mo**dify** » | faux positif |
| Refine | aucun `@refinedev` ; verbe anglais dans les prompts | faux positif |
| Lobe | `<Globe>` de lucide | faux positif |
| LangGraph, Flowise, Langflow | 0 occurrence ; ressemblance conceptuelle du `SharedState` avec checkpoint | inspiration générique au mieux |

Aucun en-tête de copyright tiers, aucun `NOTICE` ni `THIRD_PARTY`, aucune mention « ported from ». **Le moteur est natif.**

## 5. Licences

- Synapse : AGPL-3.0 (`LICENSE`, `package.json`, `pyproject.toml:10-19`), aucun en-tête par fichier, **pas de CLA** dans `CONTRIBUTING.md` : une relicence demanderait l'accord de chaque contributeur.
- Amonts : n8n (Sustainable Use License) **sans objet**, aucun code n8n présent ; la SUL ne s'applique que si l'on opère n8n à côté (usage interne permis, revente en service hébergé restreinte). `@xyflow/react`, ARQ et croniter sont MIT : réutilisables dans Rowboat.
- **Conséquences pour Rowboat (Apache 2.0)** : copier, adapter ou traduire le code Synapse (moteur, steps, context, prompts, builder, canvas) le contamine en AGPL, avec l'obligation du §13 de fournir la source aux utilisateurs réseau. Les **idées et le format fonctionnel** restent réutilisables par une réécriture clean-room à partir d'une spécification. Faire tourner Synapse **non modifié** comme service séparé, appelé par API réseau, ne crée normalement pas d'œuvre dérivée ; toute version modifiée opérée doit publier ses sources.

## 6. Faisabilité de l'extraction

- Périmètre : ~4 700 lignes de moteur, 1 589 de `builder_tools`, ~840 de `native_builder`, 3 132 de couche scale, ~5 000 lignes TSX ; Python et Next.js face à TypeScript et Electron.
- **Couplage fort** par imports paresseux : `core.llm_providers` (2 520 lignes), `core.react_engine` (1 710), `core.routes.agents` et `routes.orchestrations` (stockage JSON via les routes), `core.tools`, `core.scale.context`, client MCP transmis à l'engine ; le moteur charge les agents depuis la couche HTTP (`engine.py:46`) ; pas d'auth au niveau du moteur.
- Tests : 63 fichiers, ~1 500 lignes sur l'orchestration ; `native_builder` et `builder_tools` exclus de la couverture (`pyproject.toml:118-120`).
- **Correspondance avec la mini-app Rowboat** : aucun équivalent du HTML autonome ni du pont `window.rowboat` ; « agent backend → `data.json` sur déclencheur » correspond à orchestration + Schedule + `final_state` (`engine.py:333-338`) validé contre `dataContracts` ; `state_schema` et `output_key` jouent le rôle du contrat de données.

## 7. Notes et verdict

| Axe | Note | Justification |
|---|---|---|
| Moteur de workflow | 3 | 14 steps, checkpoint, reprise, HITL, mode distribué avec retries et DLQ ; mais `eval` et aucun credential |
| Builder et apps | 1 | méta-builder LLM intéressant, mais aucune app ni UI produite |
| Provenance (clarté) | 4 | natif ; n8n en intégration, xyflow en dépendance MIT ; faux positifs levés |
| Licences (compatibilité Apache 2.0) | 1 | tout le code utile est AGPL sans CLA ; seuls les composants MIT sont réutilisables |
| Extraction | 1 | couplage profond, Python face à TS, rien pour l'UI |

**Forces** : moteur de graphe robuste (timeouts, garde-fous, reprise, imbrication) ; mode distribué prêt (ARQ, PostgreSQL, Redis Streams, webhook HMAC) ; builder conversationnel avec validation, bonne source d'idées pour la skill de construction de mini-apps de Rowboat.
**Faiblesses** : AGPL sans CLA ; `eval()` dans `if_else` et `switch` (`steps.py:1679, 1723`), `transform` en mode hôte sans sandbox, secrets en clair ; aucune notion d'app, couplage profond.

**Verdict.** Ni extraction ni reconstruction depuis un amont, puisqu'il n'y a pas d'amont.
- **Court terme** : Synapse non modifié comme **service AGPL séparé**, appelé en HTTP `/api/v2` ou MCP par l'agent backend d'une mini-app ; empilement lourd (Python, Redis, PostgreSQL) pour un usage de mini-app, la v1 mono-processus en JSON suffit ; Redis est un écart de stack à noter.
- **À terme** : **réécriture clean-room en TypeScript** d'un sous-ensemble de steps (agent, llm, evaluator, if et switch avec un évaluateur d'expressions sûr, parallel, loop, human, end) dans le moteur de tâches de fond de Rowboat, qui a déjà déclencheurs cron, fenêtre et événement ([fiche Rowboat](02-fiche-rowboat.md) A4), avec `@xyflow/react` si un canvas est voulu. Rowboat tient déjà l'autre moitié de C16, la mini-app : HTML autonome, agent backend, contrats de données.
