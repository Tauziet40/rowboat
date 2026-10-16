---
type: Appel
title: Harbor — Accepter l'invitation
description: Join : POST /v1/invites/accept
tags:
  - serveur
  - poste
flux: Join
brique: /composants/harbor.md
appel: POST /v1/invites/accept
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Accepter l'invitation

| | |
|---|---|
| **Flux** | Join |
| **Besoin** | Accepter l'invitation |
| **Service client** | `apps/x/packages/core/src/spaces/oauth.ts` joinViaInviteLink → `apps/x/packages/spaces-client/src/client.ts` acceptInvite |
| **Appel** | POST /v1/invites/accept |
| **Contrat** | `apps/harbor/packages/protocol/src/invite.ts` AcceptInvite / AcceptInviteResult |
| **Fonction servie** | `apps/harbor/packages/server/src/http.ts:449` (exemption non-membre http.ts:137) → core/spaces.ts:436 |
| **Auth** | Bearer, identité non mappée admise |
| **Événements / statut** | `membership` + `space_added` |
| **Test au fil** | `apps/harbor/packages/server/test/api.test.ts`, auth-oidc.test.ts ; `apps/x/packages/spaces-client/src/client.test.ts` |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
