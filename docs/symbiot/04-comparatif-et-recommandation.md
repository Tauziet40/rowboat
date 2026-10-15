# Comparatif Rowboat vs Eigent et recommandation pour le client Symbiot

**Statut :** version de travail du 2026-10-15, soumise à validation ; §8 ajouté le même jour (plan v3.3), complété en v3.4 (MemoryBear, Synapse AI)
**Sources :** [02-fiche-rowboat.md](02-fiche-rowboat.md), [03-fiche-eigent.md](03-fiche-eigent.md), [02b-fiche-beeai-framework.md](02b-fiche-beeai-framework.md), [02c-fiche-agentstack.md](02c-fiche-agentstack.md), [02d-fiche-memorybear.md](02d-fiche-memorybear.md), [02e-note-synapse-ai-workflows-apps.md](02e-note-synapse-ai-workflows-apps.md), [annexe A](annexe-A-interfaces-serveur.md), [annexe B](annexe-B-dsh-seams.md) ; référentiel [01-architecture-cible-symbiot.md](01-architecture-cible-symbiot.md)

---

## 1. Grille côte à côte

Notation 0–4 ; A0 pondéré ×2 ; justifications détaillées dans les fiches.

| Axe | Rowboat | Eigent | Lecture |
|---|---|---|---|
| **A0** ressources tierces et lisibilité (×2) | **2** | **2** | Les deux consomment un MCP standard et branchent Cognee par configuration. Rowboat : accès indirect par méta-outils, permission par appel, état des connexions exposé. Eigent : outils directs mais erreurs silencieuses, mémoire soudée, trajectoires multiples. Rowboat a le chemin le plus court vers 3 (projection en outils natifs déjà codée pour Harbor). |
| A1 local-first | **3** | 2 | Rowboat : fichiers ouverts, aucune base, BYOK, cloud optionnel. Eigent : cloud par défaut, clés BYOK envoyées au serveur. |
| A2 séparation | 3 | 3 | Rowboat : mode distant validé, bearer, mono-utilisateur. Eigent : trois tiers nets, Brain distant sans auth. |
| A3 environnement partagé | **3** | 1 | Rowboat : Spaces et Harbor, membres humains et agents, projection `@rowboat`. Eigent : Space mono-utilisateur, rien à partager. |
| A4 agents | 3 | 3 | Rowboat : Hermes en connecteur, invocations durables, agents de fond, ACP ; orchestration minimale. Eigent : Workforce CAMEL, journal rejouable, HITL typé, permissions ; un seul sous-agent distant, pas de Hermes. |
| A5 mémoire et connaissances | **3** | 2 | Rowboat : Markdown versionné, distance moyenne à OKF, aucun store. Eigent : SQLite propriétaire, sémantique proche mais forme éloignée. |
| A6 extensibilité | 2 | **3** | Eigent : SKILL.md, bundles versionnés, Agent Plugins, Hands. Rowboat : SKILL.md et agents en fichiers, outils natifs par code, mini-apps sans outils. |
| A7 modèles | **3** | 2 | Rowboat : AI SDK injectable, slots par tâche, point d'insertion unique. Eigent : CAMEL ModelFactory, catalogue étroit, round-robin. |
| A8 fichiers | **3** | 2 | Rowboat : blobs par hash, merge à trois voies, S3 (SeaweedFS). Eigent : git local riche, mais métadonnées seules vers le serveur. |
| A9 identité et secrets | **2** | 1 | Rowboat : Harbor OIDC générique (Keycloak), secrets client en clair. Eigent : Stack Auth SaaS + HS256, pas d'OIDC, secrets en clair poste et serveur. |
| A10 standards | **3** | 2 | Rowboat : MCP client et serveur, ACP, OAuth 2.1, contrat zod. Eigent : MCP client, OpenAPI, contrats manuels. Aucun des deux n'a A2A. |
| A11 services in-house | 1 | **2** | Aucun des deux ne parle IMAP, CalDAV, WebDAV, Nextcloud ou WOPI. Eigent a LibreOffice en skill. |
| A12 qualité | **3** | 2 | Rowboat : strict, tests, docs datées, conventions. Eigent : gros volume de tests mais fichiers monstres, préversions figées, licence incohérente. |
| A13 déployabilité | 2 | 2 | Rowboat : Docker Harbor seul, build en cascade. Eigent : compose non durci, Redis non documenté, SSO absent. |
| **Total sur 60** | **38** | **31** | |

