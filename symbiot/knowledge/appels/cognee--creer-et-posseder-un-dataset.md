---
type: Appel
title: Cognee — Créer et posséder un dataset
description: A1 : POST /api/v1/datasets {name} ; GET /api/v1/datasets
tags:
  - serveur
  - poste
flux: A1
brique: /composants/cognee.md
appel: POST /api/v1/datasets {name} ; GET /api/v1/datasets
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Cognee — Créer et posséder un dataset

| | |
|---|---|
| **Flux** | A1 |
| **Besoin** | Créer et posséder un dataset |
| **Service client** | REST, ou implicite au premier remember |
| **Appel** | POST /api/v1/datasets {name} ; GET /api/v1/datasets |
| **Contrat** | get_datasets_router.py:198 create_new_dataset, :157 get_datasets |
| **Fonction servie** | `cognee/cognee/modules/data/methods/create_authorized_dataset.py:17` (read, write, delete, share au propriétaire) ; create_dataset.py:13 (id dérivé de nom + owner_id, tenant_id) |
| **Auth** | propriétaire = utilisateur authentifié |
| **Événements / statut** | — |
| **Test au fil** | `cognee/cognee/tests/test_remember_session_dataset_creation.py` |

Brique : [/composants/cognee.md](/composants/cognee.md) · Interface : [/interfaces/cognee.md](/interfaces/cognee.md)
