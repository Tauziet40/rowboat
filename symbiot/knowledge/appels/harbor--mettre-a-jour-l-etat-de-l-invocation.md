---
type: Appel
title: Harbor — Mettre à jour l'état de l'invocation
description: I4 : POST /v1/agent/invocations/:id/update
tags:
  - serveur
  - poste
flux: I4
brique: /composants/harbor.md
appel: POST /v1/agent/invocations/:id/update
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Mettre à jour l'état de l'invocation

| | |
|---|---|
| **Flux** | I4 |
| **Besoin** | Mettre à jour l'état de l'invocation |
| **Service client** | env.service.updateInvocation (conductor/connector.ts:456) |
| **Appel** | POST /v1/agent/invocations/:id/update |
| **Contrat** | `apps/harbor/packages/protocol/src/api.ts` routes.updateInvocation ; invocation.ts InvocationUpdate |
| **Fonction servie** | `apps/harbor/packages/server/src/http.ts:330` → service.ts:150 → core/invocations.ts:163 |
| **Auth** | agent |
| **Événements / statut** | `invocation_state` ; promotion → `invocation` |
| **Test au fil** | `apps/harbor/packages/server/test/conductor-connector.test.ts`, agent37-connector.test.ts, replicas-connector.test.ts |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
