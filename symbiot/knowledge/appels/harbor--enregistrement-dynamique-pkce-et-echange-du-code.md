---
type: Appel
title: Harbor — Enregistrement dynamique, PKCE et échange du code
description: Join : AS externe (registration, authorize, token) ; consentement /oauth/consent
tags:
  - serveur
  - poste
flux: Join
brique: /composants/harbor.md
appel: AS externe (registration, authorize, token) ; consentement /oauth/consent
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Enregistrement dynamique, PKCE et échange du code

| | |
|---|---|
| **Flux** | Join |
| **Besoin** | Enregistrement dynamique, PKCE et échange du code |
| **Service client** | `apps/x/packages/core/src/spaces/oauth.ts` danceForTokens → `apps/x/packages/core/src/auth/oauth-client.ts` registerClient, generatePKCE, exchangeCodeForTokens |
| **Appel** | AS externe (registration, authorize, token) ; consentement /oauth/consent |
| **Contrat** | — |
| **Fonction servie** | `apps/harbor/packages/server/src/http.ts:114` / apex.ts:96 (consent.ts) |
| **Auth** | — |
| **Événements / statut** | — |
| **Test au fil** | `apps/harbor/packages/server/test/consent.test.ts` ; `apps/x/packages/core/src/spaces/orgs-oauth.test.ts` |

**Note de frontière :** Pour Keycloak (chantier 01) : autoriser la DCR anonyme ou ajouter un client_id statique dans oauth.ts.

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
