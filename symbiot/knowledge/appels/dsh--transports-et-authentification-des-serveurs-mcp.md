---
type: Appel
title: DSH — Transports et authentification des serveurs MCP
description: MCP : `transport: stdio` (command, args, env, cwd) | `streamable-http` (url, headers) ; pas de SSE
tags:
  - serveur
  - sandbox
flux: MCP
brique: /composants/dsh.md
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:30:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# DSH — Transports et authentification des serveurs MCP

| | |
|---|---|
| **Flux** | MCP |
| **Besoin** | Transports et authentification des serveurs MCP |
| **Service client** | configuration |
| **Appel** | `transport: stdio` (command, args, env, cwd) | `streamable-http` (url, headers) ; pas de SSE |
| **Contrat** | createTransport(config) transport.ts:31 |
| **Fonction servie** | stdio : buildChildEnv(env) sur un env nettoyé ; http : requestInit.headers |
| **Auth** | stdio : `env: {TOKEN: !!js process.env.X}` ; http : `headers: {Authorization: !!js Bearer …}` (README:34-53) ; **pas d'OAuth** |
| **Événements / statut** | — |
| **Test au fil** | egress.spec.ts, protocol.spec.ts |

Brique : [/composants/dsh.md](/composants/dsh.md) · Interface : [/interfaces/dsh.md](/interfaces/dsh.md)
