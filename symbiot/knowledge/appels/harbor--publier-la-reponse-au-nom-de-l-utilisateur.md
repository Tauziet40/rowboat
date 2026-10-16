---
type: Appel
title: Harbor — Publier la réponse au nom de l'utilisateur
description: I3 : MCP `post_message` / POST /v1/spaces/:id/messages
tags:
  - serveur
  - poste
  - mcp
flux: I3
brique: /composants/harbor.md
appel: MCP `post_message` / POST /v1/spaces/:id/messages
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Publier la réponse au nom de l'utilisateur

| | |
|---|---|
| **Flux** | I3 |
| **Besoin** | Publier la réponse au nom de l'utilisateur |
| **Service client** | MCP `post_message` (projection, `apps/x/packages/core/src/runtime/tools/domains/spaces.ts`) ; IPC spaces:postMessage → `apps/x/packages/spaces-client/src/client.ts` postMessage |
| **Appel** | MCP `post_message` / POST /v1/spaces/:id/messages |
| **Contrat** | `apps/harbor/packages/protocol/src/api.ts` routes.postMessage (NewMessage, api.ts:54) |
| **Fonction servie** | `apps/harbor/packages/server/src/mcp.ts:339` ; http.ts:689 → service.ts:392 → core/feed.ts:331 |
| **Auth** | Bearer membre, actingMode |
| **Événements / statut** | `message` (+ `topic`, `invocation_state`, `notify`) |
| **Test au fil** | `apps/harbor/packages/server/test/mentions.test.ts`, notify.test.ts |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
