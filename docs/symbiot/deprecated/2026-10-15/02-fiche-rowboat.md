# Fiche d'analyse — Rowboat

**Dépôt :** `tauziet40/rowboat`, clone local `/home/user/rowboat`, HEAD `81d6f3e` (2026-10-14)
**Statut :** version de travail du 2026-10-15, issue de la lecture du code par agents d'exploration ; chaque constat cite un fichier
**Référentiel :** [01-architecture-cible-symbiot.md](01-architecture-cible-symbiot.md) (axes A0–A13, intégrations I1–I5, composants C1–C14) ; interfaces de Harbor dans [annexe A](annexe-A-interfaces-serveur.md) §1

Chemins relatifs à `/home/user/rowboat`. `$C` désigne `apps/x/packages/core/src`.

---

## 1. Identité

| | |
|---|---|
| Nature | Assistant personnel de bureau local-first (« Brain » de connaissances, email, réunions, agents de fond, code mode), plus Spaces, l'environnement partagé multi-joueurs servi par Harbor |
| Stack | Monorepo TypeScript, pnpm. `apps/x` : Electron (`apps/main`), React (`apps/renderer`), serveur headless Hono (`apps/server`), mobile Expo (`apps/mobile`), paquets `core`, `shared`, `client`, `spaces-client`. `apps/harbor` : serveur Spaces Node + PostgreSQL, protocole zod partagé en dépendance `link:` |
| Licence | Apache 2.0 (`LICENSE`) |
| Taille | `apps/x` ~1 300 fichiers TS/TSX, ~283 k lignes, ~268 fichiers de test vitest ; renderer 589 fichiers (~133 k), core 482 (~99,5 k) ; Harbor 56 fichiers de test (~34 k lignes) |
| Activité | clone shallow : 87 commits depuis le 2026-08-01, dernier le 2026-10-14 ; 62 d'un même auteur, 11 d'un bot : bus factor élevé |
| Gouvernance | pas de CONTRIBUTING, CODE_OF_CONDUCT ni SECURITY ; contrat Spaces déclaré « v0, deliberately unstable » (`apps/harbor/CONTRACT.md:5`) |

## 2. Architecture en bref

- **Poste.** Tout vit sous `~/.rowboat` (déplaçable par `ROWBOAT_WORKDIR`, `$C/config/config.ts:5-23`) : `knowledge/` (Markdown versionné par git local via isomorphic-git), `storage/turns` (JSONL), `config/*.json`, `agents/`, `skills/`, caches. **Aucune base de données embarquée** : ni SQLite, ni LanceDB, ni PGlite dans `apps/x` (seule une sonde `bun:sqlite` externe pour le CLI Claude Agent SDK, `apps/main/bundle.mjs:186-189`).
- **Runtime de l'assistant.** Boucle de tours event-sourcée maison sur le Vercel AI SDK v7 (`$C/runtime/turns/runtime.ts`, `real-model-registry.ts:1-19`), prompt assemblé par capacités et skills, outils par domaines, permissions par classifieur LLM ou validation manuelle.
- **Séparation client / serveur.** Serveur headless Hono : RPC `POST /rpc/{channel}`, un WebSocket `/events` (`apps/server/src/channels.ts`, `ws-hub.ts`). 273 canaux migrés sur 479 (le plan annonce « 17/356 », chiffre périmé, `SEPARATION_PLAN.md:15-19`). Mode distant validé sur EC2 + Tailscale (`REMOTE_SERVER.md`), bearer unique dans `~/.rowboat/server-key`, mono-utilisateur.
- **Spaces.** Le client ne garde localement que l'identité des orgs et un cache de blobs : « the app is a browser » (`$C/spaces/orgs.ts:9-12`). Il parle à Harbor en REST typé zod (`packages/spaces-client/src/client.ts`, 750 lignes), en WebSocket (`live.ts`) et projette les outils MCP de Harbor en outils natifs de l'agent (`$C/runtime/tools/domains/spaces.ts:1-25`).

