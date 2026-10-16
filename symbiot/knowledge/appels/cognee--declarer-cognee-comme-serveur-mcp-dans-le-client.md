---
type: Appel
title: Cognee — Déclarer Cognee comme serveur MCP dans le client
description: C0 : entrée `{type:"http", url, headers}` ou stdio `{command,args,env}`
tags:
  - serveur
  - poste
flux: C0
brique: /composants/cognee.md
appel: entrée `{type:"http", url, headers}` ou stdio `{command,args,env}`
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Cognee — Déclarer Cognee comme serveur MCP dans le client

| | |
|---|---|
| **Flux** | C0 |
| **Besoin** | Déclarer Cognee comme serveur MCP dans le client |
| **Service client** | `apps/x/packages/core/src/runtime/tools/domains/mcp.ts:14` addMcpServer → `apps/x/packages/core/src/mcp/repo.ts:18` FSMcpConfigRepo (config/mcp.json) |
| **Appel** | entrée `{type:"http", url, headers}` ou stdio `{command,args,env}` |
| **Contrat** | `apps/x/packages/shared/src/mcp.ts:3-16` StdioMcpServerConfig / HttpMcpServerConfig |
| **Fonction servie** | `apps/x/packages/core/src/mcp/mcp.ts:40` getClient, en-têtes relayés l.71-74 |
| **Auth** | headers relayés au transport, mais **ignorés par cognee-mcp** (server.py ne lit aucun en-tête entrant) |
| **Événements / statut** | n/a |
| **Test au fil** | aucun |

**Note de frontière :** Le multi-utilisateur ne passe pas par les en-têtes : une instance cognee-mcp par utilisateur, ou REST direct.

Brique : [/composants/cognee.md](/composants/cognee.md) · Interface : [/interfaces/cognee.md](/interfaces/cognee.md)
