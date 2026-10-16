---
type: Appel
title: DSH — Garde monotone et post-exécution
description: Politique : `ctx.tools.guard(guard: (exec) => string | undefined): () => void` ; `tools/execute`, `tools/post-execute → accept | block`
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
# DSH — Garde monotone et post-exécution

| | |
|---|---|
| **Flux** | Politique |
| **Besoin** | Garde monotone et post-exécution |
| **Service client** | plugin |
| **Appel** | `ctx.tools.guard(guard: (exec) => string | undefined): () => void` ; `tools/execute`, `tools/post-execute → accept | block` |
| **Contrat** | ToolRuntime.guard :731, :1136 ; index.ts:176, :617 |
| **Fonction servie** | évalué après le waterfall, seulement si allow ; aucun allow forcé |
| **Auth** | — |
| **Événements / statut** | résultat Error: <reason> |
| **Test au fil** | scoped.spec.ts, tools.spec.ts |

Brique : [/composants/dsh.md](/composants/dsh.md) · Interface : [/interfaces/dsh.md](/interfaces/dsh.md)
