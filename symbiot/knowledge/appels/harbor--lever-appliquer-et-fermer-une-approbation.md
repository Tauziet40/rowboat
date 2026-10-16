---
type: Appel
title: Harbor — Lever, appliquer et fermer une approbation
description: I4 : POST /v1/agent/invocations/:id/approvals ; …/approvals/:id/applied ; …/close
tags:
  - serveur
  - poste
flux: I4
brique: /composants/harbor.md
appel: POST /v1/agent/invocations/:id/approvals ; …/approvals/:id/applied ; …/close
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Lever, appliquer et fermer une approbation

| | |
|---|---|
| **Flux** | I4 |
| **Besoin** | Lever, appliquer et fermer une approbation |
| **Service client** | connecteur (REST) |
| **Appel** | POST /v1/agent/invocations/:id/approvals ; …/approvals/:id/applied ; …/close |
| **Contrat** | `apps/harbor/packages/protocol/src/api.ts` routes.requestApproval, applyApproval, closeApproval ; approval.ts ApprovalRequest, ApprovalClose |
| **Fonction servie** | `apps/harbor/packages/server/src/http.ts:302`, :308, :313 → service.ts:426, core/invocations.ts:397, :382 |
| **Auth** | agent |
| **Événements / statut** | `approval` + `message` (carte) |
| **Test au fil** | `apps/harbor/packages/server/test/approvals.test.ts` |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
