---
type: Appel
title: Harbor — Téléverser les octets, phase 1
description: I3 : PUT /v1/spaces/:spaceId/blobs (+ x-blob-sha256)
tags:
  - serveur
  - poste
flux: I3
brique: /composants/harbor.md
appel: PUT /v1/spaces/:spaceId/blobs (+ x-blob-sha256)
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Téléverser les octets, phase 1

| | |
|---|---|
| **Flux** | I3 |
| **Besoin** | Téléverser les octets, phase 1 |
| **Service client** | `apps/x/packages/spaces-client/src/client.ts` uploadBlob ; `apps/x/packages/core/src/runtime/tools/domains/spaces.ts:235` builtin spaces-upload-blob |
| **Appel** | PUT /v1/spaces/:spaceId/blobs (+ x-blob-sha256) |
| **Contrat** | `apps/harbor/packages/protocol/src/api.ts` routes.uploadBlob ; blob.ts BlobInfo |
| **Fonction servie** | `apps/harbor/packages/server/src/http.ts:582` → service.ts:313 → core/assets.ts:317 |
| **Auth** | Bearer membre |
| **Événements / statut** | aucun (orphelin jusqu'à référence) |
| **Test au fil** | `apps/harbor/packages/server/test/blobs-api.test.ts` ; `apps/x/packages/spaces-client/src/client.test.ts` |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
