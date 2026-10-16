---
type: Appel
title: Harbor — Résoudre un conflit
description: I3 : GET …/diff ; GET …/history ; MCP `diff`, `asset_history`
tags:
  - serveur
  - poste
  - mcp
flux: I3
brique: /composants/harbor.md
appel: GET …/diff ; GET …/history ; MCP `diff`, `asset_history`
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Résoudre un conflit

| | |
|---|---|
| **Flux** | I3 |
| **Besoin** | Résoudre un conflit |
| **Service client** | `apps/x/packages/spaces-client/src/client.ts` readAsset, diff, assetHistory puis proposeChange |
| **Appel** | GET …/diff ; GET …/history ; MCP `diff`, `asset_history` |
| **Contrat** | `apps/harbor/packages/protocol/src/api.ts` routes.diff, routes.assetHistory |
| **Fonction servie** | `apps/harbor/packages/server/src/http.ts:566` (diff), :555 (history) ; fusion core/assets.ts:403 (merge.ts) |
| **Auth** | Bearer |
| **Événements / statut** | `change` au re-propose |
| **Test au fil** | `apps/harbor/packages/server/test/merge.test.ts`, asset-ops.test.ts |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