Sans la pondération d'A0, les totaux sont 36 et 29 : l'écart ne vient pas du critère déterminant, sur lequel les deux clients sont à égalité, mais de la couverture structurelle de la cible.

## 2. Couverture de la cible

### Intégrations I1–I5

| Intégration | Rowboat | Eigent |
|---|---|---|
| I1 second cerveau local, exportable en OKF | **Acquis en substance** : dossier Markdown versionné, un concept par fichier ; convertisseur OKF à écrire hors du cœur | À construire : mémoire en tables SQLite, exporteur à écrire, pas de documents |
| I2 optimisation du second cerveau par le serveur (Cognee) | Faisable : le bundle Markdown est l'unité d'échange naturelle avec `remember` ; retour par `recall` ou par bundle OKF réécrit | Faisable mais plus lourd : export SQLite → documents, puis réimport, en concurrence avec l'extracteur interne |
| I3 productions partagées à l'organisation (Spaces, blobs Harbor) | **Acquis** : Harbor, client, blobs, merge, attribution | Absent : Space mono-utilisateur, aucun contenu téléversé ; à construire ou à déléguer à Harbor |
| I4 messagerie inter-espaces via Centaur | À construire des deux côtés : connecteur Harbor + clé d'ingress Centaur | À construire : client de session dans le Brain + ingress Centaur |
| I5 mémoire et RAG d'entreprise (MCP Cognee, MCP OKF) | Par configuration, puis projection native (faible) | Par configuration, puis remplacement de la mémoire interne (moyen) |

### Composants C1–C14

| Composant | Rowboat | Eigent |
|---|---|---|
| C1 client local-first | fort | moyen (cloud par défaut) |
| C2 environnement partagé | **Harbor, acquis** | absent |
| C3 agents autonomes façon Hermes | **connecteur Hermes existant** | absent (un seul fournisseur distant, Gemini) |
| C4 PostgreSQL | Harbor : conforme | serveur : conforme |
| C5 FalkorDB | hors client (serveur) | hors client (serveur) |
| C6 OKF + MCP dédié | convertisseur à écrire, distance moyenne | exporteur à écrire, distance élevée |
| C7 Cognee | MCP par configuration | MCP par configuration |
| C8 SeaweedFS | **S3 natif dans Harbor** | pas de téléversement serveur |
| C9 A2A | absent ; connecteur Harbor à écrire | absent ; `RemoteSubAgentProvider` à écrire |
| C10 plugins façon Cordis | éloigné (code) | éloigné (bundles de composition, pas de seams) |
| C11 routeur LLM | point d'insertion unique | point d'insertion unique |
| C12 services in-house | absent | absent (LibreOffice en skill) |
| C13 Keycloak | **Harbor compatible** ; client à ajuster (DCR) | chaîne d'auth à réécrire |
| C14 OpenBao | adaptateur à écrire, secrets en clair | adaptateur à écrire côté client (broker à capacité existant), serveur à réécrire |

## 3. Inventaire des stores et plan de migration par fork

Contrainte : rien d'autre que PostgreSQL et FalkorDB côté serveur ; un store strictement local au poste est toléré.

