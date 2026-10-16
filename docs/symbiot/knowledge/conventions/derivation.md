---
type: Convention
title: Échelle de dérivation et extraction par tranche
description: Degrés D0 à D5 de relation au code amont, règle par degré, tranches verticales, provenance, lint.
tags:
  - core
  - inspirant
  - gouvernance
generated:
  by: claude-fable-5.1/session-01MK6
  at: 2026-10-16T18:00:00+02:00
status: stable
stale_after: 2027-01-16T00:00:00+02:00
---

# Échelle de dérivation et extraction par tranche

| Degré | Relation à l'amont | Où | Licence | Maintenance |
|---|---|---|---|---|
| D0 utilisé tel quel | image, chart, bibliothèque | `stack/charts/`, `resource` = digest | celle de l'amont, isolation réseau pour le copyleft | montée de version |
| D1 étendu sans fork | plugin, sous-classe, overlay, connecteur hors dépôt amont | `stack/services/`, paquets `@symbiot/*` | la nôtre | suit l'API amont |
| D2 fork mince | adaptateur derrière une interface, un commit par patch, contribuable | `stack/forks/<x>`, branche `symbiot/storage` | celle de l'amont | rebase sur tag amont, trimestriel |
| D3 fork profond | notre produit ; paquets `@symbiot/*` séparés ; `UPSTREAM.md` des zones synchronisées et gelées | sous-module propre | amont pour l'amont, nôtre pour `@symbiot/*` | cherry-pick ; réduction tardive et tracée |
| D4a réimplémentation dérivée | logique d'un amont permissif, fragments autorisés avec en-tête et notices | `stack/services/` | Apache, MIT | amont surveillé par `stale_after` |
| D4b clean-room | logique d'un amont copyleft, depuis une spécification, aucun fragment | `stack/services/` | la spec est la frontière | — |
| D5 principe seul | idée notée, sans lecture de code pour implémenter | `knowledge/` | — | — |

Une brique se classe **par partie**. Core = D0 à D3 ; inspirants = D4 et D5 (D10).

**Règle par degré.** D0 et D2 : tout importer, verticalité par configuration. D4 et nos services : partir du core qualifié et greffer des tranches. D3 : fork entier, ajouts isolés, verticales amont désactivées par flags, suppression seulement en PR de retrait consignée.

**Extraction par tranche** : définir par un besoin (scénario ou appel) ; points d'entrée amont ; fermeture de dépendances par `symbiot slice` (`grimp`, `pydeps`, `dependency-cruiser`) ; verdict (confinée : importer ; traverse l'infrastructure : couper et adapter ; moitié du dépôt : pas une tranche) ; importer avec tests et en-tête `Derived from <dépôt>@<commit>:<chemin> (licence)` ; brancher au bas (FalkorDB via Cognee, CronJob k3s, OpenBao, sub Keycloak).

**Lint** (`symbiot lint`) : frontmatter ; liens ; lien vers `deprecated` sans note ; `stale_after` dépassé ; `generated.at` après le dernier `verified` d'un `stable` ; en-tête de dérivation sans provenance et inversement ; D4b avec `sources` vers du code copyleft ; D2 dont le tag amont a plus d'un trimestre ; brique sans degré.

**Clean-room D4b** : deux sièges, un rédacteur de spécification qui lit l'amont, un implémenteur sans accès à l'amont.
