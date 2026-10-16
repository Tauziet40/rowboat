# Annexe B — DeepSeek Harness : vérification bornée des cinq seams

**Dépôt :** `tauziet40/deepseek-harness`, clone local `/home/user/tauziet40/deepseek-harness`, release dsh 0.2.1-alpha.1, licence MIT
**Statut :** relevé du 2026-10-15, lecture limitée à cinq seams et à l'exposition ; rien n'a été exécuté
**Rôle :** DSH est le harness pressenti. L'annexe mesure sa capacité à porter les cinq principes d'Eigent et à accueillir Cognee, et sert au §8 du [comparatif](04-comparatif-et-recommandation.md).

Chemins relatifs à `/home/user/tauziet40/deepseek-harness`.

---

## 1. Journal de session — principe (1) : **couvert**

- `SessionEvent` : union discriminée sur `type`, `seq` contigu, `time` en epoch ms (`docs/subsystems/session.md:226-260`) ; vocabulaire extensible par declaration merging (`packages/core/session/src/types.ts:281`).
- Journal **append-only** ; l'historique LLM en est dérivé, jamais stocké à part (`session.md:5`) ; `Session.append` rejette toute donnée non JSON.
- Durabilité : seam `ctx.sessionPersistence` (create / open / stat / list), `SessionHandle` à écrivain unique ; backend livré JSONL + Zstandard, `fsync` par lot, troncature de fin déchirée (`docs/subsystems/persistence.md:7, 329`). Reprise après crash : `interruptedTurnClosers` ajoute les fermetures manquantes.
- Replay sans réexécuter les outils ; `SessionStore.fork(source, boundary?)` refuse une coupe au milieu d'un tour ouvert ; resume par `sessionController`.
- `tool/call` journalisé **avant** exécution avec les arguments bruts (`types.ts:361`) ; `tool/result` avec résultat, erreur et `meta` rejouable. Approbations en événements `approval/asked`, `approval/decided`, `approval/policy`, `permission/preset`, obligatoirement commitées dans un tour ouvert (`docs/subsystems/approval.md:86, 115-131`).
- Projections pures par `ctx.sessionProjections`. Format versionné `SESSION_FORMAT_VERSION = 4` avec migrations adjacentes v0→…→v4 ; générations publiées immuables ; événements inconnus `ignorable` tolérés.

**C'est le point le plus solide de DSH.** À ajouter pour Symbiot : un backend de persistance partagé (SQL ou objet) si multi-processus, et un export d'audit.

## 2. Pipeline d'outils et garde-fous — principe (2) : **partiel**

