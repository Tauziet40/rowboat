---
type: Interface
title: Cognee — surfaces MCP et REST consommées par le client
description: MCP cognee-mcp (remember, recall, forget, cognify_status) et REST /api/v1 ; variables d'environnement qui changent le comportement.
tags:
  - serveur
  - mcp
  - mémoire
  - rag
  - identité
protocole: MCP stdio/sse/streamable-http ; HTTP REST
auth: aucune en entrée MCP ; Bearer, cookie ou X-Api-Key vers le backend
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Cognee — surfaces MCP et REST consommées par le client

Les appels sont dans [/appels/](/appels/index.md), préfixe `cognee--`. Détail des outils et routes : [/interfaces/interfaces-serveur.md](/interfaces/interfaces-serveur.md) §3.

**Variables d'environnement structurantes**

| nom | fichier:ligne | effet |
|---|---|---|
| ENABLE_BACKEND_ACCESS_CONTROL | cognee/context_global_variables.py:98-99 ; modules/users/methods/get_authenticated_user.py:39 | multi-tenant : une base graphe/vecteur par dataset, ACL appliquées ; activée automatiquement si les bases le permettent ; à true, force REQUIRE_AUTHENTICATION |
| REQUIRE_AUTHENTICATION | get_authenticated_user.py:40, :81 | true : 401 sans auth ; false : repli silencieux sur get_default_user ; absente : hérite de la précédente |
| COGNEE_BASE_URL + COGNEE_API_KEY | cognee-mcp/src/server.py:1119, :1127 | mode API de cognee-mcp, **une seule identité par processus** |
| COGNEE_API_AUTH_SCHEME | cognee-mcp/src/cognee_client.py:96 ; server.py:1135 | bearer (défaut) ou x-api-key (+ X-Tenant-Id) |
| COGNEE_MCP_AGENT_SCOPED | cognee-mcp/src/server.py:1010 | true : dataset par défaut `<client>_memory` ; false : `main_dataset` |

**Constats de frontière**
- Rowboat ne référence pas Cognee ; la seule voie générique est `listMcpTools` / `executeMcpTool` par l'agent, sans service déterministe pour l'envoi en masse ou le polling (chantier 02).
- Le MCP ne téléverse ni répertoire ni ontologie et n'expose aucune lecture du graphe : I2-b, I2-c et I2-e exigent un client REST côté client (chantier 03).
- Les en-têtes de `mcp.json` ne portent pas l'identité jusqu'à Cognee (`mcp.ts:71-74` contre `server.py` sans lecture d'en-tête) : une instance par utilisateur ou REST direct (D4, incrément 3).
- `raw_data` avec chemins locaux exige ACCEPT_LOCAL_FILE_PATH côté serveur (`infrastructure/files/utils/local_path_safety.py:15`).
