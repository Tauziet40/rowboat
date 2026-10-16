---
type: Appel
title: DSH — Ouvrir une session, prompt, flux, arrêt
description: SDK : pas de `session/new` : un sessionId inconnu crée la session ; `session/prompt` {sessionId, contentBlocks} → {messageId} ; notifications `ses
tags:
  - serveur
  - sandbox
flux: SDK
brique: /composants/dsh.md
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:30:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# DSH — Ouvrir une session, prompt, flux, arrêt

| | |
|---|---|
| **Flux** | SDK |
| **Besoin** | Ouvrir une session, prompt, flux, arrêt |
| **Service client** | client SDK |
| **Appel** | pas de `session/new` : un sessionId inconnu crée la session ; `session/prompt` {sessionId, contentBlocks} → {messageId} ; notifications `session.event`, `session.status`, `subagent.started`, `subagent.finished` ; `shutdown` |
| **Contrat** | DeepSeekHarness.session(id?) api.ts:103 ; HarnessClient.prompt client.ts:291, subscribe :351, subscribeSessionTree :370 ; HarnessSdkNotificationMap |
| **Fonction servie** | server.ts:261 getOrCreateSession ; :178 ; :95-128 (ctx.on session/event, agent/status) ; :213 |
| **Auth** | — |
| **Événements / statut** | toutes les SessionEvent du runtime ; **les requêtes serveur → client ne sont pas implémentées : les approbations sont refusées** |
| **Test au fil** | sdk-client.spec.ts, protocol/tests/transport.spec.ts, dispose.spec.ts |

**Note de frontière :** Trois méthodes seulement ; pas de session/cancel.

Brique : [/composants/dsh.md](/composants/dsh.md) · Interface : [/interfaces/dsh.md](/interfaces/dsh.md)