## 3. Évaluation par axe

### A0 — Exploitation de ressources tierces et lisibilité des connexions (×2) — **note 2**

**Constat.**
- Serveurs MCP déclarés dans `~/.rowboat/config/mcp.json`, format standard `mcpServers` avec `{command, args, env}` ou `{url, headers}` (`apps/x/packages/shared/src/mcp.ts:3-21`, `$C/mcp/repo.ts:16-43`). Transports stdio, Streamable HTTP, SSE en repli ; les `headers` (Bearer) sont transmis (`$C/mcp/mcp.ts:60-85`). Clients mis en cache, reconnexion quand la config change.
- **Cognee se branche sans code** (I5) : une entrée `{"cognee": {"url": "https://…/mcp", "headers": {"Authorization": "Bearer …"}}}`, saisie dans Settings › MCP Servers (éditeur JSON brut, `settings-dialog.tsx:89-93, 2006`) ou par l'outil `addMcpServer`.
- **Mais l'accès du modèle est indirect** : pas d'outils natifs par défaut ; le copilote charge la skill `mcp-integration` puis passe par les méta-outils `listMcpServers` → `listMcpTools` → `executeMcpTool` (`$C/runtime/tools/domains/mcp.ts:13-120`). Chaque appel exige une permission (« fail closed », `real-permission-checker.ts:51-62, 88-98`). Le prompt donne la priorité à Composio puis à la mémoire locale, MCP en dernier (`instructions.ts:164, 294`).
- Des outils MCP natifs sont possibles pour un agent personnalisé `~/.rowboat/agents/*.md` (`type: mcp, mcpServerName, inputSchema`, `shared/src/agent.ts:11-35`). Et **le mécanisme de projection d'un MCP en outils natifs existe déjà** pour Harbor (`spaces.ts:1-25`, `orgs.ts:210-245`) : le reproduire pour Cognee est un changement de code court.
- Pas d'OAuth pour les serveurs MCP génériques : le code OAuth et DCR existe (`$C/auth/oauth-client.ts:105-138`) mais il est réservé aux fournisseurs fixes rowboat, google, fireflies, microsoft et aux orgs Spaces.
- **Mémoire non remplaçable** : aucune interface `IMemoryProvider` ou `IRetriever` dans le conteneur DI (`$C/di/container.ts:80-155`) ; le prompt impose `file-grep knowledge/` puis `file-readText` dès qu'une entité est nommée (`instructions.ts:271-297`).
- **Lisibilité.** Positif : tout est dans des JSON lisibles sous `config/`, l'état des connexions (connected, error, message) est exposé par `listServers` (`mcp.ts:146-162`), les tours sont journalisés en JSONL (`storage/turns`), les services dans `logs/services.jsonl`. Négatif : `mcp.ts` ne journalise pas ses connexions et l'interface MCP se limite à un éditeur JSON.

**Justification de la note.** Connexion simple, configuration lisible et état exposé ; mais accès indirect avec friction de permission, priorité basse dans le prompt, mémoire soudée au grep. Le chemin vers 3 est court : projeter Cognee comme outils natifs (modèle `spaces.ts`) et amender `instructions.ts`.

### A1 — Local-first et propriété des données — **note 3**

