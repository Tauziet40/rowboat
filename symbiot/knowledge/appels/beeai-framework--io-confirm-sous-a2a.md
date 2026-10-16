---
type: Appel
title: BeeAI Framework — io_confirm sous A2A
description: Serve : `utils.io.io_confirm(prompt, **IOConfirmKwargs)`
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
# BeeAI Framework — io_confirm sous A2A

| | |
|---|---|
| **Flux** | Serve |
| **Besoin** | io_confirm sous A2A |
| **Service client** | runtime |
| **Appel** | `utils.io.io_confirm(prompt, **IOConfirmKwargs)` |
| **Contrat** | **non mappé** : A2AContext (serve/context.py) n'appelle pas setup_io_context, TaskState.input_required jamais émis |
| **Fonction servie** | repli _default_confirm → input() stdin (io.py:38), bloque ou échoue en headless |
| **Auth** | — |
| **Événements / statut** | — |
| **Test au fil** | tests/utils/test_io.py (aucun test A2A) |

**Note de frontière :** Chantiers 15 et 17 : écrire un A2AContext qui mappe io_confirm vers input_required, sur le modèle d'AgentStackContext.

Brique : [/composants/beeai-framework.md](/composants/beeai-framework.md) · Interface : [/interfaces/beeai-framework.md](/interfaces/beeai-framework.md)
