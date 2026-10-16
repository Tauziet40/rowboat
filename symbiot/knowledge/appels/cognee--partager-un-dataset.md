---
type: Appel
title: Cognee — Partager un dataset
description: A2 : POST /api/v1/permissions/datasets/{principal_id}?permission_name=read|write|delete|share (corps : liste d'ids) ; DELETE … ; rôles et tenants /permissions/roles, /tenants
tags:
  - serveur
  - poste
flux: A2
brique: /composants/cognee.md
appel: POST /api/v1/permissions/datasets/{principal_id}?permission_name=read\|write\|delete\|share (corps : liste d'ids) ; DELETE … ; rôles et tenants /permissions/roles, /tenants
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Cognee — Partager un dataset

| | |
|---|---|
| **Flux** | A2 |
| **Besoin** | Partager un dataset |
| **Service client** | REST |
| **Appel** | POST /api/v1/permissions/datasets/{principal_id}?permission_name=read|write|delete|share (corps : liste d'ids) ; DELETE … ; rôles et tenants /permissions/roles, /tenants |
| **Contrat** | `cognee/cognee/api/v1/permissions/routers/get_permissions_router.py:39` give_datasets_permission_to_principal, :103 révocation, :146 get_principal_datasets |
| **Fonction servie** | `cognee/cognee/modules/users/permissions/methods/authorized_give_permission_on_datasets.py:10` → give_permission_on_dataset.py:23 |
| **Auth** | permission share requise |
| **Événements / statut** | — |
| **Test au fil** | `cognee/cognee/tests/unit/api/test_permissions_router.py` ; test_permissions.py, test_multi_tenancy.py, test_release_multi_user_e2e.py |

Brique : [/composants/cognee.md](/composants/cognee.md) · Interface : [/interfaces/cognee.md](/interfaces/cognee.md)
