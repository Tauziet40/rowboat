---
type: Appel
title: DSH — Nommage et robustesse des outils MCP
description: MCP : `mcp__<serverName>__<rawName>` (64 caractères, suffixe sha256 si renommé) ; toolCallTimeoutMs 60 000, failOnStartupError, reconnect {enabled
tags:
  - serveur
  - sandbox
  - mcp
flux: MCP
brique: /composants/dsh.md
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:30:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# DSH — Nommage et robustesse des outils MCP

| | |
|---|---|
| **Flux** | MCP |
| **Besoin** | Nommage et robustesse des outils MCP |
| **Service client** | runtime |
| **Appel** | `mcp__<serverName>__<rawName>` (64 caractères, suffixe sha256 si renommé) ; toolCallTimeoutMs 60 000, failOnStartupError, reconnect {enabled, initialDelayMs, maxDelayMs, maxAttempts}, maxInstructionBytes |
| **Contrat** | publicToolName(serverName, rawName) tools.ts:81 ; syncTools :113 ; ReconnectConfig connection.ts |
| **Fonction servie** | serverName [A-Za-z0-9_-]{1,32} unique par portée |
| **Auth** | — |
| **Événements / statut** | — |
| **Test au fil** | tool-definition.spec.ts, mcp-client.spec.ts, reconnect.spec.ts, negotiation-lifecycle.spec.ts |

Brique : [/composants/dsh.md](/composants/dsh.md) · Interface : [/interfaces/dsh.md](/interfaces/dsh.md)