| Client | Store | Tier | Verdict | Résorption par fork |
|---|---|---|---|---|
| Rowboat | fichiers Markdown, git local, JSONL, JSON | poste | toléré, idéal | — |
| Rowboat | PostgreSQL (Harbor) | serveur | conforme | — |
| Rowboat | blobs disque ou S3 (Harbor) | serveur | conforme via SeaweedFS S3 | configuration `BLOBS_S3_*` ; sinon pilote de blobs PostgreSQL derrière `blobs.ts` (faible) |
| Rowboat | PGlite | dev / tests | hors production | — |
| Eigent | SQLite `run-journal.sqlite3` | poste | toléré ; source de vérité de la mémoire | export nécessaire pour I2 |
| Eigent | Qdrant local | poste | toléré, inactif | retrait au fork (faible) |
| Eigent | PostgreSQL 15 | serveur | conforme | — |
| Eigent | **Redis 7** | serveur | **écart** | migrer broker Celery, sessions, blacklist et pub/sub vers PostgreSQL (`LISTEN/NOTIFY`, table de jobs) : moyen à élevé |
| Eigent | fichiers disque (captures) | serveur | **écart** | vers SeaweedFS : moyen |

Rowboat n'impose aucune migration de store. Eigent en impose deux côté serveur, en plus du modèle d'espace à inventer.

## 4. Scénarios

### (a) Partir de Rowboat — **recommandé**

Rowboat réalise déjà trois des cinq intégrations en substance (I1, I3, I5 par configuration) et porte le connecteur Hermes. Sa stack serveur est conforme sans migration, Harbor accepte Keycloak et SeaweedFS par variables d'environnement. Les écarts restants sont des chantiers bornés : projection native de Cognee, convertisseur OKF, adaptateur OpenBao, connecteurs Centaur et A2A, routeur LLM, services in-house via MCP.

Coût principal : suivre un amont instable (contrat v0, dépendances `link:`), neutraliser les défauts cloud et la télémétrie, chiffrer les secrets du poste.

### (b) Partir d'Eigent

Eigent apporte la meilleure gouvernance d'agents (journal rejouable, interactions humaines typées, permissions à tags de risque) et la meilleure extensibilité déclarative (bundles, skills, Agent Plugins). Mais il faudrait construire l'intégralité de l'environnement partagé (I3), réécrire l'identité (C13), migrer Redis et les fichiers serveur, exporter la mémoire SQLite, et écrire le client Centaur et A2A. La dette de fork est lourde (fichiers de 10 à 20 k lignes, préversions CAMEL divergentes).

### (c) Hybride : socle Rowboat, emprunts à Eigent

C'est la forme concrète de (a). Emprunts ciblés, à réimplémenter dans le socle Rowboat plutôt qu'à porter tels quels (Python CAMEL contre TypeScript) :

| Emprunt à Eigent | Pour quel besoin Symbiot | Où dans Rowboat |
|---|---|---|
| Moteur de permissions allow / prompt / deny avec profils et tags de risque (`permission_policy`) | gouvernance des agents autonomes et des appels MCP (remplacer la permission par appel) | `$C/runtime/turns/bridges/real-permission-checker.ts`, `security/` |
| Journal des runs avec `human_interactions` typées et `security_audit_events` | audit attribué des actes d'agents, I3 et I4 | `storage/turns` (JSONL) étendu, ou table Harbor pour la part partagée |
| Format de bundle déclaratif versionné (`workspace.yaml`, lockfile, `secretSlots`) | description d'un agent et de ses ressources, base d'une Agent Card A2A | `~/.rowboat/agents/*.md` → bundle |
| Abstraction `IHands` et cluster HTTP | exécution déportée (sandbox Centaur) | runtime des tours |
| Broker de secrets loopback à capacité | distribution des secrets OpenBao aux agents sans les mettre dans l'environnement | adaptateur de secret store |

## 5. Écarts priorisés et ordre de chantiers (scénario (c))

