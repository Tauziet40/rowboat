---
type: Appel
title: BeeAI Framework — Approbation et formulaire sous Agent Stack
description: Serve : `AgentStackContext.__enter__ → setup_io_context(read=_read, confirm=_confirm)` ; `_confirm(question, **kw) -> bool`
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
# BeeAI Framework — Approbation et formulaire sous Agent Stack

| | |
|---|---|
| **Flux** | Serve |
| **Besoin** | Approbation et formulaire sous Agent Stack |
| **Service client** | runtime |
| **Appel** | `AgentStackContext.__enter__ → setup_io_context(read=_read, confirm=_confirm)` ; `_confirm(question, **kw) -> bool` |
| **Contrat** | `python/beeai_framework/adapters/agentstack/context.py` AgentStackContext ; BaseAgentStackExtensions.form_request (serve/types.py:16) |
| **Fonction servie** | context.py:55 ; _confirm → form_request.request_form(FormRender(CheckboxField id=answer)) ; _read → TextField ; formulaire non supporté → False / "" |
| **Auth** | — |
| **Événements / statut** | — |
| **Test au fil** | test_execution.py partiel |

Brique : [/composants/beeai-framework.md](/composants/beeai-framework.md) · Interface : [/interfaces/beeai-framework.md](/interfaces/beeai-framework.md)
