---
type: Appel
title: Cognee — Découvrir les outils Cognee
description: C1 : MCP `tools/list`
tags:
  - serveur
  - poste
  - mcp
flux: C1
brique: /composants/cognee.md
appel: MCP `tools/list`
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Cognee — Découvrir les outils Cognee

| | |
|---|---|
| **Flux** | C1 |
| **Besoin** | Découvrir les outils Cognee |
| **Service client** | agent → domains/mcp.ts:71 listMcpTools → mcp.ts:158 listTools |
| **Appel** | MCP `tools/list` |
| **Contrat** | `cognee-mcp/src/server.py:209` apply_tool_mode (registre filtré par tag) |
| **Fonction servie** | `cognee-mcp/src/tool_registry.py` |
| **Auth** | idem C0 |
| **Événements / statut** | n/a |
| **Test au fil** | `cognee-mcp/tests/test_mcp_server_hardening.py:116`, test_tool_search.py |

Brique : [/composants/cognee.md](/composants/cognee.md) · Interface : [/interfaces/cognee.md](/interfaces/cognee.md)
