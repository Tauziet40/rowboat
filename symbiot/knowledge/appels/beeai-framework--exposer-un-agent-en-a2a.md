---
type: Appel
title: BeeAI Framework — Exposer un agent en A2A
description: Serve : `A2AServer(config=A2AServerConfig(host, port=9999, protocol=jsonrpc|grpc|http_json, agent_card_port, server_credentials), memory_manager).re
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
# BeeAI Framework — Exposer un agent en A2A

| | |
|---|---|
| **Flux** | Serve |
| **Besoin** | Exposer un agent en A2A |
| **Service client** | agent de service |
| **Appel** | `A2AServer(config=A2AServerConfig(host, port=9999, protocol=jsonrpc|grpc|http_json, agent_card_port, server_credentials), memory_manager).register(agent, **A2AServerMetadata).serve()` |
| **Contrat** | `python/beeai_framework/adapters/a2a/serve/server.py` A2AServer |
| **Fonction servie** | serve :114 ; register :174 (un seul agent ; register_many lève NotImplementedError) |
| **Auth** | **aucune côté HTTP** ; gRPC : server_credentials |
| **Événements / statut** | — |
| **Test au fil** | tests/adapters/a2a/test_execution.py |

**Note de frontière :** Derrière le reverse proxy Keycloak (incrément 4) ; serve/utils.py:21 is_api_key_valid existe mais aucun serveur ne l'utilise.

Brique : [/composants/beeai-framework.md](/composants/beeai-framework.md) · Interface : [/interfaces/beeai-framework.md](/interfaces/beeai-framework.md)
