---
type: Appel
title: Harbor — Identité et appartenance
description: Join : GET /v1/me
tags:
  - serveur
  - poste
flux: Join
brique: /composants/harbor.md
appel: GET /v1/me
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Identité et appartenance

| | |
|---|---|
| **Flux** | Join |
| **Besoin** | Identité et appartenance |
| **Service client** | `apps/x/packages/core/src/spaces/oauth.ts` signInOrg → `apps/x/packages/spaces-client/src/client.ts` me |
| **Appel** | GET /v1/me |
| **Contrat** | `apps/harbor/packages/protocol/src/api.ts` routes.me |
| **Fonction servie** | `apps/harbor/packages/server/src/http.ts:168` → core/spaces.ts:49 |
| **Auth** | Bearer |
| **Événements / statut** | — |
| **Test au fil** | `apps/harbor/packages/server/test/auth-oidc.test.ts` |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