- Waterfalls (`packages/core/tools/src/index.ts:153, 164, 176`) : `tools/pre-execute` renvoie `allow | deny | cancel | ask` (pas de réécriture d'arguments, déjà journalisés) ; guards monotones `ctx.tools.guard()` qui ne peuvent que refuser ; `tools/execute` (timeout, retry) ; `tools/post-execute` renvoie `accept | block` avec contenu de remplacement.
- Un `ask` déclenche `ctx.approval.request` ; tout résultat autre que `allowed-once` est un deny ; sans répondant, `unavailable` donc refus. Politique de session `ask | never` seulement ; presets permission = paires sandbox + approbation : `read-only/ask`, `workspace-write/ask`, `danger-full-access/never` (`packages/bundle/base/cordis.patch.yml:245-262`).
- Interactions typées : **approbation** (résultat fermé, mais `ApprovalRequest` omet les arguments et se rattache par `callId`) ; **question et choix** (`AskUserQuestionItem` : options, `multiSelect`, réponse libre, lots, `docs/subsystems/user-questions.md:49-120`) ; un seul `kind` de présentation, `plan-review`. **Revue de diff avant exécution absente** : le diff de `tool-fs` est une métadonnée de résultat.
- **Aucune étiquette de risque déterministe** ; seul Auto review, expérimental et désactivé, demande au LLM `{risk, decision}` (`packages/experimental/auto-review/src/index.ts:43-67`, « can allow unsafe actions »).
- `packages/guard` ne contient que `timeout-policy` et `repeat-tool-reminder`.
- Brancher un moteur de politique : un plugin sur `tools/pre-execute` et `ctx.tools.guard()`, plus un répondant `approval/request` ; c'est le modèle de `hooks-claude-code` et d'`auto-review`.

## 3. Environnements d'exécution — principe (3) : **partiel, bonne base**

- Seams (`docs/capability-seams.md:638-648`) : `ctx.fs` (`fs-local`, `fs-sandbox`, `fs-ssh`), `ctx.subprocess` (`-local`, `-ssh`), `ctx.sandbox` (`-local`, `-ssh`), `ctx.shell` (`bash-local`, `bash-sandbox`, `pwsh-*`). Bash, PTY, LSP et les subagents ACP / Codex / Claude passent tous par `ctx.subprocess`.
- Sandbox local : bwrap / Landlock (Linux), Seatbelt (macOS), ACL Windows (garantie partielle) ; modes `read-only | workspace-write | danger-full-access` sur les effets fichiers, **réseau non couvert**.
- SSH : une connexion OpenSSH, helper distant vérifié SHA-256 ; harness, modèle et stockage de session restent sur l'hôte ; remplacer les trois fournisseurs déplace FS, Bash, terminal, LSP (`docs/subsystems/ssh.md:9-11, 31`) ; l'hôte SSH est considéré de confiance ; **aucun bundle SSH livré**.
- **Aucun fournisseur Docker, Kubernetes ou E2B.** Un plugin doit écrire le trio fs / subprocess / sandbox pour un conteneur ou un cluster (par exemple une sandbox Centaur).

## 4. Profils, bundles, identifiants — principe (4) : **partiel**

- Profil = bundles dans l'ordre + `cordis.patch.yml` du profil + celui du home + `--patch` ; un patch remplace la config d'une ligne par id ou insère (`docs/architecture.md:20-38`). `dsh --profile web --dump-config` (sortie non contractuelle). Bundles = paquets npm avec lockfile par profil, pairs vérifiés ; `dsh plugin add | remove` et outil `plugin_manager` (exige `danger-full-access` ou approbation), restauration du manifeste en cas d'échec.
- Identifiants : la config ne porte que des **références** (noms de variables), résolues à chaque opération (`docs/subsystems/credentials.md:5, 20`) ; fournisseur local `<home>/.credentials.yaml` en 600, qui **admet ne pas pouvoir isoler les secrets de l'agent** (`packages/credentials/credentials-local/README.md:12, 32, 115`) ; atténuation : environnement nettoyé par `SENSITIVE_ENV_PATTERN = /KEY|PASSWORD|SECRET|TOKEN/i` pour les enfants et les MCP stdio. **Pas de courtier.** Seam `ctx.credentials` (`CredentialProvider`) abstrait ; seuls `credentials-local` et le compte DeepSeek existent ; **ni Vault, ni OpenBao, ni 1Password**.

## 5. Subagents et Agent Teams — principe (5) : **partiel**

- `SubagentProvider { name, capabilities, inheritsParentContext, start(), prepareContinuable?() }` ; plusieurs fournisseurs coexistent dans `ctx.subagents` (`docs/subsystems/subagent.md:391-450`). Fournisseurs : en processus `spawn` et `fork` (seuls continuables) ; hors processus `acp`, `dsh-sdk` ; délégation one-shot `claude-code`, `codex`. Outils `tool-subagent`, `tool-subagent-control` (`send_message`, `interrupt_agent`, `list_agents`) ; `delegationDepth` durable.
- Agent Teams (`packages/experimental/agent-team`) : Lead implicite, roster durable, mailbox dédupliquée, DAG de tâches avec `revision` compare-and-set et `blockedBy`, état rejoué depuis le log du Lead. Limites : un seul processus et un seul checkout, roster plat, coéquipiers limités aux fournisseurs continuables, « no stability promise ».
- **Pas de rôle planificateur** ; seulement le plan mode `exit_plan_mode`. Spécialisation par rôle à ajouter via `packages/preset/agent-preset`.

## 6. Mémoire et exposition

- **Aucun seam mémoire** : aucun paquet memory, retrieval ou RAG. La voie documentée est un **serveur MCP externe** (Memorix, Reference Memory, Engram en overlays désactivés, `docs/user/guide/mcp-memory.md`). Cognee se branche de même : ses outils deviennent `mcp__cognee__*` et passent par toute la pipeline de permission. Remplacement au niveau de la config, sans interface typée.
- `mcp-client` : une entrée Cordis par serveur, `stdio` ou `streamable-http`, outils enregistrés sous `mcp__<server>__<tool>` ; auth par `headers` statiques ou `env` ; **pas d'OAuth** ; non supportés : prompts, elicitation, tasks, abonnements. `mcp-resources` : trois outils de liste et lecture.
- **DSH n'est ni serveur MCP ni agent A2A** (grep vide). Pilotage externe : **ACP v1** sur stdio (`dsh --profile acp`, reprise de session, montage de serveurs MCP par session, `session/request_permission` que le client peut répondre) ; **SDK JSON-RPC** (`dsh --profile sdk`, clients TS et Python) où les requêtes serveur → client ne sont pas implémentées, donc les approbations restent sans répondant et sont refusées (`packages/sdk/protocol/README.md:114`).

## 7. Synthèse

| Principe | Seam | Statut | Ce qu'un plugin doit ajouter |
|---|---|---|---|
| (1) Journal rejouable | `ctx.sessions`, `ctx.sessionPersistence`, projections | **couvert** | backend durable partagé si multi-processus ; export d'audit |
| (2) Politique et HITL | `tools/pre-execute`, `tools.guard`, `ctx.approval`, `ctx.userQuestions` | partiel | moteur de règles allow / prompt / deny par outil et arguments ; étiquettes de risque déterministes ; intention `diff-review` avant exécution ; répondant SDK |
| (3) Environnements | `ctx.fs`, `ctx.subprocess`, `ctx.sandbox`, `ctx.ssh` | partiel | fournisseurs conteneur ou cluster ; bundle SSH ; confinement réseau |
| (4) Bundles et secrets | profils, bundles, plugin-manager, `ctx.credentials` | partiel | `CredentialProvider` OpenBao ; courtier injectant les secrets hors de l'environnement |
| (5) Équipe multi-agents | `ctx.subagents`, agent-team (expérimental) | partiel | rôle planificateur ; workers spécialisés par presets ; coéquipiers hors processus |
| Mémoire (Cognee) | `mcp-client`, aucun seam mémoire | partiel | overlay Cognee ; seam `ctx.memory` typé optionnel ; OAuth |
| Exposition | ACP, SDK JSON-RPC | partiel ; MCP serveur et A2A **absents** | plugin serveur MCP ou A2A ; répondant d'approbation SDK |

**Verdict.**
1. Architecturalement, DSH est un bon hôte : tout est plugin, le journal est rejouable, les seams sont typés. Des agents BeeAI ou Hermes y entrent comme fournisseurs `subagent-acp` ou `dsh-sdk`, Cognee comme overlay `mcp-client`, sans toucher la boucle.
2. Il faut combler soi-même : la politique par règles, le courtier de secrets, les environnements conteneur ou cluster, le planificateur, et toute exposition MCP ou A2A.
3. Le risque est réel et écrit : « developer preview… THERE WILL BE COMPATIBILITY-BREAKING CHANGES » (`README.md:11-13`), « not undergone a security audit… must not be treated as secure or production-ready » (`SAFETY.md:7`), « Public APIs are pre-stable » (`CLAUDE.md`), Agent Teams et Auto review sans promesse de stabilité. Épingler les versions et isoler les plugins maison derrière les seams.
