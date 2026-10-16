---
type: Appel
title: DSH — Demande de permission vers le client
description: ACP : `session/request_permission` (agent → client)
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
# DSH — Demande de permission vers le client

| | |
|---|---|
| **Flux** | ACP |
| **Besoin** | Demande de permission vers le client |
| **Service client** | DSH → client externe |
| **Appel** | `session/request_permission` (agent → client) |
| **Contrat** | écouteur waterfall `ctx.on('approval/request')` |
| **Fonction servie** | index.ts:155-173 : options allow-once / reject-once → allowed-once, rejected, cancelled |
| **Auth** | décision ponctuelle, jamais durable |
| **Événements / statut** | `tool_call` drainé avant la demande |
| **Test au fil** | approval.spec.ts |

**Note de frontière :** Pour I3 et I4 : voie par laquelle une approbation Harbor ou Centaur remonte au siège humain.

Brique : [/composants/dsh.md](/composants/dsh.md) · Interface : [/interfaces/dsh.md](/interfaces/dsh.md)
