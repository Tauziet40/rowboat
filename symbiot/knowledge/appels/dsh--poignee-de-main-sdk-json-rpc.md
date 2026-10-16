---
type: Appel
title: DSH — Poignée de main SDK JSON-RPC
description: SDK : `initialize` {cwd, provider, model, reasoningEffort?, maxTokens?}
tags:
  - serveur
  - sandbox
flux: SDK
brique: /composants/dsh.md
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:30:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# DSH — Poignée de main SDK JSON-RPC

| | |
|---|---|
| **Flux** | SDK |
| **Besoin** | Poignée de main SDK JSON-RPC |
| **Service client** | client SDK TS ou Python |
| **Appel** | `initialize` {cwd, provider, model, reasoningEffort?, maxTokens?} |
| **Contrat** | `packages/sdk/protocol/src/types.ts` HarnessSdkRequestMap, InitializeParams |
| **Fonction servie** | serveur sdk/server/src/server.ts:137 (dispatch :248) ; client HarnessClient.initialize client.ts:276 |
| **Auth** | aucune (stdio) |
| **Événements / statut** | serverInfo deepseek-harness-sdk-runtime |
| **Test au fil** | sdk/server/tests/server.spec.ts, sdk/client/tests/sdk-client.spec.ts |

Brique : [/composants/dsh.md](/composants/dsh.md) · Interface : [/interfaces/dsh.md](/interfaces/dsh.md)
