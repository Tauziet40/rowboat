---
type: Appel
title: Harbor — Un humain décide ou annule
description: I4 : POST /v1/invocations/:id/cancel ; routes.decideApproval
tags:
  - serveur
  - poste
flux: I4
brique: /composants/harbor.md
appel: POST /v1/invocations/:id/cancel ; routes.decideApproval
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Un humain décide ou annule

| | |
|---|---|
| **Flux** | I4 |
| **Besoin** | Un humain décide ou annule |
| **Service client** | `apps/x/packages/spaces-client/src/client.ts` cancelInvocation ; IPC spaces:decideApproval |
| **Appel** | POST /v1/invocations/:id/cancel ; routes.decideApproval |
| **Contrat** | `apps/harbor/packages/protocol/src/api.ts` routes.cancelInvocation, routes.decideApproval ; approval.ts ApprovalDecision |
| **Fonction servie** | `apps/harbor/packages/server/src/http.ts:357`, :319 → core/invocations.ts:264, :352 |
| **Auth** | Bearer membre |
| **Événements / statut** | `invocation_stop` / `approval_decided` (agent), `approval` |
| **Test au fil** | `apps/harbor/packages/server/test/invocations.test.ts`, approvals.test.ts |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
