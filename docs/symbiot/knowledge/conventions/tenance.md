---
type: Convention
title: Quintuplet de tenance
description: Un rôle et un schéma PostgreSQL, un graphe FalkorDB, un bucket SeaweedFS, un client Keycloak, un namespace k3s par brique.
tags:
  - tenance
  - stockage
  - identité
  - k3s
generated:
  by: claude-fable-5.1/session-01MK6
  at: 2026-10-16T18:00:00+02:00
status: stable
stale_after: 2027-01-16T00:00:00+02:00
---

# Quintuplet de tenance

| Brique | Schéma PostgreSQL | Graphe FalkorDB | Bucket SeaweedFS | Client Keycloak | Namespace |
|---|---|---|---|---|---|
| Harbor | `harbor` | — | `harbor-blobs` | `harbor` | `harbor` |
| Cognee | `cognee` | un par dataset, convention à consigner depuis l'installation (D8) | `cognee-data` (`STORAGE_BACKEND=s3`) | `cognee` | `cognee` |
| Agent Stack | `agentstack` (+ `procrastinate`) | via Cognee | `agentstack-files` | `agentstack-server`, `-ui`, `-cli` | `agentstack` |
| Centaur | `centaur` | — | PVC (StorageClass SeaweedFS CSI à qualifier) | `centaur` | `centaur` |
| Keycloak | `keycloak` | — | — | — | `identity` |
| OpenBao | — | — | — | — | `identity` |
| Console et API de politique | `console` | — | — | `console` | `console` |
| Client Symbiot | — | — | — | `symbiot-client` (public, PKCE) | — |

**Règles :** un rôle propriétaire par schéma, aucun grant croisé ; chaque outil de migration vise son schéma par `search_path` (à vérifier pour l'échelle `migrations.ts` de Harbor) ; une seule version majeure de PostgreSQL pour tous ; les graphes FalkorDB ne sont peuplés que par Cognee (D1) ; l'identité commune est le `sub` Keycloak (D4) ; les identifiants d'org et de space de Harbor sont la référence canonique dans les autres schémas.
