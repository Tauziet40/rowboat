---
type: Appel
title: Harbor — Proposer une nouvelle version, texte ou blob
description: I3 : POST /v1/spaces/:id/changes ou MCP `propose_change`
tags:
  - serveur
  - poste
  - mcp
flux: I3
brique: /composants/harbor.md
appel: POST /v1/spaces/:id/changes ou MCP `propose_change`
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Proposer une nouvelle version, texte ou blob

| | |
|---|---|
| **Flux** | I3 |
| **Besoin** | Proposer une nouvelle version, texte ou blob |
| **Service client** | `apps/x/packages/spaces-client/src/client.ts` proposeChange ; MCP callOrgTool (`apps/x/packages/core/src/runtime/tools/domains/whiteboard.ts`) |
| **Appel** | POST /v1/spaces/:id/changes ou MCP `propose_change` |
| **Contrat** | `apps/harbor/packages/protocol/src/api.ts` routes.proposeChange ; changeset.ts ProposeChange, ProposeChangeResult (applied / merged / conflict) |
| **Fonction servie** | `apps/harbor/packages/server/src/http.ts:548` ; mcp.ts:296 → service.ts:348 → core/assets.ts:403 |
| **Auth** | Bearer |
| **Événements / statut** | `change` si applied ou merged ; rien si conflict |
| **Test au fil** | `apps/harbor/packages/server/test/day-in-the-life.test.ts`, merge.test.ts, mcp.test.ts ; `apps/x/packages/core/src/runtime/tools/domains/whiteboard.test.ts` |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
