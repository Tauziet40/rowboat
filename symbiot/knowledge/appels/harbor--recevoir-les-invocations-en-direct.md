---
type: Appel
title: Harbor — Recevoir les invocations en direct
description: I4 : frames WS `invocation`, `invocation_stop`, `approval_decided`
tags:
  - serveur
  - poste
flux: I4
brique: /composants/harbor.md
appel: frames WS `invocation`, `invocation_stop`, `approval_decided`
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Recevoir les invocations en direct

| | |
|---|---|
| **Flux** | I4 |
| **Besoin** | Recevoir les invocations en direct |
| **Service client** | env.subscribe (`apps/harbor/packages/server/src/connectors/host.ts:73` → hub.subscribeMember) |
| **Appel** | frames WS `invocation`, `invocation_stop`, `approval_decided` |
| **Contrat** | `apps/harbor/packages/protocol/src/events.ts` ServerFrame |
| **Fonction servie** | `apps/harbor/packages/server/src/core/invocations.ts:476`, :289, :374 |
| **Auth** | agent |
| **Événements / statut** | — |
| **Test au fil** | `apps/harbor/packages/server/test/invocations.test.ts`, approvals.test.ts |

**Note de frontière :** Les connecteurs hébergés appellent HarborService en processus ; un connecteur externe (Centaur, Agent Stack) passe par REST /v1/agent/* et la WS.

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
