# Comparatif Rowboat vs Eigent et recommandation pour le client Symbiot

**Statut :** version de travail du 2026-10-15, soumise à validation
**Sources :** [02-fiche-rowboat.md](02-fiche-rowboat.md), [03-fiche-eigent.md](03-fiche-eigent.md), [annexe A](annexe-A-interfaces-serveur.md) ; référentiel [01-architecture-cible-symbiot.md](01-architecture-cible-symbiot.md)

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
