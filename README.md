# Scribe

Scribe est un outil en ligne de commande qui transforme un enregistrement audio
(réunion, cours, note vocale) en compte rendu écrit et structuré.

## Fonctionnement

1. L'utilisateur fournit un fichier audio.
2. Un modèle de transcription (Speech-to-Text) convertit l'audio en texte brut.
3. Un LLM reformule ce texte en compte rendu structuré : titre, points clés,
   décisions, actions.

Les modèles sont appelés via l'API serverless de Groq.

## Structure du projet

- `src/` : code source de Scribe
- `prompts/` : prompts système utilisés par le LLM
- `audio_examples/` : fichiers audio d'exemple pour les tests

## Installation

_(à compléter)_

## Utilisation

_(à compléter)_

## Réponses aux questions

**Q1 — Pourquoi le .gitignore doit-il exister avant d'écrire du code manipulant des secrets ?**
Pour garantir qu'aucune clé API ne soit jamais ajoutée accidentellement à l'historique
Git. Une fois un secret commité, il reste dans l'historique même après suppression du
fichier, et devient très difficile à effacer complètement. Ignorer .env dès le départ
supprime ce risque.

**Q2 — Quels modèles STT et LLM choisissez-vous et pourquoi ?**
STT : whisper-large-v3-turbo — bon compromis vitesse/qualité/coût pour transcrire
réunions et notes vocales, plus rapide que whisper-large-v3 à précision proche.
LLM : llama-3.3-70b-versatile — performant en rédaction structurée (titre, points clés,
décisions), servi rapidement par Groq à coût raisonnable.
Les deux identifiants sont centralisés dans src/config.py.

**Q3 — Que renvoie l'API en plus du texte ?**
Avec response_format='verbose_json', l'API renvoie, en plus du texte :
- task : le type d'opération (transcribe)
- language : la langue détectée automatiquement (ici French)
- duration : la durée de l'audio en secondes
- segments : le texte découpé en segments horodatés (start/end), avec pour chacun des
  indicateurs de confiance (avg_logprob, no_speech_prob, compression_ratio)
- x_groq : l'identifiant de la requête

Utilité pour une évolution future de Scribe : les horodatages permettraient de générer
des comptes rendus avec renvois temporels (ex : "décision prise à 00:05"), la langue
détectée permettrait un traitement multilingue, et les indicateurs de confiance
pourraient signaler les passages mal transcrits à vérifier.
