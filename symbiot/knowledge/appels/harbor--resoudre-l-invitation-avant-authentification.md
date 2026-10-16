---
type: Appel
title: Harbor — Résoudre l'invitation avant authentification
description: Join : POST /v1/invites/resolve
tags:
  - serveur
  - poste
flux: Join
brique: /composants/harbor.md
appel: POST /v1/invites/resolve
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Résoudre l'invitation avant authentification

| | |
|---|---|
| **Flux** | Join |
| **Besoin** | Résoudre l'invitation avant authentification |
| **Service client** | `apps/x/packages/core/src/spaces/oauth.ts` resolveInviteLink → `apps/x/packages/spaces-client/src/client.ts` resolveInvite ; `apps/x/packages/spaces-client/src/links.ts` parseInviteLink |
| **Appel** | POST /v1/invites/resolve |
| **Contrat** | `apps/harbor/packages/protocol/src/api.ts` routes.resolveInvite ; invite.ts ResolveInvite / ResolveInviteResult |
| **Fonction servie** | `apps/harbor/packages/server/src/http.ts:444` → core/spaces.ts:394 |
| **Auth** | aucune |
| **Événements / statut** | — |
| **Test au fil** | `apps/harbor/packages/server/test/api.test.ts` |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
