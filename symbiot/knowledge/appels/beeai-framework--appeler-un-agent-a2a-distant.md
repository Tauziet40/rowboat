---
type: Appel
title: BeeAI Framework — Appeler un agent A2A distant
description: Consommer : `A2AAgent(url=None, agent_card_path=AGENT_CARD_WELL_KNOWN_PATH, agent_card=None, memory, grpc_client_credentials=None, parameters: A2AAgentP
tags:
  - serveur
  - sandbox
  - a2a
flux: Consommer
brique: /composants/beeai-framework.md
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:30:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# BeeAI Framework — Appeler un agent A2A distant

| | |
|---|---|
| **Flux** | Consommer |
| **Besoin** | Appeler un agent A2A distant |
| **Service client** | agent ou connecteur |
| **Appel** | `A2AAgent(url=None, agent_card_path=AGENT_CARD_WELL_KNOWN_PATH, agent_card=None, memory, grpc_client_credentials=None, parameters: A2AAgentParameters)` ; `run(input, context_id, task_id, clear_context, a2a_context, httpx_client, streaming)` |
| **Contrat** | `python/beeai_framework/adapters/a2a/agents/agent.py` A2AAgent ; HttpxAsyncClientParameters (auth, headers, cookies, cert, proxy, timeout) |
| **Fonction servie** | __init__ :96 ; run :131 → ClientFactory(ClientConfig(...)).create(card) :157 ; carte étendue authentifiée :175 |
| **Auth** | parameters.httpx_async_client.auth/headers, httpx_client fourni, ou a2a_context ; gRPC ChannelCredentials. **La récupération de la carte (_load_agent_card :313) utilise un httpx.AsyncClient nu, non authentifié** |
| **Événements / statut** | namespace [a2a, agent, <name>] : update, error |
| **Test au fil** | aucun |

**Note de frontière :** Pour le connecteur Harbor → Agent Stack (chantier 17) : la carte derrière Keycloak exige un correctif ou une carte fournie en paramètre.

Brique : [/composants/beeai-framework.md](/composants/beeai-framework.md) · Interface : [/interfaces/beeai-framework.md](/interfaces/beeai-framework.md)
