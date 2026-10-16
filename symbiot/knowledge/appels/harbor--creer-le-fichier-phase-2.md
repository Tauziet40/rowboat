---
type: Appel
title: Harbor — Créer le fichier, phase 2
description: I3 : POST /v1/spaces/:id/assets ou MCP `create_asset`
tags:
  - serveur
  - poste
  - mcp
flux: I3
brique: /composants/harbor.md
appel: POST /v1/spaces/:id/assets ou MCP `create_asset`
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Créer le fichier, phase 2

| | |
|---|---|
| **Flux** | I3 |
| **Besoin** | Créer le fichier, phase 2 |
| **Service client** | `apps/x/packages/spaces-client/src/client.ts` createAsset (IPC spaces:createAsset, `apps/x/packages/spaces-client/src/channels.ts:109`) ; MCP via callOrgTool |
| **Appel** | POST /v1/spaces/:id/assets ou MCP `create_asset` |
| **Contrat** | `apps/harbor/packages/protocol/src/api.ts` routes.createAsset ; changeset.ts CreateAsset / CreateAssetResult ; mcp.ts mcpTools create_asset |
| **Fonction servie** | `apps/harbor/packages/server/src/http.ts:515` ; mcp.ts:282 → service.ts:289 → core/assets.ts:144 |
| **Auth** | Bearer |
| **Événements / statut** | SpaceEvent `change` (changeSet) |
| **Test au fil** | `apps/harbor/packages/server/test/asset-ops.test.ts`, api.test.ts, mcp.test.ts ; `apps/x/packages/spaces-client/src/client.test.ts` |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
