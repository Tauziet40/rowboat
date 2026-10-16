---
type: Appel
title: DSH — Intercepter un appel d'outil avant exécution
description: Politique : événement waterfall `tools/pre-execute (exec: ToolExecution, next) → Promise<PreToolDecision>`
tags:
  - serveur
  - sandbox
flux: Politique
brique: /composants/dsh.md
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:30:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# DSH — Intercepter un appel d'outil avant exécution

| | |
|---|---|
| **Flux** | Politique |
| **Besoin** | Intercepter un appel d'outil avant exécution |
| **Service client** | plugin de politique (chantier 13) |
| **Appel** | événement waterfall `tools/pre-execute (exec: ToolExecution, next) → Promise<PreToolDecision>` |
| **Contrat** | `packages/core/tools/src/index.ts` PreToolDecision = allow | deny {reason, info?} | cancel | ask {reason?, displayReason?} |
| **Fonction servie** | déclaré :153, type :607, exécuté :1506 |
| **Auth** | filtrage par portée (agent.ctx) |
| **Événements / statut** | `tool/call` puis `tool/result` (isError) |
| **Test au fil** | core/tools/tests/tools.spec.ts, scoped.spec.ts |

**Note de frontière :** Point d'appel de l'API de politique (D7) : le plugin interroge « U peut-il T avec ces arguments dans S ? » et renvoie allow, deny ou ask.

Brique : [/composants/dsh.md](/composants/dsh.md) · Interface : [/interfaces/dsh.md](/interfaces/dsh.md)
