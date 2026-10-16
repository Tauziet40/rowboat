---
type: Appel
title: Cognee — Exécuter un outil Cognee
description: C2 : MCP `tools/call {name, arguments}`
tags:
  - serveur
  - poste
  - mcp
flux: C2
brique: /composants/cognee.md
appel: MCP `tools/call {name, arguments}`
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Cognee — Exécuter un outil Cognee

| | |
|---|---|
| **Flux** | C2 |
| **Besoin** | Exécuter un outil Cognee |
| **Service client** | agent → domains/mcp.ts:94 executeMcpTool (permission mcp-execute) → mcp.ts:169 executeTool |
| **Appel** | MCP `tools/call {name, arguments}` |
| **Contrat** | — |
| **Fonction servie** | — |
| **Auth** | — |
| **Événements / statut** | résultat textuel synchrone |
| **Test au fil** | aucun |

Brique : [/composants/cognee.md](/composants/cognee.md) · Interface : [/interfaces/cognee.md](/interfaces/cognee.md)
