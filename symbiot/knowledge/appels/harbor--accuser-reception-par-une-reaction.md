---
type: Appel
title: Harbor — Accuser réception par une réaction
description: I3 : MCP `react` / POST …/messages/:id/reactions
tags:
  - serveur
  - poste
  - mcp
flux: I3
brique: /composants/harbor.md
appel: MCP `react` / POST …/messages/:id/reactions
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Accuser réception par une réaction

| | |
|---|---|
| **Flux** | I3 |
| **Besoin** | Accuser réception par une réaction |
| **Service client** | MCP `react` via callOrgTool |
| **Appel** | MCP `react` / POST …/messages/:id/reactions |
| **Contrat** | `apps/harbor/packages/protocol/src/api.ts` routes.reactToMessage |
| **Fonction servie** | `apps/harbor/packages/server/src/mcp.ts:378` ; http.ts:709 → core/feed.ts:704 |
| **Auth** | Bearer |
| **Événements / statut** | `reaction` |
| **Test au fil** | `apps/harbor/packages/server/test/mcp.test.ts` |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
