---
type: Appel
title: DSH — Demander une approbation humaine
description: Politique : `ctx.approval.request(req: {agent, toolName, callId?, reason?, displayReason?, signal?}): Promise<allowed-once | rejected | cancelled | unav
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
# DSH — Demander une approbation humaine

| | |
|---|---|
| **Flux** | Politique |
| **Besoin** | Demander une approbation humaine |
| **Service client** | plugin ou runtime |
| **Appel** | `ctx.approval.request(req: {agent, toolName, callId?, reason?, displayReason?, signal?}): Promise<allowed-once | rejected | cancelled | unavailable>` |
| **Contrat** | `packages/interaction/user-approval/src/index.ts` ApprovalService (service approval) ; waterfall approval/request |
| **Fonction servie** | serviceAsk tools/index.ts:1727 → user-approval index.ts:215 |
| **Auth** | sans service ou sans agent → deny |
| **Événements / statut** | SessionEvent `approval/asked`, `approval/decided`, `approval/policy` |
| **Test au fil** | interaction/user-approval/tests/approval.spec.ts |

Brique : [/composants/dsh.md](/composants/dsh.md) · Interface : [/interfaces/dsh.md](/interfaces/dsh.md)