| # | Chantier | Intégration / composant | Effort | Dépend de |
|---|---|---|---|---|
| 0 | Neutraliser les défauts cloud : `API_URL`, apex Spaces, PostHog opt-in, Composio et TypeSafe désactivés par défaut ; chiffrer `models.json`, `oauth.json`, `spaces_orgs.json`, `mcp.json` par `safeStorage` | C1, C14 | faible | — |
| 1 | Keycloak : Harbor `AUTH_ISSUER` ; client avec `client_id` statique ou DCR autorisée | C13 | faible | — |
| 2 | Cognee natif : projection des outils MCP de Cognee en outils natifs (modèle `domains/spaces.ts`), `memory-recall` et `memory-remember` dans les outils de base, amendement du prompt (`instructions.ts:271-297`), double écriture de `save-to-memory` ; journalisation des connexions MCP | I5, A0 | faible à moyen | 0 |
| 3 | Convertisseur OKF : Brain ↔ bundle (frontmatter `type`, `title`, `sources`, `generated`, `verified`, `status`, `stale_after` ; `index.md` par dossier ; `log.md` depuis git ; wikilinks → liens) ; commande « soumettre au serveur » qui envoie le bundle à `remember` et réintègre le résultat | I1, I2, C6 | moyen | 2 |
| 4 | OpenBao : adaptateur de secret store client (quatre dépôts JSON) et source de `HARBOR_INTEGRATION_KEY` et des clés de plateforme côté Harbor | C14 | moyen | 0 |
| 5 | Centaur : connecteur Harbor `connectors/centaur/` (thread ↔ `thread_key`, SSE `session.output.line` → messages, approbations) ; côté Centaur, une clé d'ingress dédiée au connecteur | I4 | moyen | 1 |
| 6 | A2A : connecteur Harbor `connectors/a2a/` lisant une Agent Card et pilotant les tâches ; génération d'Agent Cards pour les agents Rowboat et Hermes depuis un bundle (emprunt Eigent) | C9 | moyen | 5 |
| 7 | Routeur LLM : flavor « router » ou middleware dans `RealModelRegistry.resolve()`, règles local / cloud par tâche et par sensibilité ; lever la limite d'une instance par flavor | C11 | faible | — |
| 8 | SeaweedFS : `BLOBS_S3_*` sur Harbor ; cache local inchangé | C8 | nul | — |
| 9 | Gouvernance des agents : moteur de permissions à profils et tags de risque, journal d'interactions typées (emprunts Eigent) | C3, A4 | moyen | 2 |
| 10 | Services in-house : serveurs MCP IMAP / SMTP, CalDAV, WebDAV Nextcloud, et connecteur bot Harbor pour Nextcloud ; bureautique via conversion locale ou WOPI ultérieur | C12 | élevé | 2 |
| 11 | Ergonomie des connexions : UI MCP au-delà de l'éditeur JSON, état et journal par connexion | A0 | faible | 2 |

Les chantiers 0, 1, 7 et 8 sont indépendants et courts : ils constituent le premier incrément. Les chantiers 2 et 3 forment le cœur de valeur (second cerveau ↔ Cognee ↔ OKF). Les chantiers 5 et 6 ouvrent la messagerie inter-espaces et l'interopérabilité d'agents.

## 6. Risques et points ouverts

- **Amont Rowboat instable** : contrat Spaces v0, dépendances `link:`, séparation client / serveur inachevée. Mitigation : figer une révision, fork déclaré, rebases planifiés par trimestre.
- **Cognee en MCP sans authentification entrante** (annexe A §3) : à exposer derrière un reverse proxy qui vérifie le JWT Keycloak, ou à patcher.
- **Centaur n'a pas d'OIDC générique sur son API** (annexe A §2) : le connecteur Harbor portera une clé d'ingress ; l'unification sur Keycloak demande un travail côté Centaur, hors de ce périmètre.
- **Unification des identités** : Harbor mappe (iss, sub) → membre ; Cognee a ses utilisateurs et datasets ; Centaur ses principaux. Un annuaire de correspondance (sub Keycloak → membre Harbor → utilisateur Cognee → principal Centaur) est à définir avant les chantiers 2, 5 et 6.
- **Chiffrement des contenus du poste** : hors périmètre des deux clients ; à décider (chiffrement disque OS ou applicatif).
- **Licence** : Rowboat Apache 2.0, Eigent Apache 2.0 avec un `package.json` en MIT ; les emprunts à Eigent sont réimplémentés, pas copiés.

## 7. Recommandation

