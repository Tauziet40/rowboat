---
type: Appel
title: BeeAI Framework — Méthodes A2A servies
description: Serve : DefaultRequestHandler : message/send, message/stream, tasks/get, tasks/cancel, push ; A2AStarletteApplication, A2ARESTFastAPIApplication, gR
tags:
  - serveur
  - sandbox
  - a2a
flux: Serve
brique: /composants/beeai-framework.md
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:30:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# BeeAI Framework — Méthodes A2A servies

| | |
|---|---|
| **Flux** | Serve |
| **Besoin** | Méthodes A2A servies |
| **Service client** | SDK a2a |
| **Appel** | DefaultRequestHandler : message/send, message/stream, tasks/get, tasks/cancel, push ; A2AStarletteApplication, A2ARESTFastAPIApplication, gRPC |
| **Contrat** | BaseA2AExecutor.execute(context, event_queue) / cancel |
| **Fonction servie** | executors/base_a2a_executor.py:51, :90 ; base_a2a_agent_executor.py:49 (updater.submit / start_work / complete / failed) ; InMemoryTaskStore par défaut |
| **Auth** | — |
| **Événements / statut** | emitter.on(update) (ReAct, react_agent_executor.py:60), start / success (tool_calling_agent_executor.py:70) → start_work(message) si send_trajectory |
| **Test au fil** | test_execution.py |

Brique : [/composants/beeai-framework.md](/composants/beeai-framework.md) · Interface : [/interfaces/beeai-framework.md](/interfaces/beeai-framework.md)
