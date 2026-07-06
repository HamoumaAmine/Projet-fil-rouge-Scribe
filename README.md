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
