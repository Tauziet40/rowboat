---
type: Appel
title: DSH — Envoyer un prompt et recevoir les mises à jour
description: ACP : `session/prompt`
tags:
  - serveur
  - sandbox
flux: ACP
brique: /composants/dsh.md
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:30:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# DSH — Envoyer un prompt et recevoir les mises à jour

| | |
|---|---|
| **Flux** | ACP |
| **Besoin** | Envoyer un prompt et recevoir les mises à jour |
| **Service client** | client externe |
| **Appel** | `session/prompt` |
| **Contrat** | `AcpSession.prompt(params, imagePromptEnabled, signal)` |
| **Fonction servie** | index.ts:361 → session.ts:243 (un seul prompt en vol) |
| **Auth** | — |
| **Événements / statut** | `session/update` : agent_thought_chunk, agent_message_chunk, usage_update, tool_call, tool_call_update (updates.ts:16, :52, :69 ; dérivés de assistant/message, tool/call, tool/result, turn/end) |
| **Test au fil** | turns.spec.ts, updates.spec.ts, content.spec.ts |

Brique : [/composants/dsh.md](/composants/dsh.md) · Interface : [/interfaces/dsh.md](/interfaces/dsh.md)
