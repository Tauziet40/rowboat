# interfaces

- [BeeAI Framework — serve A2A, MCP et Agent Stack, client MCP et A2A, interception](beeai-framework.md) — Surfaces par lesquelles un agent BeeAI est exposé et consomme des ressources. (draft)
- [Cognee — surfaces MCP et REST consommées par le client](cognee.md) — MCP cognee-mcp (remember, recall, forget, cognify_status) et REST /api/v1 ; variables d'environnement qui changent le comportement. (draft)
- [DSH — ACP, SDK JSON-RPC, client MCP, politique, credentials](dsh.md) — Surfaces par lesquelles un client pilote DSH et par lesquelles DSH consomme Cognee, est gouverné et résout ses secrets. (draft)
- [Harbor — appels du client et frames initiées par le serveur](harbor.md) — Trois canaux : REST par SpacesClient, MCP par le serveur spaces-<org> projeté en outils natifs, WebSocket /v1/live ; frames poussées par le serveur et leurs consommateurs. (draft)
- [Interfaces côté client de la stack serveur](interfaces-serveur.md) — Conversion OKF du document de travail annexe-A-interfaces-serveur.md du dossier docs/symbiot (cycle des 15 et 16 octobre 2026). (stable)
