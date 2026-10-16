---
type: Appel
title: Cognee — Relire les résultats enrichis
description: I2 : GET /api/v1/datasets/{id}/data ; GET …/graph ; GET …/data/{data_id}/raw ; GET …/schema
tags:
  - serveur
  - poste
flux: I2
brique: /composants/cognee.md
appel: GET /api/v1/datasets/{id}/data ; GET …/graph ; GET …/data/{data_id}/raw ; GET …/schema
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Cognee — Relire les résultats enrichis

| | |
|---|---|
| **Flux** | I2 |
| **Besoin** | Relire les résultats enrichis |
| **Service client** | client HTTP, aucun outil MCP dédié |
| **Appel** | GET /api/v1/datasets/{id}/data ; GET …/graph ; GET …/data/{data_id}/raw ; GET …/schema |
| **Contrat** | get_datasets_router.py:385, :354 get_dataset_graph, :800 get_raw_data, :918 get_dataset_schema |
| **Fonction servie** | `cognee/cognee/modules/data/methods/get_authorized_existing_datasets.py:12` |
| **Auth** | permission read |
| **Événements / statut** | n/a |
| **Test au fil** | `cognee/cognee/tests/unit/api/test_dataset_data_pagination.py`, test_get_raw_data_endpoint.py |

**Note de frontière :** Le sens retour de l'aller-retour second cerveau ↔ serveur (scénario incrément 2, pas 5) passe par REST, pas par MCP.

Brique : [/composants/cognee.md](/composants/cognee.md) · Interface : [/interfaces/cognee.md](/interfaces/cognee.md)
