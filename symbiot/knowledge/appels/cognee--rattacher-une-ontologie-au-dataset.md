---
type: Appel
title: Cognee — Rattacher une ontologie au dataset
description: I2 : POST /api/v1/ontologies (form : ontology_key, fichier) ; puis ontology_key dans remember ; GET /api/v1/ontologies ; DELETE /api/v1/ontologies/{key}
tags:
  - serveur
  - poste
flux: I2
brique: /composants/cognee.md
appel: POST /api/v1/ontologies (form : ontology_key, fichier) ; puis ontology_key dans remember ; GET /api/v1/ontologies ; DELETE /api/v1/ontologies/{key}
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Cognee — Rattacher une ontologie au dataset

| | |
|---|---|
| **Flux** | I2 |
| **Besoin** | Rattacher une ontologie au dataset |
| **Service client** | client HTTP, aucun outil MCP de téléversement |
| **Appel** | POST /api/v1/ontologies (form : ontology_key, fichier) ; puis ontology_key dans remember ; GET /api/v1/ontologies ; DELETE /api/v1/ontologies/{key} |
| **Contrat** | `cognee/cognee/api/v1/ontologies/routers/get_ontology_router.py:23` upload_ontology, :122 delete_ontology, :172 list_ontologies |
| **Fonction servie** | `cognee/cognee/api/v1/ontologies/ontologies.py:78` ; consommée dans get_remember_router.py:577-580 get_ontology_contents(keys, user) |
| **Auth** | ontologie liée à l'**utilisateur**, pas au dataset ; appliquée à chaque remember ou cognify |
| **Événements / statut** | 409 si clé inconnue |
| **Test au fil** | `cognee/cognee/tests/unit/api/test_ontology_endpoint.py`, test_delete_ontology.py, test_remember_router_ontology_session.py ; `cognee-mcp/tests/test_remember_ontology.py` |

**Note de frontière :** Conséquence pour D8 : l'ontologie maintenue est rattachée au compte de service qui ingère, pas au dataset.

Brique : [/composants/cognee.md](/composants/cognee.md) · Interface : [/interfaces/cognee.md](/interfaces/cognee.md)
