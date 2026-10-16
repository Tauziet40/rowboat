---
type: Appel
title: Cognee — Portée par utilisateur
description: I5 : une instance cognee-mcp par utilisateur Rowboat, ou REST direct avec le jeton de l'utilisateur
tags:
  - serveur
  - poste
flux: I5
brique: /composants/cognee.md
appel: une instance cognee-mcp par utilisateur Rowboat, ou REST direct avec le jeton de l'utilisateur
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Cognee — Portée par utilisateur

| | |
|---|---|
| **Flux** | I5 |
| **Besoin** | Portée par utilisateur |
| **Service client** | **un seul** jeton par processus cognee-mcp (COGNEE_API_KEY) |
| **Appel** | une instance cognee-mcp par utilisateur Rowboat, ou REST direct avec le jeton de l'utilisateur |
| **Contrat** | `cognee-mcp/src/server.py:1119-1135` (--api-url, --api-token, --api-auth-scheme) |
| **Fonction servie** | `cognee/cognee/modules/users/methods/get_authenticated_user.py:84` |
| **Auth** | voir « provisionner et authentifier » |
| **Événements / statut** | — |
| **Test au fil** | `cognee-mcp/tests/test_mcp_server_hardening.py:55` test_cognee_client_auth_schemes |

**Note de frontière :** Point structurant pour D4 : le MCP Cognee ne porte pas l'identité de l'appelant. Le reverse proxy Keycloak devant le MCP (incrément 3) doit soit instancier un cognee-mcp par sub, soit traduire le JWT en jeton Cognee par utilisateur.

Brique : [/composants/cognee.md](/composants/cognee.md) · Interface : [/interfaces/cognee.md](/interfaces/cognee.md)
