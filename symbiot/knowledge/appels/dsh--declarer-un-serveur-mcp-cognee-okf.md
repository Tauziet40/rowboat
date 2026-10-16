---
type: Appel
title: DSH — Déclarer un serveur MCP (Cognee, OKF)
description: MCP : entrée `name: @deepseek-ai/dsh-mcp-client`, `config: {serverName, transport, …}` (modèle preset/agent-preset/skills/cordis-plugin-developmen
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
# DSH — Déclarer un serveur MCP (Cognee, OKF)

| | |
|---|---|
| **Flux** | MCP |
| **Besoin** | Déclarer un serveur MCP (Cognee, OKF) |
| **Service client** | configuration Cordis |
| **Appel** | entrée `name: @deepseek-ai/dsh-mcp-client`, `config: {serverName, transport, …}` (modèle preset/agent-preset/skills/cordis-plugin-development/templates/mcp/cordis.patch.yml) |
| **Contrat** | `packages/mcp/mcp-client/src/index.ts` Config (StdioConfig | StreamableHttpConfig), apply(ctx, config) |
| **Fonction servie** | index.ts:119 (schéma), :154 (apply) |
| **Auth** | — |
| **Événements / statut** | — |
| **Test au fil** | tests/apply.spec.ts, load-path.spec.ts |

Brique : [/composants/dsh.md](/composants/dsh.md) · Interface : [/interfaces/dsh.md](/interfaces/dsh.md)
