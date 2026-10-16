---
type: Appel
title: BeeAI Framework — Consommer un serveur MCP (Cognee, OKF)
description: Consommer : `await MCPTool.from_client(client: MCPClient | ClientSession, smart_parsing: bool, exclude_none: bool) -> list[MCPTool]`
tags:
  - serveur
  - sandbox
  - mcp
flux: Consommer
brique: /composants/beeai-framework.md
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:30:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# BeeAI Framework — Consommer un serveur MCP (Cognee, OKF)

| | |
|---|---|
| **Flux** | Consommer |
| **Besoin** | Consommer un serveur MCP (Cognee, OKF) |
| **Service client** | agent |
| **Appel** | `await MCPTool.from_client(client: MCPClient | ClientSession, smart_parsing: bool, exclude_none: bool) -> list[MCPTool]` |
| **Contrat** | `python/beeai_framework/tools/mcp/mcp.py` MCPTool ; MCPClient = AbstractAsyncContextManager[(recv, send[, GetSessionIdCallback])] |
| **Fonction servie** | mcp.py:110 ; from_session :128 (pagination list_tools) ; MCPSessionProvider(client).session() session_provider.py:34, :60 (compteur de refs) |
| **Auth** | portée par le client fourni : stdio_client, streamablehttp_client(headers=…) |
| **Événements / statut** | namespace [tool, mcp, <name>] : start, success, error, finish |
| **Test au fil** | tests/tools/test_mcp_tool.py |

Brique : [/composants/beeai-framework.md](/composants/beeai-framework.md) · Interface : [/interfaces/beeai-framework.md](/interfaces/beeai-framework.md)
