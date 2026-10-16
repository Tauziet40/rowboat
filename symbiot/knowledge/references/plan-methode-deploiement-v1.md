---
type: Référence
title: Plan court de L5, validé le 16 octobre
description: Plan de production validé, conservé comme référence.
tags:
  - okf
sources:
  - resource: /deprecated/2026-10-15/05-plan-methode-deploiement-v1.md
generated:
  by: claude-fable-5.1/session-01MK6
  at: 2026-10-16T18:00:00+02:00
status: stable
stale_after: 2027-01-16T00:00:00+02:00
---

# Plan court de L5, validé le 16 octobre

**Statut :** plan soumis à validation le 2026-10-16 ; aucun contenu rédigé avant accord
**Remplace :** le livrable L5 initial (« contextes OKF pour l'équipe OpenRig »), absorbé
**Sources :** l'ensemble du dossier `docs/symbiot/` et les échanges des 15 et 16 octobre ; décisions validées le 16 octobre
**Format :** Markdown de travail, un document principal `05-methode-deploiement-v1.md` et trois annexes

---

## 0. Ce qui est déjà tranché et que L5 fige

| # | Décision validée | Conséquence |
|---|---|---|
| D1 | Bases : PostgreSQL pour le relationnel, FalkorDB pour vecteurs et graphe, pas de pgvector ; Cognee comme middleware de peuplement des bases vecteur et graphe pour les frameworks | les forks de stockage sont des adaptateurs minces, déjà expérimentés |
| D2 | Substrat d'exécution et de sandbox commun : k3s | Agent Stack et Centaur reviennent en V1 ; DSH tourne en pod |
| D3 | Rôles PostgreSQL et schémas par application, FalkorDB en graphes nommés, SeaweedFS en buckets, Keycloak en clients, namespaces k3s : le quintuplet de tenance | isolation par rôle, unification par les clés |
| D4 | Identité : `sub` Keycloak partout, un realm, orgs = orgs Harbor ; Agent Stack forké pour identifier par `sub` ; Centaur reçoit la validation JWT Keycloak ; Cognee provisionné depuis Keycloak | l'annuaire d'identités est le premier chantier |
| D5 | Secrets : OpenBao source unique, un seul patron de courtier (modèle iron-proxy), un adaptateur par brique | — |
| D6 | Hébergement des agents : CRD Agent Sandbox comme primitive commune ; Centaur = sessions en sandbox et workflows durables ; Agent Stack = agents de service A2A et registre ; DSH = harness dans une sandbox Centaur | scénario S1 à frontière nette |
| D7 | Gouvernance : une API de politique unique adossée à la console des spaces, consultée par Harbor, DSH, BeeAI, Agent Stack, Cognee | pas de moteur par langage |
| D8 | Connaissance : OKF format d'échange, Brain converti, Cognee ingère ; règle d'alignement `type` OKF ↔ classes de l'ontologie Cognee ; convention de tenance Cognee à consigner depuis l'installation existante | une seule ontologie maintenue |
| D9 | Modèles : le proxy serveur (Agent Stack) est l'autorité de routage et de quota, GPU publié au cluster ; le routeur client ne décide qu'en local ou hors ligne | — |
| D10 | Processus core (qualifié par fork de stockage et substrat) distinct du processus inspirants (principes transplantés sur les core validés) : MemoryBear, Eigent, ElephantBroker, Synapse sont inspirants | V1 = core ; V2 = augmentation |
| D11 | Flux d'événements canonique : le journal append-only de Harbor ; versions de Harbor et DSH épinglées | pas de bus supplémentaire |

## 1. Structure proposée de L5

### Partie A — La stack V1, « qui fait quoi »
1. Schéma d'ensemble à trois couches : poste (client Symbiot, second cerveau, DSH local), serveur (k3s : Harbor, Cognee et FalkorDB, Agent Stack, Centaur, Keycloak, OpenBao, SeaweedFS, proxy LLM et GPU), connaissance (OKF, ontologie).
2. Fiche de rôle par brique core : responsabilité unique, interfaces exposées et consommées (reprises de l'annexe A et des fiches), quintuplet de tenance, version épinglée, statut réel (installé, évalué, bêta, à faire).
3. Table des flux : les cinq intégrations I1 à I5 traduites en flux concrets entre briques, avec l'authentification de chaque saut.
4. Ce que V1 ne fait pas : post-traitement de Cognee, workflows no-code, gouvernance avancée ; renvoyés en V2 avec leurs inspirants.

### Partie B — Le bundle OKF `symbiot-stack`
5. Arborescence du bundle : `composants/`, `interfaces/`, `appels/`, `decisions/`, `chantiers/`, `conventions/`, `inventaire/`, avec `index.md` par dossier et `log.md` racine.
6. Gabarit de concept par type (composant, interface, appel, décision, chantier, convention), champs OKF utilisés et règles de `verified` et `stale_after`.
7. Un concept d'exemple complet par type, tiré du dossier (par exemple le composant Harbor, l'appel `propose_change`, la décision D4).
8. Règle d'alignement `type` OKF ↔ ontologie Cognee, et le flux d'ingestion du bundle dans Cognee.

### Partie C — Les six mouvements de la méthode
9. **M1 Formaliser** : conversion du dossier `docs/symbiot` en bundle, par agents, vérifié par toi.
10. **M2 Relever l'existant** : inventaire de la machine d'évaluation et des installations (Cognee et FalkorDB réglés, bêta UX, bêta client), en OKF `generated: process:inventory`.
11. **M2 bis Carte des appels** : descente récursive depuis les besoins vers les services Rowboat puis les contrats des briques, arrêt à la frontière d'interface, passe montante des événements ; chaîne besoin → service → appel → fonction serveuse → test au fil ; format OKF `appels/`.
12. **M3 Qualifier par fork** : protocole en sept étapes sur les trois axes (PostgreSQL, FalkorDB via Cognee, k3s), tableau d'effort par brique, ordre de qualification, critères go et no-go.
13. **M4 Dépôt et outils unifiés** : `symbiot-infra` (bundle OKF, charts et manifestes k3s, runbooks sous une commande unique `symbiot`), conventions reprises de Rowboat, règle « les agents n'agissent que par runbook ».
14. **M5 Équipe d'agents OpenRig** : rôles (opérateur, cartographe, intégrateur, vérificateur, gardien de stack, scribe), règles de séparation, permissions par rôle, contexte chargé (bundle via MCP OKF et Cognee), un rig YAML par incrément.
15. **M6 Incréments vérifiés** : définition de fini en trois points (scénario d'acceptation « une journée dans la vie », démonstration sur la machine, bundle mis à jour et vérifié), sauvegardes et retour arrière, revue hebdomadaire, note de modifications par cycle.

### Partie D — Plan V1 par incréments
16. Incrément 0 : identité et tenance (D3, D4) : Keycloak realm, rôles PostgreSQL, graphes FalkorDB, buckets, namespaces ; convention consignée.
17. Incrément 1 : socle client (nettoyage cloud, Keycloak, routeur local, SeaweedFS).
18. Incrément 2 : cœur de valeur (Cognee en outils natifs, convertisseur OKF, aller-retour second cerveau ↔ serveur).
19. Incrément 3 : socle serveur qualifié (Harbor, Agent Stack forké par `sub` et sans Redis, Centaur avec JWT Keycloak, OpenBao et courtier).
20. Incrément 4 : harness et agents (DSH en sandbox Centaur, BeeAI, serve A2A, connecteurs Harbor, adaptateur DSH ou ACP chez Centaur).
21. Incrément 5 : gouvernance (console des spaces avec UX reprise, API de politique, proxy LLM autorité de routage).
22. Pour chaque incrément : chantiers couverts (renvoi aux §5 et §8.5 du comparatif), scénario d'acceptation, rig OpenRig, risques.

### Partie E — V2, l'augmentation par les inspirants
23. Post-traitement de Cognee d'après MemoryBear, gouvernance d'après Eigent, workflows d'après Synapse, contrat mémoire d'après ElephantBroker ; chacun comme fonctionnalité sur une brique core, avec sa brique hôte et son scénario.

### Annexes
- **Annexe C** : rig OpenRig de l'incrément 0 en YAML, avec les prompts de rôle.
- **Annexe D** : scénario d'acceptation « une journée dans la vie » de l'incrément 2, pas à pas, avec les appels de la carte.
- **Annexe E** : liste des runbooks `symbiot` de V1 avec leur effet et leur retour arrière.

## 2. Méthode de rédaction

- Rédigé à partir du dossier existant, sans nouvelle lecture de code, sauf deux vérifications ciblées entrant dans la qualification : le stockage des fichiers de travail des sandboxes Centaur et le stockage de données de Cognee, pour confirmer qu'ils peuvent pointer SeaweedFS.
- Chaque fiche de rôle de la partie A cite les fichiers déjà relevés dans les fiches et annexes ; L5 ne restate pas, il renvoie.
- Contrôle de cohérence final sur tout le dossier (D1 à D11 reportées dans le comparatif §8 et le référentiel), puis note de modifications du cycle.

## 3. Points à valider

1. La structure A à E et les annexes C à E.
2. Le nom et l'emplacement du dépôt `symbiot-infra` (nouveau dépôt, ou sous-dossier de rowboat ?).
3. L'incrément 0 « identité et tenance » placé avant le socle client : il déplace Keycloak en tête, parce que D4 conditionne tout.
4. Les deux vérifications ciblées de code autorisées (Centaur, Cognee ↔ SeaweedFS).
