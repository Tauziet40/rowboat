---
type: Appel
title: Harbor — Détecter @rowboat et lancer l'assistant local
description: I3 : local, sans appel Harbor ; grammaire `apps/harbor/packages/protocol/src/mentions.ts` addressesRowboat
tags:
  - serveur
  - poste
flux: I3
brique: /composants/harbor.md
appel: local, sans appel Harbor ; grammaire `apps/harbor/packages/protocol/src/mentions.ts` addressesRowboat
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Détecter @rowboat et lancer l'assistant local

| | |
|---|---|
| **Flux** | I3 |
| **Besoin** | Détecter @rowboat et lancer l'assistant local |
| **Service client** | renderer lib/spaces-rowboat.ts maybeInvokeRowboat → IPC spaces:invokeRowboat → `apps/x/packages/core/src/spaces/topic-agent.ts` invokeTopicAgent (arrêt stopTopicAgent) |
| **Appel** | local, sans appel Harbor ; grammaire `apps/harbor/packages/protocol/src/mentions.ts` addressesRowboat |
| **Contrat** | `apps/harbor/packages/protocol/src/mentions.ts` MENTION_TOKEN_RE, addressesRowboat |
| **Fonction servie** | — (Harbor stampe mentionsRowboat : core/feed.ts:67) |
| **Auth** | — |
| **Événements / statut** | — |
| **Test au fil** | aucun (pas de test appelant invokeTopicAgent) |

**Note de frontière :** Le @rowboat est déclenché **côté client**, sans invocation Harbor : la projection du contexte local est un flux poste → espace, pas un flux d'agent membre.

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
