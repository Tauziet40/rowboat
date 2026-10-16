---
type: Interface
title: Harbor — appels du client et frames initiées par le serveur
description: Trois canaux : REST par SpacesClient, MCP par le serveur spaces-<org> projeté en outils natifs, WebSocket /v1/live ; frames poussées par le serveur et leurs consommateurs.
tags:
  - serveur
  - poste
  - mcp
  - a2a
protocole: REST JSON zod ; MCP StreamableHTTP ; WebSocket
auth: Bearer OIDC, cookie web, clé agent rbk_
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — appels du client et frames initiées par le serveur

Les appels sont dans [/appels/](/appels/index.md), préfixe `harbor--`. Contrat complet : [/interfaces/interfaces-serveur.md](/interfaces/interfaces-serveur.md) §1.

Trois canaux : REST via `SpacesClient` (`apps/x/packages/spaces-client/src/client.ts`), MCP via le serveur `spaces-<org>` projeté en outils natifs (`apps/x/packages/core/src/runtime/tools/domains/spaces.ts` callOrgTool → `apps/harbor/packages/server/src/runtime.ts:100` /mcp → `apps/harbor/packages/server/src/mcp.ts:155` dispatch), WebSocket `/v1/live`. Les connecteurs hébergés (`apps/harbor/packages/server/src/connectors/*`) appellent `HarborService` en processus ; un connecteur externe passe par REST `/v1/agent/*` et la WS. Le `@rowboat` se déclenche côté client (IPC `spaces:invokeRowboat`), sans invocation Harbor.

**Frames initiées par le serveur**

| frame | émise par | consommée côté client par |
|---|---|---|
| `invocation` | `apps/harbor/packages/server/src/core/invocations.ts:476` (agent, état pending) | connecteurs : `apps/harbor/packages/server/src/connectors/conductor/connector.ts:139` ; pas consommée par apps/x |
| `invocation_stop` | `apps/harbor/packages/server/src/core/invocations.ts:289` | conductor/connector.ts:140 ; côté client, l'arrêt du @rowboat local passe par stopTopicAgent |
| `approval_decided` | `apps/harbor/packages/server/src/core/invocations.ts:374` | connecteurs seulement |
| `invocation_state` | `apps/harbor/packages/server/src/core/invocations.ts:475` | apps/x/apps/renderer/src/hooks/use-space-invocations.ts:62 |
| `notify` | `apps/harbor/packages/server/src/notify.ts:116` | `apps/x/packages/spaces-client/src/live.ts:344` → `apps/x/packages/core/src/spaces/orgs.ts:391` onMemberFrame → `apps/x/packages/core/src/spaces/notify.ts:21` |
| `space_added` | `apps/harbor/packages/server/src/core/spaces.ts:115`, :289, :359 ; via acceptInvite | `apps/x/packages/spaces-client/src/live.ts:344` → renderer hooks/use-spaces.ts:470, lib/spaces-read-state.ts:380 |

Note : le dossier de tests est `apps/harbor/packages/server/test`, pas `apps/harbor/test` comme l'indiquait l'annexe A.