- Fichiers simples uniquement : Markdown, JSONL, JSON, git (`$C/knowledge/README.md:3`, `version_history.ts:1-55`, `runtime/turns/fs-repo.ts:24-31`). Aucune base.
- Hors ligne : le cœur fonctionne avec un modèle local (`ollama`, `openai-compatible`, `shared/src/models.ts:19`) ; Spaces n'a pas de mode hors ligne (seuls les blobs sont en cache, `spaces/blob-cache.ts:9-21`).
- Pas de synchronisation entre appareils des données personnelles ; connecteurs en synchronisation descendante vers Markdown (`knowledge/sync_*.ts`).
- Chiffrement : seulement les jetons (`safeStorage` desktop ; AES-256-GCM avec `~/.rowboat/cipher-key` en headless, `apps/server/src/file-cipher.ts:6-30`). Notes, conversations, emails en clair.
- Cloud : `api.x.rowboatlabs.com` **optionnel** mais support de la passerelle LLM, facturation, recherche Exa, TTS, OAuth Google géré, config distante (`config/env.ts`, `models/gateway.ts:23`, `web.ts:57`, `voice.ts:49`) ; Composio et TypeSafe optionnels en BYOK ; apex Spaces `spaces.x.rowboatlabs.com` par défaut, Harbor auto-hébergé pris en charge en org « foreign » (`orgs.ts:22-26`). **PostHog actif par défaut** dans les binaires officiels, opt-out par `DO_NOT_TRACK=1`, `ROWBOAT_TELEMETRY_DISABLED=1` ou `telemetryOptOut` (`ANALYTICS.md:284-309`), identification par email après connexion.

**Justification.** Modèle de données ouvert et auditable, exactement le « second cerveau » visé (I1) ; à nettoyer : télémétrie opt-out, défauts cloud, chiffrement des contenus.

### A2 — Séparation client / serveur — **note 3**

- Transport, auth et WS en place ; 273 canaux migrés, restent `spaces` 26, `browser` 17, `quickAsk` 25, `app` 15, `video` 9… (`apps/server/src/channels.ts`, `shared/src/ipc.ts`).
- `serverHostMode()` renvoie `remote` si `ROWBOAT_REMOTE_SERVER` ou `config/client.json` est défini (`apps/main/src/server-host.ts:38-87`) ; **le cœur tourne aujourd'hui sur une machine distante**, en HTTP clair (VPN ou reverse proxy TLS requis), pour un seul utilisateur, verrou PID (`lock.ts:5-25`).
- Reste desktop : fenêtres, tray, audio / vidéo, push-to-talk, navigateur intégré, quick-ask ; phases 7 et 9 du plan ouvertes.

### A3 — Environnement partagé — **note 3**

- Modèle Harbor (SPEC §4, §5) : org = origine URL, serveur de ressources OIDC pur ; membres `human | agent` ; un bit admin ; espace = assets (wiki Markdown) + flux + membres, une seule copie canonique ; DM = espace `direct` à 2, illisible par les admins ; visibilité `private | open`, browse et self-join ; threads plats et topics ; read state serveur ; mentions tokens `[@Nom](#member:<id>)`.
- Client : `packages/spaces-client` (REST, WS avec watchdog et replay par offset), UI complète (`apps/renderer/src/components/spaces/`), whiteboards Excalidraw en LWW par élément (`$C/spaces/whiteboard.ts`), envoi programmé (`spaces/scheduler.ts`).
- Rejoindre une org : découverte RFC 9728, **DCR obligatoire** (`$C/spaces/oauth.ts:87`, `auth/oauth-client.ts:100-121`), PKCE S256, navigateur système, refresh token exigé ; invitations `https://<org>/join/<token>` liant (iss, sub) au membre à l'acceptation. Pas de chemin `client_id` pré-enregistré (`oauth.ts:91-94`).
- Projection du contexte local (le cœur de I3) : `@rowboat` désigne l'agent local de l'orateur, qui tourne sur sa machine (SPEC §8) ; une session locale par thread (`spaces/topic-agent.ts:10-32`), dernier acte `post_message` ; en-tête `x-agent-name: Rowboat` → `actingMode: 'agent'`, affiché « Nom (via Rowboat) ».

**Justification.** C'est le modèle même que Symbiot vise pour C2 et I3 ; limites : protocole propriétaire v0, pas de copie locale des espaces, pas d'inter-orgs.

### A4 — Agents autonomes et orchestration — **note 3**

