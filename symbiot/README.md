# symbiot

Dépôt du projet Symbiot : la connaissance (bundle OKF), la stack V1 et les équipes d'agents. Trois racines, par nature d'artefact ([knowledge/methode/deploiement-v1.md](knowledge/methode/deploiement-v1.md), partie B).

| Racine | Contenu |
|---|---|
| [`knowledge/`](knowledge/index.md) | bundle OKF 0.2 : un concept par fichier, un répertoire par type ; journal [`knowledge/log.md`](knowledge/log.md) |
| [`stack/`](stack/README.md) | ce qui s'exécute : cluster k3s, charts, forks épinglés, nos services, runbooks `symbiot <action>`, valeurs par environnement |
| [`rigs/`](rigs/README.md) | équipes d'agents OpenRig, un rig par incrément, prompts de rôle |
| `deprecated/` | documents de travail datés après conversion |

**Doctrine** (décisions D1 à D11 dans [`knowledge/decisions/`](knowledge/decisions/index.md)) : bases PostgreSQL et FalkorDB ; fichiers SeaweedFS ; exécution k3s ; identité Keycloak `sub` ; secrets OpenBao ; tout ce qui ne tient pas sur ces cinq-là est soit forké derrière une interface, soit inspirant.

**Origine.** Dépôt privé [`Tauziet40/symbiot`](https://github.com/Tauziet40/symbiot), ouvert le 16 octobre 2026. L'arborescence a été construite dans la branche de travail `claude/gallant-heisenberg-6gsemz` de `rowboat` sous `symbiot/` et extraite par `git subtree split` : l'historique de chaque fichier remonte à cette branche. À partir de cette date, ce dépôt est la seule source ; la copie restée dans `rowboat` n'est plus mise à jour.
