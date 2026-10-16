---
type: Appel
title: Cognee — Provisionner un utilisateur et l'authentifier
description: A3 : POST /api/v1/auth/register (fastapi-users) ; POST /api/v1/auth/login (cookie + JWT) ; GET /api/v1/auth/me ; POST /api/v1/auth/api-keys
tags:
  - serveur
  - poste
flux: A3
brique: /composants/cognee.md
appel: POST /api/v1/auth/register (fastapi-users) ; POST /api/v1/auth/login (cookie + JWT) ; GET /api/v1/auth/me ; POST /api/v1/auth/api-keys
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Cognee — Provisionner un utilisateur et l'authentifier

| | |
|---|---|
| **Flux** | A3 |
| **Besoin** | Provisionner un utilisateur et l'authentifier |
| **Service client** | REST |
| **Appel** | POST /api/v1/auth/register (fastapi-users) ; POST /api/v1/auth/login (cookie + JWT) ; GET /api/v1/auth/me ; POST /api/v1/auth/api-keys |
| **Contrat** | `cognee/cognee/api/v1/users/routers/get_auth_router.py:15` login, :53 get_me ; `cognee/cognee/api/v1/api_keys/routers/get_api_key_management_router.py:60` create_api_key_for_user |
| **Fonction servie** | `cognee/cognee/modules/users/methods/create_user.py:16` ; `cognee/cognee/modules/users/api_key/create_api_key.py:26` |
| **Auth** | Bearer (api_bearer/api_bearer_transport.py), cookie (default/default_transport.py), X-Api-Key (api_key/get_api_key_transport.py:29) ; FASTAPI_USERS_JWT_SECRET, JWT_LIFETIME_SECONDS |
| **Événements / statut** | 401 si l'authentification est requise |
| **Test au fil** | `cognee/cognee/tests/unit/modules/users/test_conditional_authentication.py`, test_authenticated_websocket_user.py, test_unauthorized_response_enrichment.py |

**Note de frontière :** Pour D4 : pas d'OIDC ; le provisionnement depuis Keycloak passe par register + api-keys, ou par un pont JWT à écrire (chantier 12 étendu à Cognee).

Brique : [/composants/cognee.md](/composants/cognee.md) · Interface : [/interfaces/cognee.md](/interfaces/cognee.md)
