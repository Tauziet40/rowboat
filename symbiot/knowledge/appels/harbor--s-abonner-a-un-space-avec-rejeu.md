---
type: Appel
title: Harbor — S'abonner à un space avec rejeu
description: Live : frame client {kind: subscribe, spaceId, afterOffset}
tags:
  - serveur
  - poste
flux: Live
brique: /composants/harbor.md
appel: frame client {kind: subscribe, spaceId, afterOffset}
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — S'abonner à un space avec rejeu

| | |
|---|---|
| **Flux** | Live |
| **Besoin** | S'abonner à un space avec rejeu |
| **Service client** | `apps/x/packages/spaces-client/src/live.ts` subscribe(spaceId, h, afterOffset) ; `apps/x/packages/spaces-client/src/subscriptions.ts` SpaceSubscriptions.subscribe ; IPC spaces:subscribeSpace (`apps/x/packages/spaces-client/src/channels.ts:267`) |
| **Appel** | frame client {kind: subscribe, spaceId, afterOffset} |
| **Contrat** | `apps/harbor/packages/protocol/src/events.ts` ClientFrame, ServerFrame |
| **Fonction servie** | `apps/harbor/packages/server/src/ws.ts:192` → service.ts:278 → core/spaces.ts:524 replay |
| **Auth** | socket authentifié, membre |
| **Événements / statut** | `subscribed{fromOffset}` puis `event{offset, event}` (ws.ts:223, :227 ; core/kernel.ts:150) |
| **Test au fil** | `apps/harbor/packages/server/test/ws.test.ts`, open-spaces.test.ts ; `apps/x/packages/spaces-client/src/live.test.ts`, subscriptions.test.ts |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