**Retenir Rowboat comme socle du client Symbiot, en scénario hybride (c).** Il couvre déjà l'environnement partagé, la projection du contexte local vers l'organisation, le connecteur Hermes, un second cerveau en Markdown proche d'OKF, et une stack serveur conforme sans migration. Les écarts sont des chantiers bornés, dont les quatre premiers sont courts. Eigent reste la référence pour la gouvernance des agents et le format de bundle, à réimplémenter dans le socle.

Décisions attendues à la validation de ce document :
1. Confirmer le scénario (c) et l'ordre des chantiers du §5.
2. Trancher l'annuaire d'identités (§6) avant le chantier 2.
3. Lancer le plan court du livrable L5 (contextes OKF pour l'équipe OpenRig) sur la base des chantiers 2 et 3.


## 8. Couche agents : BeeAI, DSH, Agent Stack, Centaur, et la place d'Eigent

Ce paragraphe répond à trois questions posées après la recommandation du §7 : Eigent peut-il se substituer à Rowboat ; DSH peut-il reprendre les principes d'Eigent ; comment s'articulent BeeAI Framework et Agent Stack, pressentis pour la couche agents. Les §1 à §7 restent valides : Rowboat est le client.

### 8.1 Eigent face à Rowboat

Eigent ne peut se substituer à Rowboat ni en totalité ni en partie sur le poste. En totalité, il faudrait reconstruire l'environnement partagé, l'identité OIDC, le connecteur Hermes et le téléversement de contenu (fiche Eigent, A3, A9, A8). En partie, la cohabitation de deux runtimes d'agents, deux mémoires locales, deux `mcp.json` et deux systèmes de permissions sur le même poste est le contraire de la lisibilité des connexions, et aucun des deux ne sait déléguer à l'autre. Eigent n'entre dans Symbiot que comme **agent membre d'un Space**, par un pont parlant le contrat d'agent de Harbor, et seulement si sa Workforce apporte quelque chose que la couche agents ci-dessous ne couvre pas. Les cinq principes d'Eigent sont désormais mesurés sur DSH et BeeAI ; ils ne justifient plus de garder Eigent.

### 8.2 Les cinq principes d'Eigent, portés par qui

| Principe | Eigent | DSH ([annexe B](annexe-B-dsh-seams.md)) | BeeAI ([fiche](02b-fiche-beeai-framework.md) §4) | Agent Stack ([fiche](02c-fiche-agentstack.md)) | Centaur ([annexe A](annexe-A-interfaces-serveur.md) §2) |
|---|---|---|---|---|---|
| (1) Journal durable rejouable | couvert (SQLite) | **couvert** (JSONL + zstd, fork, resume, approbations journalisées, format versionné) | partiel (événements, trajectoire ; ni persistance ni rejeu) | partiel (contexts et `context_history` en PostgreSQL) | couvert (sessions et événements SSE rejouables en PostgreSQL) |
| (2) Politique allow / prompt / deny, HITL typé, tags de risque | couvert | partiel (ask / deny / allow, question et choix ; pas de moteur de règles, de diff review ni de tags) | partiel (`AskPermission` binaire, règles conditionnelles) | partiel (extensions `approval` et `tool call`) | partiel (approbations via harness) |
| (3) Environnements d'exécution | partiel (`RemoteHands` placeholder) | partiel (local, sandbox OS, SSH ; pas de conteneur) | partiel (shell et fichiers locaux ou ACP ; interpréteur HTTP) | partiel (un pod par agent, pas de sandbox) | **couvert** (sandbox Kubernetes par session, iron-proxy) |
| (4) Bundles déclaratifs, secrets hors environnement | couvert | partiel (profils et bundles patchables ; secrets sans courtier) | absent | partiel (registre d'images, Fernet, Secrets k8s ; adaptateur OpenBao faisable) | partiel (tools et workflows en plugins ; secrets par iron-proxy depuis 1Password) |
| (5) Workforce coordinateur, planificateur, workers | couvert | partiel (subagents, Agent Teams expérimental, pas de planificateur) | partiel (coordinateur + handoffs, workflows séquentiels) | absent (délégué au framework) | partiel (`run_agents`, agents enfants) |
| Mémoire remplaçable → Cognee | soudée | overlay `mcp-client`, sans seam typé | `BaseMemory` sync, précédent Dakera en TS | connecteur MCP OAuth par utilisateur | MCP via catalogue d'outils |
| Description A2A | absent | absent | serve A2A (sans auth) | **natif**, agents unmanaged | absent |
| Exposition MCP | absent | absent | serve MCP | absent | `/mcp` console |
| Stabilité | préversions CAMEL | developer preview, ruptures annoncées, pas d'audit | 0.x mensuel, LF | 0.7 pré-1.0, LF | dépôt actif, Rust |

Lecture : aucun candidat ne couvre les cinq principes. Les deux qui en couvrent le plus sont DSH (journal, composition, exécution) et Centaur (sandbox, journal). Ce que personne ne fournit et qu'il faut écrire une fois : **le moteur de politique** avec interactions typées et étiquettes de risque, et **le courtier de secrets OpenBao**.

### 8.3 Articulation recommandée

| Rôle | Brique | Pourquoi | Ce qu'il faut ajouter |
|---|---|---|---|
| Client et second cerveau | **Rowboat** | §7 | chantiers 0 à 4 du §5 |
| Espaces d'organisation | **Harbor** | acquis, Keycloak et SeaweedFS par configuration | connecteurs (ci-dessous) |
| Écriture des agents | **BeeAI Framework, Python** | la couverture de protocoles la plus large (A2A, MCP, ACP, OpenAI), `RequirementAgent` comme base de politique, DeepSeek et Ollama natifs, LF et Apache 2.0 | loader OKF ; `BaseMemory` Cognee ; auth sur le serve A2A ; mapping `io_confirm` → `input_required` |
| Harness d'exécution | **DSH**, épinglé | journal rejouable, bundles Cordis, sandbox et SSH, ACP ; même langage que Rowboat ; profil ACP que le code mode de Rowboat sait déjà piloter | plugin de politique ; `CredentialProvider` OpenBao ; fournisseur sandbox Centaur ; presets de rôles ; plugin de connexion à Harbor (clé `rbk_`, invocations) |
| Registre et runtime des agents de service, A2A | **Agent Stack** | A2A natif avec Agent Card, Keycloak intégré, PostgreSQL et SeaweedFS natifs, proxy LLM comme point d'insertion du routeur, connecteurs MCP OAuth par utilisateur | corriger l'identité par email, chiffrer `connectors.auth`, adaptateur OpenBao, migrer Redis (2 à 4 jours) ; wrapper Python pour DSH et Hermes ou enregistrement unmanaged |
| Console d'administration des spaces (C15) | **à construire**, UX reprise de MemoryBear, back-office neuf | MemoryBear a le modèle tenant → espace → membre et l'UX, mais ni liste blanche de capacités par espace, ni API de politique, ni OIDC, ni audit, et son plan d'administration est imbriqué dans le moteur mémoire ([fiche](02d-fiche-memorybear.md) §3 A3, §4) ; l'UX a déjà été reprise, pas le back-office | back-office sur PostgreSQL et Keycloak : espaces alignés sur les orgs et spaces de Harbor, table espace ↔ capacité (modèles, skills, plugins, MCP, contextes OKF et datasets Cognee), API de politique consultée par Harbor (`policy.ts`), DSH (plugin `tools/pre-execute`), Agent Stack (permissions) et Cognee (datasets), audit |
| Workflows et apps no-code (C16) | **Rowboat** pour les mini-apps ; moteur de workflow à écrire en clean-room, Synapse non modifié en service séparé à court terme | Synapse est natif, AGPL sans CLA, sans builder d'app ([note](02e-note-synapse-ai-workflows-apps.md)) ; Rowboat tient déjà la mini-app (HTML autonome, agent backend, contrats de données) et les déclencheurs de fond | sous-ensemble de steps en TypeScript dans le moteur de tâches de fond de Rowboat (agent, llm, evaluator, if et switch avec évaluateur sûr, parallel, loop, human, end), `@xyflow/react` MIT si canvas |
| Messagerie inter-espaces et exécution en sandbox | **Centaur** | sandbox par session, workflows durables, iron-proxy ; mais pas d'OIDC et recouvrement avec Agent Stack | **décision** : le garder pour les sandboxes et les workflows, ou confier ces rôles à Agent Stack (sans sandbox) et à DSH (sandbox locale) ; dans les deux cas, I4 est un connecteur Harbor |

**Point de décision serveur.** Agent Stack et Centaur hébergent tous deux des agents partagés sur PostgreSQL et Kubernetes. Les garder tous deux double l'hébergement d'agents. Trois options :
- **S1, les deux** : Agent Stack comme registre A2A et passerelle LLM, Centaur pour les sandboxes et les workflows durables ; un connecteur Harbor vers chacun. Le plus complet, le plus lourd.
- **S2, Agent Stack seul** : les agents de service y tournent en pods ; DSH fournit la sandbox locale pour les agents de code ; les workflows durables sont à réécrire ou abandonnés. Le plus cohérent avec Keycloak et A2A.
- **S3, Centaur seul** : A2A par le serve BeeAI, Keycloak à ajouter sur l'API Centaur. Le plus de travail d'identité.

Recommandation : **S2**, sauf si l'exécution en sandbox serveur de harness en ligne de commande (Claude Code, Codex, Hermes) et les workflows durables sont des besoins confirmés, auquel cas S1.

### 8.4 Mémoire et connaissances dans cette articulation

- **Cognee** reste le fournisseur unique de mémoire et de RAG, atteint partout par MCP : overlay `mcp-client` dans DSH, `MCPTool.from_client` dans BeeAI, connecteur OAuth dans Agent Stack, `mcp.json` puis outils natifs dans Rowboat. Aucune brique n'a de seam mémoire typé ; c'est acceptable tant que Cognee est le seul fournisseur. Son MCP doit être placé derrière un reverse proxy qui vérifie le JWT Keycloak (annexe A §3).
- **OKF** : le second cerveau Rowboat en est la source côté poste (chantier 3 du §5) ; côté agents, un loader OKF BeeAI d'environ 50 lignes et un prompt qui cite `source` ; côté Cognee, `remember` ingère les bundles et `ontology_key` porte l'ontologie maintenue.
- **ElephantBroker** reste une illustration : il impose Neo4j, Qdrant, Redis et ClickHouse, et son authentification est un stub.
- **MemoryBear en post-traitement de Cognee** ([fiche](02d-fiche-memorybear.md) §4) : sa science est réelle (extraction bitemporelle, réflexion Layer2, insights, oubli audité, ontologie OWL compatible), mais il n'est pas branchable derrière Cognee : il n'ingère que des conversations, n'exporte rien en masse, impose Neo4j avec APOC et GDS, Elasticsearch et Redis, et traite le français comme du chinois. Il est une **carrière de logique de consolidation** à transplanter dans un post-traitement écrit autour de Cognee et FalkorDB, où ontologie, données et graphe restent uniques. Transplanter coûte moins que porter.

### 8.5 Chantiers supplémentaires (complètent le §5)

| # | Chantier | Composant | Effort | Dépend de |
|---|---|---|---|---|
| 12 | Déployer Agent Stack sur la stack existante : Keycloak existant via `externalOidcProvider`, SeaweedFS existant, migration du cache et du rate-limit hors Redis, chiffrement de `connectors.auth`, identité par `sub` | C9, C13, C8 | moyen | 1 |
| 13 | Moteur de politique partagé : règles allow / prompt / deny par outil et arguments, étiquettes de risque déterministes, interactions typées (question, choix, approbation, diff review) ; implémenté une fois comme plugin DSH (`tools/pre-execute`, `ctx.tools.guard`) et comme middleware BeeAI (`start` d'outil) | C3 | moyen à élevé | — |
| 14 | Courtier de secrets OpenBao : `CredentialProvider` DSH, `IEnvVariableRepository` Agent Stack, injection au constructeur pour BeeAI, adaptateur Rowboat (chantier 4) | C14 | moyen | — |
| 15 | DSH comme moteur de code mode de Rowboat par ACP (profil `acp`), et comme fournisseur `subagent-acp` pour les agents BeeAI | C3 | faible | — |
| 16 | Exposition A2A de DSH et Hermes : wrapper Python BeeAI ou Agent Stack enregistré unmanaged ; Agent Cards générées depuis les bundles | C9 | moyen | 12 |
| 17 | Connecteur Harbor vers Agent Stack (`connectors/agentstack/`, proxy A2A, approbations par `input_required`) ; remplace ou complète le connecteur Centaur du chantier 5 selon S1 / S2 | I3, I4 | moyen | 12 |
| 18 | Routeur LLM côté serveur dans le proxy OpenAI d'Agent Stack, cohérent avec le routeur client du chantier 7 | C11 | moyen | 12 |

| 19 | Console d'administration des spaces (C15) : back-office neuf sur PostgreSQL et Keycloak derrière l'UX reprise de MemoryBear ; modèle de données inspiré de MemoryBear (tenant, espace, membre, invitations, clés à scopes et quotas, emplacements de modèles) ; table espace ↔ capacité ; **API de politique** « U peut-il utiliser M / T / K dans S ? » consommée par Harbor, DSH, Agent Stack et Cognee ; audit des actions d'administration | C15 | élevé | 1, 12 |
| 20 | Post-traitement de Cognee : service de consolidation sur FalkorDB transplantant la logique MemoryBear (ancrage bitemporel, Layer2, insights, oubli audité), alimenté par `recall` ou par export de graphe, écrivant par `remember` et en bundles OKF ; détection de langue française | C7, C6 | élevé | 2, 3 |
| 21 | Workflows no-code (C16) : court terme, Synapse non modifié en service AGPL séparé appelé par l'agent backend d'une mini-app, v1 mono-processus ; à terme, sous-ensemble de steps en clean-room TypeScript dans le moteur de tâches de fond de Rowboat | C16 | moyen puis élevé | 2 |

Ordre suggéré après le premier incrément du §5 : 12 et 14 (socle serveur et secrets), puis 13 et 15 (gouvernance et harness), puis 19 (console et API de politique, qui conditionne la gouvernance partagée), puis 16, 17, 18, 20 et 21.

### 8.7 Relations repensées : ce qui gouverne quoi

- **Harbor** reste la source de vérité des orgs, des spaces et des membres (I3). La console C15 n'invente pas ses espaces : elle administre les capacités des spaces Harbor et pousse les décisions aux autres briques par l'API de politique. C'est ce qui rend « UX MemoryBear, back-office neuf » cohérent : le back-office est un plan de contrôle au-dessus de Harbor, pas une seconde base d'espaces.
- **Cognee** reste l'unique point d'unification du RAG et de la mémoire ; la console lui assigne datasets et ontologie par space ; le post-traitement (chantier 20) tourne derrière lui sur FalkorDB.
- **DSH** exécute, sous la politique de la console (plugin `tools/pre-execute` interrogeant l'API de politique) et avec les ressources que la console autorise (overlays `mcp-client` par space).
- **Agent Stack** héberge et expose en A2A ; ses permissions et ses connecteurs par utilisateur reçoivent les décisions de la console.
- **Rowboat** tient le poste : second cerveau, mini-apps et tâches de fond (C16 côté poste), projection vers les spaces.

### 8.8 Décisions attendues (suite)

7. Confirmer le rôle de MemoryBear : UX de la console et carrière de logique de consolidation, sans adoption du back-office ni du moteur. Sinon, dire quel autre rôle il tient.
8. Trancher C16 : Synapse en service AGPL séparé à court terme, puis clean-room TypeScript ; ou clean-room directement.

### 8.6 Décisions attendues (en plus du §7)

4. Confirmer l'articulation du §8.3 : BeeAI pour écrire les agents, DSH épinglé comme harness, Agent Stack comme registre A2A.
5. Trancher S1 / S2 / S3 pour Centaur.
6. Confirmer l'abandon d'Eigent et de MemoryBear comme briques, et leur maintien comme références.
