---
type: Appel
title: DSH — Annuler
description: ACP : `session/cancel` (notification)
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
# DSH — Annuler

| | |
|---|---|
| **Flux** | ACP |
| **Besoin** | Annuler |
| **Service client** | client externe |
| **Appel** | `session/cancel` (notification) |
| **Contrat** | `AcpSession.cancel()` |
| **Fonction servie** | index.ts:367 → session.ts:334 (agent.cancel {kind: user}) |
| **Auth** | — |
| **Événements / statut** | `turn/end` raison cancelled |
| **Test au fil** | turns.spec.ts, edges.spec.ts |

Brique : [/composants/dsh.md](/composants/dsh.md) · Interface : [/interfaces/dsh.md](/interfaces/dsh.md)
