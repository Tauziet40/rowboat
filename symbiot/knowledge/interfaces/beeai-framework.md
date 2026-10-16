---
type: Interface
title: BeeAI Framework — serve A2A, MCP et Agent Stack, client MCP et A2A, interception
description: Surfaces par lesquelles un agent BeeAI est exposé et consomme des ressources.
tags:
  - serveur
  - a2a
  - mcp
  - gouvernance
protocole: A2A jsonrpc, http_json, grpc ; MCP ; Agent Stack
auth: aucune sur le serve A2A et MCP ; security_schemes déclaratifs sur Agent Stack
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:30:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# BeeAI Framework — serve A2A, MCP et Agent Stack, client MCP et A2A, interception

Appels dans [/appels/](/appels/index.md), préfixe `beeai-framework--`. Évaluation : [/evaluations/beeai-framework.md](/evaluations/beeai-framework.md). Deux lacunes structurantes : `io_confirm` non mappé sous A2A (stdin), et la récupération de l'Agent Card distante non authentifiée.