- Agents de fond : planifiés (cron, fenêtre, unique, `agent-schedule/runner.ts`) ou déclenchés par événements `manual | cron | window | event` (`shared/src/background-task.ts:109`) ; événements en fichiers JSON sous `events/pending` produits par Gmail, Calendar, Outlook, Slack, réunions ; routage par classifieur LLM sur `eventMatchCriteria` en langage naturel. Une tâche peut lancer des sessions de code dans un worktree git.
- Sous-agents : `spawn-agent`, enfant headless isolé, **un seul niveau** (`runtime/assembly/spawn-agent.ts:17-75`) ; agents-outils `type: "agent"`.
- Code mode : client ACP complet (`@agentclientprotocol/sdk`, adaptateurs Claude Code et Codex, `code-mode/acp/`).
- Agents membres de Spaces (SPEC §8) : contrat Invocation → Progress → Actions (outils MCP) → Approvals, file durable par (agent, thread), hand-offs limités à 3 hops, approvals à 4 choix. Paires `AGENT_PAIRS` : custom/contract, **hermes/plugin**, replicas, agent37, conductor, posthog, cal (`protocol/src/core.ts:87-98`). Connecteur minimal `examples/echo-agent.mjs`. **Hermes Agent est déjà un connecteur** (`rowboatlabs/hermes-rowboat`, plugin plateforme Hermes) et les agents apprennent l'étiquette par `skills/rowboat-spaces/SKILL.md` : C3 est couvert tel quel.
- Description d'agent : Markdown à frontmatter zod `{name, provider, model, description, instructions, tools}` dans `~/.rowboat/agents/*.md` (`runtime/assembly/repo.ts:21-66`). **Aucune Agent Card A2A.**
- Point d'insertion A2A (C9) : un connecteur Harbor `connectors/a2a/` avec une paire dans `AGENT_PAIRS`, ou un connecteur externe `custom/contract` sur clé `rbk_`.

**Justification.** Hermes et le contrat d'invocation durable sont des acquis directs ; faiblesses : orchestration minimale (pas de workforce ni de planificateur), pas d'A2A.

### A5 — Mémoire et connaissances — **note 3**

- Brain : dossier Markdown style Obsidian sous `~/.rowboat/knowledge/`, arborescence par type (`Notes/`, `People/`, `Organizations/`, `Projects/`, `Topics/`, `Meetings/`, `Voice Memos/`, `Workspace/`, `Agent Notes/`, `instructions.ts:262-269`, `sources/repo.ts:30-46`). Modèles de notes par type (`note_system.ts:14-160`) : H1, section `## Info` en champs gras, Summary, Connected to, Activity datée, Key facts, Open items. Wikilinks absolus `[[People/Sarah Chen]]`, chaque lien devient une arête (`note_creation.ts:84, 1253`). Frontmatter YAML ajouté après coup par un agent de tagging (`relationship`, `topic`, `source`, `status`, `action`, `role`, `email`, `first_met`, `last_update`, `note_tagging_agent.ts:18-50`), `curated_at` par la curation quotidienne. Versionné par git local, vues graphe et « Bases » filtrées sur le frontmatter.
- Alimentation : connecteurs → Markdown → `buildGraph` (mtime puis sha256) → agent LLM `note_creation`, un fichier par exécution (`build_graph.ts:30-60`). Enum fermé de sources `gmail | meeting | voice_memo | slack | github | linear` (`sources/types.ts:3-10`).
- Mémoire utilisateur : `save-to-memory` → `Agent Notes/inbox.md`, rangé ensuite dans `user.md`, `preferences.md`, `style/email.md` ; `user.md` et `preferences.md` injectés à chaque tour (`workspace-context.ts:34-80`).
- **Ni base, ni index vectoriel, ni embeddings** : recherche par `grep -ril` (`search/search.ts:70-130`), index en mémoire reconstruit par regex pour les agents d'extraction.
- **Distance à OKF : moyenne.** Communs : dossier Markdown, un concept par fichier, frontmatter possible, tags. À traiter : métadonnées surtout dans le corps (`**Field:**`), frontmatter optionnel et tardif, dupliqué avec le corps (`note_creation.ts:1261`) ; absents `type` (déduit du dossier), `title` (H1), `description`, `resource`, `sources`, `generated`, `verified`, `stale_after` ; `status` avec une autre sémantique ; ni `index.md` ni `log.md` (historique dans git et les sections Activity) ; wikilinks à convertir en liens Markdown. **Un convertisseur bidirectionnel est faisable sans toucher au cœur** (I1, I2).

