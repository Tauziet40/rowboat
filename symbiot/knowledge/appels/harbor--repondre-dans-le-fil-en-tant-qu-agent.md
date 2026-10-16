---
type: Appel
title: Harbor — Répondre dans le fil en tant qu'agent
description: I4 : POST /v1/spaces/:id/messages
tags:
  - serveur
  - poste
flux: I4
brique: /composants/harbor.md
appel: POST /v1/spaces/:id/messages
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Répondre dans le fil en tant qu'agent

| | |
|---|---|
| **Flux** | I4 |
| **Besoin** | Répondre dans le fil en tant qu'agent |
| **Service client** | env.service.postMessage / answerInvocation (conductor/connector.ts:403, :408) |
| **Appel** | POST /v1/spaces/:id/messages |
| **Contrat** | `apps/harbor/packages/protocol/src/api.ts` routes.postMessage |
| **Fonction servie** | `apps/harbor/packages/server/src/service.ts:392` / :401 |
| **Auth** | agent |
| **Événements / statut** | `message`, `invocation_state` |
| **Test au fil** | `apps/harbor/packages/server/test/conductor-turns.test.ts` |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
