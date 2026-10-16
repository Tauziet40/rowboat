---
type: Appel
title: DSH — Ouvrir une session et monter des serveurs MCP
description: ACP : `session/new` {cwd, mcpServers}
tags:
  - serveur
  - sandbox
  - mcp
flux: ACP
brique: /composants/dsh.md
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:30:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# DSH — Ouvrir une session et monter des serveurs MCP

| | |
|---|---|
| **Flux** | ACP |
| **Besoin** | Ouvrir une session et monter des serveurs MCP |
| **Service client** | client externe |
| **Appel** | `session/new` {cwd, mcpServers} |
| **Contrat** | `AcpSession.create` (session.ts) + mountAcpMcpServers(agentCtx, servers, cwd) (mcp.ts:26) |
| **Fonction servie** | index.ts:196 → session.ts:135 → mcp.ts:36 resolveMcpConfigs |
| **Auth** | stdio : env [{name,value}], command absolu ; http : headers [{name,value}] ; `sse` refusé (AcpMcpConfigError) |
| **Événements / statut** | réponse {sessionId, configOptions} |
| **Test au fil** | acp/tests/mcp.spec.ts, multi-session.spec.ts |

**Note de frontière :** Le montage de Cognee et du MCP OKF par session passe par ce paramètre : le client externe fournit l'URL et le Bearer.

Brique : [/composants/dsh.md](/composants/dsh.md) · Interface : [/interfaces/dsh.md](/interfaces/dsh.md)