**Justification.** Le second cerveau est déjà un dossier Markdown versionné, proche d'OKF, sans aucun store à migrer ; l'absence d'index local est un non-problème pour Symbiot, où l'indexation est le rôle du serveur (Cognee, I2).

### A6 — Outillage et extensibilité — **note 2**

- Skills : `SKILL.md` (`name`, `description`, `tools` / `allowed-tools`), lues dans `~/.rowboat/skills` puis `~/.agents/skills`, rechargées à chaud (`skills/disk-loader.ts:26-140`, `watcher.ts`) ; une skill disque ne peut déclarer que des outils builtin, et ne peut pas injecter de fragment éager dans le prompt (frontière de confiance typée). 25 skills intégrées en TypeScript.
- Outils natifs : catalogue statique d'environ 25 domaines (`runtime/tools/catalog.ts:86-118`), ajout par code et recompilation.
- Agents en fichiers `~/.rowboat/agents/*.md` : configuration seule.
- Mini-apps : manifeste `agents`, `capabilities`, `dataContracts` (`shared/src/rowboat-app.ts:12-34`), registre GitHub, installeur protégé ; elles n'ajoutent ni outil ni MCP.
- Navigateur Electron piloté par l'agent, terminal `node-pty`.
- **Distance à Cordis** : pas de plugin tree ni de seams ; le catalogue d'outils, la mémoire et le runtime sont du code. Les skills et agents en fichiers couvrent la composition, pas le remplacement de fournisseurs.

### A7 — Modèles et routage LLM — **note 3**

- Vercel AI SDK v7, 9 flavors : openai, anthropic, google, openrouter, aigateway, ollama, openai-compatible, rowboat, codex (`$C/models/models.ts:26-90`). `config/models.json` v2 : providers (clé, baseURL, headers, contextLength, reasoningEffort), `assistantModel`, `taskModels`, `imageModel`.
- Local : Ollama (contexte 32k forcé, mappage `think`, `models/local.ts`) ; LM Studio, vLLM et autres via openai-compatible (`localhost:1234/v1` par défaut). Capacités sondées (`models.ts:113-185`). **Une seule instance par flavor** (`shared/models.ts:37-39`) : impossible d'avoir vLLM et LM Studio en même temps.
- Slots par tâche : `knowledgeGraph`, `meetingNotes`, `liveNoteAgent`, `autoPermissionDecision`, `chatTitle`, `backgroundTask`, `subagent` (`models/defaults.ts:93-153`) ; `deferBackgroundTasks` pour le matériel local.
- Aucun routage dynamique. Point d'insertion d'un routeur (C11) : `RealModelRegistry.resolve()` (`real-model-registry.ts:85-118`, injecté par le conteneur), ou un flavor « router » / middleware `wrapLanguageModel`, ou `getCategoryModel` pour un routage par tâche.

### A8 — Fichiers et ressources — **note 3**

