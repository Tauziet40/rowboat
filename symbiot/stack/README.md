# stack

| Dossier | Contenu | État |
|---|---|---|
| `cluster/` | amorçage k3s, namespaces, NetworkPolicy, StorageClass, plugin GPU | à écrire, incrément 0 |
| `charts/` | un chart ou kustomization par brique core | à écrire, incréments 0 et 3 |
| `forks/` | sous-modules épinglés sur la branche `symbiot/storage` ([forks/README.md](forks/README.md)) | à ajouter en M3 |
| `services/` | api-politique, console, mcp-okf, convertisseur-okf ; consolidation et workflows en V2 | à écrire |
| `runbooks/` | un fichier par action `symbiot <action>` ([runbooks/README.md](runbooks/README.md)) | lint et vues disponibles |
| `env/` | valeurs par environnement, sans aucun secret | `eval/` à créer en M2 |

Règle : les agents n'agissent sur le serveur qu'à travers `symbiot <runbook>`.
