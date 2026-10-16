---
type: Appel
title: BeeAI Framework — Exposer un agent sur Agent Stack
description: Serve : `AgentStackServer(config, memory_manager).register(agent, **AgentStackServerMetadata).serve()`
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
# BeeAI Framework — Exposer un agent sur Agent Stack

| | |
|---|---|
| **Flux** | Serve |
| **Besoin** | Exposer un agent sur Agent Stack |
| **Service client** | agent de service |
| **Appel** | `AgentStackServer(config, memory_manager).register(agent, **AgentStackServerMetadata).serve()` |
| **Contrat** | `python/beeai_framework/adapters/agentstack/serve/server.py` ; métadonnées security, security_schemes, detail: AgentDetail, settings, extensions |
| **Fonction servie** | server.py:200 (AgentDetail interaction_mode=multi-turn, liste des outils) ; factories.py:55, :124, :172 |
| **Auth** | security_schemes déclaratifs ; LLM fourni par LLMServiceExtensionServer |
| **Événements / statut** | trajectoire via extra_extensions[trajectory] (factories.py:106) |
| **Test au fil** | tests/adapters/agentstack/test_execution.py |

Brique : [/composants/beeai-framework.md](/composants/beeai-framework.md) · Interface : [/interfaces/beeai-framework.md](/interfaces/beeai-framework.md)