- Envoi en deux temps : `PUT /v1/spaces/:id/blobs` avec `x-blob-sha256` calculé côté client, Harbor recalcule, détecte le MIME (`client.ts:495-520`) ; puis `createAsset {path, newContent | blob}` ou `proposeChange {assetId, baseVersion, newContent | blob}`. Outil agent `spaces-upload-blob` puis `create_asset` (`domains/spaces.ts:234-270`). Pas de bouton « partager cette note locale » : le partage passe par la conversation, l'agent ou le glisser-déposer.
- Versionnement : contenu entier contre une version de base, merge à trois voies ligne à ligne, issues `applied | merged | conflict` avec `currentContent` et régions ; UI de résolution `spaces/file-conflict.tsx:29-90`. Assets par id, déplacer ou supprimer ne change pas la version.
- Téléchargement en streaming ou 302 vers S3 présigné, cache local adressé par contenu. Limites : 100 MiB par blob, 1 MiB avatar, 2 MiB tampon WS.
- Stockage Harbor : Postgres (PGlite en dev), blobs disque (`blobs-disk.ts`) ou S3 (`blobs-s3.ts`). **Point d'insertion de SeaweedFS (C8) : son API S3, par `BLOBS_S3_*`, sans code.**

### A9 — Identité, secrets, politiques — **note 2**

