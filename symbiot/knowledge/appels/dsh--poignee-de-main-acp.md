---
type: Appel
title: DSH — Poignée de main ACP
description: ACP : `initialize`
tags:
  - serveur
  - sandbox
flux: ACP
brique: /composants/dsh.md
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:30:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# DSH — Poignée de main ACP

| | |
|---|---|
| **Flux** | ACP |
| **Besoin** | Poignée de main ACP |
| **Service client** | client externe (code mode du client Symbiot, Centaur) |
| **Appel** | `initialize` |
| **Contrat** | `packages/acp/acp/src/index.ts` apply (plugin acp, inject agents, llm, sessionPersistence, sessions) |
| **Fonction servie** | index.ts:176 : mcpCapabilities {http:true}, sessionCapabilities {close, list, resume} |
| **Auth** | `authMethods: []` ; `authenticate` sans effet (index.ts:192) : **aucune authentification ACP** |
| **Événements / statut** | — |
| **Test au fil** | acp/tests/bridge.spec.ts |

Brique : [/composants/dsh.md](/composants/dsh.md) · Interface : [/interfaces/dsh.md](/interfaces/dsh.md)
