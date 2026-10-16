---
type: Appel
title: BeeAI Framework — Exposer outils, agents et prompts en MCP
description: Serve : `MCPServer(config=MCPServerConfig(transport=stdio|sse|streamable-http, name, instructions, settings: MCPSettings)).register(input, *, execut
tags:
  - serveur
  - sandbox
  - mcp
flux: Serve
brique: /composants/beeai-framework.md
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:30:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# BeeAI Framework — Exposer outils, agents et prompts en MCP

| | |
|---|---|
| **Flux** | Serve |
| **Besoin** | Exposer outils, agents et prompts en MCP |
| **Service client** | agent de service |
| **Appel** | `MCPServer(config=MCPServerConfig(transport=stdio|sse|streamable-http, name, instructions, settings: MCPSettings)).register(input, *, execution=None).serve()` |
| **Contrat** | `python/beeai_framework/adapters/mcp/serve/server.py` MCPServer (FastMCP) |
| **Fonction servie** | serve :142, aserve :146 ; _tool_factory :191 ; _runnable_factory :243 (outil run(input:str)) ; _prompt_template_factory :264 |
| **Auth** | MCPSettings.transport_security seulement |
| **Événements / statut** | — |
| **Test au fil** | tests/adapters/mcp/serve/test_tool_factory.py |

Brique : [/composants/beeai-framework.md](/composants/beeai-framework.md) · Interface : [/interfaces/beeai-framework.md](/interfaces/beeai-framework.md)