- Harbor : `auth-oidc.ts:1-133`, émetteur épinglé, découverte RFC 8414, JWKS (`jose`, ES256 / RS256), audience optionnelle, mapping (iss, sub) → membre sans création automatique. **Générique, Keycloak cité et compatible** (C13) via `AUTH_ISSUER` ; un seul AS par déploiement (`deployment.ts:49-103`) ; page de consentement `consent.ts` spécifique Supabase, non montée si Keycloak héberge son login.
- Client : DCR obligatoire pour rejoindre une org (`spaces/oauth.ts:87-94`) : Keycloak devra autoriser la registration anonyme, ou il faudra un `client_id` statique.
- Clés d'agent `rbk_` hashées SHA-256, résolues avant tout driver, jamais exposées par un outil. Identifiants de plateforme scellés AES-256-GCM sous `HARBOR_INTEGRATION_KEY` (`sealing.ts`) ; KMS évoqué comme futur (SPEC:559).
- **Secrets client en JSON clair** sous `config/` : `models.json` (« the only copy of the user's keys », `models/repo.ts:199`), `oauth.json`, `spaces_orgs.json`, `composio.json`, `mcp.json` ; `safeStorage` seulement pour GitHub et ChatGPT (`apps/main/src/main.ts:687-698`). Écart doc / code : SPEC:144 dit « tokens stored in the OS keychain ». **Aucune intégration Vault, OpenBao ou 1Password.**
- Attribution universelle des actes (`actingMode`, « via agent »), politiques pures dans `policy.ts`, utile pour l'audit (I3).
- Point d'insertion OpenBao (C14) : un adaptateur de secret store côté client (repo `models`, `oauth`, `spaces_orgs`, `mcp`) et, côté Harbor, la source de `HARBOR_INTEGRATION_KEY` et des clés de plateforme.

### A10 — Interopérabilité standards — **note 3**

- MCP client (stdio, Streamable HTTP, SSE) ; Harbor expose `/mcp` avec parité REST / MCP testée (`mcp-parity.test.ts`) ; le client desktop n'expose pas de serveur MCP.
- ACP complet (code mode). A2A absent. OpenAPI absent pour Harbor.
- Contrat client-serveur zod partagé (`protocol/src/api.ts`, `events.ts`, `invocation.ts`), réponses validées avant envoi, zod 4.2.1 imposé des deux côtés ; préfixe `/v1` mais **v0 instable, sans négociation de version**.
- Auth conforme OAuth 2.1, RFC 9728, 8414, 7591.
- Pour I4 (Centaur) : rien côté client ; un connecteur Harbor `connectors/centaur/` (modèle des connecteurs replicas / agent37 / conductor) ou un bot (`connectors/commands.ts`) relierait un espace à une session Centaur par `thread_key`.

### A11 — Intégration services in-house — **note 1**

- Email : Gmail API ou Microsoft Graph uniquement (`knowledge/email/provider.ts:5-9`) ; **pas d'IMAP / SMTP ni JMAP**. Agenda : Google et Outlook Graph ; **pas de CalDAV**. Réunions : micro, Fireflies, Granola. Voix : Deepgram, ElevenLabs. Slack : CLI `agent-slack` avec jeton xoxc importé. Composio : 68 toolkits, optionnel, via le cloud Composio. WhatsApp : `baileys`.
- Documents : xlsx / csv via SheetJS, docx via mammoth et `@eigenpal/docx-editor-react`, pptx éditeur et création ; traitement local, pas de WOPI.
- **Nextcloud, WebDAV, CalDAV, CardDAV, OnlyOffice, Collabora : aucune occurrence.** Chemins indirects : MCP tiers (Nextcloud MCP, IMAP MCP), outils shell, ou connecteur Harbor de type bot (modèle `posthog/`, qui accepte déjà une instance auto-hébergée).

### A12 — Qualité d'ingénierie et pérennité — **note 3**

- `strict: true` partout, aucun `@ts-ignore`, ~42 `any` ; ~268 fichiers de test x, 56 Harbor, tout Harbor sur Postgres en processus ; lint du renderer exclu (« lint debt »).
- Documentation abondante et datée (SPEC 738 lignes, CONTRACT 246, `harbor/AGENTS.md` 128, plans) avec des conventions fortes (commentaires « pourquoi + date + PR », un document par type de fait, doc mise à jour dans la PR) ; dérives constatées (« 17/356 », défaut in-process) ; `apps/x` sans guide.
- Bus factor élevé, pas de documents de gouvernance, contrat v0.

### A13 — Déployabilité on-premise — **note 2**

- Build pnpm en cascade (protocol → shared → spaces-client → core → server → client → preload), Harbor à construire d'abord (`AGENTS.md:9-17`) ; electron-forge avec makers dmg, squirrel, deb, rpm, pacman, zip ; CI `electron-build.yml` (macOS arm64 / x64 signés, Linux, Windows), `x-tests.yml` (lint, vitest, typecheck) ; CI PR signalée « flaky ».
- Docker : **Harbor seulement** (`apps/harbor/Dockerfile`, Node 22) ; serveur Rowboat headless en tarball + systemd, sans image.
- Mobile Expo iOS centré Spaces, sans test ; web Spaces Vite sur Vercel, cookie de session, sans runtime local.

**Inventaire des stores (contrainte de stack, §5 du référentiel).**

| Tier | Moteur | Rôle | Verdict |
|---|---|---|---|
| Client | fichiers Markdown + git local, JSONL, JSON | connaissances, tours, config | local, **aucune base** : idéal |
| Client | localStorage | état UI | local, toléré |
| Client | cache `cache/blobs/<sha256>` | blobs Spaces | local, toléré |
| Harbor | PostgreSQL | tout l'état des Spaces | **conforme** |
| Harbor | PGlite | dev et tests seulement | hors production |
| Harbor | blobs disque ou S3 | contenu des fichiers | **conforme via SeaweedFS S3** (`BLOBS_S3_*`) ; sinon un pilote de blobs PostgreSQL derrière l'interface `blobs.ts` |
| — | Redis, vecteur, graphe | — | **aucun** |

## 4. Points d'insertion pour la cible

| Cible | Où | Effort |
|---|---|---|
| Cognee MCP (I5) | `config/mcp.json` avec `headers` ; puis projection en outils natifs sur le modèle de `domains/spaces.ts`, outils `memory-recall` / `memory-remember` dans `COPILOT_BASE_TOOLS`, amendement de `instructions.ts:271-297` | nul en configuration ; faible en code |
| OKF (I1, I2) | convertisseur Brain ↔ bundle OKF (frontmatter, `index.md`, `log.md` depuis git, wikilinks → liens) sans toucher au cœur ; `save-to-memory` en double écriture vers Cognee | moyen |
| Keycloak (C13) | Harbor : `AUTH_ISSUER` ; client : autoriser la DCR ou ajouter un `client_id` statique dans `spaces/oauth.ts` | faible |
| OpenBao (C14) | adaptateur de secret store côté client (quatre fichiers JSON) ; source de `HARBOR_INTEGRATION_KEY` côté Harbor | moyen |
| A2A, Hermes (C3, C9) | Hermes : acquis (`hermes/plugin`) ; A2A : connecteur Harbor `connectors/a2a/` + paire `AGENT_PAIRS` | faible pour Hermes, moyen pour A2A |
| Centaur (I4) | connecteur Harbor `connectors/centaur/` (thread ↔ `thread_key`, SSE → messages) ; côté Centaur, une clé d'ingress dédiée (annexe A §2) | moyen |
| Spaces d'organisation (I3) | acquis : Harbor et le client | nul |
| Routeur LLM (C11) | `RealModelRegistry.resolve()` ou flavor « router » ; lever la limite d'une instance par flavor | faible |
| SeaweedFS (C8) | `BLOBS_S3_*` | nul |
| Services in-house (C12) | MCP tiers ou connecteur bot Harbor ; IMAP / CalDAV / WebDAV à écrire | élevé |

## 5. Forces, faiblesses, risques

**Forces**
1. Le poste est un second cerveau en fichiers ouverts : Markdown versionné, JSONL, aucune base ; distance moyenne à OKF, convertisseur faisable hors du cœur.
2. Spaces et Harbor réalisent déjà I3 : espace d'organisation, membres humains et agents, projection du contexte local par `@rowboat`, blobs adressés par contenu, merge à trois voies, MCP de parité, OIDC générique compatible Keycloak, S3 compatible SeaweedFS, PostgreSQL seul.
3. Hermes Agent est un connecteur existant ; le contrat d'invocation durable et les connecteurs isolés sont des points d'insertion propres pour A2A et Centaur ; la couche modèles est injectable avec un point d'insertion unique pour le routeur.

**Faiblesses**
1. Ressources tierces consommées indirectement : méta-outils MCP, permission par appel, priorité basse, mémoire soudée au grep ; pas d'OAuth MCP générique ; interface MCP réduite à du JSON.
2. Secrets client en clair et absence d'abstraction de secret store ; DCR obligatoire ; télémétrie opt-out et défauts cloud à surcharger.
3. Services in-house absents (ni IMAP, CalDAV, WebDAV, Nextcloud, WOPI) ; extensibilité par code pour les outils natifs ; contrat v0 instable, séparation inachevée, bus factor élevé.

**Risques de fork**
- Contrat Spaces « deliberately unstable » et dépendances `link:` : suivre l'amont coûtera des rebases fréquents.
- Produit cloud-adjacent : passerelle LLM, Exa, TTS, Composio, apex, PostHog à neutraliser par configuration et nettoyage.

## 6. Tableau des notes

| Axe | Note | Pondération | Contribution |
|---|---|---|---|
| A0 ressources tierces et lisibilité | 2 | ×2 | 4 |
| A1 local-first | 3 | ×1 | 3 |
| A2 séparation | 3 | ×1 | 3 |
| A3 environnement partagé | 3 | ×1 | 3 |
| A4 agents | 3 | ×1 | 3 |
| A5 mémoire et connaissances | 3 | ×1 | 3 |
| A6 extensibilité | 2 | ×1 | 2 |
| A7 modèles | 3 | ×1 | 3 |
| A8 fichiers | 3 | ×1 | 3 |
| A9 identité et secrets | 2 | ×1 | 2 |
| A10 standards | 3 | ×1 | 3 |
| A11 services in-house | 1 | ×1 | 1 |
| A12 qualité | 3 | ×1 | 3 |
| A13 déployabilité | 2 | ×1 | 2 |
| **Total** | | sur 60 | **38** |
