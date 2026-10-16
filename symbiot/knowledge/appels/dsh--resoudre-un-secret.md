---
type: Appel
title: DSH — Résoudre un secret
description: Secrets : `resolve(ref: CredentialRef): Promise<ResolvedCredential | undefined>` ; aussi describe, set, unset, readRecord, describeRecord, listRecords
tags:
  - serveur
  - sandbox
flux: Secrets
brique: /composants/dsh.md
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:30:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# DSH — Résoudre un secret

| | |
|---|---|
| **Flux** | Secrets |
| **Besoin** | Résoudre un secret |
| **Service client** | runtime → fournisseur de credentials (OpenBao, chantier 14) |
| **Appel** | `resolve(ref: CredentialRef): Promise<ResolvedCredential | undefined>` ; aussi describe, set, unset, readRecord, describeRecord, listRecords, modifyRecord (seul chemin d'écriture, verrou inter-process), deleteRecord |
| **Contrat** | `packages/credentials/credentials/src/index.ts` abstract class CredentialProvider (service credentials) |
| **Fonction servie** | décl. :183-256 ; impl. LocalCredentialProvider credentials-local/src/index.ts:609-666 |
| **Auth** | couches : env process > store géré > .env ; valeur vide = absente ; pas de cache |
| **Événements / statut** | `credentials/reference-updated`, `credentials/record-updated` (types.ts:87, :99) |
| **Test au fil** | credentials/tests/credentials.spec.ts, credentials-local/tests/local.spec.ts, records.spec.ts, watcher.spec.ts |

**Note de frontière :** Un CredentialProvider OpenBao implémente resolve et describe ; les méthodes d'écriture peuvent lever « non supporté ».

Brique : [/composants/dsh.md](/composants/dsh.md) · Interface : [/interfaces/dsh.md](/interfaces/dsh.md)
