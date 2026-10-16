# decisions

- [D1 — Bases de données](D01-bases-de-donnees.md) — PostgreSQL pour le relationnel, FalkorDB pour vecteurs et graphe, pas de pgvector ; Cognee comme middleware de peuplement des bases vecteur et graphe pour les frameworks. (stable)
- [D2 — Substrat d'exécution et de sandbox commun](D02-substrat-d-execution-et-de-sandbox-commun.md) — k3s pour tous les éléments serveur ; la primitive de sandbox est le CRD Agent Sandbox. (stable)
- [D3 — Tenance](D03-tenance.md) — Rôles PostgreSQL et schémas par application, FalkorDB en graphes nommés, SeaweedFS en buckets, Keycloak en clients, namespaces k3s : le quintuplet de tenance. (stable)
- [D4 — Identité](D04-identite.md) — Le sub Keycloak partout, un realm, orgs = orgs Harbor ; Agent Stack forké pour identifier par sub ; Centaur reçoit la validation JWT Keycloak ; Cognee provisionné depuis Keycloak. (stable)
- [D5 — Secrets](D05-secrets.md) — OpenBao source unique, un seul patron de courtier (modèle iron-proxy), un adaptateur par brique. (stable)
- [D6 — Hébergement des agents](D06-hebergement-des-agents.md) — CRD Agent Sandbox comme primitive commune ; Centaur = sessions en sandbox et workflows durables ; Agent Stack = agents de service A2A et registre ; DSH = harness dans une sandbox Centaur. (stable)
- [D7 — Gouvernance](D07-gouvernance.md) — Une API de politique unique adossée à la console des spaces, consultée par Harbor, DSH, BeeAI, Agent Stack, Cognee. (stable)
- [D8 — Connaissance](D08-connaissance.md) — OKF format d'échange, Brain converti, Cognee ingère ; règle d'alignement type OKF ↔ classes de l'ontologie Cognee ; convention de tenance Cognee consignée depuis l'installation existante. (stable)
- [D9 — Modèles](D09-modeles.md) — Le proxy serveur (Agent Stack) est l'autorité de routage et de quota, GPU publié au cluster ; le routeur client ne décide qu'en local ou hors ligne. (stable)
- [D10 — Core et inspirants](D10-core-et-inspirants.md) — Processus core (D0 à D3, qualifié par fork de stockage et substrat) distinct du processus inspirants (D4 et D5, principes transplantés sur les core validés) : MemoryBear, Eigent, ElephantBroker, Synapse sont inspirants. (stable)
- [D11 — Flux d'événements et versions](D11-flux-d-evenements-et-versions.md) — Le journal append-only de Harbor est le flux canonique ; aucun bus supplémentaire ; versions de Harbor et DSH épinglées. (stable)
