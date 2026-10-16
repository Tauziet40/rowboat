---
type: Appel
title: Harbor — Lister les invocations en attente et les décisions
description: I4 : GET /v1/agent/invocations
tags:
  - serveur
  - poste
flux: I4
brique: /composants/harbor.md
appel: GET /v1/agent/invocations
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Lister les invocations en attente et les décisions

| | |
|---|---|
| **Flux** | I4 |
| **Besoin** | Lister les invocations en attente et les décisions |
| **Service client** | connecteur : env.service.listAgentInvocations (`apps/harbor/packages/server/src/connectors/conductor/connector.ts:129`) |
| **Appel** | GET /v1/agent/invocations |
| **Contrat** | `apps/harbor/packages/protocol/src/api.ts` routes.listAgentInvocations ; invocation.ts Invocation ; approval.ts Approval |
| **Fonction servie** | `apps/harbor/packages/server/src/http.ts:295` → service.ts:144 → core/invocations.ts:140 |
| **Auth** | clé agent rbk_ |
| **Événements / statut** | aucun |
| **Test au fil** | `apps/harbor/packages/server/test/agent-connections.test.ts` |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
