# forks

Sous-modules à ajouter en mouvement M3, chacun épinglé sur une release et porteur d'une branche `symbiot/storage` (un commit par patch, contribuable en amont). Degrés dans `knowledge/conventions/derivation.md`.

| Sous-module | Amont | Degré | Patchs prévus |
|---|---|---|---|
| `harbor` | rowboatlabs/rowboat, `apps/harbor` | D2 | `search_path` du schéma |
| `symbiot-client` | fork de rowboat `apps/x` (dépôt propre) | D3 | paquets `@symbiot/*`, `UPSTREAM.md` |
| `cognee` | topoteretes/cognee + adaptateur communautaire FalkorDB | D2 | déjà en place chez toi |
| `agentstack` | i-am-bee/agentstack | D0 chart + D2 | identité par `sub`, sans Redis, `connectors.auth` chiffré, vecteurs via Cognee |
| `centaur` | paradigmxyz/centaur | D0 chart + D2 | validation JWT Keycloak, source de secrets OpenBao, adaptateur DSH |
| `dsh` | deepseek-ai/deepseek-harness | D0 image + D1 plugins | plugin de politique, `CredentialProvider` OpenBao |
| `beeai` | i-am-bee/beeai-framework (python) | D1 | sous-classes seulement |

```sh
git submodule add -b symbiot/storage <url> stack/forks/<nom>
```
