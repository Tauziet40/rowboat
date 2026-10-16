---
type: Appel
title: BeeAI Framework — Produire l'Agent Card
description: Serve : `_create_agent_card(metadata, runnable) -> AgentCard`
tags:
  - serveur
  - sandbox
flux: Serve
brique: /composants/beeai-framework.md
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:30:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# BeeAI Framework — Produire l'Agent Card

| | |
|---|---|
| **Flux** | Serve |
| **Besoin** | Produire l'Agent Card |
| **Service client** | runtime |
| **Appel** | `_create_agent_card(metadata, runnable) -> AgentCard` |
| **Contrat** | A2AServerMetadata (name, description, url, version, default_input/output_modes, capabilities, skills, task_store, queue_manager, push_notifier, request_context_builder, send_trajectory, execution) |
| **Fonction servie** | server.py:321 ; défauts meta.name / meta.description, capabilities streaming=True, une AgentSkill(id=name), url réécrite serve :133, :140, :145 |
| **Auth** | — |
| **Événements / statut** | — |
| **Test au fil** | test_execution.py |

**Note de frontière :** Les Agent Cards consignées en concepts OKF (chantier 16) partent de cette structure.

Brique : [/composants/beeai-framework.md](/composants/beeai-framework.md) · Interface : [/interfaces/beeai-framework.md](/interfaces/beeai-framework.md)
