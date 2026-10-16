---
type: Appel
title: Harbor — Relire un fichier, version courante ou datée
description: I3 : GET /v1/spaces/:id/assets/:assetId?version= ou MCP `read_asset`
tags:
  - serveur
  - poste
  - mcp
flux: I3
brique: /composants/harbor.md
appel: GET /v1/spaces/:id/assets/:assetId?version= ou MCP `read_asset`
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Relire un fichier, version courante ou datée

| | |
|---|---|
| **Flux** | I3 |
| **Besoin** | Relire un fichier, version courante ou datée |
| **Service client** | `apps/x/packages/spaces-client/src/client.ts` readAsset ; `apps/x/packages/core/src/spaces/document-file.ts` materializeDocument |
| **Appel** | GET /v1/spaces/:id/assets/:assetId?version= ou MCP `read_asset` |
| **Contrat** | `apps/harbor/packages/protocol/src/api.ts` routes.readAsset ; changeset.ts ReadAssetResult |
| **Fonction servie** | `apps/harbor/packages/server/src/http.ts:540` ; mcp.ts:278 → core/assets.ts:95 |
| **Auth** | Bearer |
| **Événements / statut** | aucun |
| **Test au fil** | `apps/harbor/packages/server/test/open-spaces.test.ts`, mcp.test.ts |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
