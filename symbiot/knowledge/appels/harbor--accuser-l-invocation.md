---
type: Appel
title: Harbor — Accuser l'invocation
description: I4 : POST /v1/agent/invocations/:id/ack
tags:
  - serveur
  - poste
flux: I4
brique: /composants/harbor.md
appel: POST /v1/agent/invocations/:id/ack
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Accuser l'invocation

| | |
|---|---|
| **Flux** | I4 |
| **Besoin** | Accuser l'invocation |
| **Service client** | env.service.acknowledgeInvocation (conductor/connector.ts:154) |
| **Appel** | POST /v1/agent/invocations/:id/ack |
| **Contrat** | `apps/harbor/packages/protocol/src/api.ts` routes.acknowledgeInvocation |
| **Fonction servie** | `apps/harbor/packages/server/src/http.ts:325` → service.ts:147 → core/invocations.ts:146 |
| **Auth** | agent |
| **Événements / statut** | `invocation_state` (espace) |
| **Test au fil** | `apps/harbor/packages/server/test/agent-connections.test.ts` |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
