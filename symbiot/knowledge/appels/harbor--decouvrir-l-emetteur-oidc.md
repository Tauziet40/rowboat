---
type: Appel
title: Harbor — Découvrir l'émetteur OIDC
description: Join : GET /.well-known/oauth-protected-resource
tags:
  - serveur
  - poste
flux: Join
brique: /composants/harbor.md
appel: GET /.well-known/oauth-protected-resource
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Découvrir l'émetteur OIDC

| | |
|---|---|
| **Flux** | Join |
| **Besoin** | Découvrir l'émetteur OIDC |
| **Service client** | `apps/x/packages/core/src/spaces/oauth.ts` discoverOrgIssuer (`apps/x/packages/spaces-client/src/oauth.ts` discoverIssuer) |
| **Appel** | GET /.well-known/oauth-protected-resource |
| **Contrat** | — (hors protocol) |
| **Fonction servie** | `apps/harbor/packages/server/src/http.ts:104` (apex.ts:103) ; en-tête 401 auth.ts:145 |
| **Auth** | aucune |
| **Événements / statut** | — |
| **Test au fil** | `apps/harbor/packages/server/test/auth-oidc.test.ts`, multi-org.test.ts |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
