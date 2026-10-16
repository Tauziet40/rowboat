---
type: Appel
title: Harbor — Relire les octets binaires
description: I3 : GET /v1/spaces/:id/blobs/:hash (302 ou flux)
tags:
  - serveur
  - poste
flux: I3
brique: /composants/harbor.md
appel: GET /v1/spaces/:id/blobs/:hash (302 ou flux)
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Relire les octets binaires

| | |
|---|---|
| **Flux** | I3 |
| **Besoin** | Relire les octets binaires |
| **Service client** | `apps/x/packages/spaces-client/src/client.ts` fetchBlob ; `apps/x/packages/core/src/spaces/blob-cache.ts` getBlob ; builtin spaces-download-blob |
| **Appel** | GET /v1/spaces/:id/blobs/:hash (302 ou flux) |
| **Contrat** | `apps/harbor/packages/protocol/src/api.ts` routes.getBlob ; ids.ts BlobHash |
| **Fonction servie** | `apps/harbor/packages/server/src/http.ts:605` → service.ts:339 downloadBlob |
| **Auth** | Bearer ou cookie |
| **Événements / statut** | aucun |
| **Test au fil** | `apps/harbor/packages/server/test/blobs-api.test.ts` |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
