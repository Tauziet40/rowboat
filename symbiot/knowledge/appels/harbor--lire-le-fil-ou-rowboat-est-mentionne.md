---
type: Appel
title: Harbor — Lire le fil où @rowboat est mentionné
description: I3 : GET /v1/spaces/:id/threads/:root ; GET …/messages/:id
tags:
  - serveur
  - poste
flux: I3
brique: /composants/harbor.md
appel: GET /v1/spaces/:id/threads/:root ; GET …/messages/:id
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Lire le fil où @rowboat est mentionné

| | |
|---|---|
| **Flux** | I3 |
| **Besoin** | Lire le fil où @rowboat est mentionné |
| **Service client** | `apps/x/packages/spaces-client/src/client.ts` listThread, getMessage ; MCP `read_thread` |
| **Appel** | GET /v1/spaces/:id/threads/:root ; GET …/messages/:id |
| **Contrat** | `apps/harbor/packages/protocol/src/api.ts` routes.listThread, routes.getMessage |
| **Fonction servie** | `apps/harbor/packages/server/src/http.ts:672`, :667 → core/feed.ts:267, :299 ; mcp.ts:239 |
| **Auth** | Bearer |
| **Événements / statut** | aucun |
| **Test au fil** | `apps/harbor/packages/server/test/pagination.test.ts` |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
