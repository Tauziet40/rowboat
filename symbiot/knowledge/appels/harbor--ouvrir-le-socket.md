---
type: Appel
title: Harbor — Ouvrir le socket
description: Live : GET /v1/live (upgrade WS)
tags:
  - serveur
  - poste
flux: Live
brique: /composants/harbor.md
appel: GET /v1/live (upgrade WS)
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Ouvrir le socket

| | |
|---|---|
| **Flux** | Live |
| **Besoin** | Ouvrir le socket |
| **Service client** | `apps/x/packages/spaces-client/src/live.ts` SpacesLive |
| **Appel** | GET /v1/live (upgrade WS) |
| **Contrat** | `apps/harbor/packages/protocol/src/api.ts` routes.live |
| **Fonction servie** | `apps/harbor/packages/server/src/ws.ts:76` |
| **Auth** | Bearer ou ?token, cookie |
| **Événements / statut** | `ping` |
| **Test au fil** | `apps/harbor/packages/server/test/ws.test.ts` |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
