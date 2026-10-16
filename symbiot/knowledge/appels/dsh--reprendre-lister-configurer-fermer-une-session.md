---
type: Appel
title: DSH — Reprendre, lister, configurer, fermer une session
description: ACP : `session/resume`, `session/list`, `session/set_config_option`, `session/close`
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
# DSH — Reprendre, lister, configurer, fermer une session

| | |
|---|---|
| **Flux** | ACP |
| **Besoin** | Reprendre, lister, configurer, fermer une session |
| **Service client** | client externe |
| **Appel** | `session/resume`, `session/list`, `session/set_config_option`, `session/close` |
| **Contrat** | methods.agent.session.* |
| **Fonction servie** | index.ts:239, :292, :333, :347 |
| **Auth** | — |
| **Événements / statut** | `config_option_update` (session.ts:221) |
| **Test au fil** | bridge.spec.ts, model-control.spec.ts, dispose.spec.ts |

Brique : [/composants/dsh.md](/composants/dsh.md) · Interface : [/interfaces/dsh.md](/interfaces/dsh.md)
