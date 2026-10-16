---
type: Appel
title: BeeAI Framework — Intercepter par middleware
description: Politique : `RunMiddlewareProtocol.bind(self, ctx: RunContext)` ; `Run.middleware(*fns)`
tags:
  - serveur
  - sandbox
flux: Politique
brique: /composants/beeai-framework.md
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:30:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# BeeAI Framework — Intercepter par middleware

| | |
|---|---|
| **Flux** | Politique |
| **Besoin** | Intercepter par middleware |
| **Service client** | runtime |
| **Appel** | `RunMiddlewareProtocol.bind(self, ctx: RunContext)` ; `Run.middleware(*fns)` |
| **Contrat** | `python/beeai_framework/context.py` :37 ; :102 |
| **Fonction servie** | RunContext : `start` (RunContextStartEvent {input, output} ; fixer output court-circuite :226), success, error, finish |
| **Auth** | — |
| **Événements / statut** | start, success, error, finish |
| **Test au fil** | tests/middleware/test_trajectory.py, test_stream_tool_call.py |

**Note de frontière :** Point d'appel de l'API de politique côté BeeAI (D7, chantier 13).

Brique : [/composants/beeai-framework.md](/composants/beeai-framework.md) · Interface : [/interfaces/beeai-framework.md](/interfaces/beeai-framework.md)
