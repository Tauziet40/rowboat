---
type: Scénario
title: Une journée dans la vie, incrément 2
description: Scénario d'acceptation de l'incrément 2, joué par le vérificateur avec symbiot verify increment-2.
tags:
  - poste
  - mémoire
  - okf
  - mcp
generated:
  by: claude-fable-5.1/session-01MK6
  at: 2026-10-16T18:00:00+02:00
status: stable
stale_after: 2027-01-16T00:00:00+02:00
increment: 2
---

# Une journée dans la vie, incrément 2

Une journée dans la vie, jouée par le vérificateur avec `symbiot verify increment-2`.

| Pas | Action | Appel de la carte | Preuve |
|---|---|---|---|
| 1 | L'utilisateur prend des notes de réunion ; le Brain crée `People/…` et `Projects/…` avec wikilinks | fichiers locaux, `build_graph` | fichiers présents, frontmatter de tagging |
| 2 | « Soumettre au serveur » convertit le dossier en bundle OKF : `type` par dossier, `title` du H1, `sources`, `generated: symbiot-client/<v>`, `index.md`, `log.md` depuis git | convertisseur | bundle valide par `okf` lint |
| 3 | Le client appelle `remember` avec le bundle, `dataset_name = sub + "_brain"`, `ontology_key` de l'ontologie Symbiot | MCP Cognee, Bearer Keycloak | `cognify_status` terminé, graphe FalkorDB peuplé |
| 4 | L'assistant répond à « qui travaille sur le projet X ? » par l'outil natif `memory-recall` | MCP Cognee `recall` projeté en outil natif | réponse citant les `source` OKF |
| 5 | Le serveur renvoie un bundle enrichi (relations déduites) ; le client le réintègre en notes `status: draft` et `verified` absent | convertisseur, sens retour | notes nouvelles marquées non vérifiées, aucune note existante écrasée |
| 6 | L'utilisateur vérifie une note : `verified: human:<sub>` ; `log.md` du Brain l'enregistre | fichiers locaux | ligne de `log.md` |
| 7 | Hors ligne : les pas 1, 4 (sur le grep local) et 6 fonctionnent ; 3 et 5 sont mis en file et rejoués au retour | — | file visible, rejeu sans doublon |
| 8 | Aucun appel sortant vers un domaine éditeur pendant la journée | — | capture réseau vide hors du cluster |
